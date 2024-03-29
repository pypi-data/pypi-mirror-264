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
from browserstack_sdk.bstack111ll11l_opy_ import bstack1l1l1l1l11_opy_
from browserstack_sdk.bstack1l11111ll1_opy_ import RobotHandler
def bstack11lll1ll1_opy_(framework):
    if framework.lower() == bstack1ll11l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧᆀ"):
        return bstack1l1l1l1l11_opy_.version()
    elif framework.lower() == bstack1ll11l_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧᆁ"):
        return RobotHandler.version()
    elif framework.lower() == bstack1ll11l_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩᆂ"):
        import behave
        return behave.__version__
    else:
        return bstack1ll11l_opy_ (u"ࠪࡹࡳࡱ࡮ࡰࡹࡱࠫᆃ")