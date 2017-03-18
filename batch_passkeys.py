#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 03:27:26 2017

@author: dfi
"""

from flatbencode import encode as benc
from flatbencode import decode as bdec
import os


def read_result(file_name):
    with open(file_name, 'rb') as o:
        r = o.read()
        return bdec(r)
    
    
def replace_passkey(content, old_pk, new_pk):
    replaced = False
    for k in content:
        try:
            if b'passkey=' in content[k]:
                temp = content[k].replace(str.encode(old_pk), str.encode(new_pk))
                if temp != content[k]:
                    replaced = True
                    content[k] = temp
        except:
            pass
    return replaced


def write_result(content, new_file_name):
    output_dir = './output_torrents'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    with open(os.path.join(output_dir, new_file_name), 'wb') as w:
        w.write(benc(content))


def compare_two_torrents(file_1, file_2):
    r1 = {}
    r2 = {}
    result = []
    with open(file_1, 'rb') as o1:
        r1 = bdec(o1.read())
    with open(file_2, 'rb') as o2:
        r2 = bdec(o2.read())
    for k in r1:
        if not k in r2:
            result.append('file_1 has diff key')
    for k in r2:
        if not k in r2:
            result.append('file_2 has diff key')
    for k in r1:
        if r1[k] != r2[k]:
            result.append('diff:\n', r1[k], '\n', r2[k])
        
        
def process_all_torrent_files():
    old_pk, new_pk = receive_input_passkeys()
    for root, dirs, files in os.walk('./input_torrents/'):
        for file in files:
            filename = os.path.join(root,file)
            suffix = os.path.splitext(filename)[1][1:]
            if suffix == 'torrent':
                r = read_result(filename)
                if replace_passkey(r, old_pk, new_pk):
                    write_result(r, file)
                
                
def receive_input_passkeys():
    old_passkey = input('Enter old passkey: ')
    new_passkey = input('Enter new passkey: ')
    return (old_passkey, new_passkey)

process_all_torrent_files()
