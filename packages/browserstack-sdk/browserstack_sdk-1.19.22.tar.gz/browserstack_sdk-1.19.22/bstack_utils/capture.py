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
import sys
class bstack11lll1lll1_opy_:
    def __init__(self, handler):
        self._11l1l1ll11_opy_ = sys.stdout.write
        self._11l1l1ll1l_opy_ = sys.stderr.write
        self.handler = handler
        self._started = False
    def start(self):
        if self._started:
            return
        self._started = True
        sys.stdout.write = self.bstack11l1l1lll1_opy_
        sys.stdout.error = self.bstack11l1l1llll_opy_
    def bstack11l1l1lll1_opy_(self, _str):
        self._11l1l1ll11_opy_(_str)
        if self.handler:
            self.handler({bstack1ll11l_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ໦"): bstack1ll11l_opy_ (u"ࠧࡊࡐࡉࡓࠬ໧"), bstack1ll11l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ໨"): _str})
    def bstack11l1l1llll_opy_(self, _str):
        self._11l1l1ll1l_opy_(_str)
        if self.handler:
            self.handler({bstack1ll11l_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ໩"): bstack1ll11l_opy_ (u"ࠪࡉࡗࡘࡏࡓࠩ໪"), bstack1ll11l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ໫"): _str})
    def reset(self):
        if not self._started:
            return
        self._started = False
        sys.stdout.write = self._11l1l1ll11_opy_
        sys.stderr.write = self._11l1l1ll1l_opy_