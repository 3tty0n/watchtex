# -*- coding: utf-8 -*-

import time
import os

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

observed_file_type = (
    '.tex',
    '.jpg',
    '.png',
    '.eps',
    '.sty',
)

BASEDIR = os.path.abspath(os.path.dirname(__file__))
TARGET = 'doc'
LATEX = 'platex'
OUTPUT = 'build'
LATEX_OPTION = '-interaction=nonstopmode -output-directory=%s' % OUTPUT
DVIPDFMX = 'dvipdfmx'
DVIPDFMX_OPTION=''

latex_compile = ' '.join([
    LATEX,
    LATEX_OPTION,
    TARGET + '.tex',
])

dvi2pdf = ' '.join([
    DVIPDFMX,
    DVIPDFMX_OPTION,
    '-o %s/%s.pdf' % (OUTPUT, TARGET),
    '%s/%s.dvi' % (OUTPUT, TARGET),
])


def match(path):
    return any([path.endswith(ft) for ft in observed_file_type])


def build():
    os.system(latex_compile)
    os.system(dvi2pdf)


class ChangeHandler(FileSystemEventHandler):
    def on_create(self, event):
        if event.is_directory:
            return
        if match(event.src_path):
            build()

    def on_modified(self, event):
        if event.is_directory:
            return
        if match(event.src_path):
            build()

    def on_deleted(self, event):
        if event.is_directory:
            return
        if match(event.src_path):
            build()


if __name__ in '__main__':
    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, BASEDIR, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
