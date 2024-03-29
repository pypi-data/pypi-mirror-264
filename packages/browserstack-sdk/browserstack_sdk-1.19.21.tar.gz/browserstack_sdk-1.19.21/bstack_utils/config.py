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
conf = {
    bstack1llll1l_opy_ (u"ࠬࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ໬"): False,
    bstack1llll1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧ໭"): True,
    bstack1llll1l_opy_ (u"ࠧࡴ࡭࡬ࡴࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡳࡵࡣࡷࡹࡸ࠭໮"): False
}
class Config(object):
    instance = None
    def __init__(self):
        self._11l1l1l1l1_opy_ = conf
    @classmethod
    def bstack11ll1ll1_opy_(cls):
        if cls.instance:
            return cls.instance
        return Config()
    def get_property(self, property_name):
        return self._11l1l1l1l1_opy_.get(property_name, None)
    def bstack1llll111_opy_(self, property_name, bstack11l1l1l1ll_opy_):
        self._11l1l1l1l1_opy_[property_name] = bstack11l1l1l1ll_opy_
    def bstack1llll1lll1_opy_(self, val):
        self._11l1l1l1l1_opy_[bstack1llll1l_opy_ (u"ࠨࡵ࡮࡭ࡵࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡴࡶࡤࡸࡺࡹࠧ໯")] = bool(val)
    def bstack11ll1lll11_opy_(self):
        return self._11l1l1l1l1_opy_.get(bstack1llll1l_opy_ (u"ࠩࡶ࡯࡮ࡶ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡵࡷࡥࡹࡻࡳࠨ໰"), False)