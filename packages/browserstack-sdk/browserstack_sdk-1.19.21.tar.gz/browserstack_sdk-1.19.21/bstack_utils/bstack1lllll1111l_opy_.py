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
import threading
bstack1lllll1l1l1_opy_ = 1000
bstack1lllll11111_opy_ = 5
bstack1llll1lllll_opy_ = 30
bstack1lllll11l1l_opy_ = 2
class bstack1lllll111l1_opy_:
    def __init__(self, handler, bstack1lllll11lll_opy_=bstack1lllll1l1l1_opy_, bstack1lllll1l111_opy_=bstack1lllll11111_opy_):
        self.queue = []
        self.handler = handler
        self.bstack1lllll11lll_opy_ = bstack1lllll11lll_opy_
        self.bstack1lllll1l111_opy_ = bstack1lllll1l111_opy_
        self.lock = threading.Lock()
        self.timer = None
    def start(self):
        if not self.timer:
            self.bstack1lllll111ll_opy_()
    def bstack1lllll111ll_opy_(self):
        self.timer = threading.Timer(self.bstack1lllll1l111_opy_, self.bstack1lllll11ll1_opy_)
        self.timer.start()
    def bstack1lllll1l11l_opy_(self):
        self.timer.cancel()
    def bstack1lllll11l11_opy_(self):
        self.bstack1lllll1l11l_opy_()
        self.bstack1lllll111ll_opy_()
    def add(self, event):
        with self.lock:
            self.queue.append(event)
            if len(self.queue) >= self.bstack1lllll11lll_opy_:
                t = threading.Thread(target=self.bstack1lllll11ll1_opy_)
                t.start()
                self.bstack1lllll11l11_opy_()
    def bstack1lllll11ll1_opy_(self):
        if len(self.queue) <= 0:
            return
        data = self.queue[:self.bstack1lllll11lll_opy_]
        del self.queue[:self.bstack1lllll11lll_opy_]
        self.handler(data)
    def shutdown(self):
        self.bstack1lllll1l11l_opy_()
        while len(self.queue) > 0:
            self.bstack1lllll11ll1_opy_()