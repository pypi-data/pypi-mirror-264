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
import os
class RobotHandler():
    def __init__(self, args, logger, bstack11ll1l1ll1_opy_, bstack11ll1l1lll_opy_):
        self.args = args
        self.logger = logger
        self.bstack11ll1l1ll1_opy_ = bstack11ll1l1ll1_opy_
        self.bstack11ll1l1lll_opy_ = bstack11ll1l1lll_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack1l111l11l1_opy_(bstack11ll1l11ll_opy_):
        bstack11ll1l1l1l_opy_ = []
        if bstack11ll1l11ll_opy_:
            tokens = str(os.path.basename(bstack11ll1l11ll_opy_)).split(bstack1ll11l_opy_ (u"ࠥࡣࠧอ"))
            camelcase_name = bstack1ll11l_opy_ (u"ࠦࠥࠨฮ").join(t.title() for t in tokens)
            suite_name, bstack11ll1l11l1_opy_ = os.path.splitext(camelcase_name)
            bstack11ll1l1l1l_opy_.append(suite_name)
        return bstack11ll1l1l1l_opy_
    @staticmethod
    def bstack11ll1l1l11_opy_(typename):
        if bstack1ll11l_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࠣฯ") in typename:
            return bstack1ll11l_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢะ")
        return bstack1ll11l_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣั")