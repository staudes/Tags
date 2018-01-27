#!/usr/bin/env python3

import os

def find_tags(start_dir):
    """ returns paths to all .tags files beneath the given directory
    """
    for p, d, files in os.walk(start_dir):
        for f in files:
            if f == '.tags':
                yield p + '/.tags'

def create_link(target, name):
    os.symlink(target, name)

def parse_line(line):
    try:
        tag, name = line.split(',')
        if not name.strip():
            name = None
    except ValueError:
        tag = line
        name = None
    return tag.split('/'), name

def create_dirs(base_dir, dirs: list):
    base_path = os.path.abspath(base_dir)
    os.chdir(base_path)
    for d in dirs:
        if os.path.exists(d):
            if not os.path.isdir(d) or os.path.islink(d):
                raise ValueError('Cannot create directory "{}". Path is blocked'.format(d))
        else:
            os.mkdir(d)
            os.chdir(d)
    os.chdir(base_path)

def process_file(tags_file, base_dir):
    with open(tags_file, 'r') as f:
        for l in f.readlines():
            dirs, name = parse_line(l)
            if name is None:
                name = tags_file.rsplit('/.', 1)[0].rsplit('/', 1)[1]
            create_dirs(base_dir, dirs)
            create_link(tags_file.rsplit('/', 1)[0], name)

def process_file(conf):
    with open(conf, 'r') as f:
        path, tag_dir = f.read().strip().split('\n')
        for t in find_tags(path):
            process_file(t)

