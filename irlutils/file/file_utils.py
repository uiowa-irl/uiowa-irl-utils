import os
import json
import shutil
import tarfile
import fnmatch
import argparse
import tempfile

"""
References: 
[1] Englehardt, Steven, and Arvind Narayanan. 
    "Online tracking: A 1-million-site measurement and analysis." 
    In Proceedings of the 2016 ACM SIGSAC Conference on Computer and 
    Communications Security, pp. 1388-1401. ACM, 2016.
"""
__author__="senorchow"

def gen_find_files(**kwargs):
    """returns filenames that matches the given pattern under() a given dir


    Kwargs:
        file_pattern (str): a regex style string . 
        root (str): top level folder to begin search from. 

    Yields:
        path: matching path str

    Examples:
        gen_find_files(file_pattern="*.sql", root="/mnt/data/).

        >>> gen_find_files(file_pattern="*.sql", root="/mnt/data/)
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
    """Clears all subfolders and files in location"""
    location = kwargs.get("location", "")
    for root, dirs, files in os.walk(location):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))



def tar_unpacker(**kwargs):
    """ unpacks tar to a tmp directory. 


    Kwargs:

        tar_path (str): tar file path
        versbose (bool): True enables verbose

    Yields:

        tmp_path: extracted contents path

    Examples:

        tar_unpacker(file_pattern="/mnt/data/tarfile.tar.gz").

        >>> tar_unpacker(file_pattern="/mnt/data/tarfile.tar.gz").
        /tmp/FZ4245_Zb/
    """
    tar_path = kwargs.get('tar_path','')
    verbose = kwargs.get("verbose", False)
    count=1
    
    tmp_path = tempfile.mkdtemp()

    count+=1
    command ="tar -xf {}".format(tar_path)

    if verbose: 
        command ="tar -xvf {}".format(tar_path)
    os.system(command)
    return tmp_path


def json_flatten(**kwargs):
    data = kwargs.get('data',"")
    kv = kwargs.get('kv', {})
    try: 
        for key,value in data.items():
            # print("{}->{}".format(key, value))
            if type(value) == type(dict()):
                json_flatten(data=value, kv=kv)
            elif type(value) == type(list()):
                for val in value:
                    if type(val) == type(str()):
                        
                        kv[key] = val
                        # print("kv str: {}".format(kv))
                        pass
                    elif type(val) == type(list()):
                        kv[key] = val
                        # print("kv list: {}".format(kv))
                        pass
                    else:
                        json_flatten(data=val, kv=kv)
            else: 
                kv[key] = value
                # print("kv: {}".format(kv))

        return kv
    except Exception: 
        return kv
        

