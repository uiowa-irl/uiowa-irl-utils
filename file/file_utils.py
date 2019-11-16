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
def rm(self,d):
    shutil.rmtree()

def mkdir(self,d):
    os.makedirs(d)

def touch(self,d):
    open(d,'w')

def compress_path(self, path):
    tmp = tar_packer(tar_dir=path)
    return tmp

def rm(self,d):
    fu.rmsubtree(location=d)

def chmod(path, mode=0o777, exist=False):
    os.system('sudo chmod {}} -R /home/user'.format(mode, ))


def chownUser(self):
    os.system('sudo chown -R user:user /home/user')

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

def tar_packer(**kwargs): 
    tar_dir = kwargs.get('tar_path','')
    os.system('tar_')
    

def tar_unpacker(**kwargs):
    tar_path = kwargs.get('tar_path','')
    count=1
    tmp_path = tempfile.mkdtemp()
    if tmp_path != '' and tar_path !='':
        count+=1
        path = os.path.join(tar_path, tar_path)
        os.system('tar -xf {} path -C {}'.format(tar_path, path))
        return tmp_path
    else: 
        return ""

def compress_path(path):
    tmp = tar_packer(tar_path=path)
    return tmp

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
        

