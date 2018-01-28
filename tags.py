#!/usr/bin/env python3

import os
import sys
import shutil

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
        name = name.strip()
        if not name:
            name = None
    except ValueError:
        tag = line
        name = None
    return tag.strip().split('/'), name

def create_dirs(base_dir, dirs: list):
    cwd = os.getcwd()
    base_path = os.path.abspath(base_dir)
    os.chdir(base_path)
    for d in dirs:
        if os.path.exists(d):
            if not os.path.isdir(d) or os.path.islink(d):
                raise ValueError('Cannot create directory "{}". Path is blocked'.format(d))
        else:
            os.mkdir(d)
            os.chdir(d)
    os.chdir(cwd)

def process_file(tags_file, base_dir):
    with open(tags_file, 'r') as f:
        for l in f.readlines():
            dirs, name = parse_line(l)
            if name is None:
                name = tags_file.rsplit('/.', 1)[0].rsplit('/', 1)[1]
            create_dirs(base_dir, dirs)
            create_link(os.path.abspath(tags_file.rsplit('/', 1)[0]), os.path.join(base_dir, *dirs, name))

def run(conf):
    with open(conf, 'r') as f:
        path, tag_dir = f.read().strip().split('\n')
        shutil.rmtree(tag_dir)
        os.mkdir(tag_dir)
        os.rmdir
        for t in find_tags(path):
            process_file(t, tag_dir)

if __name__ == '__main__':
    run(sys.argv[1])
