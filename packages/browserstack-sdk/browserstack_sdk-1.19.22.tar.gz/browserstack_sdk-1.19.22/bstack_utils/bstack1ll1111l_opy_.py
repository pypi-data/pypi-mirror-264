# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack11_opy_ = 2048
bstack1lll1ll_opy_ = 7
def bstack1ll11l_opy_ (bstack111lll_opy_):
    global bstack1l11l1l_opy_
    bstack1111l_opy_ = ord (bstack111lll_opy_ [-1])
    bstack11lll11_opy_ = bstack111lll_opy_ [:-1]
    bstack11lll_opy_ = bstack1111l_opy_ % len (bstack11lll11_opy_)
    bstack111l1l1_opy_ = bstack11lll11_opy_ [:bstack11lll_opy_] + bstack11lll11_opy_ [bstack11lll_opy_:]
    if bstack111ll1_opy_:
        bstack1llllll1_opy_ = unicode () .join ([unichr (ord (char) - bstack11_opy_ - (bstack1l1l11l_opy_ + bstack1111l_opy_) % bstack1lll1ll_opy_) for bstack1l1l11l_opy_, char in enumerate (bstack111l1l1_opy_)])
    else:
        bstack1llllll1_opy_ = str () .join ([chr (ord (char) - bstack11_opy_ - (bstack1l1l11l_opy_ + bstack1111l_opy_) % bstack1lll1ll_opy_) for bstack1l1l11l_opy_, char in enumerate (bstack111l1l1_opy_)])
    return eval (bstack1llllll1_opy_)
from collections import deque
from bstack_utils.constants import *
class bstack111l1lll1_opy_:
    def __init__(self):
        self._1111111ll1_opy_ = deque()
        self._1111111l1l_opy_ = {}
        self._111111ll1l_opy_ = False
    def bstack111111ll11_opy_(self, test_name, bstack111111l11l_opy_):
        bstack111111l1l1_opy_ = self._1111111l1l_opy_.get(test_name, {})
        return bstack111111l1l1_opy_.get(bstack111111l11l_opy_, 0)
    def bstack111111l1ll_opy_(self, test_name, bstack111111l11l_opy_):
        bstack111111l111_opy_ = self.bstack111111ll11_opy_(test_name, bstack111111l11l_opy_)
        self.bstack111111llll_opy_(test_name, bstack111111l11l_opy_)
        return bstack111111l111_opy_
    def bstack111111llll_opy_(self, test_name, bstack111111l11l_opy_):
        if test_name not in self._1111111l1l_opy_:
            self._1111111l1l_opy_[test_name] = {}
        bstack111111l1l1_opy_ = self._1111111l1l_opy_[test_name]
        bstack111111l111_opy_ = bstack111111l1l1_opy_.get(bstack111111l11l_opy_, 0)
        bstack111111l1l1_opy_[bstack111111l11l_opy_] = bstack111111l111_opy_ + 1
    def bstack1ll1ll1l11_opy_(self, bstack1111111l11_opy_, bstack11111l11l1_opy_):
        bstack11111l111l_opy_ = self.bstack111111l1ll_opy_(bstack1111111l11_opy_, bstack11111l11l1_opy_)
        bstack111111lll1_opy_ = bstack11l1l1111l_opy_[bstack11111l11l1_opy_]
        bstack1111111lll_opy_ = bstack1ll11l_opy_ (u"ࠤࡾࢁ࠲ࢁࡽ࠮ࡽࢀࠦᐛ").format(bstack1111111l11_opy_, bstack111111lll1_opy_, bstack11111l111l_opy_)
        self._1111111ll1_opy_.append(bstack1111111lll_opy_)
    def bstack1lll1lll_opy_(self):
        return len(self._1111111ll1_opy_) == 0
    def bstack1ll11l11ll_opy_(self):
        bstack11111l1111_opy_ = self._1111111ll1_opy_.popleft()
        return bstack11111l1111_opy_
    def capturing(self):
        return self._111111ll1l_opy_
    def bstack11l1l1ll_opy_(self):
        self._111111ll1l_opy_ = True
    def bstack1ll11lll1_opy_(self):
        self._111111ll1l_opy_ = False