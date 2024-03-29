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
class bstack1l111l1l_opy_:
    def __init__(self, handler):
        self._1lllll11111_opy_ = None
        self.handler = handler
        self._1llll1lllll_opy_ = self.bstack1lllll1111l_opy_()
        self.patch()
    def patch(self):
        self._1lllll11111_opy_ = self._1llll1lllll_opy_.execute
        self._1llll1lllll_opy_.execute = self.bstack1lllll111l1_opy_()
    def bstack1lllll111l1_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack1l_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫ࠢᑴ"), driver_command, None, this, args)
            response = self._1lllll11111_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack1l_opy_ (u"ࠣࡣࡩࡸࡪࡸࠢᑵ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1llll1lllll_opy_.execute = self._1lllll11111_opy_
    @staticmethod
    def bstack1lllll1111l_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver