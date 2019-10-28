
# IRL Utilities
# Installation
## git

```
git clone https://github.com/uiowa-irl/uiowa-irl-utils.git
cd uiowa-irl-utils
pip install --user .
```

## pypi

```
pip install irlutils
``` 
 
import the  module: 

```
import irlutils
```


# Documentation


## file_utils
```
FUNCTIONS
    gen_find_files(**kwargs)
        returns filenames that matches the given pattern under() a given dir
        
        
        Kwargs:
            file_pattern (str): a regex style string . 
            root (str): top level folder to begin search from. 
        
        Yields:
            path (generator): matching path str
        
        Examples:
            gen_find_files(file_pattern="*.sql", root="/mnt/data/).
        
            >>> gen_find_files(file_pattern="*.sql", root="/mnt/data/).__next__()
            /mnt/data/first_folder/last_folder/file.sqlite
            
        Reference: 
            [1] http://www.dabeaz.com/generators/
    
    json_flatten(y)
        flattens nested structures within a json file
        
        
        Kwargs:
        
            data (dict): data from nested dictionary
            kv (dict): dictionary containing key,value pairs. 
        
        returns:
        
            kv (dict): a dictionary object containing flattened structures
        
        Examples:
            data = {'k1':{'kv1':['v1', 'v2'], 'kv2': 'v3'}}
        
            >>> json_flatten(data)
                {'k1_kv1_0': 'v1', 'k1_kv1_1': 'v2', 'k1_kv2': 'v3'}
    
    rmsubtree(**kwargs)
        Clears all subfolders and files in location
        kwargs:
            location (str): target directory to remove
        Examples:
        
            >>> rmsubtree(location="/path/to/target_dir").
    
    tar_unpacker(**kwargs)
        unpacks tar to a tmp directory. 
        
        
        Kwargs:
        
            tar_path (str): tar file path
            versbose (bool): True enables verbose
        
        returns:
        
            tmp_path (generator): extracted contents path
        
        Examples:
        
            tar_unpacker(file_pattern="/mnt/data/tarfile.tar.gz").
        
            >>> tar_unpacker(file_pattern="/mnt/data/tarfile.tar.gz").
            /tmp/FZ4245_Zb/

AUTHOR
    senorchow

FILE
    irlutils/file/file_utils.py
```
## database_utils
```
FUNCTIONS
    build_index(cursor, column, tables)
        Build an index on `column` for each table in `tables`
    
    drop_tables(sqlite_con, tables=[])
    
    fetchiter(cursor, arraysize=10000)
        Generator for cursor results
    
    get_channel_content(visit_id, channel_id, sqlite_cur, ldb_con, beautify=True)
        Return javascript content for given channel_id.
        Parameters
        ----------
        visit_id : int
            `visit_id` of the page visit where this URL was loaded
        channel_id : string
            `channel_id` to search content hash for
        sqlite_cur : sqlite3.Cursor
            cursor for crawl database
        ldb_con : plyvel.DB
            leveldb database storing javascript content
        beautify : boolean
            Control weather or not to beautify output
    
    get_channel_content_with_hash(visit_id, channel_id, sqlite_cur, ldb_con, beautify=True)
        Return javascript content for given channel_id.
        Parameters
        ----------
        visit_id : int
            `visit_id` of the page visit where this URL was loaded
        channel_id : string
            `channel_id` to search content hash for
        sqlite_cur : sqlite3.Cursor
            cursor for crawl database
        ldb_con : plyvel.DB
            leveldb database storing javascript content
        beautify : boolean
            Control weather or not to beautify output
    
    get_content(db, content_hash, compression='snappy', beautify=True)
        Returns decompressed content from javascript leveldb database
    
    get_ldb_content(ldb_addr, content_hash)
    
    get_leveldb(db_path, compression='snappy')
        Returns an open handle for a leveldb database
        with proper configuration settings.
    
    get_url_content(url, sqlite_cur, ldb_con, beautify=True, visit_id=None)
        Return javascript content for given url.
        Parameters
        ----------
        url : string
            url to search content hash for
        sqlite_cur : sqlite3.Cursor
            cursor for crawl database
        ldb_con : plyvel.DB
            leveldb database storing javascript content
        beautify : boolean
            Control weather or not to beautify output
        visit_id : int
            (optional) `visit_id` of the page visit where this URL was loaded
    
    get_url_content_with_hash(url, sqlite_cur, ldb_con, beautify=True, visit_id=None)
        Return javascript content for given url.
        Parameters
        ----------
        url : string
            url to search content hash for
        sqlite_cur : sqlite3.Cursor
            cursor for crawl database
        ldb_con : plyvel.DB
            leveldb database storing javascript content
        beautify : boolean
            Control weather or not to beautify output
        visit_id : int
            (optional) `visit_id` of the page visit where this URL was loaded
    
    list_placeholder(length, is_pg=False)
        Returns a (?,?,?,?...) string of the desired length
    
    optimize_db(cursor)
        Set options to make sqlite more efficient on a high memory machine

FILE
    irlutils/url/crawl/database_utils.py
```

## domain_utils

```
FUNCTIONS
    get_hostname(url)
        strips out the hostname from a url
    
    get_ps_plus_1(url, **kwargs)
        Returns the PS+1 of the url. This will also return
        an IP address if the hostname of the url is a valid
        IP address.
        
        An (optional) PublicSuffixList object can be passed with keyword arg 'psl',
        otherwise a version cached in the system temp directory is used.
    
    get_psl(location='public_suffix_list.dat')
        Grabs an updated public suffix list.
    
    get_stripped_query_string(url)
    
    get_stripped_url(url, scheme=False)
        Returns a url stripped to (scheme)?+hostname+path
    
    get_stripped_urls(urls, scheme=False)
        Returns a set (or list) of urls stripped to (scheme)?+hostname+path
    
    hostname_subparts(url, include_ps=False, **kwargs)
        Returns a list of slices of a url's hostname down to the PS+1
        
        If `include_ps` is set, the hostname slices will include the public suffix
        
        For example: http://a.b.c.d.com/path?query#frag would yield:
            [a.b.c.d.com, b.c.d.com, c.d.com, d.com] if include_ps == False
            [a.b.c.d.com, b.c.d.com, c.d.com, d.com, com] if include_ps == True
        
        An (optional) PublicSuffixList object can be passed with keyword arg 'psl'.
        otherwise a version cached in the system temp directory is used.
    
    is_ip_address(hostname)
        Check if the given string is a valid IP address
    
    load_psl(function)

DATA
    PSL_CACHE_LOC = 'public_suffix_list.dat'
    absolute_import = _Feature((2, 5, 0, 'alpha', 1), (3, 0, 0, 'alpha', 0...
    print_function = _Feature((2, 6, 0, 'alpha', 2), (3, 0, 0, 'alpha', 0)...

FILE
    irlutils/url/crawl/domain_utils.py
```

## blocklist_utils

```
FUNCTIONS
    get_option_dict(request)
        Build an options dict for BlockListParser
        
        Parameters
        ----------
        request : sqlite3.Row
            A single HTTP request record pulled from OpenWPM's http_requests table
        public_suffix_list : PublicSuffixList
            An instance of PublicSuffixList()
        
               BINARY_OPTIONS = [
            "script",
            "image",
            "stylesheet",
            "object",
            "xmlhttprequest",
            "object-subrequest",
            "subdocument",
            "document",
            "elemhide",
            "other",
            "background",
            "xbl",
            "ping",
            "dtd",
            "media",
            "third-party",
            "match-case",
            "collapse",
            "donottrack",
        ]
        
        Returns
        -------
        dict
            An "options" dictionary for use with BlockListParser
            refs: [1] https://github.com/MoonchildProductions/UXP/blob/master/dom/base/nsIContentPolicyBase.idl
                  [2] https://adblockplus.org/en/filters#options
                  [3]

FILE
    irlutils/url/crawl/blocklist_utils.py
```

## analysis_utils

```
FUNCTIONS
    add_col_bare_script_url(js_df)
        Add a col for script URL without scheme, www and query.
    
    add_col_set_of_script_ps1s_from_call_stack(js_df)
        map psls to call stack in scripts
        
        Args: 
            js_df (pandas dataFrame): javascript table
    
    add_col_set_of_script_urls_from_call_stack(js_df)
    
    add_col_unix_timestamp(df)
    
    datetime_from_iso(iso_date)
        Convert from ISO.
    
    get_cookie(headers)
        A special case of parse headers that extracts only the cookie. 
        
        Args: 
            headers (list): http request headers
        
        Returns:
        
            item(string): name value pairs of a cookie
    
    get_func_and_script_url_from_initiator(initiator)
        Remove line number and column number from the initiator.
    
    get_host_from_url(url)
    
    get_initiator_from_call_stack(call_stack)
        Return the bottom element of the call stack.
    
    get_initiator_from_req_call_stack(req_call_stack)
        Return the bottom element of a request call stack.
        Request call stacks have an extra field (async_cause) at the end.
    
    get_requests_from_visits(con, visit_ids)
        Extact http requests matching visit_ids
        
        Args: 
            con (sqlite3.connection): A connection to a sqlite data base
            visit_ids (list): A list of ids for from each web visit
        
        Returns:
             df(pandas DataFrame): A table containing visits that conincide with http requests
    
    get_responses_from_visits(con, visit_ids)
        Extact http requests matching visit_ids
        
        Args: 
            con (sqlite3.connection): A connection to a sqlite data base
            visit_ids (list): A list of ids for from each web visit
        
        Returns:
             df(pandas DataFrame): A table containing visits that conincide with http responses
    
    get_script_url_from_initiator(initiator)
        Remove the scheme and query section of a URL.
    
    get_script_urls_from_call_stack_as_set(call_stack)
        Return the urls of the scripts involved in the call stack as a set.
    
    get_set_cookie(header)
        A special case of parse headers that returns 'Set-Cookies'
        
        Args: 
            headers (string): http request headers
        
        Returns:
             item(string): name value pairs of Set Cookie field
    
    get_set_of_script_hosts_from_call_stack(call_stack)
        Return the urls of the scripts involved in the call stack.
    
    get_set_of_script_ps1s_from_call_stack(script_urls, du)
        extract a unique set of urls from a list of urls detected in scripts
        
        Args: 
            script_urls (list): A list of urls extracted from javascripts
            du (list): A domain utilities instance
        
        Returns:
             psls(set): a set of tld+1(string)
    
    get_set_of_script_urls_from_call_stack(call_stack)
        Return the urls of the scripts involved in the call stack as a
        string.
    
    parse_headers(header)
        parses http header into kv pairs
        
        Args: 
            headers (string): http request headers
        
        Returns:
             kv(dict): name value pairs of http headers
    
    strip_scheme_www_and_query(url)
        Remove the scheme and query section of a URL.

DATA
    absolute_import = _Feature((2, 5, 0, 'alpha', 1), (3, 0, 0, 'alpha', 0...
    print_function = _Feature((2, 6, 0, 'alpha', 2), (3, 0, 0, 'alpha', 0)...

FILE
    irlutils/url/crawl/analysis_utils.py
```

## chi2_proportions

```
FUNCTIONS
    chi2Proportions(count, nobs)
        A wrapper for the chi2 testing proportions based upon the chi-square test
        
        Args:
            count (:obj `list` of :obj`int` or a single `int`):  the number of successes in nobs trials. If this is 
            array_like, then the assumption is that this represents the number of successes 
            for each independent sample 
        
        
            nobs (:obj `list` of :obj`int` or a single `int`):  The number of trials or observations, with the same length as count. 
        
        Returns: 
            chi2  (:obj `float`): The test statistic.
        
            p (:obj `float`): The p-value of the test
        
            dof (int) : Degrees of freedom
        
            expected (:obj `list`): list same shape as observed. The expected frequencies, based on the marginal sums of the table
        
        
        References: 
        [1] "scipy.stats.chi2_contingency" https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.chi2_contingency.html
        [2] "statsmodels.stats.proportion.proportions_chisquare"  https://www.statsmodels.org/dev/generated/statsmodels.stats.proportion.proportions_chisquare.html
        [3] (1, 2) “Contingency table”, https://en.wikipedia.org/wiki/Contingency_table
        [4] (1, 2) “Pearson’s chi-squared test”, https://en.wikipedia.org/wiki/Pearson%27s_chi-squared_test
        [5] (1, 2) Cressie, N. and Read, T. R. C., “Multinomial Goodness-of-Fit Tests”, J. Royal Stat. Soc. Series B, Vol. 46, No. 3 (1984), pp. 440-464.
        
        Sample use: 
            input: 
            [10,10,20] - number of successes in trial 
            [20,20,20] - number of trials 
            chi2Proportions([10,10,20], [20,20,20])
            
            output: 
            (2.7777777777777777,
            0.24935220877729619,
            2,
            array([[ 12.,  12.,  16.],
                [ 18.,  18.,  24.]]))

FILE
    irlutils/stats/tests/proportions/chi2_proportions.py
```
