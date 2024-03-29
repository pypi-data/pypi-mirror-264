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
import multiprocessing
import os
import json
from time import sleep
import bstack_utils.bstack1ll1ll11l_opy_ as bstack11lllll1l_opy_
from browserstack_sdk.bstack1l1lllllll_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack1lllll11ll_opy_
class bstack1l1lll1lll_opy_:
    def __init__(self, args, logger, bstack11ll1lllll_opy_, bstack11lll11l1l_opy_):
        self.args = args
        self.logger = logger
        self.bstack11ll1lllll_opy_ = bstack11ll1lllll_opy_
        self.bstack11lll11l1l_opy_ = bstack11lll11l1l_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack1ll1ll111_opy_ = []
        self.bstack11lll1111l_opy_ = None
        self.bstack1ll1llll1_opy_ = []
        self.bstack11lll11l11_opy_ = self.bstack1l1l1l1l1l_opy_()
        self.bstack1l11ll1111_opy_ = -1
    def bstack1111lllll_opy_(self, bstack11lll111ll_opy_):
        self.parse_args()
        self.bstack11ll1llll1_opy_()
        self.bstack11lll11111_opy_(bstack11lll111ll_opy_)
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    @staticmethod
    def bstack11ll1ll11l_opy_():
        import importlib
        if getattr(importlib, bstack1llll1l_opy_ (u"ࠧࡧ࡫ࡱࡨࡤࡲ࡯ࡢࡦࡨࡶࠬฎ"), False):
            bstack11ll1l1ll1_opy_ = importlib.find_loader(bstack1llll1l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡵࡨࡰࡪࡴࡩࡶ࡯ࠪฏ"))
        else:
            bstack11ll1l1ll1_opy_ = importlib.util.find_spec(bstack1llll1l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡶࡩࡱ࡫࡮ࡪࡷࡰࠫฐ"))
    def bstack11ll1lll1l_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack1l11ll1111_opy_ = -1
        if bstack1llll1l_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪฑ") in self.bstack11ll1lllll_opy_:
            self.bstack1l11ll1111_opy_ = int(self.bstack11ll1lllll_opy_[bstack1llll1l_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫฒ")])
        try:
            bstack11ll1l1lll_opy_ = [bstack1llll1l_opy_ (u"ࠬ࠳࠭ࡥࡴ࡬ࡺࡪࡸࠧณ"), bstack1llll1l_opy_ (u"࠭࠭࠮ࡲ࡯ࡹ࡬࡯࡮ࡴࠩด"), bstack1llll1l_opy_ (u"ࠧ࠮ࡲࠪต")]
            if self.bstack1l11ll1111_opy_ >= 0:
                bstack11ll1l1lll_opy_.extend([bstack1llll1l_opy_ (u"ࠨ࠯࠰ࡲࡺࡳࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩถ"), bstack1llll1l_opy_ (u"ࠩ࠰ࡲࠬท")])
            for arg in bstack11ll1l1lll_opy_:
                self.bstack11ll1lll1l_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack11ll1llll1_opy_(self):
        bstack11lll1111l_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack11lll1111l_opy_ = bstack11lll1111l_opy_
        return bstack11lll1111l_opy_
    def bstack1lllll111l_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            self.bstack11ll1ll11l_opy_()
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warn(e, bstack1lllll11ll_opy_)
    def bstack11lll11111_opy_(self, bstack11lll111ll_opy_):
        bstack1l1lll1ll1_opy_ = Config.bstack11ll1ll1_opy_()
        if bstack11lll111ll_opy_:
            self.bstack11lll1111l_opy_.append(bstack1llll1l_opy_ (u"ࠪ࠱࠲ࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧธ"))
            self.bstack11lll1111l_opy_.append(bstack1llll1l_opy_ (u"࡙ࠫࡸࡵࡦࠩน"))
        if bstack1l1lll1ll1_opy_.bstack11ll1lll11_opy_():
            self.bstack11lll1111l_opy_.append(bstack1llll1l_opy_ (u"ࠬ࠳࠭ࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫบ"))
            self.bstack11lll1111l_opy_.append(bstack1llll1l_opy_ (u"࠭ࡔࡳࡷࡨࠫป"))
        self.bstack11lll1111l_opy_.append(bstack1llll1l_opy_ (u"ࠧ࠮ࡲࠪผ"))
        self.bstack11lll1111l_opy_.append(bstack1llll1l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡰ࡭ࡷࡪ࡭ࡳ࠭ฝ"))
        self.bstack11lll1111l_opy_.append(bstack1llll1l_opy_ (u"ࠩ࠰࠱ࡩࡸࡩࡷࡧࡵࠫพ"))
        self.bstack11lll1111l_opy_.append(bstack1llll1l_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪฟ"))
        if self.bstack1l11ll1111_opy_ > 1:
            self.bstack11lll1111l_opy_.append(bstack1llll1l_opy_ (u"ࠫ࠲ࡴࠧภ"))
            self.bstack11lll1111l_opy_.append(str(self.bstack1l11ll1111_opy_))
    def bstack11ll1ll111_opy_(self):
        bstack1ll1llll1_opy_ = []
        for spec in self.bstack1ll1ll111_opy_:
            bstack1111ll1ll_opy_ = [spec]
            bstack1111ll1ll_opy_ += self.bstack11lll1111l_opy_
            bstack1ll1llll1_opy_.append(bstack1111ll1ll_opy_)
        self.bstack1ll1llll1_opy_ = bstack1ll1llll1_opy_
        return bstack1ll1llll1_opy_
    def bstack1l1l1l1l1l_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack11lll11l11_opy_ = True
            return True
        except Exception as e:
            self.bstack11lll11l11_opy_ = False
        return self.bstack11lll11l11_opy_
    def bstack11ll1111_opy_(self, bstack11lll111l1_opy_, bstack1111lllll_opy_):
        bstack1111lllll_opy_[bstack1llll1l_opy_ (u"ࠬࡉࡏࡏࡈࡌࡋࠬม")] = self.bstack11ll1lllll_opy_
        multiprocessing.set_start_method(bstack1llll1l_opy_ (u"࠭ࡳࡱࡣࡺࡲࠬย"))
        if bstack1llll1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪร") in self.bstack11ll1lllll_opy_:
            bstack11ll1111l_opy_ = []
            manager = multiprocessing.Manager()
            bstack1ll11l1ll_opy_ = manager.list()
            for index, platform in enumerate(self.bstack11ll1lllll_opy_[bstack1llll1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫฤ")]):
                bstack11ll1111l_opy_.append(multiprocessing.Process(name=str(index),
                                                           target=bstack11lll111l1_opy_,
                                                           args=(self.bstack11lll1111l_opy_, bstack1111lllll_opy_, bstack1ll11l1ll_opy_)))
            i = 0
            bstack11ll1ll1l1_opy_ = len(self.bstack11ll1lllll_opy_[bstack1llll1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬล")])
            for t in bstack11ll1111l_opy_:
                os.environ[bstack1llll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪฦ")] = str(i)
                os.environ[bstack1llll1l_opy_ (u"ࠫࡈ࡛ࡒࡓࡇࡑࡘࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡅࡃࡗࡅࠬว")] = json.dumps(self.bstack11ll1lllll_opy_[bstack1llll1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨศ")][i % bstack11ll1ll1l1_opy_])
                i += 1
                t.start()
            for t in bstack11ll1111l_opy_:
                t.join()
            return list(bstack1ll11l1ll_opy_)
    @staticmethod
    def bstack11ll11111_opy_(driver, bstack11lll11l_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstack1llll1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪษ"), None)
        if item and getattr(item, bstack1llll1l_opy_ (u"ࠧࡠࡣ࠴࠵ࡾࡥࡴࡦࡵࡷࡣࡨࡧࡳࡦࠩส"), None) and not getattr(item, bstack1llll1l_opy_ (u"ࠨࡡࡤ࠵࠶ࡿ࡟ࡴࡶࡲࡴࡤࡪ࡯࡯ࡧࠪห"), False):
            logger.info(
                bstack1llll1l_opy_ (u"ࠤࡄࡹࡹࡵ࡭ࡢࡶࡨࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡦࡺࡨࡧࡺࡺࡩࡰࡰࠣ࡬ࡦࡹࠠࡦࡰࡧࡩࡩ࠴ࠠࡑࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤ࡫ࡵࡲࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡶࡨࡷࡹ࡯࡮ࡨࠢ࡬ࡷࠥࡻ࡮ࡥࡧࡵࡻࡦࡿ࠮ࠣฬ"))
            bstack11ll1ll1ll_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack11lllll1l_opy_.bstack1ll111ll_opy_(driver, bstack11ll1ll1ll_opy_, item.name, item.module.__name__, item.path, bstack11lll11l_opy_)
            item._a11y_stop_done = True
            if wait:
                sleep(2)