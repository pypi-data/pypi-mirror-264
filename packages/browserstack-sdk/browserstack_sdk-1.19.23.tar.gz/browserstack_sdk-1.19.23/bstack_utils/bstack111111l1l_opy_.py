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
from browserstack_sdk.bstack1lll1l111l_opy_ import bstack1lll1l1l11_opy_
from browserstack_sdk.bstack11lll1lll1_opy_ import RobotHandler
def bstack1l11ll1l11_opy_(framework):
    if framework.lower() == bstack1l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧᆀ"):
        return bstack1lll1l1l11_opy_.version()
    elif framework.lower() == bstack1l_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧᆁ"):
        return RobotHandler.version()
    elif framework.lower() == bstack1l_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩᆂ"):
        import behave
        return behave.__version__
    else:
        return bstack1l_opy_ (u"ࠪࡹࡳࡱ࡮ࡰࡹࡱࠫᆃ")