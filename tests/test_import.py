# -*- coding: utf-8 -*-
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

from blocksync import *  # noqa
from blocksync.adapters.steem import * # noqa

# pylint: disable=unused-import,unused-variable
def test_import():
    _ = Blocksync()
    _ = SteemAdapter()
