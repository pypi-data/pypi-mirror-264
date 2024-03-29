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
import sys
class bstack11llll11ll_opy_:
    def __init__(self, handler):
        self._11l1l1llll_opy_ = sys.stdout.write
        self._11l1l1ll11_opy_ = sys.stderr.write
        self.handler = handler
        self._started = False
    def start(self):
        if self._started:
            return
        self._started = True
        sys.stdout.write = self.bstack11l1l1lll1_opy_
        sys.stdout.error = self.bstack11l1l1ll1l_opy_
    def bstack11l1l1lll1_opy_(self, _str):
        self._11l1l1llll_opy_(_str)
        if self.handler:
            self.handler({bstack1l_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ໦"): bstack1l_opy_ (u"ࠧࡊࡐࡉࡓࠬ໧"), bstack1l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ໨"): _str})
    def bstack11l1l1ll1l_opy_(self, _str):
        self._11l1l1ll11_opy_(_str)
        if self.handler:
            self.handler({bstack1l_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ໩"): bstack1l_opy_ (u"ࠪࡉࡗࡘࡏࡓࠩ໪"), bstack1l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ໫"): _str})
    def reset(self):
        if not self._started:
            return
        self._started = False
        sys.stdout.write = self._11l1l1llll_opy_
        sys.stderr.write = self._11l1l1ll11_opy_