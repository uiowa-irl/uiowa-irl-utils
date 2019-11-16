
import os
import json
import shutil
import fnmatch
import argparse
import tempfile
from pathlib import PurePath
import lcdk.lcdk as LeslieChow
"""
References: 
[1] Englehardt, Steven, and Arvind Narayanan. 
    "Online tracking: A 1-million-site measurement and analysis." 
    In Proceedings of the 2016 ACM SIGSAC Conference on Computer and 
    Communications Security, pp. 1388-1401. ACM, 2016.
"""
__author__="johncook"
DBG = LeslieChow.lcdk(logsPath='file_utils_debug.log')



def gen_find_files(**kwargs):
    """returns filenames that matches the given pattern under() a given dir


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
    """

    file_pattern = kwargs.get("file_pattern", "")
    root = kwargs.get("root", "")
    for path, _, filelist in os.walk(root):
        for name in fnmatch.filter(filelist, file_pattern):
            yield os.path.join(path, name)

def rmsubtree(**kwargs):
    """Clears all subfolders and files in location
    kwargs:
        location (str): target directory to remove
    Examples:

        >>> rmsubtree(location="/path/to/target_dir").

    """
    path = kwargs.get("path", "")
    for root, dirs, files in os.walk(path):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))

def mv(s,d):
    try: 
        shutil.move(s,d) 
    except Exception as e:
        DBG.error(e)
        return -1 
    return 0

def cp(s,d):
    try: 
        shutil.copy(s,d) 
    except Exception as e:
        DBG.error(e)
        return -1 
    return 0
        

def mkdir(d, mode=0o777, exist_ok=True):
    try: 
        os.makedirs(d, mode=mode, exist_ok=exist_ok)
    except Exception as e:
        DBG.error(e)
        return -1 
    return 0

def touch(d):
    status=""
    if not os.path.exists(d):
        status = open(d,'w')
    return status

def chmod(path, mode=777, recursive=False):
    try:
        if recursive: 
            os.system('sudo chmod {} -R {}'.format(mode, path))
        else:
            os.system('sudo chmod {} {}'.format(mode, path))
    except Exception as e:
        DBG.error(e)
        return -1 
    return 0

def chownUser(path, recursive=False, owner='user', group='user'):
    try:
        if recursive:
            os.system('sudo chown  {} -R {}')
        else:
            os.system('sudo chown  {} {}')
    except Exception as e:
        DBG.error(e)
        return -1 
    return 0

def file_ext(path, **kwargs):
    """file extension finder
    kwargs:
        path (str): path or file name
    Returns:
        dotted file extension of a file
    Examples:

        >>> file_ext('/path/to_file/with_ext/test.py')
            .py
    """
    f = PurePath(path).suffix
    return f

def tar_unpacker(tar_path, **kwargs):
    """ unpacks tar to a tmp directory. 


    Kwargs:

        tar_path (str): tar file path
        versbose (bool): True enables verbose

    returns:

        tmp_path (generator): extracted contents path

    Examples:

        tar_unpacker(tar_path="/mnt/data/tarfile.tar.gz").

        >>> tar_unpacker(tar_path="/mnt/data/tarfile.tar.gz").
        /tmp/FZ4245_Zb/
    """
    verbose = kwargs.get("verbose", False)
    tmp_path = tempfile.mktemp()
    extract_dir = kwargs.get("extract_dir", tmp_path)

    cmd = "tar -xf {}".format(tar_path)
    if extract_dir != tmp_path: 
        cmd  = "tar -xf {} -C {}".format(tar_path, extract_dir)
    if verbose: 
        cmd = "tar -xf {}".format(tar_path)
        if extract_dir != tmp_path: 
            cmd  = "tar -xvf {} -C {}".format(tar_path, extract_dir)
    os.system(cmd)
    return tmp_path

def tar_packer(tar_dir, **kwargs):
    """ tars up  directory 


    Kwargs:

        dir (str): top level dir
        compression (bool): compression type. gz, xz supported now
        versbose (bool): True enables verbose

    returns:

        tar_path (generator): path to tar file

    Examples:

        tar_packer(dir="/path/to/top_level_dir", [compression=gz|xz]

        >>> 
            /tmp/FZ4245_Zb/top_level_dir.tar
    """
    compression = kwargs.get('compression','')
    verbose = kwargs.get("verbose", False)
    tmp_path = tempfile.mkdtemp()
    file = tar_dir+'.tar'
    path = os.path.join(tmp_path, file)
    cmd ="tar -cf {}".format(path)
    if verbose: 
        cmd ="tar -cvf {}".format(path)
    if compression == 'xz': 
        cmd ="tar -cJf {}".format(path)
        if verbose: 
            cmd ="tar -cJvf {}".format(path)
    if compression == 'gz': 
        cmd ="tar -czf {}".format(path)
        if verbose: 
            cmd ="tar -czvf {}".format(path)

    os.system(cmd)
    return tmp_path

def rm(d):
    try:
        rmsubtree(path=d)
    except Exception as e:
        DBG.error(e)
        return -1 
    return 0

def compress_path( path):
    try:
        tmp = tar_packer(tar_dir=path)
    except Exception as e:
        DBG.error(e)
        return '' 
    return tmp

def json_flatten(y):
    """ flattens nested structures within a json file


    Kwargs:

        data (dict): data from nested dictionary
        kv (dict): dictionary containing key,value pairs. 

    returns:

        kv (dict): a dictionary object containing flattened structures

    Examples:
        data = {'k1':{'kv1':['v1', 'v2'], 'kv2': 'v3'}}

        >>> json_flatten(data)
            {'k1_kv1_0': 'v1', 'k1_kv1_1': 'v2', 'k1_kv2': 'v3'}

    """
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

