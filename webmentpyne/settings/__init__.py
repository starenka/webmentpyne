#!/usr/bin/env python
# -*- coding: utf-8 -*-
from base import *

try:
    from local import *
except ImportError:
    from prod import *
