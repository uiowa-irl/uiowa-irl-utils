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


def gen_find_files(filepat, top):
    """
    http://www.dabeaz.com/generators/
    returns filenames that matches the given pattern under() a given dir
    """
    for path, _, filelist in os.walk(top):
        for name in fnmatch.filter(filelist, filepat):
            yield os.path.join(path, name)

def rmsubtree(location):
    """Clears all subfolders and files in location"""
    for root, dirs, files in os.walk(location):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))



def tar_unpacker(**kwargs):
    tar_path = kwargs.get('tar_path','')
    num_files = len(os.listdir(tar_path))
    count=1
    for file in os.listdir(tar_path):
        tmp_path = tempfile.mkdtemp()

        count+=1
        path = os.path.join(tar_path, file)
        tf = tarfile.open(path)
        tf.extractall(path=tmp_path)

def tar_unpacker_and_search(tar_path, pattern="", extract_parent_dir='', extract_tmp_dir=''):
    path = tar_path
    tf = tarfile.open(path)
    tf.extractall(path=extract_tmp_dir)        
    tmp_dir = os.path.join(extract_tmp_dir, extract_tmp_dir)
    tmp_path = gen_find_files(pattern, tmp_dir)
    return tmp_path           

def json_flatten( **kwargs):
    data = kwargs.get('data')
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
        

