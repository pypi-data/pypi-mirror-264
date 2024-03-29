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
class bstack11l11111l_opy_:
    def __init__(self, handler):
        self._1llll1lll11_opy_ = None
        self.handler = handler
        self._1llll1llll1_opy_ = self.bstack1llll1ll1ll_opy_()
        self.patch()
    def patch(self):
        self._1llll1lll11_opy_ = self._1llll1llll1_opy_.execute
        self._1llll1llll1_opy_.execute = self.bstack1llll1lll1l_opy_()
    def bstack1llll1lll1l_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack1llll1l_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫ࠢᑴ"), driver_command, None, this, args)
            response = self._1llll1lll11_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack1llll1l_opy_ (u"ࠣࡣࡩࡸࡪࡸࠢᑵ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1llll1llll1_opy_.execute = self._1llll1lll11_opy_
    @staticmethod
    def bstack1llll1ll1ll_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver