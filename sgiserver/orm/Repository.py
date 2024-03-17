from lib.db import *
from .Client import *
# from .Message import *

class Repository:
    def __init__(self):
        conn = connect()
        self.conn = conn[0]
        self.curs = conn[1]
