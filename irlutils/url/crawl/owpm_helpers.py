""" A collection of utilities for the analysis of crawl databases """
import operator
import plyvel
import hashlib
import zlib
import glob
import gzip
import json
import os
import pandas as pd
import jsbeautifier

from irlutils.url.crawl import domain_utils as du


# General ##########


def unique(seq):
    # Not order preserving
    return {}.fromkeys(seq).keys()


def sort_by_value(dct, reverse=True):
    """ Sort a dictionary by value """
    return sorted(dct.items(), key=operator.itemgetter(1), reverse=reverse)


def sort_by_length(dct, reverse=True):
    """ Sort a dictionary by value length """
    return sorted(dct.iteritems(), key=lambda x: len(x[1]), reverse=reverse)


def get_dct_subset(dct, keys):
    """ Returns a subset of the dictionary, limited to the input keys """
    return dict((k, dct[k]) for k in keys if k in dct)


# Analysis ##########


def get_ranked_sites(location, as_list=False):
    """
    returns a dictionary of site rank from the
    top-1m.csv file located at <location>
    <as_list> (True)   returns rank ordered list
              (False)  returns dict[url] = rank
    """
    with open(location, 'r') as f:
        sites = ['http://' + x.split(',')[1]
                 for x in f.read().strip().split('\n')]
    if as_list:
        return sites
    site_rank = dict()
    for i in range(len(sites)):
        site_rank[sites[i]] = i + 1
    return site_rank


# print(utilities ##########)

def expand_params(url):
    purl = urlparse(url)
    print("\n====================================")
    print("Scheme: {}".format(purl.scheme))
    print("Hostname: {}".format(purl.hostname))
    print("Path: {}".format(purl.path))
    print("Query Parameters:")
    for item in purl.query.split('&'):
        try:
            key, value = item.split('=')
            print(("\t {:<30} = {}".format(key, value)))
        except ValueError:
            print(("\t {}".format(item)))
    print(purl.fragment)


def prettify(item):
    """ creates a json representation of item and returns as string """
    if type(item) == set:
        item = list(item)
    return json.dumps(item, indent=2,
                      separators=(',', ': '))


def pretty_print(item):
    """ Pretty prints a json representation of item """
    print(prettify(item))


def print_as_markdown_table(l, heading=None):
    """print(`l` as a markdown formatted table)

    Parameters
    ----------
    l : list of lists or list of tuples or pandas.Series
        the list of data you want printed. All rows must be same length
    heading : list
        a list of column headings. Must be same width as items of l
    """
    if type(l) != list and type(l) != pd.Series:
        raise TypeError("only supports printing list or pandas.Series")
    if type(l) == pd.Series:
        new_l = list()
        for key in l.keys():
            value = l.get_value(key)
            if type(value) != tuple:
                value = (value,)
            new_l.append(key + value)
        l = new_l
    output = ''
    if heading is not None:
        output += ' | '.join([str(x) for x in heading]) + '\n'
        output += '-|-'.join(['-'*len(str(x)) for x in heading]) + '\n'
    for item in l:
        output += ' | '.join([str(x) for x in item]) + '\n'
    print(output)


# Dataframe ##########

def add_tp_col(df, col1, col2):
    """ Add a third-party boolean column to dataframe `df`

    Parameters
    ----------
    df : pandas.DataFrame
        the dataframe the third-party column will be added to
    col1 : str
        first column to retrieve a url from
    col2 : str
        second column to retrieve a url from
    """
    df['is_tp'] = df[col1].apply(du.get_ps_plus_1) != \
        df[col2].apply(du.get_ps_plus_1)


def read_cache_or_query_db(con, db_query, csv_file="", versioned=True):
    """Read from the cached CSV file or the database.

    Cache the results to a CSV file. If `versioned` is True, the cache will
    be tied to the `db_query`. If `db_query` changes, the cache will be
    rebuilt."""
    if csv_file != "" and versioned:
        parts = csv_file.rsplit('.')
        csv_file = "{}-{}.csv".format(parts[0], hashlib.md5(db_query).hexdigest())
    used_cache = False
    should_query_db = False
    try:
        results = pd.read_csv(csv_file, sep="\t", keep_default_na=False)
        used_cache = True
    except Exception:
        should_query_db = True

    if should_query_db:
        results = pd.read_sql_query(db_query, con)

    if csv_file and not used_cache:  # only save if we queried the DB
        results.to_csv(csv_file, sep='\t', encoding='utf-8',
                       index=False)
    return results


# Sqlite ##########

def fetchiter(cursor, arraysize=10000):
    """ Generator for cursor results """
    while True:
        rows = cursor.fetchmany(arraysize)
        if rows == []:
            break
        for row in rows:
            yield row


def list_placeholder(length, is_pg=False):
    """
    Returns a (?,?,?,?...) string of the desired length
    if is_pg, returns ({},{},{},....) instead.
    """
    if is_pg:
        return '(' + '{},'*(length-1) + '{})'
    else:
        return '(' + '?,'*(length-1) + '?)'


def optimize_db(cursor):
    """ Runs PRAGMA queries to make sqlite better """
    cursor.execute("PRAGMA cache_size = -{}".format((0.1 * 10**7)))  # 10 GB
    # Store temp tables, indicies in memory
    cursor.execute("PRAGMA temp_store = 2")


def insert_get_id(cursor, table, arguments, unique):
    """
    Executes an INSERT OR IGNORE on a table where one column is unique
    The resulting ID is grabbed avoiding an extra SELECT statement if possible
    <table> - table name as string
    <arguments> - a dict of fields to insert
    <unique> - string or list of the fields that have a unique constraint
    """
    cursor.execute("INSERT OR IGNORE INTO {} ({}) VALUES {}".format(
        table, ','.join(arguments.keys()), list_placeholder(len(arguments)),
        arguments.values()))

    cursor.execute("SELECT last_insert_rowid(), changes();")
    ret_id, insert = cursor.fetchone()
    if not insert:
        if type(unique) == str:
            unique = [unique]
        cursor.execute("SELECT id FROM {} WHERE {}".format(table, " AND ".join(map(lambda x: "{} = ?".format((x, unique), map(lambda x: arguments[x], unique))))))

        ret_id = cursor.fetchone()[0]
    return ret_id


def insert_ignore(cursor, table, arguments, unique, index_fn=None):
    """
    Execute an INSERT OR IGNORE on a table with at least one unique column
    The ID of the new INSERT (or current row) is returned.
    <table> - table name as string
    <arguments> - a dict of fields to insert of form
        i.e. {<col1_name>:<col1_value>, <col2_name>:<col2_value>, ...}
    <unique> - string or list of the fields that have a unique constraint
        i.e. 'col1' or ['col1','col2']
    <index_fn> - A function name if the table has a functional index. e.g 'MD5'

    ONLY arguments' values should come from untrusted sources as the rest are
    not sanitized.
    """
    if type(unique) == str:
        unique = [unique]
    if index_fn is not None:
        where_str = index_fn + "({}) = " + index_fn + "(%{})"
    else:
        where_str = "{} = {}"

    query = "".join((  # makes substitutions more readable
        "WITH s AS ( ",
            "SELECT id ",
            "FROM {} ".format(table),
            "WHERE {} ".format(" AND ".join(map(lambda x: where_str.format(x, unique)))),
        "), i AS ( ",
            "INSERT INTO {} ({}) ".format(table, ','.join(arguments.keys())),
            "SELECT {} ".format(",".join(["{}"]*len(arguments))),
            "WHERE NOT EXISTS (SELECT 1 FROM s) ",
            "RETURNING id ",
        ") ",
        "SELECT id ",
        "FROM i ",
        "UNION ALL ",
        "SELECT id ",
        "FROM s "
    ))
    cursor.execute(query,
                   map(lambda x: arguments[x], unique) + arguments.values())
    return cursor.fetchone()[0]


def get_distinct_content_hashes(cur, url):
    cur.execute(
        "SELECT content_hash FROM http_responses WHERE url = ?", (url,))
    return set([x[0] for x in cur.fetchall()])

# LevelDB ##########


def get_leveldb(db_path, compression='snappy'):
    """
    Returns an open handle for a leveldb database
    with proper configuration settings.
    """
    db = plyvel.DB(db_path,
                   lru_cache_size=10**9,
                   write_buffer_size=128*10**4,
                   bloom_filter_bits=128,
                   compression=compression)
    return db


def get_url_content(url, sqlite_cur, ldb_con, beautify=True, visit_id=None):
    """Return javascript content for given url.

    Parameters
    ----------
    url : str
        url to search content hash for
    sqlite_cur : sqlite3.Cursor
        cursor for crawl database
    ldb_con : plyvel.DB
        leveldb database storing javascript content
    beautify : boolean
        Control weather or not to beautify output
    visit_id : int
        (optional) `visit_id` of the page visit where this URL was loaded
    """
    if visit_id is not None:
        sqlite_cur.execute(
            "SELECT content_hash FROM http_responses WHERE "
            "visit_id = ? AND url = ? LIMIT 1;", (visit_id, url))
    else:
        sqlite_cur.execute(
            "SELECT content_hash FROM http_responses WHERE url = ? LIMIT 1;",
            (url,))
    content_hash = sqlite_cur.fetchone()
    if content_hash is None or len(content_hash) == 0:
        print("Content hash not found for url {}".format( url))
        return
    return get_content(ldb_con, content_hash[0], beautify=beautify)


def get_content(db, content_hash, compression='snappy', beautify=True):
    """ Returns decompressed content from javascript leveldb database """
    content_hash=bytes(content_hash, "utf-8")
    if content_hash is None:
        print("ERROR: content_hash can't be None...")
        return
    content = db.get(content_hash)

    if content is None:
        print("ERROR: content hash: {} NOT FOUND".format(content_hash))
        return

    supported = ['snappy', 'none', 'gzip']
    if compression not in supported:
        print("Unsupported compression type {}. Only {} are the supported options.".format(compression, str(supported)))
        return
    elif compression == 'gzip':
        try:
            content = zlib.decompress(content, zlib.MAX_WBITS | 16)
        except Exception:
            try:
                content = zlib.decompress(content)
            except Exception:
                print("Failed to decompress gzipped content...")
                return
    if beautify:
        return jsbeautifier.beautify(str(content))
    else:
        return content


# ##### Page Source

def parse_src_frame(visit_id, url_hash, suffix, src_dict,
                    include_iframes, rv=None, parent=None):
    """Parse a frame from a page source dump into a flat return value"""
    if rv is None:
        rv = list()
    document_url = src_dict['doc_url']
    src = src_dict['source']
    children = set()
    for frame in src_dict['iframes'].values():
        if include_iframes:
            parse_src_frame(visit_id, url_hash, suffix, frame, include_iframes,
                            rv=rv, parent=document_url)
        children.add(frame['doc_url'])
    rv.append((visit_id, url_hash, suffix,
               document_url, src, tuple(children), parent))
    return


def build_page_source_df(src_dir, visit_ids=None, include_iframes=False):
    """Build a dataframe from crawl page source directory

    Output columns:
    visit_id, tab_url_hash, suffix, document_url, page_source,
    children (tuple of document URLs), parent (document URL)
    """
    if not os.path.isdir(src_dir):
        raise ValueError("{} not found".format(src_dir))

    src_zips = glob.glob(os.path.join(src_dir, '*.json.gz'))

    if len(src_zips) == 0:
        raise ValueError(" {} contains no source files".format(src_dir))

    sources = list()
    for src_zip in src_zips:
        basename = os.path.basename(src_zip)
        visit_id, url_hash, suffix = basename.rsplit('.', 2)[0].split('-')[0:3]
        visit_id = int(visit_id)

        if visit_ids is not None and visit_id not in visit_ids:
            continue

        with gzip.open(src_zip, 'rb') as f:
            try:
                page_src = json.load(f)
            except ValueError:
                continue

        # Flatten frames
        parse_src_frame(visit_id, url_hash, suffix,
                        page_src, include_iframes, rv=sources)

    df = pd.DataFrame(sources)
    df.columns = ['visit_id', 'tab_url_hash', 'suffix', 'document_url',
                  'page_source', 'children', 'parent']
    return df


def get_page_source(src_dir, visit_id, include_iframes=False):
    """Output: a list of dict sources
    visit_id, tab_url_hash, suffix, document_url, page_source,
    children (tuple of document URLs), parent (document URL)
    """
    if not os.path.isdir(src_dir):
        raise ValueError("{} not found".format(src_dir))

    src_zips = glob.glob(os.path.join(src_dir, '{}-*.json.gz'.format(visit_id)))

    if len(src_zips) == 0:
        raise ValueError("{} contains no source files from visit_id {}".format(src_dir, visit_id))

    out = list()
    for src_zip in src_zips:
        basename = os.path.basename(src_zip)
        visit_id, url_hash, suffix = basename.rsplit('.', 2)[0].split('-')[0:3]
        visit_id = int(visit_id)

        with gzip.open(src_zip, 'rb') as f:
            try:
                page_src = json.load(f)
            except ValueError:
                continue

        # Flatten frames
        parse_src_frame(visit_id, url_hash, suffix,
                        page_src, include_iframes, rv=out)
    df = pd.DataFrame(out)
    df.columns = ['visit_id', 'tab_url_hash', 'suffix', 'document_url',
                  'page_source', 'children', 'parent']
    return df


def create_visit_id_index(cur, table):
    if table in ["requests", "http_requests"]:
        print("CREATE INDEX http_requests")
        cur.execute("CREATE INDEX IF NOT EXISTS http_request_visit_id_index "
                    "ON http_requests(visit_id);")

    if table in ["responses", "http_responses"]:
        print("CREATE INDEX http_responses")
        cur.execute("CREATE INDEX IF NOT EXISTS http_responses_visit_id_index "
                    "ON http_responses(visit_id);")

    if table == "javascript":
        print("CREATE INDEX javascript")
        cur.execute("CREATE INDEX IF NOT EXISTS javascript_visit_id_index ON "
                    "javascript(visit_id);")
    print("Finished adding visit_id index to the table", table)


def dump_as_json(obj, json_path):
    with open(json_path, 'w') as f:
        json.dump(obj, f)


def load_json_file(json_path):
    with open(json_path) as json_file:
        return json.load(json_file)





##############################################################################

def get_top_url(script_url=None, visit_id=None):
    if visit_id is not None and script_url is not None:
        cur.execute(
            "SELECT top_level_url FROM javascript WHERE "
            "visit_id = ? AND script_url = ? LIMIT 1;", (visit_id, script_url))
    elif script_url is not None:
        cur.execute(
            "SELECT top_level_url FROM javascript WHERE script_url = ? LIMIT 1;",
            (script_url,))
    elif visit_id is not None:
        cur.execute(
            "SELECT top_level_url FROM javascript WHERE visit_id = ? LIMIT 1;",
            (visit_id,))

    top_url = cur.fetchone()
    if top_url is None or len(top_url) == 0 or top_url[0] is None or top_url[0].strip() == '':
#         print("Content hash not found for url {}".format(url)
        return ''
    return top_url[0]
