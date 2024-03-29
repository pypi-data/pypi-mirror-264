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
conf = {
    bstack1l_opy_ (u"ࠬࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ໬"): False,
    bstack1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧ໭"): True,
    bstack1l_opy_ (u"ࠧࡴ࡭࡬ࡴࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡳࡵࡣࡷࡹࡸ࠭໮"): False
}
class Config(object):
    instance = None
    def __init__(self):
        self._11l1l1l1ll_opy_ = conf
    @classmethod
    def bstack1l1l1lll1l_opy_(cls):
        if cls.instance:
            return cls.instance
        return Config()
    def get_property(self, property_name):
        return self._11l1l1l1ll_opy_.get(property_name, None)
    def bstack11llll11l_opy_(self, property_name, bstack11l1l1l1l1_opy_):
        self._11l1l1l1ll_opy_[property_name] = bstack11l1l1l1l1_opy_
    def bstack111ll1l1_opy_(self, val):
        self._11l1l1l1ll_opy_[bstack1l_opy_ (u"ࠨࡵ࡮࡭ࡵࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡴࡶࡤࡸࡺࡹࠧ໯")] = bool(val)
    def bstack11ll1ll11l_opy_(self):
        return self._11l1l1l1ll_opy_.get(bstack1l_opy_ (u"ࠩࡶ࡯࡮ࡶ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡵࡷࡥࡹࡻࡳࠨ໰"), False)