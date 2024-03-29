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
from browserstack_sdk.bstack11l11l1ll_opy_ import bstack1l1lll1lll_opy_
from browserstack_sdk.bstack1l111l11ll_opy_ import RobotHandler
def bstack1ll1111l11_opy_(framework):
    if framework.lower() == bstack1llll1l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧᆀ"):
        return bstack1l1lll1lll_opy_.version()
    elif framework.lower() == bstack1llll1l_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧᆁ"):
        return RobotHandler.version()
    elif framework.lower() == bstack1llll1l_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩᆂ"):
        import behave
        return behave.__version__
    else:
        return bstack1llll1l_opy_ (u"ࠪࡹࡳࡱ࡮ࡰࡹࡱࠫᆃ")