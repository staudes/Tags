#!/usr/bin/env python3

import os

def find_tags(start_dir):
    """ returns paths to all .tags files beneath the given directory
    """
    for p, d, files in os.walk(start_dir):
        for f in files:
            if f == '.tags':
                yield p

def create_link(target, name):

    os.symlink(target, name)

def process_line(line):
    try:
        tag, name = line.split(',')
        if not name.strip():
            name = None
    except ValueError:
        tag = line
        name = None
    if os.path.exists(tag):
        if not os.path.isdir(tag):
            raise FileExistsError(tag + ' exists and is no directory!')
    else:
        os.path.mkdir(tag)
    os.chdir(tag)
    create_link(target, name)
    os.chdir('..')

def process_file(tags_file):
    with open(tags_file, 'r') as f:
        for l in f.readlines():
            process_line(l)
