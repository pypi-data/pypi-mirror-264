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
class bstack111111l1_opy_:
    def __init__(self, handler):
        self._1lllll11111_opy_ = None
        self.handler = handler
        self._1lllll111l1_opy_ = self.bstack1llll1lllll_opy_()
        self.patch()
    def patch(self):
        self._1lllll11111_opy_ = self._1lllll111l1_opy_.execute
        self._1lllll111l1_opy_.execute = self.bstack1lllll1111l_opy_()
    def bstack1lllll1111l_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack1ll11l_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫ࠢᑴ"), driver_command, None, this, args)
            response = self._1lllll11111_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack1ll11l_opy_ (u"ࠣࡣࡩࡸࡪࡸࠢᑵ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1lllll111l1_opy_.execute = self._1lllll11111_opy_
    @staticmethod
    def bstack1llll1lllll_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver