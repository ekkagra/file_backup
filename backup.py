# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 20:41:28 2020

@author: Ekkagra
"""
import os
import hashlib
import argparse
import copy
import json
import re
from datetime import datetime as dt

import util

timestamp = dt.now().strftime('%Y%m%d_%H%M%S')
os.makedirs(f'./{timestamp}/')
cur_path = f'./{timestamp}'

def get_dirs():
    with open(os.path.join(cur_path,'backup_todo.txt'),'r') as f:
        files = f.read() 
    files = files.split('\n')

    dir_names = []
    for file in files: 
        if os.path.dirname(file) not in dir_names: 
            dir_names.append(os.path.dirname(file)) 

    with open(os.path.join(cur_path,'dir_names.txt'),'w') as f: 
        for dirr in dir_names: 
            f.write(str(dirr)+'\n')

exclude_list = [r'\.git', 'e[0-9]+', 'env[0-9]+','dlib','face_recogni',r'\.pyc']
exclude_list_re = [re.compile(ele) for ele in exclude_list]

def calc_hash(filepath):
    a = hashlib.sha256()
    with open(filepath,'rb') as f:
        for chunk in f:
            a.update(chunk)
    return a

def exclude_check(path,exclude_list_re):
    exclude = False
    for regx in exclude_list_re:
        if regx.search(path):
            exclude = True
            break
    return exclude

def main(args):
    if args['backup_manifest']:
        with open(args['backup_manifest'],'r') as f:
            manifest = json.load(f)
        file_hash = manifest['file_hash']
        hash_file = manifest['hash_file']
    else:
        file_hash = {}
        hash_file = {}
        for root,dirs,files in os.walk(args['backup_dir']):
            for file in files:
                filepath = os.path.join(root,file)
                if not exclude_check(filepath,exclude_list_re):
                    a = calc_hash(filepath)
                    a_hash = a.hexdigest()
                    if a.hexdigest() not in hash_file:
                        hash_file[a.hexdigest()] = []
                    hash_file[a.hexdigest()].append(filepath)
                    file_hash[filepath] = a.hexdigest()
    #                 if a.hexdigest() in hash_file:
    # #                    print(filepath)
    #                     b = calc_hash(hash_file[a.hexdigest()])
    #                     b.update('0'.encode())
    #                     a.update('0'.encode())
    #                     if a.hexdigest() == b.hexdigest():
    # #                        print('Same File:{0} || {1}'.format(filepath,hash_file[a_hash]))
    #                         temp = hash_file[a.hexdigest()]
    #                         hash_file[a.hexdigest()]
    #                     else:
    #                         print('Different file:{0} || {1}'.format(filepath,hash_file[a_hash]))
        manifest = {}
        manifest['file_hash'] = file_hash
        manifest['hash_file'] = hash_file
        with open(os.path.join(cur_path,'existing_backup_hash.json'),'w') as f:
            json.dump(manifest,f,indent=4)
    
    if args['target_dir']:
        to_be_backup = []
        for root,dirs,files in os.walk(args['target_dir']):
            for file in files:
                filepath = os.path.join(root,file)
                if not exclude_check(filepath,exclude_list_re):
                    h = calc_hash(filepath)
                    h_digest = h.hexdigest()
                    if h_digest in hash_file:
                        h.update('0'.encode())
                        match_found = False
                        for pth in hash_file[h_digest]:
                            backup_h = calc_hash(pth)
                            backup_h.update('0'.encode())
                            if h.hexdigest() == backup_h.hexdigest():
                                print('.')
                                match_found = True
                                break
                        if not match_found:
                            print(filepath)
                            to_be_backup.append(filepath)
                    else:
                        print(filepath)
                        to_be_backup.append(filepath)
        
        print('done')                        
        with open(os.path.join(cur_path,'backup_todo.txt'),'w') as f:
            for ele in to_be_backup:
                f.write(str(ele)+'\n')
        out_dict = util.convert_paths_to_dict(to_be_backup)        
        with open(os.path.join(cur_path,'backup_todo.json'), 'w') as f:
            json.dump(out_dict, f, indent=4)
    else:
        print(f'No target_dir found. \nWritten json for backup_dir @ \'existing_backup_hash.json\'.\nFinished.')

    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t',dest='target_dir',help='Target directory which needs to be backed up')
    parser.add_argument('-b',dest='backup_dir',help='Backup directory root',required=True)
    parser.add_argument('-f',dest='backup_manifest',help='Backup Hash file')
    args = parser.parse_args()
    args=vars(args)
    main(args)