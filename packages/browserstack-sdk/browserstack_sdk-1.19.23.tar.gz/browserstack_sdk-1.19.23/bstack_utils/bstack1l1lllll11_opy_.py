# coding: UTF-8
import sys
bstack1lllll1_opy_ = sys.version_info [0] == 2
bstack1l1ll1l_opy_ = 2048
bstack11l11_opy_ = 7
def bstack1l_opy_ (bstack1l1l1l_opy_):
    global bstack11ll_opy_
    bstack1l1111l_opy_ = ord (bstack1l1l1l_opy_ [-1])
    bstack1l1l111_opy_ = bstack1l1l1l_opy_ [:-1]
    bstack1lll1l_opy_ = bstack1l1111l_opy_ % len (bstack1l1l111_opy_)
    bstack1l1l11l_opy_ = bstack1l1l111_opy_ [:bstack1lll1l_opy_] + bstack1l1l111_opy_ [bstack1lll1l_opy_:]
    if bstack1lllll1_opy_:
        bstack11111l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll1l_opy_ - (bstack11l1l_opy_ + bstack1l1111l_opy_) % bstack11l11_opy_) for bstack11l1l_opy_, char in enumerate (bstack1l1l11l_opy_)])
    else:
        bstack11111l_opy_ = str () .join ([chr (ord (char) - bstack1l1ll1l_opy_ - (bstack11l1l_opy_ + bstack1l1111l_opy_) % bstack11l11_opy_) for bstack11l1l_opy_, char in enumerate (bstack1l1l11l_opy_)])
    return eval (bstack11111l_opy_)
from collections import deque
from bstack_utils.constants import *
class bstack1l1l1l111l_opy_:
    def __init__(self):
        self._111111ll11_opy_ = deque()
        self._111111ll1l_opy_ = {}
        self._11111l11l1_opy_ = False
    def bstack1111111ll1_opy_(self, test_name, bstack1111111l1l_opy_):
        bstack111111llll_opy_ = self._111111ll1l_opy_.get(test_name, {})
        return bstack111111llll_opy_.get(bstack1111111l1l_opy_, 0)
    def bstack11111l111l_opy_(self, test_name, bstack1111111l1l_opy_):
        bstack11111l1111_opy_ = self.bstack1111111ll1_opy_(test_name, bstack1111111l1l_opy_)
        self.bstack111111l11l_opy_(test_name, bstack1111111l1l_opy_)
        return bstack11111l1111_opy_
    def bstack111111l11l_opy_(self, test_name, bstack1111111l1l_opy_):
        if test_name not in self._111111ll1l_opy_:
            self._111111ll1l_opy_[test_name] = {}
        bstack111111llll_opy_ = self._111111ll1l_opy_[test_name]
        bstack11111l1111_opy_ = bstack111111llll_opy_.get(bstack1111111l1l_opy_, 0)
        bstack111111llll_opy_[bstack1111111l1l_opy_] = bstack11111l1111_opy_ + 1
    def bstack111111l11_opy_(self, bstack1111111l11_opy_, bstack111111lll1_opy_):
        bstack111111l1l1_opy_ = self.bstack11111l111l_opy_(bstack1111111l11_opy_, bstack111111lll1_opy_)
        bstack111111l111_opy_ = bstack11l1l111ll_opy_[bstack111111lll1_opy_]
        bstack1111111lll_opy_ = bstack1l_opy_ (u"ࠤࡾࢁ࠲ࢁࡽ࠮ࡽࢀࠦᐛ").format(bstack1111111l11_opy_, bstack111111l111_opy_, bstack111111l1l1_opy_)
        self._111111ll11_opy_.append(bstack1111111lll_opy_)
    def bstack11ll11111_opy_(self):
        return len(self._111111ll11_opy_) == 0
    def bstack1111l1l11_opy_(self):
        bstack111111l1ll_opy_ = self._111111ll11_opy_.popleft()
        return bstack111111l1ll_opy_
    def capturing(self):
        return self._11111l11l1_opy_
    def bstack1111l1ll_opy_(self):
        self._11111l11l1_opy_ = True
    def bstack1ll11ll11_opy_(self):
        self._11111l11l1_opy_ = False