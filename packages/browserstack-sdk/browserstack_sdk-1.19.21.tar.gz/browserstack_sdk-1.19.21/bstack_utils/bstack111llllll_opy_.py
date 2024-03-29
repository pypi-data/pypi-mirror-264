# coding: UTF-8
import sys
bstack1ll1_opy_ = sys.version_info [0] == 2
bstack1111l11_opy_ = 2048
bstack111lll_opy_ = 7
def bstack1llll1l_opy_ (bstack1l1lll_opy_):
    global bstack1l1l1ll_opy_
    bstack1l1ll11_opy_ = ord (bstack1l1lll_opy_ [-1])
    bstack11ll1ll_opy_ = bstack1l1lll_opy_ [:-1]
    bstack1l1llll_opy_ = bstack1l1ll11_opy_ % len (bstack11ll1ll_opy_)
    bstack1l1l111_opy_ = bstack11ll1ll_opy_ [:bstack1l1llll_opy_] + bstack11ll1ll_opy_ [bstack1l1llll_opy_:]
    if bstack1ll1_opy_:
        bstack11ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l11_opy_ - (bstack1lll1_opy_ + bstack1l1ll11_opy_) % bstack111lll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l1l111_opy_)])
    else:
        bstack11ll1_opy_ = str () .join ([chr (ord (char) - bstack1111l11_opy_ - (bstack1lll1_opy_ + bstack1l1ll11_opy_) % bstack111lll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l1l111_opy_)])
    return eval (bstack11ll1_opy_)
from collections import deque
from bstack_utils.constants import *
class bstack1l111l1l_opy_:
    def __init__(self):
        self._111111ll1l_opy_ = deque()
        self._11111111l1_opy_ = {}
        self._111111l111_opy_ = False
    def bstack11111111ll_opy_(self, test_name, bstack111111lll1_opy_):
        bstack1111111l11_opy_ = self._11111111l1_opy_.get(test_name, {})
        return bstack1111111l11_opy_.get(bstack111111lll1_opy_, 0)
    def bstack1111111l1l_opy_(self, test_name, bstack111111lll1_opy_):
        bstack111111l1l1_opy_ = self.bstack11111111ll_opy_(test_name, bstack111111lll1_opy_)
        self.bstack111111ll11_opy_(test_name, bstack111111lll1_opy_)
        return bstack111111l1l1_opy_
    def bstack111111ll11_opy_(self, test_name, bstack111111lll1_opy_):
        if test_name not in self._11111111l1_opy_:
            self._11111111l1_opy_[test_name] = {}
        bstack1111111l11_opy_ = self._11111111l1_opy_[test_name]
        bstack111111l1l1_opy_ = bstack1111111l11_opy_.get(bstack111111lll1_opy_, 0)
        bstack1111111l11_opy_[bstack111111lll1_opy_] = bstack111111l1l1_opy_ + 1
    def bstack1l1111ll1_opy_(self, bstack1111111111_opy_, bstack1111111ll1_opy_):
        bstack111111l11l_opy_ = self.bstack1111111l1l_opy_(bstack1111111111_opy_, bstack1111111ll1_opy_)
        bstack111111111l_opy_ = bstack11l1l11lll_opy_[bstack1111111ll1_opy_]
        bstack111111l1ll_opy_ = bstack1llll1l_opy_ (u"ࠤࡾࢁ࠲ࢁࡽ࠮ࡽࢀࠦᐛ").format(bstack1111111111_opy_, bstack111111111l_opy_, bstack111111l11l_opy_)
        self._111111ll1l_opy_.append(bstack111111l1ll_opy_)
    def bstack1l111lll_opy_(self):
        return len(self._111111ll1l_opy_) == 0
    def bstack1ll11l1l11_opy_(self):
        bstack1111111lll_opy_ = self._111111ll1l_opy_.popleft()
        return bstack1111111lll_opy_
    def capturing(self):
        return self._111111l111_opy_
    def bstack1ll1l1llll_opy_(self):
        self._111111l111_opy_ = True
    def bstack1llll1l1l_opy_(self):
        self._111111l111_opy_ = False