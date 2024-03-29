#!/usr/bin/python3
#

from .constants import GLOBALS
from signal import signal,SIGINT,SIGTERM
from tempfile import TemporaryDirectory

class Tempfolder:
    folder: TemporaryDirectory = None

    @classmethod
    def init(cls):
        cls.folder = TemporaryDirectory(prefix='%s-' % GLOBALS['program_name'])

class Terminator:
    interrupt = False
    __initialized = False

    def init(cls):
        if not cls.__initialized:
            signal(SIGINT, cls.set_interrupt)
            signal(SIGTERM, cls.set_interrupt)
            cls.__initialized = True

    @classmethod
    def set_interrupt(cls, *args):
        cls.interrupt = True
