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
import os
import datetime
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack11lll1lll1_opy_ import RobotHandler
from bstack_utils.capture import bstack11llll11ll_opy_
from bstack_utils.bstack1l111l1l1l_opy_ import bstack1l111ll11l_opy_, bstack1l11111l11_opy_, bstack11llll1111_opy_
from bstack_utils.bstack1l11l1ll1_opy_ import bstack1llll1111l_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack11lll11ll_opy_, bstack1l11lll111_opy_, Result, \
    bstack11llll1l11_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    store = {
        bstack1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪൂ"): [],
        bstack1l_opy_ (u"ࠧࡨ࡮ࡲࡦࡦࡲ࡟ࡩࡱࡲ࡯ࡸ࠭ൃ"): [],
        bstack1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡷࠬൄ"): []
    }
    bstack1l111111l1_opy_ = []
    bstack1l1111l11l_opy_ = []
    @staticmethod
    def bstack1l1111l1ll_opy_(log):
        if not (log[bstack1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ൅")] and log[bstack1l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫെ")].strip()):
            return
        active = bstack1llll1111l_opy_.bstack1l1111l111_opy_()
        log = {
            bstack1l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪേ"): log[bstack1l_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫൈ")],
            bstack1l_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩ൉"): datetime.datetime.utcnow().isoformat() + bstack1l_opy_ (u"࡛ࠧࠩൊ"),
            bstack1l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩോ"): log[bstack1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪൌ")],
        }
        if active:
            if active[bstack1l_opy_ (u"ࠪࡸࡾࡶࡥࠨ്")] == bstack1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩൎ"):
                log[bstack1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ൏")] = active[bstack1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭൐")]
            elif active[bstack1l_opy_ (u"ࠧࡵࡻࡳࡩࠬ൑")] == bstack1l_opy_ (u"ࠨࡶࡨࡷࡹ࠭൒"):
                log[bstack1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ൓")] = active[bstack1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪൔ")]
        bstack1llll1111l_opy_.bstack1ll1l1lll_opy_([log])
    def __init__(self):
        self.messages = Messages()
        self._1l111llll1_opy_ = None
        self._1l1111llll_opy_ = None
        self._1l111l111l_opy_ = OrderedDict()
        self.bstack1l11l111ll_opy_ = bstack11llll11ll_opy_(self.bstack1l1111l1ll_opy_)
    @bstack11llll1l11_opy_(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack11lll1l11l_opy_()
        if not self._1l111l111l_opy_.get(attrs.get(bstack1l_opy_ (u"ࠫ࡮ࡪࠧൕ")), None):
            self._1l111l111l_opy_[attrs.get(bstack1l_opy_ (u"ࠬ࡯ࡤࠨൖ"))] = {}
        bstack11lllll1l1_opy_ = bstack11llll1111_opy_(
                bstack11llllll11_opy_=attrs.get(bstack1l_opy_ (u"࠭ࡩࡥࠩൗ")),
                name=name,
                bstack11lllll111_opy_=bstack1l11lll111_opy_(),
                file_path=os.path.relpath(attrs[bstack1l_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧ൘")], start=os.getcwd()) if attrs.get(bstack1l_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨ൙")) != bstack1l_opy_ (u"ࠩࠪ൚") else bstack1l_opy_ (u"ࠪࠫ൛"),
                framework=bstack1l_opy_ (u"ࠫࡗࡵࡢࡰࡶࠪ൜")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack1l_opy_ (u"ࠬ࡯ࡤࠨ൝"), None)
        self._1l111l111l_opy_[attrs.get(bstack1l_opy_ (u"࠭ࡩࡥࠩ൞"))][bstack1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪൟ")] = bstack11lllll1l1_opy_
    @bstack11llll1l11_opy_(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack11lllllll1_opy_()
        self._1l11l11l11_opy_(messages)
        for bstack1l1111111l_opy_ in self.bstack1l111111l1_opy_:
            bstack1l1111111l_opy_[bstack1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪൠ")][bstack1l_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨൡ")].extend(self.store[bstack1l_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮ࡢ࡬ࡴࡵ࡫ࡴࠩൢ")])
            bstack1llll1111l_opy_.bstack1l111lll11_opy_(bstack1l1111111l_opy_)
        self.bstack1l111111l1_opy_ = []
        self.store[bstack1l_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯ࡣ࡭ࡵ࡯࡬ࡵࠪൣ")] = []
    @bstack11llll1l11_opy_(class_method=True)
    def start_test(self, name, attrs):
        self.bstack1l11l111ll_opy_.start()
        if not self._1l111l111l_opy_.get(attrs.get(bstack1l_opy_ (u"ࠬ࡯ࡤࠨ൤")), None):
            self._1l111l111l_opy_[attrs.get(bstack1l_opy_ (u"࠭ࡩࡥࠩ൥"))] = {}
        driver = bstack11lll11ll_opy_(threading.current_thread(), bstack1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭൦"), None)
        bstack1l111l1l1l_opy_ = bstack11llll1111_opy_(
            bstack11llllll11_opy_=attrs.get(bstack1l_opy_ (u"ࠨ࡫ࡧࠫ൧")),
            name=name,
            bstack11lllll111_opy_=bstack1l11lll111_opy_(),
            file_path=os.path.relpath(attrs[bstack1l_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩ൨")], start=os.getcwd()),
            scope=RobotHandler.bstack1l1111ll1l_opy_(attrs.get(bstack1l_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪ൩"), None)),
            framework=bstack1l_opy_ (u"ࠫࡗࡵࡢࡰࡶࠪ൪"),
            tags=attrs[bstack1l_opy_ (u"ࠬࡺࡡࡨࡵࠪ൫")],
            hooks=self.store[bstack1l_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡥࡨࡰࡱ࡮ࡷࠬ൬")],
            bstack1l111lll1l_opy_=bstack1llll1111l_opy_.bstack1l111l1111_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack1l_opy_ (u"ࠢࡼࡿࠣࡠࡳࠦࡻࡾࠤ൭").format(bstack1l_opy_ (u"ࠣࠢࠥ൮").join(attrs[bstack1l_opy_ (u"ࠩࡷࡥ࡬ࡹࠧ൯")]), name) if attrs[bstack1l_opy_ (u"ࠪࡸࡦ࡭ࡳࠨ൰")] else name
        )
        self._1l111l111l_opy_[attrs.get(bstack1l_opy_ (u"ࠫ࡮ࡪࠧ൱"))][bstack1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ൲")] = bstack1l111l1l1l_opy_
        threading.current_thread().current_test_uuid = bstack1l111l1l1l_opy_.bstack1l111l1lll_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack1l_opy_ (u"࠭ࡩࡥࠩ൳"), None)
        self.bstack1l111ll1ll_opy_(bstack1l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ൴"), bstack1l111l1l1l_opy_)
    @bstack11llll1l11_opy_(class_method=True)
    def end_test(self, name, attrs):
        self.bstack1l11l111ll_opy_.reset()
        bstack11lll11lll_opy_ = bstack11lll1ll11_opy_.get(attrs.get(bstack1l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ൵")), bstack1l_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ൶"))
        self._1l111l111l_opy_[attrs.get(bstack1l_opy_ (u"ࠪ࡭ࡩ࠭൷"))][bstack1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ൸")].stop(time=bstack1l11lll111_opy_(), duration=int(attrs.get(bstack1l_opy_ (u"ࠬ࡫࡬ࡢࡲࡶࡩࡩࡺࡩ࡮ࡧࠪ൹"), bstack1l_opy_ (u"࠭࠰ࠨൺ"))), result=Result(result=bstack11lll11lll_opy_, exception=attrs.get(bstack1l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨൻ")), bstack1l1111lll1_opy_=[attrs.get(bstack1l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩർ"))]))
        self.bstack1l111ll1ll_opy_(bstack1l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫൽ"), self._1l111l111l_opy_[attrs.get(bstack1l_opy_ (u"ࠪ࡭ࡩ࠭ൾ"))][bstack1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧൿ")], True)
        self.store[bstack1l_opy_ (u"ࠬࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࠩ඀")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @bstack11llll1l11_opy_(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack11lll1l11l_opy_()
        current_test_id = bstack11lll11ll_opy_(threading.current_thread(), bstack1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡤࠨඁ"), None)
        bstack1l11111lll_opy_ = current_test_id if bstack11lll11ll_opy_(threading.current_thread(), bstack1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡥࠩං"), None) else bstack11lll11ll_opy_(threading.current_thread(), bstack1l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡶࡹ࡮ࡺࡥࡠ࡫ࡧࠫඃ"), None)
        if attrs.get(bstack1l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ඄"), bstack1l_opy_ (u"ࠪࠫඅ")).lower() in [bstack1l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪආ"), bstack1l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧඇ")]:
            hook_type = bstack1l111lllll_opy_(attrs.get(bstack1l_opy_ (u"࠭ࡴࡺࡲࡨࠫඈ")), bstack11lll11ll_opy_(threading.current_thread(), bstack1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫඉ"), None))
            hook_name = bstack1l_opy_ (u"ࠨࡽࢀࠫඊ").format(attrs.get(bstack1l_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦࠩඋ"), bstack1l_opy_ (u"ࠪࠫඌ")))
            if hook_type in [bstack1l_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡆࡒࡌࠨඍ"), bstack1l_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡆࡒࡌࠨඎ")]:
                hook_name = bstack1l_opy_ (u"࡛࠭ࡼࡿࡠࠤࢀࢃࠧඏ").format(bstack11llllll1l_opy_.get(hook_type), attrs.get(bstack1l_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫ࠧඐ"), bstack1l_opy_ (u"ࠨࠩඑ")))
            bstack1l111l11l1_opy_ = bstack1l11111l11_opy_(
                bstack11llllll11_opy_=bstack1l11111lll_opy_ + bstack1l_opy_ (u"ࠩ࠰ࠫඒ") + attrs.get(bstack1l_opy_ (u"ࠪࡸࡾࡶࡥࠨඓ"), bstack1l_opy_ (u"ࠫࠬඔ")).lower(),
                name=hook_name,
                bstack11lllll111_opy_=bstack1l11lll111_opy_(),
                file_path=os.path.relpath(attrs.get(bstack1l_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬඕ")), start=os.getcwd()),
                framework=bstack1l_opy_ (u"࠭ࡒࡰࡤࡲࡸࠬඖ"),
                tags=attrs[bstack1l_opy_ (u"ࠧࡵࡣࡪࡷࠬ඗")],
                scope=RobotHandler.bstack1l1111ll1l_opy_(attrs.get(bstack1l_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨ඘"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack1l111l11l1_opy_.bstack1l111l1lll_opy_()
            threading.current_thread().current_hook_id = bstack1l11111lll_opy_ + bstack1l_opy_ (u"ࠩ࠰ࠫ඙") + attrs.get(bstack1l_opy_ (u"ࠪࡸࡾࡶࡥࠨක"), bstack1l_opy_ (u"ࠫࠬඛ")).lower()
            self.store[bstack1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩග")] = [bstack1l111l11l1_opy_.bstack1l111l1lll_opy_()]
            if bstack11lll11ll_opy_(threading.current_thread(), bstack1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪඝ"), None):
                self.store[bstack1l_opy_ (u"ࠧࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࠫඞ")].append(bstack1l111l11l1_opy_.bstack1l111l1lll_opy_())
            else:
                self.store[bstack1l_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬ࡠࡪࡲࡳࡰࡹࠧඟ")].append(bstack1l111l11l1_opy_.bstack1l111l1lll_opy_())
            if bstack1l11111lll_opy_:
                self._1l111l111l_opy_[bstack1l11111lll_opy_ + bstack1l_opy_ (u"ࠩ࠰ࠫච") + attrs.get(bstack1l_opy_ (u"ࠪࡸࡾࡶࡥࠨඡ"), bstack1l_opy_ (u"ࠫࠬජ")).lower()] = { bstack1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨඣ"): bstack1l111l11l1_opy_ }
            bstack1llll1111l_opy_.bstack1l111ll1ll_opy_(bstack1l_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧඤ"), bstack1l111l11l1_opy_)
        else:
            bstack11llll1ll1_opy_ = {
                bstack1l_opy_ (u"ࠧࡪࡦࠪඥ"): uuid4().__str__(),
                bstack1l_opy_ (u"ࠨࡶࡨࡼࡹ࠭ඦ"): bstack1l_opy_ (u"ࠩࡾࢁࠥࢁࡽࠨට").format(attrs.get(bstack1l_opy_ (u"ࠪ࡯ࡼࡴࡡ࡮ࡧࠪඨ")), attrs.get(bstack1l_opy_ (u"ࠫࡦࡸࡧࡴࠩඩ"), bstack1l_opy_ (u"ࠬ࠭ඪ"))) if attrs.get(bstack1l_opy_ (u"࠭ࡡࡳࡩࡶࠫණ"), []) else attrs.get(bstack1l_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫ࠧඬ")),
                bstack1l_opy_ (u"ࠨࡵࡷࡩࡵࡥࡡࡳࡩࡸࡱࡪࡴࡴࠨත"): attrs.get(bstack1l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧථ"), []),
                bstack1l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧද"): bstack1l11lll111_opy_(),
                bstack1l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫධ"): bstack1l_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭න"),
                bstack1l_opy_ (u"࠭ࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫ඲"): attrs.get(bstack1l_opy_ (u"ࠧࡥࡱࡦࠫඳ"), bstack1l_opy_ (u"ࠨࠩප"))
            }
            if attrs.get(bstack1l_opy_ (u"ࠩ࡯࡭ࡧࡴࡡ࡮ࡧࠪඵ"), bstack1l_opy_ (u"ࠪࠫබ")) != bstack1l_opy_ (u"ࠫࠬභ"):
                bstack11llll1ll1_opy_[bstack1l_opy_ (u"ࠬࡱࡥࡺࡹࡲࡶࡩ࠭ම")] = attrs.get(bstack1l_opy_ (u"࠭࡬ࡪࡤࡱࡥࡲ࡫ࠧඹ"))
            if not self.bstack1l1111l11l_opy_:
                self._1l111l111l_opy_[self._11lllll11l_opy_()][bstack1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪය")].add_step(bstack11llll1ll1_opy_)
                threading.current_thread().current_step_uuid = bstack11llll1ll1_opy_[bstack1l_opy_ (u"ࠨ࡫ࡧࠫර")]
            self.bstack1l1111l11l_opy_.append(bstack11llll1ll1_opy_)
    @bstack11llll1l11_opy_(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack11lllllll1_opy_()
        self._1l11l11l11_opy_(messages)
        current_test_id = bstack11lll11ll_opy_(threading.current_thread(), bstack1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡧࠫ඼"), None)
        bstack1l11111lll_opy_ = current_test_id if current_test_id else bstack11lll11ll_opy_(threading.current_thread(), bstack1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡸࡻࡩࡵࡧࡢ࡭ࡩ࠭ල"), None)
        bstack1l111ll1l1_opy_ = bstack11lll1ll11_opy_.get(attrs.get(bstack1l_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ඾")), bstack1l_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭඿"))
        bstack1l1111l1l1_opy_ = attrs.get(bstack1l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧව"))
        if bstack1l111ll1l1_opy_ != bstack1l_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨශ") and not attrs.get(bstack1l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩෂ")) and self._1l111llll1_opy_:
            bstack1l1111l1l1_opy_ = self._1l111llll1_opy_
        bstack1l1111ll11_opy_ = Result(result=bstack1l111ll1l1_opy_, exception=bstack1l1111l1l1_opy_, bstack1l1111lll1_opy_=[bstack1l1111l1l1_opy_])
        if attrs.get(bstack1l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧස"), bstack1l_opy_ (u"ࠪࠫහ")).lower() in [bstack1l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪළ"), bstack1l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧෆ")]:
            bstack1l11111lll_opy_ = current_test_id if current_test_id else bstack11lll11ll_opy_(threading.current_thread(), bstack1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡴࡷ࡬ࡸࡪࡥࡩࡥࠩ෇"), None)
            if bstack1l11111lll_opy_:
                bstack11llll11l1_opy_ = bstack1l11111lll_opy_ + bstack1l_opy_ (u"ࠢ࠮ࠤ෈") + attrs.get(bstack1l_opy_ (u"ࠨࡶࡼࡴࡪ࠭෉"), bstack1l_opy_ (u"්ࠩࠪ")).lower()
                self._1l111l111l_opy_[bstack11llll11l1_opy_][bstack1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭෋")].stop(time=bstack1l11lll111_opy_(), duration=int(attrs.get(bstack1l_opy_ (u"ࠫࡪࡲࡡࡱࡵࡨࡨࡹ࡯࡭ࡦࠩ෌"), bstack1l_opy_ (u"ࠬ࠶ࠧ෍"))), result=bstack1l1111ll11_opy_)
                bstack1llll1111l_opy_.bstack1l111ll1ll_opy_(bstack1l_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ෎"), self._1l111l111l_opy_[bstack11llll11l1_opy_][bstack1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪා")])
        else:
            bstack1l11111lll_opy_ = current_test_id if current_test_id else bstack11lll11ll_opy_(threading.current_thread(), bstack1l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡪࡦࠪැ"), None)
            if bstack1l11111lll_opy_ and len(self.bstack1l1111l11l_opy_) == 1:
                current_step_uuid = bstack11lll11ll_opy_(threading.current_thread(), bstack1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡷࡹ࡫ࡰࡠࡷࡸ࡭ࡩ࠭ෑ"), None)
                self._1l111l111l_opy_[bstack1l11111lll_opy_][bstack1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ි")].bstack11llllllll_opy_(current_step_uuid, duration=int(attrs.get(bstack1l_opy_ (u"ࠫࡪࡲࡡࡱࡵࡨࡨࡹ࡯࡭ࡦࠩී"), bstack1l_opy_ (u"ࠬ࠶ࠧු"))), result=bstack1l1111ll11_opy_)
            else:
                self.bstack1l11l11l1l_opy_(attrs)
            self.bstack1l1111l11l_opy_.pop()
    def log_message(self, message):
        try:
            if message.get(bstack1l_opy_ (u"࠭ࡨࡵ࡯࡯ࠫ෕"), bstack1l_opy_ (u"ࠧ࡯ࡱࠪූ")) == bstack1l_opy_ (u"ࠨࡻࡨࡷࠬ෗"):
                return
            self.messages.push(message)
            bstack11lll1llll_opy_ = []
            if bstack1llll1111l_opy_.bstack1l1111l111_opy_():
                bstack11lll1llll_opy_.append({
                    bstack1l_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬෘ"): bstack1l11lll111_opy_(),
                    bstack1l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫෙ"): message.get(bstack1l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬේ")),
                    bstack1l_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫෛ"): message.get(bstack1l_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬො")),
                    **bstack1llll1111l_opy_.bstack1l1111l111_opy_()
                })
                if len(bstack11lll1llll_opy_) > 0:
                    bstack1llll1111l_opy_.bstack1ll1l1lll_opy_(bstack11lll1llll_opy_)
        except Exception as err:
            pass
    def close(self):
        bstack1llll1111l_opy_.bstack11lll1l1ll_opy_()
    def bstack1l11l11l1l_opy_(self, bstack11llll1l1l_opy_):
        if not bstack1llll1111l_opy_.bstack1l1111l111_opy_():
            return
        kwname = bstack1l_opy_ (u"ࠧࡼࡿࠣࡿࢂ࠭ෝ").format(bstack11llll1l1l_opy_.get(bstack1l_opy_ (u"ࠨ࡭ࡺࡲࡦࡳࡥࠨෞ")), bstack11llll1l1l_opy_.get(bstack1l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧෟ"), bstack1l_opy_ (u"ࠪࠫ෠"))) if bstack11llll1l1l_opy_.get(bstack1l_opy_ (u"ࠫࡦࡸࡧࡴࠩ෡"), []) else bstack11llll1l1l_opy_.get(bstack1l_opy_ (u"ࠬࡱࡷ࡯ࡣࡰࡩࠬ෢"))
        error_message = bstack1l_opy_ (u"ࠨ࡫ࡸࡰࡤࡱࡪࡀࠠ࡝ࠤࡾ࠴ࢂࡢࠢࠡࡾࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࡡࠨࡻ࠲ࡿ࡟ࠦࠥࢂࠠࡦࡺࡦࡩࡵࡺࡩࡰࡰ࠽ࠤࡡࠨࡻ࠳ࡿ࡟ࠦࠧ෣").format(kwname, bstack11llll1l1l_opy_.get(bstack1l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ෤")), str(bstack11llll1l1l_opy_.get(bstack1l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ෥"))))
        bstack11lll11ll1_opy_ = bstack1l_opy_ (u"ࠤ࡮ࡻࡳࡧ࡭ࡦ࠼ࠣࡠࠧࢁ࠰ࡾ࡞ࠥࠤࢁࠦࡳࡵࡣࡷࡹࡸࡀࠠ࡝ࠤࡾ࠵ࢂࡢࠢࠣ෦").format(kwname, bstack11llll1l1l_opy_.get(bstack1l_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ෧")))
        bstack11llll111l_opy_ = error_message if bstack11llll1l1l_opy_.get(bstack1l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ෨")) else bstack11lll11ll1_opy_
        bstack11lll1l1l1_opy_ = {
            bstack1l_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ෩"): self.bstack1l1111l11l_opy_[-1].get(bstack1l_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ෪"), bstack1l11lll111_opy_()),
            bstack1l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ෫"): bstack11llll111l_opy_,
            bstack1l_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ෬"): bstack1l_opy_ (u"ࠩࡈࡖࡗࡕࡒࠨ෭") if bstack11llll1l1l_opy_.get(bstack1l_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ෮")) == bstack1l_opy_ (u"ࠫࡋࡇࡉࡍࠩ෯") else bstack1l_opy_ (u"ࠬࡏࡎࡇࡑࠪ෰"),
            **bstack1llll1111l_opy_.bstack1l1111l111_opy_()
        }
        bstack1llll1111l_opy_.bstack1ll1l1lll_opy_([bstack11lll1l1l1_opy_])
    def _11lllll11l_opy_(self):
        for bstack11llllll11_opy_ in reversed(self._1l111l111l_opy_):
            bstack11lll1l111_opy_ = bstack11llllll11_opy_
            data = self._1l111l111l_opy_[bstack11llllll11_opy_][bstack1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ෱")]
            if isinstance(data, bstack1l11111l11_opy_):
                if not bstack1l_opy_ (u"ࠧࡆࡃࡆࡌࠬෲ") in data.bstack1l111111ll_opy_():
                    return bstack11lll1l111_opy_
            else:
                return bstack11lll1l111_opy_
    def _1l11l11l11_opy_(self, messages):
        try:
            bstack1l111l1l11_opy_ = BuiltIn().get_variable_value(bstack1l_opy_ (u"ࠣࠦࡾࡐࡔࡍࠠࡍࡇ࡙ࡉࡑࢃࠢෳ")) in (bstack11lll1ll1l_opy_.DEBUG, bstack11lll1ll1l_opy_.TRACE)
            for message, bstack1l111l1ll1_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ෴"))
                level = message.get(bstack1l_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ෵"))
                if level == bstack11lll1ll1l_opy_.FAIL:
                    self._1l111llll1_opy_ = name or self._1l111llll1_opy_
                    self._1l1111llll_opy_ = bstack1l111l1ll1_opy_.get(bstack1l_opy_ (u"ࠦࡲ࡫ࡳࡴࡣࡪࡩࠧ෶")) if bstack1l111l1l11_opy_ and bstack1l111l1ll1_opy_ else self._1l1111llll_opy_
        except:
            pass
    @classmethod
    def bstack1l111ll1ll_opy_(self, event: str, bstack1l11l11111_opy_: bstack1l111ll11l_opy_, bstack1l111ll111_opy_=False):
        if event == bstack1l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ෷"):
            bstack1l11l11111_opy_.set(hooks=self.store[bstack1l_opy_ (u"࠭ࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡵࠪ෸")])
        if event == bstack1l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨ෹"):
            event = bstack1l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ෺")
        if bstack1l111ll111_opy_:
            bstack1l11l111l1_opy_ = {
                bstack1l_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭෻"): event,
                bstack1l11l11111_opy_.bstack11lllll1ll_opy_(): bstack1l11l11111_opy_.bstack1l11l1111l_opy_(event)
            }
            self.bstack1l111111l1_opy_.append(bstack1l11l111l1_opy_)
        else:
            bstack1llll1111l_opy_.bstack1l111ll1ll_opy_(event, bstack1l11l11111_opy_)
class Messages:
    def __init__(self):
        self._1l11111ll1_opy_ = []
    def bstack11lll1l11l_opy_(self):
        self._1l11111ll1_opy_.append([])
    def bstack11lllllll1_opy_(self):
        return self._1l11111ll1_opy_.pop() if self._1l11111ll1_opy_ else list()
    def push(self, message):
        self._1l11111ll1_opy_[-1].append(message) if self._1l11111ll1_opy_ else self._1l11111ll1_opy_.append([message])
class bstack11lll1ll1l_opy_:
    FAIL = bstack1l_opy_ (u"ࠪࡊࡆࡏࡌࠨ෼")
    ERROR = bstack1l_opy_ (u"ࠫࡊࡘࡒࡐࡔࠪ෽")
    WARNING = bstack1l_opy_ (u"ࠬ࡝ࡁࡓࡐࠪ෾")
    bstack1l11111l1l_opy_ = bstack1l_opy_ (u"࠭ࡉࡏࡈࡒࠫ෿")
    DEBUG = bstack1l_opy_ (u"ࠧࡅࡇࡅ࡙ࡌ࠭฀")
    TRACE = bstack1l_opy_ (u"ࠨࡖࡕࡅࡈࡋࠧก")
    bstack1l111l11ll_opy_ = [FAIL, ERROR]
def bstack11llll1lll_opy_(bstack1l11111111_opy_):
    if not bstack1l11111111_opy_:
        return None
    if bstack1l11111111_opy_.get(bstack1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬข"), None):
        return getattr(bstack1l11111111_opy_[bstack1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ฃ")], bstack1l_opy_ (u"ࠫࡺࡻࡩࡥࠩค"), None)
    return bstack1l11111111_opy_.get(bstack1l_opy_ (u"ࠬࡻࡵࡪࡦࠪฅ"), None)
def bstack1l111lllll_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack1l_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬฆ"), bstack1l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩง")]:
        return
    if hook_type.lower() == bstack1l_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧจ"):
        if current_test_uuid is None:
            return bstack1l_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡄࡐࡑ࠭ฉ")
        else:
            return bstack1l_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠨช")
    elif hook_type.lower() == bstack1l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭ซ"):
        if current_test_uuid is None:
            return bstack1l_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡆࡒࡌࠨฌ")
        else:
            return bstack1l_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪญ")