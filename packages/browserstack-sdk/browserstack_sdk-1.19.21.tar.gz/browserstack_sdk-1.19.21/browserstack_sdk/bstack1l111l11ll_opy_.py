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
import os
class RobotHandler():
    def __init__(self, args, logger, bstack11ll1lllll_opy_, bstack11lll11l1l_opy_):
        self.args = args
        self.logger = logger
        self.bstack11ll1lllll_opy_ = bstack11ll1lllll_opy_
        self.bstack11lll11l1l_opy_ = bstack11lll11l1l_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack1l111111ll_opy_(bstack11ll1l11ll_opy_):
        bstack11ll1l1l11_opy_ = []
        if bstack11ll1l11ll_opy_:
            tokens = str(os.path.basename(bstack11ll1l11ll_opy_)).split(bstack1llll1l_opy_ (u"ࠥࡣࠧอ"))
            camelcase_name = bstack1llll1l_opy_ (u"ࠦࠥࠨฮ").join(t.title() for t in tokens)
            suite_name, bstack11ll1l1l1l_opy_ = os.path.splitext(camelcase_name)
            bstack11ll1l1l11_opy_.append(suite_name)
        return bstack11ll1l1l11_opy_
    @staticmethod
    def bstack11ll1l11l1_opy_(typename):
        if bstack1llll1l_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࠣฯ") in typename:
            return bstack1llll1l_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢะ")
        return bstack1llll1l_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣั")