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
import atexit
import datetime
import inspect
import logging
import os
import signal
import sys
import threading
from uuid import uuid4
from bstack_utils.percy_sdk import PercySDK
import tempfile
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack1l11llll_opy_, bstack1ll11l1l11_opy_, update, bstack1l1l11l1ll_opy_,
                                       bstack1l1llll1_opy_, bstack1lllll111l_opy_, bstack11l1l11l1_opy_, bstack1l1l11l11_opy_,
                                       bstack11l11ll11_opy_, bstack1l1ll111l_opy_, bstack1lllll11ll_opy_, bstack1l1l111lll_opy_,
                                       bstack1l1lll11l_opy_, getAccessibilityResults, getAccessibilityResultsSummary, perform_scan, bstack1lll1ll1l1_opy_)
from browserstack_sdk.bstack1lll1l111l_opy_ import bstack1lll1l1l11_opy_
from browserstack_sdk._version import __version__
from bstack_utils import bstack1lll1ll1ll_opy_
from bstack_utils.capture import bstack11llll11ll_opy_
from bstack_utils.config import Config
from bstack_utils.constants import bstack11111l1l_opy_, bstack1lll1lll_opy_, bstack1ll1lllll1_opy_, \
    bstack1l1llll111_opy_
from bstack_utils.helper import bstack11lll11ll_opy_, bstack1111lllll_opy_, bstack111lll111l_opy_, bstack1l11lll111_opy_, \
    bstack11l11ll111_opy_, \
    bstack111lll1l1l_opy_, bstack1ll1ll1l1_opy_, bstack11l11lll1_opy_, bstack111lll1lll_opy_, bstack1lllll1111_opy_, Notset, \
    bstack1l1l1llll1_opy_, bstack11l1111lll_opy_, bstack11l111111l_opy_, Result, bstack11l1111111_opy_, bstack11l11l1lll_opy_, bstack11llll1l11_opy_, \
    bstack1ll1l11lll_opy_, bstack11ll111l_opy_, bstack11l1l1lll_opy_, bstack11l11111l1_opy_
from bstack_utils.bstack111ll1l111_opy_ import bstack111ll11l1l_opy_
from bstack_utils.messages import bstack1l1l1ll11l_opy_, bstack1lll11l1_opy_, bstack1ll1ll11l_opy_, bstack11ll11ll1_opy_, bstack1l1lll1l1l_opy_, \
    bstack1l1llllll1_opy_, bstack1l111ll11_opy_, bstack1ll1llll_opy_, bstack1l1ll111_opy_, bstack1l1l111l1_opy_, \
    bstack11ll11l11_opy_, bstack11l11l11l_opy_
from bstack_utils.proxy import bstack1l1ll1lll1_opy_, bstack1l11ll1l1_opy_
from bstack_utils.bstack1lll1ll1_opy_ import bstack1llllll1l1l_opy_, bstack1llllll111l_opy_, bstack1lllllll1l1_opy_, bstack1llllll11l1_opy_, \
    bstack1lllll1llll_opy_, bstack1lllllll1ll_opy_, bstack1llllll11ll_opy_, bstack1ll111111l_opy_, bstack1llllll1111_opy_
from bstack_utils.bstack1l11lllll1_opy_ import bstack1l111l1l_opy_
from bstack_utils.bstack1l111ll1l_opy_ import bstack1lllllll1l_opy_, bstack11l1ll111_opy_, bstack1111l1111_opy_, \
    bstack1lll1l11ll_opy_, bstack1lll1ll11l_opy_
from bstack_utils.bstack1l111l1l1l_opy_ import bstack11llll1111_opy_
from bstack_utils.bstack1l11l1ll1_opy_ import bstack1llll1111l_opy_
import bstack_utils.bstack11111111l_opy_ as bstack1ll1l11l1l_opy_
from bstack_utils.bstack1lll11111_opy_ import bstack1lll11111_opy_
bstack1l1ll1l1l_opy_ = None
bstack1l11l1l11l_opy_ = None
bstack1ll11ll11l_opy_ = None
bstack1l11ll1ll1_opy_ = None
bstack11l1ll11_opy_ = None
bstack1ll111ll_opy_ = None
bstack1l11l11l_opy_ = None
bstack1l1l11lll_opy_ = None
bstack1l1llllll_opy_ = None
bstack1lllllll11_opy_ = None
bstack1ll11l111_opy_ = None
bstack111l11ll1_opy_ = None
bstack1llll11l1l_opy_ = None
bstack11l1lllll_opy_ = bstack1l_opy_ (u"ࠨࠩᗌ")
CONFIG = {}
bstack11l1llll_opy_ = False
bstack1l1ll1l1ll_opy_ = bstack1l_opy_ (u"ࠩࠪᗍ")
bstack11l111ll_opy_ = bstack1l_opy_ (u"ࠪࠫᗎ")
bstack1llll1ll1l_opy_ = False
bstack1l11l111l_opy_ = []
bstack11ll1lll_opy_ = bstack11111l1l_opy_
bstack1lll11l11ll_opy_ = bstack1l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫᗏ")
bstack1lll1l1l1l1_opy_ = False
bstack1lllllllll_opy_ = {}
bstack1l1l11l1l1_opy_ = False
logger = bstack1lll1ll1ll_opy_.get_logger(__name__, bstack11ll1lll_opy_)
store = {
    bstack1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩᗐ"): []
}
bstack1lll1l111l1_opy_ = False
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_1l111l111l_opy_ = {}
current_test_uuid = None
def bstack1l11ll111_opy_(page, bstack11l111l1_opy_):
    try:
        page.evaluate(bstack1l_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢᗑ"),
                      bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠫᗒ") + json.dumps(
                          bstack11l111l1_opy_) + bstack1l_opy_ (u"ࠣࡿࢀࠦᗓ"))
    except Exception as e:
        print(bstack1l_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠤࢀࢃࠢᗔ"), e)
def bstack1lll1l1l1l_opy_(page, message, level):
    try:
        page.evaluate(bstack1l_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦᗕ"), bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩᗖ") + json.dumps(
            message) + bstack1l_opy_ (u"ࠬ࠲ࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠨᗗ") + json.dumps(level) + bstack1l_opy_ (u"࠭ࡽࡾࠩᗘ"))
    except Exception as e:
        print(bstack1l_opy_ (u"ࠢࡦࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡥࡳࡴ࡯ࡵࡣࡷ࡭ࡴࡴࠠࡼࡿࠥᗙ"), e)
def pytest_configure(config):
    bstack1l1l1l1l1l_opy_ = Config.bstack1l1l1lll1l_opy_()
    config.args = bstack1llll1111l_opy_.bstack1llll1111l1_opy_(config.args)
    bstack1l1l1l1l1l_opy_.bstack111ll1l1_opy_(bstack11l1l1lll_opy_(config.getoption(bstack1l_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬᗚ"))))
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    bstack1lll1ll11l1_opy_ = item.config.getoption(bstack1l_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫᗛ"))
    plugins = item.config.getoption(bstack1l_opy_ (u"ࠥࡴࡱࡻࡧࡪࡰࡶࠦᗜ"))
    report = outcome.get_result()
    bstack1lll1l11lll_opy_(item, call, report)
    if bstack1l_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷࡣࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡳࡰࡺ࡭ࡩ࡯ࠤᗝ") not in plugins or bstack1lllll1111_opy_():
        return
    summary = []
    driver = getattr(item, bstack1l_opy_ (u"ࠧࡥࡤࡳ࡫ࡹࡩࡷࠨᗞ"), None)
    page = getattr(item, bstack1l_opy_ (u"ࠨ࡟ࡱࡣࡪࡩࠧᗟ"), None)
    try:
        if (driver == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None):
        bstack1lll11lll1l_opy_(item, report, summary, bstack1lll1ll11l1_opy_)
    if (page is not None):
        bstack1lll1l1111l_opy_(item, report, summary, bstack1lll1ll11l1_opy_)
def bstack1lll11lll1l_opy_(item, report, summary, bstack1lll1ll11l1_opy_):
    if report.when == bstack1l_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ᗠ") and report.skipped:
        bstack1llllll1111_opy_(report)
    if report.when in [bstack1l_opy_ (u"ࠣࡵࡨࡸࡺࡶࠢᗡ"), bstack1l_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࠦᗢ")]:
        return
    if not bstack111lll111l_opy_():
        return
    try:
        if (str(bstack1lll1ll11l1_opy_).lower() != bstack1l_opy_ (u"ࠪࡸࡷࡻࡥࠨᗣ")):
            item._driver.execute_script(
                bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠡࠩᗤ") + json.dumps(
                    report.nodeid) + bstack1l_opy_ (u"ࠬࢃࡽࠨᗥ"))
        os.environ[bstack1l_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙ࡥࡔࡆࡕࡗࡣࡓࡇࡍࡆࠩᗦ")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack1l_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡳࡡࡳ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦ࠼ࠣࡿ࠵ࢃࠢᗧ").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1l_opy_ (u"ࠣࡹࡤࡷࡽ࡬ࡡࡪ࡮ࠥᗨ")))
    bstack111lllll_opy_ = bstack1l_opy_ (u"ࠤࠥᗩ")
    bstack1llllll1111_opy_(report)
    if not passed:
        try:
            bstack111lllll_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack1l_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡦࡨࡸࡪࡸ࡭ࡪࡰࡨࠤ࡫ࡧࡩ࡭ࡷࡵࡩࠥࡸࡥࡢࡵࡲࡲ࠿ࠦࡻ࠱ࡿࠥᗪ").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack111lllll_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack1l_opy_ (u"ࠦࡼࡧࡳࡹࡨࡤ࡭ࡱࠨᗫ")))
        bstack111lllll_opy_ = bstack1l_opy_ (u"ࠧࠨᗬ")
        if not passed:
            try:
                bstack111lllll_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1l_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡩ࡫ࡴࡦࡴࡰ࡭ࡳ࡫ࠠࡧࡣ࡬ࡰࡺࡸࡥࠡࡴࡨࡥࡸࡵ࡮࠻ࠢࡾ࠴ࢂࠨᗭ").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack111lllll_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥ࡭ࡳ࡬࡯ࠣ࠮ࠣࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡨࡦࡺࡡࠣ࠼ࠣࠫᗮ")
                    + json.dumps(bstack1l_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠢࠤᗯ"))
                    + bstack1l_opy_ (u"ࠤ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࠧᗰ")
                )
            else:
                item._driver.execute_script(
                    bstack1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡥࡳࡴࡲࡶࠧ࠲ࠠ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡥࡣࡷࡥࠧࡀࠠࠨᗱ")
                    + json.dumps(str(bstack111lllll_opy_))
                    + bstack1l_opy_ (u"ࠦࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃࠢᗲ")
                )
        except Exception as e:
            summary.append(bstack1l_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡥࡳࡴ࡯ࡵࡣࡷࡩ࠿ࠦࡻ࠱ࡿࠥᗳ").format(e))
def bstack1lll11ll1l1_opy_(test_name, error_message):
    try:
        bstack1lll11l1lll_opy_ = []
        bstack1ll1l1lll1_opy_ = os.environ.get(bstack1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ᗴ"), bstack1l_opy_ (u"ࠧ࠱ࠩᗵ"))
        bstack1llll111l_opy_ = {bstack1l_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᗶ"): test_name, bstack1l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨᗷ"): error_message, bstack1l_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩᗸ"): bstack1ll1l1lll1_opy_}
        bstack1lll1l11ll1_opy_ = os.path.join(tempfile.gettempdir(), bstack1l_opy_ (u"ࠫࡵࡽ࡟ࡱࡻࡷࡩࡸࡺ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷ࠲࡯ࡹ࡯࡯ࠩᗹ"))
        if os.path.exists(bstack1lll1l11ll1_opy_):
            with open(bstack1lll1l11ll1_opy_) as f:
                bstack1lll11l1lll_opy_ = json.load(f)
        bstack1lll11l1lll_opy_.append(bstack1llll111l_opy_)
        with open(bstack1lll1l11ll1_opy_, bstack1l_opy_ (u"ࠬࡽࠧᗺ")) as f:
            json.dump(bstack1lll11l1lll_opy_, f)
    except Exception as e:
        logger.debug(bstack1l_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡲࡨࡶࡸ࡯ࡳࡵ࡫ࡱ࡫ࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡳࡽࡹ࡫ࡳࡵࠢࡨࡶࡷࡵࡲࡴ࠼ࠣࠫᗻ") + str(e))
def bstack1lll1l1111l_opy_(item, report, summary, bstack1lll1ll11l1_opy_):
    if report.when in [bstack1l_opy_ (u"ࠢࡴࡧࡷࡹࡵࠨᗼ"), bstack1l_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࠥᗽ")]:
        return
    if (str(bstack1lll1ll11l1_opy_).lower() != bstack1l_opy_ (u"ࠩࡷࡶࡺ࡫ࠧᗾ")):
        bstack1l11ll111_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1l_opy_ (u"ࠥࡻࡦࡹࡸࡧࡣ࡬ࡰࠧᗿ")))
    bstack111lllll_opy_ = bstack1l_opy_ (u"ࠦࠧᘀ")
    bstack1llllll1111_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack111lllll_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1l_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡨࡪࡺࡥࡳ࡯࡬ࡲࡪࠦࡦࡢ࡫࡯ࡹࡷ࡫ࠠࡳࡧࡤࡷࡴࡴ࠺ࠡࡽ࠳ࢁࠧᘁ").format(e)
                )
        try:
            if passed:
                bstack1lll1ll11l_opy_(getattr(item, bstack1l_opy_ (u"࠭࡟ࡱࡣࡪࡩࠬᘂ"), None), bstack1l_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢᘃ"))
            else:
                error_message = bstack1l_opy_ (u"ࠨࠩᘄ")
                if bstack111lllll_opy_:
                    bstack1lll1l1l1l_opy_(item._page, str(bstack111lllll_opy_), bstack1l_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣᘅ"))
                    bstack1lll1ll11l_opy_(getattr(item, bstack1l_opy_ (u"ࠪࡣࡵࡧࡧࡦࠩᘆ"), None), bstack1l_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦᘇ"), str(bstack111lllll_opy_))
                    error_message = str(bstack111lllll_opy_)
                else:
                    bstack1lll1ll11l_opy_(getattr(item, bstack1l_opy_ (u"ࠬࡥࡰࡢࡩࡨࠫᘈ"), None), bstack1l_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨᘉ"))
                bstack1lll11ll1l1_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack1l_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡻࡰࡥࡣࡷࡩࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡳࡵࡣࡷࡹࡸࡀࠠࡼ࠲ࢀࠦᘊ").format(e))
try:
    from typing import Generator
    import pytest_playwright.pytest_playwright as p
    @pytest.fixture
    def page(context: BrowserContext, request: pytest.FixtureRequest) -> Generator[Page, None, None]:
        page = context.new_page()
        request.node._page = page
        yield page
except:
    pass
def pytest_addoption(parser):
    parser.addoption(bstack1l_opy_ (u"ࠣ࠯࠰ࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧᘋ"), default=bstack1l_opy_ (u"ࠤࡉࡥࡱࡹࡥࠣᘌ"), help=bstack1l_opy_ (u"ࠥࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡨࠦࡳࡦࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠤᘍ"))
    parser.addoption(bstack1l_opy_ (u"ࠦ࠲࠳ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠥᘎ"), default=bstack1l_opy_ (u"ࠧࡌࡡ࡭ࡵࡨࠦᘏ"), help=bstack1l_opy_ (u"ࠨࡁࡶࡶࡲࡱࡦࡺࡩࡤࠢࡶࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠧᘐ"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack1l_opy_ (u"ࠢ࠮࠯ࡧࡶ࡮ࡼࡥࡳࠤᘑ"), action=bstack1l_opy_ (u"ࠣࡵࡷࡳࡷ࡫ࠢᘒ"), default=bstack1l_opy_ (u"ࠤࡦ࡬ࡷࡵ࡭ࡦࠤᘓ"),
                         help=bstack1l_opy_ (u"ࠥࡈࡷ࡯ࡶࡦࡴࠣࡸࡴࠦࡲࡶࡰࠣࡸࡪࡹࡴࡴࠤᘔ"))
def bstack1l1111l1ll_opy_(log):
    if not (log[bstack1l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᘕ")] and log[bstack1l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᘖ")].strip()):
        return
    active = bstack1l1111l111_opy_()
    log = {
        bstack1l_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬᘗ"): log[bstack1l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ᘘ")],
        bstack1l_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫᘙ"): datetime.datetime.utcnow().isoformat() + bstack1l_opy_ (u"ࠩ࡝ࠫᘚ"),
        bstack1l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᘛ"): log[bstack1l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᘜ")],
    }
    if active:
        if active[bstack1l_opy_ (u"ࠬࡺࡹࡱࡧࠪᘝ")] == bstack1l_opy_ (u"࠭ࡨࡰࡱ࡮ࠫᘞ"):
            log[bstack1l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᘟ")] = active[bstack1l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᘠ")]
        elif active[bstack1l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧᘡ")] == bstack1l_opy_ (u"ࠪࡸࡪࡹࡴࠨᘢ"):
            log[bstack1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᘣ")] = active[bstack1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᘤ")]
    bstack1llll1111l_opy_.bstack1ll1l1lll_opy_([log])
def bstack1l1111l111_opy_():
    if len(store[bstack1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪᘥ")]) > 0 and store[bstack1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫᘦ")][-1]:
        return {
            bstack1l_opy_ (u"ࠨࡶࡼࡴࡪ࠭ᘧ"): bstack1l_opy_ (u"ࠩ࡫ࡳࡴࡱࠧᘨ"),
            bstack1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᘩ"): store[bstack1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨᘪ")][-1]
        }
    if store.get(bstack1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩᘫ"), None):
        return {
            bstack1l_opy_ (u"࠭ࡴࡺࡲࡨࠫᘬ"): bstack1l_opy_ (u"ࠧࡵࡧࡶࡸࠬᘭ"),
            bstack1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᘮ"): store[bstack1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ᘯ")]
        }
    return None
bstack1l11l111ll_opy_ = bstack11llll11ll_opy_(bstack1l1111l1ll_opy_)
def pytest_runtest_call(item):
    try:
        global CONFIG
        global bstack1lll1l1l1l1_opy_
        item._1lll1l1ll11_opy_ = True
        bstack11l1111l_opy_ = bstack1ll1l11l1l_opy_.bstack1ll1l111l_opy_(CONFIG, bstack111lll1l1l_opy_(item.own_markers))
        item._a11y_test_case = bstack11l1111l_opy_
        if bstack1lll1l1l1l1_opy_:
            driver = getattr(item, bstack1l_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫᘰ"), None)
            item._a11y_started = bstack1ll1l11l1l_opy_.bstack1111ll11_opy_(driver, bstack11l1111l_opy_)
        if not bstack1llll1111l_opy_.on() or bstack1lll11l11ll_opy_ != bstack1l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫᘱ"):
            return
        global current_test_uuid, bstack1l11l111ll_opy_
        bstack1l11l111ll_opy_.start()
        bstack1l11111111_opy_ = {
            bstack1l_opy_ (u"ࠬࡻࡵࡪࡦࠪᘲ"): uuid4().__str__(),
            bstack1l_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᘳ"): datetime.datetime.utcnow().isoformat() + bstack1l_opy_ (u"࡛ࠧࠩᘴ")
        }
        current_test_uuid = bstack1l11111111_opy_[bstack1l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᘵ")]
        store[bstack1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ᘶ")] = bstack1l11111111_opy_[bstack1l_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᘷ")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _1l111l111l_opy_[item.nodeid] = {**_1l111l111l_opy_[item.nodeid], **bstack1l11111111_opy_}
        bstack1lll1l1lll1_opy_(item, _1l111l111l_opy_[item.nodeid], bstack1l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬᘸ"))
    except Exception as err:
        print(bstack1l_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡷࡻ࡮ࡵࡧࡶࡸࡤࡩࡡ࡭࡮࠽ࠤࢀࢃࠧᘹ"), str(err))
def pytest_runtest_setup(item):
    global bstack1lll1l111l1_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack111lll1lll_opy_():
        atexit.register(bstack1l1l111l1l_opy_)
        if not bstack1lll1l111l1_opy_:
            try:
                bstack1lll11lll11_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack11l11111l1_opy_():
                    bstack1lll11lll11_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack1lll11lll11_opy_:
                    signal.signal(s, bstack1lll1ll11ll_opy_)
                bstack1lll1l111l1_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack1l_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡴࡨ࡫࡮ࡹࡴࡦࡴࠣࡷ࡮࡭࡮ࡢ࡮ࠣ࡬ࡦࡴࡤ࡭ࡧࡵࡷ࠿ࠦࠢᘺ") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack1llllll1l1l_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack1l_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᘻ")
    try:
        if not bstack1llll1111l_opy_.on():
            return
        bstack1l11l111ll_opy_.start()
        uuid = uuid4().__str__()
        bstack1l11111111_opy_ = {
            bstack1l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᘼ"): uuid,
            bstack1l_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᘽ"): datetime.datetime.utcnow().isoformat() + bstack1l_opy_ (u"ࠪ࡞ࠬᘾ"),
            bstack1l_opy_ (u"ࠫࡹࡿࡰࡦࠩᘿ"): bstack1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪᙀ"),
            bstack1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩᙁ"): bstack1l_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬᙂ"),
            bstack1l_opy_ (u"ࠨࡪࡲࡳࡰࡥ࡮ࡢ࡯ࡨࠫᙃ"): bstack1l_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨᙄ")
        }
        threading.current_thread().current_hook_uuid = uuid
        threading.current_thread().current_test_item = item
        store[bstack1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧᙅ")] = item
        store[bstack1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨᙆ")] = [uuid]
        if not _1l111l111l_opy_.get(item.nodeid, None):
            _1l111l111l_opy_[item.nodeid] = {bstack1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫᙇ"): [], bstack1l_opy_ (u"࠭ࡦࡪࡺࡷࡹࡷ࡫ࡳࠨᙈ"): []}
        _1l111l111l_opy_[item.nodeid][bstack1l_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ᙉ")].append(bstack1l11111111_opy_[bstack1l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᙊ")])
        _1l111l111l_opy_[item.nodeid + bstack1l_opy_ (u"ࠩ࠰ࡷࡪࡺࡵࡱࠩᙋ")] = bstack1l11111111_opy_
        bstack1lll1l1l111_opy_(item, bstack1l11111111_opy_, bstack1l_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫᙌ"))
    except Exception as err:
        print(bstack1l_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡶࡺࡴࡴࡦࡵࡷࡣࡸ࡫ࡴࡶࡲ࠽ࠤࢀࢃࠧᙍ"), str(err))
def pytest_runtest_teardown(item):
    try:
        global bstack1lllllllll_opy_
        if CONFIG.get(bstack1l_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫᙎ"), False):
            if CONFIG.get(bstack1l_opy_ (u"࠭ࡰࡦࡴࡦࡽࡈࡧࡰࡵࡷࡵࡩࡒࡵࡤࡦࠩᙏ"), bstack1l_opy_ (u"ࠢࡢࡷࡷࡳࠧᙐ")) == bstack1l_opy_ (u"ࠣࡶࡨࡷࡹࡩࡡࡴࡧࠥᙑ"):
                bstack1lll1l11111_opy_ = bstack11lll11ll_opy_(threading.current_thread(), bstack1l_opy_ (u"ࠩࡳࡩࡷࡩࡹࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬᙒ"), None)
                bstack1lllllll1_opy_ = bstack1lll1l11111_opy_ + bstack1l_opy_ (u"ࠥ࠱ࡹ࡫ࡳࡵࡥࡤࡷࡪࠨᙓ")
                driver = getattr(item, bstack1l_opy_ (u"ࠫࡤࡪࡲࡪࡸࡨࡶࠬᙔ"), None)
                PercySDK.screenshot(driver, bstack1lllllll1_opy_)
        if getattr(item, bstack1l_opy_ (u"ࠬࡥࡡ࠲࠳ࡼࡣࡸࡺࡡࡳࡶࡨࡨࠬᙕ"), False):
            bstack1lll1l1l11_opy_.bstack1ll111l111_opy_(getattr(item, bstack1l_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧᙖ"), None), bstack1lllllllll_opy_, logger, item)
        if not bstack1llll1111l_opy_.on():
            return
        bstack1l11111111_opy_ = {
            bstack1l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᙗ"): uuid4().__str__(),
            bstack1l_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᙘ"): datetime.datetime.utcnow().isoformat() + bstack1l_opy_ (u"ࠩ࡝ࠫᙙ"),
            bstack1l_opy_ (u"ࠪࡸࡾࡶࡥࠨᙚ"): bstack1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩᙛ"),
            bstack1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨᙜ"): bstack1l_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪᙝ"),
            bstack1l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡴࡡ࡮ࡧࠪᙞ"): bstack1l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪᙟ")
        }
        _1l111l111l_opy_[item.nodeid + bstack1l_opy_ (u"ࠩ࠰ࡸࡪࡧࡲࡥࡱࡺࡲࠬᙠ")] = bstack1l11111111_opy_
        bstack1lll1l1l111_opy_(item, bstack1l11111111_opy_, bstack1l_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫᙡ"))
    except Exception as err:
        print(bstack1l_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡶࡺࡴࡴࡦࡵࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡀࠠࡼࡿࠪᙢ"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if not bstack1llll1111l_opy_.on():
        yield
        return
    start_time = datetime.datetime.now()
    if bstack1llllll11l1_opy_(fixturedef.argname):
        store[bstack1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥ࡭ࡰࡦࡸࡰࡪࡥࡩࡵࡧࡰࠫᙣ")] = request.node
    elif bstack1lllll1llll_opy_(fixturedef.argname):
        store[bstack1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡤ࡮ࡤࡷࡸࡥࡩࡵࡧࡰࠫᙤ")] = request.node
    outcome = yield
    try:
        fixture = {
            bstack1l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᙥ"): fixturedef.argname,
            bstack1l_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᙦ"): bstack11l11ll111_opy_(outcome),
            bstack1l_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫᙧ"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        current_test_item = store[bstack1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧᙨ")]
        if not _1l111l111l_opy_.get(current_test_item.nodeid, None):
            _1l111l111l_opy_[current_test_item.nodeid] = {bstack1l_opy_ (u"ࠫ࡫࡯ࡸࡵࡷࡵࡩࡸ࠭ᙩ"): []}
        _1l111l111l_opy_[current_test_item.nodeid][bstack1l_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧᙪ")].append(fixture)
    except Exception as err:
        logger.debug(bstack1l_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤ࡬ࡩࡹࡶࡸࡶࡪࡥࡳࡦࡶࡸࡴ࠿ࠦࡻࡾࠩᙫ"), str(err))
if bstack1lllll1111_opy_() and bstack1llll1111l_opy_.on():
    def pytest_bdd_before_step(request, step):
        try:
            _1l111l111l_opy_[request.node.nodeid][bstack1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪᙬ")].bstack1llll1l1111_opy_(id(step))
        except Exception as err:
            print(bstack1l_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡧ࡫ࡦࡰࡴࡨࡣࡸࡺࡥࡱ࠼ࠣࡿࢂ࠭᙭"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        try:
            _1l111l111l_opy_[request.node.nodeid][bstack1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ᙮")].bstack11llllllll_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack1l_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡥࡨࡩࡥࡳࡵࡧࡳࡣࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠧᙯ"), str(err))
    def pytest_bdd_after_step(request, step):
        try:
            bstack1l111l1l1l_opy_: bstack11llll1111_opy_ = _1l111l111l_opy_[request.node.nodeid][bstack1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧᙰ")]
            bstack1l111l1l1l_opy_.bstack11llllllll_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack1l_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡧࡪࡤࡠࡵࡷࡩࡵࡥࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠩᙱ"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack1lll11l11ll_opy_
        try:
            if not bstack1llll1111l_opy_.on() or bstack1lll11l11ll_opy_ != bstack1l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠪᙲ"):
                return
            global bstack1l11l111ll_opy_
            bstack1l11l111ll_opy_.start()
            driver = bstack11lll11ll_opy_(threading.current_thread(), bstack1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ᙳ"), None)
            if not _1l111l111l_opy_.get(request.node.nodeid, None):
                _1l111l111l_opy_[request.node.nodeid] = {}
            bstack1l111l1l1l_opy_ = bstack11llll1111_opy_.bstack1llll11lll1_opy_(
                scenario, feature, request.node,
                name=bstack1lllllll1ll_opy_(request.node, scenario),
                bstack11lllll111_opy_=bstack1l11lll111_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack1l_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴ࠮ࡥࡸࡧࡺࡳࡢࡦࡴࠪᙴ"),
                tags=bstack1llllll11ll_opy_(feature, scenario),
                bstack1l111lll1l_opy_=bstack1llll1111l_opy_.bstack1l111l1111_opy_(driver) if driver and driver.session_id else {}
            )
            _1l111l111l_opy_[request.node.nodeid][bstack1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᙵ")] = bstack1l111l1l1l_opy_
            bstack1lll1l1l11l_opy_(bstack1l111l1l1l_opy_.uuid)
            bstack1llll1111l_opy_.bstack1l111ll1ll_opy_(bstack1l_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫᙶ"), bstack1l111l1l1l_opy_)
        except Exception as err:
            print(bstack1l_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰ࠼ࠣࡿࢂ࠭ᙷ"), str(err))
def bstack1lll11l1l1l_opy_(bstack1lll1l1l1ll_opy_):
    if bstack1lll1l1l1ll_opy_ in store[bstack1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩᙸ")]:
        store[bstack1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪᙹ")].remove(bstack1lll1l1l1ll_opy_)
def bstack1lll1l1l11l_opy_(bstack1lll11l1ll1_opy_):
    store[bstack1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫᙺ")] = bstack1lll11l1ll1_opy_
    threading.current_thread().current_test_uuid = bstack1lll11l1ll1_opy_
@bstack1llll1111l_opy_.bstack1lll1lllll1_opy_
def bstack1lll1l11lll_opy_(item, call, report):
    global bstack1lll11l11ll_opy_
    bstack1l1l1l11l1_opy_ = bstack1l11lll111_opy_()
    if hasattr(report, bstack1l_opy_ (u"ࠨࡵࡷࡳࡵ࠭ᙻ")):
        bstack1l1l1l11l1_opy_ = bstack11l1111111_opy_(report.stop)
    if hasattr(report, bstack1l_opy_ (u"ࠩࡶࡸࡦࡸࡴࠨᙼ")):
        bstack1l1l1l11l1_opy_ = bstack11l1111111_opy_(report.start)
    try:
        if getattr(report, bstack1l_opy_ (u"ࠪࡻ࡭࡫࡮ࠨᙽ"), bstack1l_opy_ (u"ࠫࠬᙾ")) == bstack1l_opy_ (u"ࠬࡩࡡ࡭࡮ࠪᙿ"):
            bstack1l11l111ll_opy_.reset()
        if getattr(report, bstack1l_opy_ (u"࠭ࡷࡩࡧࡱࠫ "), bstack1l_opy_ (u"ࠧࠨᚁ")) == bstack1l_opy_ (u"ࠨࡥࡤࡰࡱ࠭ᚂ"):
            if bstack1lll11l11ll_opy_ == bstack1l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩᚃ"):
                _1l111l111l_opy_[item.nodeid][bstack1l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᚄ")] = bstack1l1l1l11l1_opy_
                bstack1lll1l1lll1_opy_(item, _1l111l111l_opy_[item.nodeid], bstack1l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᚅ"), report, call)
                store[bstack1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩᚆ")] = None
            elif bstack1lll11l11ll_opy_ == bstack1l_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠥᚇ"):
                bstack1l111l1l1l_opy_ = _1l111l111l_opy_[item.nodeid][bstack1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪᚈ")]
                bstack1l111l1l1l_opy_.set(hooks=_1l111l111l_opy_[item.nodeid].get(bstack1l_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧᚉ"), []))
                exception, bstack1l1111lll1_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack1l1111lll1_opy_ = [call.excinfo.exconly(), getattr(report, bstack1l_opy_ (u"ࠩ࡯ࡳࡳ࡭ࡲࡦࡲࡵࡸࡪࡾࡴࠨᚊ"), bstack1l_opy_ (u"ࠪࠫᚋ"))]
                bstack1l111l1l1l_opy_.stop(time=bstack1l1l1l11l1_opy_, result=Result(result=getattr(report, bstack1l_opy_ (u"ࠫࡴࡻࡴࡤࡱࡰࡩࠬᚌ"), bstack1l_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᚍ")), exception=exception, bstack1l1111lll1_opy_=bstack1l1111lll1_opy_))
                bstack1llll1111l_opy_.bstack1l111ll1ll_opy_(bstack1l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨᚎ"), _1l111l111l_opy_[item.nodeid][bstack1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪᚏ")])
        elif getattr(report, bstack1l_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭ᚐ"), bstack1l_opy_ (u"ࠩࠪᚑ")) in [bstack1l_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩᚒ"), bstack1l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭ᚓ")]:
            bstack11llll11l1_opy_ = item.nodeid + bstack1l_opy_ (u"ࠬ࠳ࠧᚔ") + getattr(report, bstack1l_opy_ (u"࠭ࡷࡩࡧࡱࠫᚕ"), bstack1l_opy_ (u"ࠧࠨᚖ"))
            if getattr(report, bstack1l_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩᚗ"), False):
                hook_type = bstack1l_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧᚘ") if getattr(report, bstack1l_opy_ (u"ࠪࡻ࡭࡫࡮ࠨᚙ"), bstack1l_opy_ (u"ࠫࠬᚚ")) == bstack1l_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫ᚛") else bstack1l_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪ᚜")
                _1l111l111l_opy_[bstack11llll11l1_opy_] = {
                    bstack1l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ᚝"): uuid4().__str__(),
                    bstack1l_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ᚞"): bstack1l1l1l11l1_opy_,
                    bstack1l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬ᚟"): hook_type
                }
            _1l111l111l_opy_[bstack11llll11l1_opy_][bstack1l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᚠ")] = bstack1l1l1l11l1_opy_
            bstack1lll11l1l1l_opy_(_1l111l111l_opy_[bstack11llll11l1_opy_][bstack1l_opy_ (u"ࠫࡺࡻࡩࡥࠩᚡ")])
            bstack1lll1l1l111_opy_(item, _1l111l111l_opy_[bstack11llll11l1_opy_], bstack1l_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧᚢ"), report, call)
            if getattr(report, bstack1l_opy_ (u"࠭ࡷࡩࡧࡱࠫᚣ"), bstack1l_opy_ (u"ࠧࠨᚤ")) == bstack1l_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧᚥ"):
                if getattr(report, bstack1l_opy_ (u"ࠩࡲࡹࡹࡩ࡯࡮ࡧࠪᚦ"), bstack1l_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᚧ")) == bstack1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᚨ"):
                    bstack1l11111111_opy_ = {
                        bstack1l_opy_ (u"ࠬࡻࡵࡪࡦࠪᚩ"): uuid4().__str__(),
                        bstack1l_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᚪ"): bstack1l11lll111_opy_(),
                        bstack1l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᚫ"): bstack1l11lll111_opy_()
                    }
                    _1l111l111l_opy_[item.nodeid] = {**_1l111l111l_opy_[item.nodeid], **bstack1l11111111_opy_}
                    bstack1lll1l1lll1_opy_(item, _1l111l111l_opy_[item.nodeid], bstack1l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩᚬ"))
                    bstack1lll1l1lll1_opy_(item, _1l111l111l_opy_[item.nodeid], bstack1l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫᚭ"), report, call)
    except Exception as err:
        print(bstack1l_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢ࡫ࡥࡳࡪ࡬ࡦࡡࡲ࠵࠶ࡿ࡟ࡵࡧࡶࡸࡤ࡫ࡶࡦࡰࡷ࠾ࠥࢁࡽࠨᚮ"), str(err))
def bstack1lll11l111l_opy_(test, bstack1l11111111_opy_, result=None, call=None, bstack11lllllll_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack1l111l1l1l_opy_ = {
        bstack1l_opy_ (u"ࠫࡺࡻࡩࡥࠩᚯ"): bstack1l11111111_opy_[bstack1l_opy_ (u"ࠬࡻࡵࡪࡦࠪᚰ")],
        bstack1l_opy_ (u"࠭ࡴࡺࡲࡨࠫᚱ"): bstack1l_opy_ (u"ࠧࡵࡧࡶࡸࠬᚲ"),
        bstack1l_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᚳ"): test.name,
        bstack1l_opy_ (u"ࠩࡥࡳࡩࡿࠧᚴ"): {
            bstack1l_opy_ (u"ࠪࡰࡦࡴࡧࠨᚵ"): bstack1l_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫᚶ"),
            bstack1l_opy_ (u"ࠬࡩ࡯ࡥࡧࠪᚷ"): inspect.getsource(test.obj)
        },
        bstack1l_opy_ (u"࠭ࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪᚸ"): test.name,
        bstack1l_opy_ (u"ࠧࡴࡥࡲࡴࡪ࠭ᚹ"): test.name,
        bstack1l_opy_ (u"ࠨࡵࡦࡳࡵ࡫ࡳࠨᚺ"): bstack1llll1111l_opy_.bstack1l1111ll1l_opy_(test),
        bstack1l_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬᚻ"): file_path,
        bstack1l_opy_ (u"ࠪࡰࡴࡩࡡࡵ࡫ࡲࡲࠬᚼ"): file_path,
        bstack1l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᚽ"): bstack1l_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭ᚾ"),
        bstack1l_opy_ (u"࠭ࡶࡤࡡࡩ࡭ࡱ࡫ࡰࡢࡶ࡫ࠫᚿ"): file_path,
        bstack1l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᛀ"): bstack1l11111111_opy_[bstack1l_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᛁ")],
        bstack1l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬᛂ"): bstack1l_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶࠪᛃ"),
        bstack1l_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡖࡪࡸࡵ࡯ࡒࡤࡶࡦࡳࠧᛄ"): {
            bstack1l_opy_ (u"ࠬࡸࡥࡳࡷࡱࡣࡳࡧ࡭ࡦࠩᛅ"): test.nodeid
        },
        bstack1l_opy_ (u"࠭ࡴࡢࡩࡶࠫᛆ"): bstack111lll1l1l_opy_(test.own_markers)
    }
    if bstack11lllllll_opy_ in [bstack1l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨᛇ"), bstack1l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪᛈ")]:
        bstack1l111l1l1l_opy_[bstack1l_opy_ (u"ࠩࡰࡩࡹࡧࠧᛉ")] = {
            bstack1l_opy_ (u"ࠪࡪ࡮ࡾࡴࡶࡴࡨࡷࠬᛊ"): bstack1l11111111_opy_.get(bstack1l_opy_ (u"ࠫ࡫࡯ࡸࡵࡷࡵࡩࡸ࠭ᛋ"), [])
        }
    if bstack11lllllll_opy_ == bstack1l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙࡫ࡪࡲࡳࡩࡩ࠭ᛌ"):
        bstack1l111l1l1l_opy_[bstack1l_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᛍ")] = bstack1l_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨᛎ")
        bstack1l111l1l1l_opy_[bstack1l_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧᛏ")] = bstack1l11111111_opy_[bstack1l_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨᛐ")]
        bstack1l111l1l1l_opy_[bstack1l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᛑ")] = bstack1l11111111_opy_[bstack1l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᛒ")]
    if result:
        bstack1l111l1l1l_opy_[bstack1l_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᛓ")] = result.outcome
        bstack1l111l1l1l_opy_[bstack1l_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧᛔ")] = result.duration * 1000
        bstack1l111l1l1l_opy_[bstack1l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᛕ")] = bstack1l11111111_opy_[bstack1l_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᛖ")]
        if result.failed:
            bstack1l111l1l1l_opy_[bstack1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨᛗ")] = bstack1llll1111l_opy_.bstack11ll1l1l1l_opy_(call.excinfo.typename)
            bstack1l111l1l1l_opy_[bstack1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫᛘ")] = bstack1llll1111l_opy_.bstack1llll11111l_opy_(call.excinfo, result)
        bstack1l111l1l1l_opy_[bstack1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪᛙ")] = bstack1l11111111_opy_[bstack1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫᛚ")]
    if outcome:
        bstack1l111l1l1l_opy_[bstack1l_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᛛ")] = bstack11l11ll111_opy_(outcome)
        bstack1l111l1l1l_opy_[bstack1l_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨᛜ")] = 0
        bstack1l111l1l1l_opy_[bstack1l_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᛝ")] = bstack1l11111111_opy_[bstack1l_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᛞ")]
        if bstack1l111l1l1l_opy_[bstack1l_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᛟ")] == bstack1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᛠ"):
            bstack1l111l1l1l_opy_[bstack1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫᛡ")] = bstack1l_opy_ (u"࠭ࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠧᛢ")  # bstack1lll11l1l11_opy_
            bstack1l111l1l1l_opy_[bstack1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨᛣ")] = [{bstack1l_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫᛤ"): [bstack1l_opy_ (u"ࠩࡶࡳࡲ࡫ࠠࡦࡴࡵࡳࡷ࠭ᛥ")]}]
        bstack1l111l1l1l_opy_[bstack1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩᛦ")] = bstack1l11111111_opy_[bstack1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪᛧ")]
    return bstack1l111l1l1l_opy_
def bstack1lll11ll1ll_opy_(test, bstack1l111l11l1_opy_, bstack11lllllll_opy_, result, call, outcome, bstack1lll11llll1_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack1l111l11l1_opy_[bstack1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨᛨ")]
    hook_name = bstack1l111l11l1_opy_[bstack1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡳࡧ࡭ࡦࠩᛩ")]
    hook_data = {
        bstack1l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᛪ"): bstack1l111l11l1_opy_[bstack1l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭᛫")],
        bstack1l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ᛬"): bstack1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨ᛭"),
        bstack1l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᛮ"): bstack1l_opy_ (u"ࠬࢁࡽࠨᛯ").format(bstack1llllll111l_opy_(hook_name)),
        bstack1l_opy_ (u"࠭ࡢࡰࡦࡼࠫᛰ"): {
            bstack1l_opy_ (u"ࠧ࡭ࡣࡱ࡫ࠬᛱ"): bstack1l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨᛲ"),
            bstack1l_opy_ (u"ࠩࡦࡳࡩ࡫ࠧᛳ"): None
        },
        bstack1l_opy_ (u"ࠪࡷࡨࡵࡰࡦࠩᛴ"): test.name,
        bstack1l_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࡶࠫᛵ"): bstack1llll1111l_opy_.bstack1l1111ll1l_opy_(test, hook_name),
        bstack1l_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨᛶ"): file_path,
        bstack1l_opy_ (u"࠭࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠨᛷ"): file_path,
        bstack1l_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᛸ"): bstack1l_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩ᛹"),
        bstack1l_opy_ (u"ࠩࡹࡧࡤ࡬ࡩ࡭ࡧࡳࡥࡹ࡮ࠧ᛺"): file_path,
        bstack1l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ᛻"): bstack1l111l11l1_opy_[bstack1l_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ᛼")],
        bstack1l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ᛽"): bstack1l_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠳ࡣࡶࡥࡸࡱࡧ࡫ࡲࠨ᛾") if bstack1lll11l11ll_opy_ == bstack1l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠫ᛿") else bstack1l_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴࠨᜀ"),
        bstack1l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬᜁ"): hook_type
    }
    bstack1lll1l1ll1l_opy_ = bstack11llll1lll_opy_(_1l111l111l_opy_.get(test.nodeid, None))
    if bstack1lll1l1ll1l_opy_:
        hook_data[bstack1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤ࡯ࡤࠨᜂ")] = bstack1lll1l1ll1l_opy_
    if result:
        hook_data[bstack1l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᜃ")] = result.outcome
        hook_data[bstack1l_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡢࡱࡸ࠭ᜄ")] = result.duration * 1000
        hook_data[bstack1l_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᜅ")] = bstack1l111l11l1_opy_[bstack1l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᜆ")]
        if result.failed:
            hook_data[bstack1l_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧᜇ")] = bstack1llll1111l_opy_.bstack11ll1l1l1l_opy_(call.excinfo.typename)
            hook_data[bstack1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪᜈ")] = bstack1llll1111l_opy_.bstack1llll11111l_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack1l_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᜉ")] = bstack11l11ll111_opy_(outcome)
        hook_data[bstack1l_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬᜊ")] = 100
        hook_data[bstack1l_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᜋ")] = bstack1l111l11l1_opy_[bstack1l_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᜌ")]
        if hook_data[bstack1l_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᜍ")] == bstack1l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᜎ"):
            hook_data[bstack1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨᜏ")] = bstack1l_opy_ (u"࡙ࠪࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠫᜐ")  # bstack1lll11l1l11_opy_
            hook_data[bstack1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬᜑ")] = [{bstack1l_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨᜒ"): [bstack1l_opy_ (u"࠭ࡳࡰ࡯ࡨࠤࡪࡸࡲࡰࡴࠪᜓ")]}]
    if bstack1lll11llll1_opy_:
        hook_data[bstack1l_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺ᜔ࠧ")] = bstack1lll11llll1_opy_.result
        hook_data[bstack1l_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴ᜕ࠩ")] = bstack11l1111lll_opy_(bstack1l111l11l1_opy_[bstack1l_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭᜖")], bstack1l111l11l1_opy_[bstack1l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ᜗")])
        hook_data[bstack1l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ᜘")] = bstack1l111l11l1_opy_[bstack1l_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ᜙")]
        if hook_data[bstack1l_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭᜚")] == bstack1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ᜛"):
            hook_data[bstack1l_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧ᜜")] = bstack1llll1111l_opy_.bstack11ll1l1l1l_opy_(bstack1lll11llll1_opy_.exception_type)
            hook_data[bstack1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪ᜝")] = [{bstack1l_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭᜞"): bstack11l111111l_opy_(bstack1lll11llll1_opy_.exception)}]
    return hook_data
def bstack1lll1l1lll1_opy_(test, bstack1l11111111_opy_, bstack11lllllll_opy_, result=None, call=None, outcome=None):
    bstack1l111l1l1l_opy_ = bstack1lll11l111l_opy_(test, bstack1l11111111_opy_, result, call, bstack11lllllll_opy_, outcome)
    driver = getattr(test, bstack1l_opy_ (u"ࠫࡤࡪࡲࡪࡸࡨࡶࠬᜟ"), None)
    if bstack11lllllll_opy_ == bstack1l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ᜠ") and driver:
        bstack1l111l1l1l_opy_[bstack1l_opy_ (u"࠭ࡩ࡯ࡶࡨ࡫ࡷࡧࡴࡪࡱࡱࡷࠬᜡ")] = bstack1llll1111l_opy_.bstack1l111l1111_opy_(driver)
    if bstack11lllllll_opy_ == bstack1l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨᜢ"):
        bstack11lllllll_opy_ = bstack1l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪᜣ")
    bstack1l11l111l1_opy_ = {
        bstack1l_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭ᜤ"): bstack11lllllll_opy_,
        bstack1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬᜥ"): bstack1l111l1l1l_opy_
    }
    bstack1llll1111l_opy_.bstack1l111lll11_opy_(bstack1l11l111l1_opy_)
def bstack1lll1l1l111_opy_(test, bstack1l11111111_opy_, bstack11lllllll_opy_, result=None, call=None, outcome=None, bstack1lll11llll1_opy_=None):
    hook_data = bstack1lll11ll1ll_opy_(test, bstack1l11111111_opy_, bstack11lllllll_opy_, result, call, outcome, bstack1lll11llll1_opy_)
    bstack1l11l111l1_opy_ = {
        bstack1l_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨᜦ"): bstack11lllllll_opy_,
        bstack1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴࠧᜧ"): hook_data
    }
    bstack1llll1111l_opy_.bstack1l111lll11_opy_(bstack1l11l111l1_opy_)
def bstack11llll1lll_opy_(bstack1l11111111_opy_):
    if not bstack1l11111111_opy_:
        return None
    if bstack1l11111111_opy_.get(bstack1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩᜨ"), None):
        return getattr(bstack1l11111111_opy_[bstack1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪᜩ")], bstack1l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᜪ"), None)
    return bstack1l11111111_opy_.get(bstack1l_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᜫ"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    yield
    try:
        if not bstack1llll1111l_opy_.on():
            return
        places = [bstack1l_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩᜬ"), bstack1l_opy_ (u"ࠫࡨࡧ࡬࡭ࠩᜭ"), bstack1l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧᜮ")]
        bstack11lll1llll_opy_ = []
        for bstack1lll11lllll_opy_ in places:
            records = caplog.get_records(bstack1lll11lllll_opy_)
            bstack1lll1l11l11_opy_ = bstack1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᜯ") if bstack1lll11lllll_opy_ == bstack1l_opy_ (u"ࠧࡤࡣ࡯ࡰࠬᜰ") else bstack1l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᜱ")
            bstack1lll1l1llll_opy_ = request.node.nodeid + (bstack1l_opy_ (u"ࠩࠪᜲ") if bstack1lll11lllll_opy_ == bstack1l_opy_ (u"ࠪࡧࡦࡲ࡬ࠨᜳ") else bstack1l_opy_ (u"ࠫ࠲᜴࠭") + bstack1lll11lllll_opy_)
            bstack1lll11l1ll1_opy_ = bstack11llll1lll_opy_(_1l111l111l_opy_.get(bstack1lll1l1llll_opy_, None))
            if not bstack1lll11l1ll1_opy_:
                continue
            for record in records:
                if bstack11l11l1lll_opy_(record.message):
                    continue
                bstack11lll1llll_opy_.append({
                    bstack1l_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ᜵"): datetime.datetime.utcfromtimestamp(record.created).isoformat() + bstack1l_opy_ (u"࡚࠭ࠨ᜶"),
                    bstack1l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭᜷"): record.levelname,
                    bstack1l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ᜸"): record.message,
                    bstack1lll1l11l11_opy_: bstack1lll11l1ll1_opy_
                })
        if len(bstack11lll1llll_opy_) > 0:
            bstack1llll1111l_opy_.bstack1ll1l1lll_opy_(bstack11lll1llll_opy_)
    except Exception as err:
        print(bstack1l_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡨࡧࡴࡴࡤࡠࡨ࡬ࡼࡹࡻࡲࡦ࠼ࠣࡿࢂ࠭᜹"), str(err))
def bstack1l1l1l1l_opy_(sequence, driver_command, response=None, driver = None, args = None):
    global bstack1l1l11l1l1_opy_
    bstack1ll1ll1ll_opy_ = bstack11lll11ll_opy_(threading.current_thread(), bstack1l_opy_ (u"ࠪ࡭ࡸࡇ࠱࠲ࡻࡗࡩࡸࡺࠧ᜺"), None) and bstack11lll11ll_opy_(
            threading.current_thread(), bstack1l_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ᜻"), None)
    bstack11l111ll1_opy_ = getattr(driver, bstack1l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡆ࠷࠱ࡺࡕ࡫ࡳࡺࡲࡤࡔࡥࡤࡲࠬ᜼"), None) != None and getattr(driver, bstack1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࡖ࡬ࡴࡻ࡬ࡥࡕࡦࡥࡳ࠭᜽"), None) == True
    if sequence == bstack1l_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫ࠧ᜾") and driver != None:
      if not bstack1l1l11l1l1_opy_ and bstack111lll111l_opy_() and bstack1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ᜿") in CONFIG and CONFIG[bstack1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᝀ")] == True and bstack1lll11111_opy_.bstack1l11ll1l1l_opy_(driver_command) and (bstack11l111ll1_opy_ or bstack1ll1ll1ll_opy_) and not bstack1lll1ll1l1_opy_(args):
        try:
          bstack1l1l11l1l1_opy_ = True
          logger.debug(bstack1l_opy_ (u"ࠪࡔࡪࡸࡦࡰࡴࡰ࡭ࡳ࡭ࠠࡴࡥࡤࡲࠥ࡬࡯ࡳࠢࡾࢁࠬᝁ").format(driver_command))
          logger.debug(perform_scan(driver, driver_command=driver_command))
        except Exception as err:
          logger.debug(bstack1l_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡱࡧࡵࡪࡴࡸ࡭ࠡࡵࡦࡥࡳࠦࡻࡾࠩᝂ").format(str(err)))
        bstack1l1l11l1l1_opy_ = False
    if sequence == bstack1l_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫᝃ"):
        if driver_command == bstack1l_opy_ (u"࠭ࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠪᝄ"):
            bstack1llll1111l_opy_.bstack11l1lll11_opy_({
                bstack1l_opy_ (u"ࠧࡪ࡯ࡤ࡫ࡪ࠭ᝅ"): response[bstack1l_opy_ (u"ࠨࡸࡤࡰࡺ࡫ࠧᝆ")],
                bstack1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᝇ"): store[bstack1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧᝈ")]
            })
def bstack1l1l111l1l_opy_():
    global bstack1l11l111l_opy_
    bstack1lll1ll1ll_opy_.bstack1l11lll1l1_opy_()
    logging.shutdown()
    bstack1llll1111l_opy_.bstack11lll1l1ll_opy_()
    for driver in bstack1l11l111l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1lll1ll11ll_opy_(*args):
    global bstack1l11l111l_opy_
    bstack1llll1111l_opy_.bstack11lll1l1ll_opy_()
    for driver in bstack1l11l111l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1llllll11l_opy_(self, *args, **kwargs):
    bstack1l11lllll_opy_ = bstack1l1ll1l1l_opy_(self, *args, **kwargs)
    bstack1llll1111l_opy_.bstack11l1lll1_opy_(self)
    return bstack1l11lllll_opy_
def bstack11111111_opy_(framework_name):
    global bstack11l1lllll_opy_
    global bstack1l1l1111l_opy_
    bstack11l1lllll_opy_ = framework_name
    logger.info(bstack11l11l11l_opy_.format(bstack11l1lllll_opy_.split(bstack1l_opy_ (u"ࠫ࠲࠭ᝉ"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack111lll111l_opy_():
            Service.start = bstack11l1l11l1_opy_
            Service.stop = bstack1l1l11l11_opy_
            webdriver.Remote.__init__ = bstack1ll1l1l1_opy_
            webdriver.Remote.get = bstack1l1ll1llll_opy_
            if not isinstance(os.getenv(bstack1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕ࡟ࡔࡆࡕࡗࡣࡕࡇࡒࡂࡎࡏࡉࡑ࠭ᝊ")), str):
                return
            WebDriver.close = bstack11l11ll11_opy_
            WebDriver.quit = bstack11l11l111_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.get_accessibility_results = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
        if not bstack111lll111l_opy_() and bstack1llll1111l_opy_.on():
            webdriver.Remote.__init__ = bstack1llllll11l_opy_
        bstack1l1l1111l_opy_ = True
    except Exception as e:
        pass
    bstack1ll1lll1l_opy_()
    if os.environ.get(bstack1l_opy_ (u"࠭ࡓࡆࡎࡈࡒࡎ࡛ࡍࡠࡑࡕࡣࡕࡒࡁ࡚࡙ࡕࡍࡌࡎࡔࡠࡋࡑࡗ࡙ࡇࡌࡍࡇࡇࠫᝋ")):
        bstack1l1l1111l_opy_ = eval(os.environ.get(bstack1l_opy_ (u"ࠧࡔࡇࡏࡉࡓࡏࡕࡎࡡࡒࡖࡤࡖࡌࡂ࡛࡚ࡖࡎࡍࡈࡕࡡࡌࡒࡘ࡚ࡁࡍࡎࡈࡈࠬᝌ")))
    if not bstack1l1l1111l_opy_:
        bstack1lllll11ll_opy_(bstack1l_opy_ (u"ࠣࡒࡤࡧࡰࡧࡧࡦࡵࠣࡲࡴࡺࠠࡪࡰࡶࡸࡦࡲ࡬ࡦࡦࠥᝍ"), bstack11ll11l11_opy_)
    if bstack1l11ll11ll_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            RemoteConnection._get_proxy_url = bstack1lll11l11l_opy_
        except Exception as e:
            logger.error(bstack1l1llllll1_opy_.format(str(e)))
    if bstack1l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩᝎ") in str(framework_name).lower():
        if not bstack111lll111l_opy_():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack1l1llll1_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack1lllll111l_opy_
            Config.getoption = bstack1lllll111_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack1lll11lll_opy_
        except Exception as e:
            pass
def bstack11l11l111_opy_(self):
    global bstack11l1lllll_opy_
    global bstack1ll11l1l_opy_
    global bstack1l11l1l11l_opy_
    try:
        if bstack1l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪᝏ") in bstack11l1lllll_opy_ and self.session_id != None and bstack11lll11ll_opy_(threading.current_thread(), bstack1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡕࡷࡥࡹࡻࡳࠨᝐ"), bstack1l_opy_ (u"ࠬ࠭ᝑ")) != bstack1l_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧᝒ"):
            bstack1ll111ll1_opy_ = bstack1l_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᝓ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ᝔")
            bstack11ll111l_opy_(logger, True)
            if self != None:
                bstack1lll1l11ll_opy_(self, bstack1ll111ll1_opy_, bstack1l_opy_ (u"ࠩ࠯ࠤࠬ᝕").join(threading.current_thread().bstackTestErrorMessages))
        item = store.get(bstack1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧ᝖"), None)
        if item is not None and bstack1lll1l1l1l1_opy_:
            bstack1lll1l1l11_opy_.bstack1ll111l111_opy_(self, bstack1lllllllll_opy_, logger, item)
        threading.current_thread().testStatus = bstack1l_opy_ (u"ࠫࠬ᝗")
    except Exception as e:
        logger.debug(bstack1l_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡱࡦࡸ࡫ࡪࡰࡪࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࠨ᝘") + str(e))
    bstack1l11l1l11l_opy_(self)
    self.session_id = None
def bstack1ll1l1l1_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack1ll11l1l_opy_
    global bstack1ll1l1l1l_opy_
    global bstack1llll1ll1l_opy_
    global bstack11l1lllll_opy_
    global bstack1l1ll1l1l_opy_
    global bstack1l11l111l_opy_
    global bstack1l1ll1l1ll_opy_
    global bstack11l111ll_opy_
    global bstack1lll1l1l1l1_opy_
    global bstack1lllllllll_opy_
    CONFIG[bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨ᝙")] = str(bstack11l1lllll_opy_) + str(__version__)
    command_executor = bstack11l11lll1_opy_(bstack1l1ll1l1ll_opy_)
    logger.debug(bstack11ll11ll1_opy_.format(command_executor))
    proxy = bstack1l1lll11l_opy_(CONFIG, proxy)
    bstack1ll1l1lll1_opy_ = 0
    try:
        if bstack1llll1ll1l_opy_ is True:
            bstack1ll1l1lll1_opy_ = int(os.environ.get(bstack1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧ᝚")))
    except:
        bstack1ll1l1lll1_opy_ = 0
    bstack11l1l11l_opy_ = bstack1l11llll_opy_(CONFIG, bstack1ll1l1lll1_opy_)
    logger.debug(bstack1ll1llll_opy_.format(str(bstack11l1l11l_opy_)))
    bstack1lllllllll_opy_ = CONFIG.get(bstack1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ᝛"))[bstack1ll1l1lll1_opy_]
    if bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭᝜") in CONFIG and CONFIG[bstack1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ᝝")]:
        bstack1111l1111_opy_(bstack11l1l11l_opy_, bstack11l111ll_opy_)
    if bstack1ll1l11l1l_opy_.bstack1ll1ll11_opy_(CONFIG, bstack1ll1l1lll1_opy_) and bstack1ll1l11l1l_opy_.bstack11ll1l111_opy_(bstack11l1l11l_opy_, options):
        bstack1lll1l1l1l1_opy_ = True
        bstack1ll1l11l1l_opy_.set_capabilities(bstack11l1l11l_opy_, CONFIG)
    if desired_capabilities:
        bstack1l1l1l1l11_opy_ = bstack1ll11l1l11_opy_(desired_capabilities)
        bstack1l1l1l1l11_opy_[bstack1l_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫ᝞")] = bstack1l1l1llll1_opy_(CONFIG)
        bstack1lll1l1l_opy_ = bstack1l11llll_opy_(bstack1l1l1l1l11_opy_)
        if bstack1lll1l1l_opy_:
            bstack11l1l11l_opy_ = update(bstack1lll1l1l_opy_, bstack11l1l11l_opy_)
        desired_capabilities = None
    if options:
        bstack1l1ll111l_opy_(options, bstack11l1l11l_opy_)
    if not options:
        options = bstack1l1l11l1ll_opy_(bstack11l1l11l_opy_)
    if proxy and bstack1ll1ll1l1_opy_() >= version.parse(bstack1l_opy_ (u"ࠬ࠺࠮࠲࠲࠱࠴ࠬ᝟")):
        options.proxy(proxy)
    if options and bstack1ll1ll1l1_opy_() >= version.parse(bstack1l_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬᝠ")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack1ll1ll1l1_opy_() < version.parse(bstack1l_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭ᝡ")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack11l1l11l_opy_)
    logger.info(bstack1ll1ll11l_opy_)
    if bstack1ll1ll1l1_opy_() >= version.parse(bstack1l_opy_ (u"ࠨ࠶࠱࠵࠵࠴࠰ࠨᝢ")):
        bstack1l1ll1l1l_opy_(self, command_executor=command_executor,
                  options=options, keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1ll1ll1l1_opy_() >= version.parse(bstack1l_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨᝣ")):
        bstack1l1ll1l1l_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities, options=options,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1ll1ll1l1_opy_() >= version.parse(bstack1l_opy_ (u"ࠪ࠶࠳࠻࠳࠯࠲ࠪᝤ")):
        bstack1l1ll1l1l_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    else:
        bstack1l1ll1l1l_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive)
    try:
        bstack1lllll11l_opy_ = bstack1l_opy_ (u"ࠫࠬᝥ")
        if bstack1ll1ll1l1_opy_() >= version.parse(bstack1l_opy_ (u"ࠬ࠺࠮࠱࠰࠳ࡦ࠶࠭ᝦ")):
            bstack1lllll11l_opy_ = self.caps.get(bstack1l_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡱࡦࡲࡈࡶࡤࡘࡶࡱࠨᝧ"))
        else:
            bstack1lllll11l_opy_ = self.capabilities.get(bstack1l_opy_ (u"ࠢࡰࡲࡷ࡭ࡲࡧ࡬ࡉࡷࡥ࡙ࡷࡲࠢᝨ"))
        if bstack1lllll11l_opy_:
            bstack1ll1l11lll_opy_(bstack1lllll11l_opy_)
            if bstack1ll1ll1l1_opy_() <= version.parse(bstack1l_opy_ (u"ࠨ࠵࠱࠵࠸࠴࠰ࠨᝩ")):
                self.command_executor._url = bstack1l_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥᝪ") + bstack1l1ll1l1ll_opy_ + bstack1l_opy_ (u"ࠥ࠾࠽࠶࠯ࡸࡦ࠲࡬ࡺࡨࠢᝫ")
            else:
                self.command_executor._url = bstack1l_opy_ (u"ࠦ࡭ࡺࡴࡱࡵ࠽࠳࠴ࠨᝬ") + bstack1lllll11l_opy_ + bstack1l_opy_ (u"ࠧ࠵ࡷࡥ࠱࡫ࡹࡧࠨ᝭")
            logger.debug(bstack1lll11l1_opy_.format(bstack1lllll11l_opy_))
        else:
            logger.debug(bstack1l1l1ll11l_opy_.format(bstack1l_opy_ (u"ࠨࡏࡱࡶ࡬ࡱࡦࡲࠠࡉࡷࡥࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠢᝮ")))
    except Exception as e:
        logger.debug(bstack1l1l1ll11l_opy_.format(e))
    bstack1ll11l1l_opy_ = self.session_id
    if bstack1l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧᝯ") in bstack11l1lllll_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        item = store.get(bstack1l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬᝰ"), None)
        if item:
            bstack1lll11ll11l_opy_ = getattr(item, bstack1l_opy_ (u"ࠩࡢࡸࡪࡹࡴࡠࡥࡤࡷࡪࡥࡳࡵࡣࡵࡸࡪࡪࠧ᝱"), False)
            if not getattr(item, bstack1l_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫᝲ"), None) and bstack1lll11ll11l_opy_:
                setattr(store[bstack1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨᝳ")], bstack1l_opy_ (u"ࠬࡥࡤࡳ࡫ࡹࡩࡷ࠭᝴"), self)
        bstack1llll1111l_opy_.bstack11l1lll1_opy_(self)
    bstack1l11l111l_opy_.append(self)
    if bstack1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ᝵") in CONFIG and bstack1l_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ᝶") in CONFIG[bstack1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ᝷")][bstack1ll1l1lll1_opy_]:
        bstack1ll1l1l1l_opy_ = CONFIG[bstack1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ᝸")][bstack1ll1l1lll1_opy_][bstack1l_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ᝹")]
    logger.debug(bstack1l1l111l1_opy_.format(bstack1ll11l1l_opy_))
def bstack1l1ll1llll_opy_(self, url):
    global bstack1l1llllll_opy_
    global CONFIG
    try:
        bstack11l1ll111_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack1l1ll111_opy_.format(str(err)))
    try:
        bstack1l1llllll_opy_(self, url)
    except Exception as e:
        try:
            bstack11lll1l1l_opy_ = str(e)
            if any(err_msg in bstack11lll1l1l_opy_ for err_msg in bstack1ll1lllll1_opy_):
                bstack11l1ll111_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack1l1ll111_opy_.format(str(err)))
        raise e
def bstack111l11l11_opy_(item, when):
    global bstack111l11ll1_opy_
    try:
        bstack111l11ll1_opy_(item, when)
    except Exception as e:
        pass
def bstack1lll11lll_opy_(item, call, rep):
    global bstack1llll11l1l_opy_
    global bstack1l11l111l_opy_
    name = bstack1l_opy_ (u"ࠫࠬ᝺")
    try:
        if rep.when == bstack1l_opy_ (u"ࠬࡩࡡ࡭࡮ࠪ᝻"):
            bstack1ll11l1l_opy_ = threading.current_thread().bstackSessionId
            bstack1lll1ll11l1_opy_ = item.config.getoption(bstack1l_opy_ (u"࠭ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ᝼"))
            try:
                if (str(bstack1lll1ll11l1_opy_).lower() != bstack1l_opy_ (u"ࠧࡵࡴࡸࡩࠬ᝽")):
                    name = str(rep.nodeid)
                    bstack11l1l1l11_opy_ = bstack1lllllll1l_opy_(bstack1l_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ᝾"), name, bstack1l_opy_ (u"ࠩࠪ᝿"), bstack1l_opy_ (u"ࠪࠫក"), bstack1l_opy_ (u"ࠫࠬខ"), bstack1l_opy_ (u"ࠬ࠭គ"))
                    os.environ[bstack1l_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙ࡥࡔࡆࡕࡗࡣࡓࡇࡍࡆࠩឃ")] = name
                    for driver in bstack1l11l111l_opy_:
                        if bstack1ll11l1l_opy_ == driver.session_id:
                            driver.execute_script(bstack11l1l1l11_opy_)
            except Exception as e:
                logger.debug(bstack1l_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠡࡨࡲࡶࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡶࡩࡸࡹࡩࡰࡰ࠽ࠤࢀࢃࠧង").format(str(e)))
            try:
                bstack1ll111111l_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack1l_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩច"):
                    status = bstack1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩឆ") if rep.outcome.lower() == bstack1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪជ") else bstack1l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫឈ")
                    reason = bstack1l_opy_ (u"ࠬ࠭ញ")
                    if status == bstack1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ដ"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack1l_opy_ (u"ࠧࡪࡰࡩࡳࠬឋ") if status == bstack1l_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨឌ") else bstack1l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨឍ")
                    data = name + bstack1l_opy_ (u"ࠪࠤࡵࡧࡳࡴࡧࡧࠥࠬណ") if status == bstack1l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫត") else name + bstack1l_opy_ (u"ࠬࠦࡦࡢ࡫࡯ࡩࡩࠧࠠࠨថ") + reason
                    bstack1111lll1l_opy_ = bstack1lllllll1l_opy_(bstack1l_opy_ (u"࠭ࡡ࡯ࡰࡲࡸࡦࡺࡥࠨទ"), bstack1l_opy_ (u"ࠧࠨធ"), bstack1l_opy_ (u"ࠨࠩន"), bstack1l_opy_ (u"ࠩࠪប"), level, data)
                    for driver in bstack1l11l111l_opy_:
                        if bstack1ll11l1l_opy_ == driver.session_id:
                            driver.execute_script(bstack1111lll1l_opy_)
            except Exception as e:
                logger.debug(bstack1l_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡤࡱࡱࡸࡪࡾࡴࠡࡨࡲࡶࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡶࡩࡸࡹࡩࡰࡰ࠽ࠤࢀࢃࠧផ").format(str(e)))
    except Exception as e:
        logger.debug(bstack1l_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡶࡤࡸࡪࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡦࡵࡷࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࢁࡽࠨព").format(str(e)))
    bstack1llll11l1l_opy_(item, call, rep)
notset = Notset()
def bstack1lllll111_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack1ll11l111_opy_
    if str(name).lower() == bstack1l_opy_ (u"ࠬࡪࡲࡪࡸࡨࡶࠬភ"):
        return bstack1l_opy_ (u"ࠨࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠧម")
    else:
        return bstack1ll11l111_opy_(self, name, default, skip)
def bstack1lll11l11l_opy_(self):
    global CONFIG
    global bstack1l11l11l_opy_
    try:
        proxy = bstack1l1ll1lll1_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack1l_opy_ (u"ࠧ࠯ࡲࡤࡧࠬយ")):
                proxies = bstack1l11ll1l1_opy_(proxy, bstack11l11lll1_opy_())
                if len(proxies) > 0:
                    protocol, bstack1111l111_opy_ = proxies.popitem()
                    if bstack1l_opy_ (u"ࠣ࠼࠲࠳ࠧរ") in bstack1111l111_opy_:
                        return bstack1111l111_opy_
                    else:
                        return bstack1l_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥល") + bstack1111l111_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack1l_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡰࡳࡱࡻࡽࠥࡻࡲ࡭ࠢ࠽ࠤࢀࢃࠢវ").format(str(e)))
    return bstack1l11l11l_opy_(self)
def bstack1l11ll11ll_opy_():
    return (bstack1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧឝ") in CONFIG or bstack1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩឞ") in CONFIG) and bstack1111lllll_opy_() and bstack1ll1ll1l1_opy_() >= version.parse(
        bstack1lll1lll_opy_)
def bstack1llll1l11_opy_(self,
               executablePath=None,
               channel=None,
               args=None,
               ignoreDefaultArgs=None,
               handleSIGINT=None,
               handleSIGTERM=None,
               handleSIGHUP=None,
               timeout=None,
               env=None,
               headless=None,
               devtools=None,
               proxy=None,
               downloadsPath=None,
               slowMo=None,
               tracesDir=None,
               chromiumSandbox=None,
               firefoxUserPrefs=None
               ):
    global CONFIG
    global bstack1ll1l1l1l_opy_
    global bstack1llll1ll1l_opy_
    global bstack11l1lllll_opy_
    CONFIG[bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨស")] = str(bstack11l1lllll_opy_) + str(__version__)
    bstack1ll1l1lll1_opy_ = 0
    try:
        if bstack1llll1ll1l_opy_ is True:
            bstack1ll1l1lll1_opy_ = int(os.environ.get(bstack1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧហ")))
    except:
        bstack1ll1l1lll1_opy_ = 0
    CONFIG[bstack1l_opy_ (u"ࠣ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢឡ")] = True
    bstack11l1l11l_opy_ = bstack1l11llll_opy_(CONFIG, bstack1ll1l1lll1_opy_)
    logger.debug(bstack1ll1llll_opy_.format(str(bstack11l1l11l_opy_)))
    if CONFIG.get(bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭អ")):
        bstack1111l1111_opy_(bstack11l1l11l_opy_, bstack11l111ll_opy_)
    if bstack1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ឣ") in CONFIG and bstack1l_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩឤ") in CONFIG[bstack1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨឥ")][bstack1ll1l1lll1_opy_]:
        bstack1ll1l1l1l_opy_ = CONFIG[bstack1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩឦ")][bstack1ll1l1lll1_opy_][bstack1l_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬឧ")]
    import urllib
    import json
    bstack11l11111l_opy_ = bstack1l_opy_ (u"ࠨࡹࡶࡷ࠿࠵࠯ࡤࡦࡳ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࡃࡨࡧࡰࡴ࠿ࠪឨ") + urllib.parse.quote(json.dumps(bstack11l1l11l_opy_))
    browser = self.connect(bstack11l11111l_opy_)
    return browser
def bstack1ll1lll1l_opy_():
    global bstack1l1l1111l_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        BrowserType.launch = bstack1llll1l11_opy_
        bstack1l1l1111l_opy_ = True
    except Exception as e:
        pass
def bstack1lll1l111ll_opy_():
    global CONFIG
    global bstack11l1llll_opy_
    global bstack1l1ll1l1ll_opy_
    global bstack11l111ll_opy_
    global bstack1llll1ll1l_opy_
    global bstack11ll1lll_opy_
    CONFIG = json.loads(os.environ.get(bstack1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡒࡒࡋࡏࡇࠨឩ")))
    bstack11l1llll_opy_ = eval(os.environ.get(bstack1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫឪ")))
    bstack1l1ll1l1ll_opy_ = os.environ.get(bstack1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡌ࡚ࡈ࡟ࡖࡔࡏࠫឫ"))
    bstack1l1l111lll_opy_(CONFIG, bstack11l1llll_opy_)
    bstack11ll1lll_opy_ = bstack1lll1ll1ll_opy_.bstack11l1l11ll_opy_(CONFIG, bstack11ll1lll_opy_)
    global bstack1l1ll1l1l_opy_
    global bstack1l11l1l11l_opy_
    global bstack1ll11ll11l_opy_
    global bstack1l11ll1ll1_opy_
    global bstack11l1ll11_opy_
    global bstack1ll111ll_opy_
    global bstack1l1l11lll_opy_
    global bstack1l1llllll_opy_
    global bstack1l11l11l_opy_
    global bstack1ll11l111_opy_
    global bstack111l11ll1_opy_
    global bstack1llll11l1l_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack1l1ll1l1l_opy_ = webdriver.Remote.__init__
        bstack1l11l1l11l_opy_ = WebDriver.quit
        bstack1l1l11lll_opy_ = WebDriver.close
        bstack1l1llllll_opy_ = WebDriver.get
    except Exception as e:
        pass
    if (bstack1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨឬ") in CONFIG or bstack1l_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪឭ") in CONFIG) and bstack1111lllll_opy_():
        if bstack1ll1ll1l1_opy_() < version.parse(bstack1lll1lll_opy_):
            logger.error(bstack1l111ll11_opy_.format(bstack1ll1ll1l1_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                bstack1l11l11l_opy_ = RemoteConnection._get_proxy_url
            except Exception as e:
                logger.error(bstack1l1llllll1_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack1ll11l111_opy_ = Config.getoption
        from _pytest import runner
        bstack111l11ll1_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warn(e, bstack1l1lll1l1l_opy_)
    try:
        from pytest_bdd import reporting
        bstack1llll11l1l_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstack1l_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺ࡯ࠡࡴࡸࡲࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡩࡸࡺࡳࠨឮ"))
    bstack11l111ll_opy_ = CONFIG.get(bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬឯ"), {}).get(bstack1l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫឰ"))
    bstack1llll1ll1l_opy_ = True
    bstack11111111_opy_(bstack1l1llll111_opy_)
if (bstack111lll1lll_opy_()):
    bstack1lll1l111ll_opy_()
@bstack11llll1l11_opy_(class_method=False)
def bstack1lll1l11l1l_opy_(hook_name, event, bstack1lll11ll111_opy_=None):
    if hook_name not in [bstack1l_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡩࡹࡳࡩࡴࡪࡱࡱࠫឱ"), bstack1l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨឲ"), bstack1l_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠫឳ"), bstack1l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠨ឴"), bstack1l_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡣ࡭ࡣࡶࡷࠬ឵"), bstack1l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠩា"), bstack1l_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡨࡸ࡭ࡵࡤࠨិ"), bstack1l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨࠬី")]:
        return
    node = store[bstack1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨឹ")]
    if hook_name in [bstack1l_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠫឺ"), bstack1l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡲࡨࡺࡲࡥࠨុ")]:
        node = store[bstack1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠ࡯ࡲࡨࡺࡲࡥࡠ࡫ࡷࡩࡲ࠭ូ")]
    elif hook_name in [bstack1l_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡤ࡮ࡤࡷࡸ࠭ួ"), bstack1l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡨࡲࡡࡴࡵࠪើ")]:
        node = store[bstack1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡨࡲࡡࡴࡵࡢ࡭ࡹ࡫࡭ࠨឿ")]
    if event == bstack1l_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࠫៀ"):
        hook_type = bstack1lllllll1l1_opy_(hook_name)
        uuid = uuid4().__str__()
        bstack1l111l11l1_opy_ = {
            bstack1l_opy_ (u"ࠬࡻࡵࡪࡦࠪេ"): uuid,
            bstack1l_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪែ"): bstack1l11lll111_opy_(),
            bstack1l_opy_ (u"ࠧࡵࡻࡳࡩࠬៃ"): bstack1l_opy_ (u"ࠨࡪࡲࡳࡰ࠭ោ"),
            bstack1l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬៅ"): hook_type,
            bstack1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡰࡤࡱࡪ࠭ំ"): hook_name
        }
        store[bstack1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨះ")].append(uuid)
        bstack1lll1ll1111_opy_ = node.nodeid
        if hook_type == bstack1l_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪៈ"):
            if not _1l111l111l_opy_.get(bstack1lll1ll1111_opy_, None):
                _1l111l111l_opy_[bstack1lll1ll1111_opy_] = {bstack1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ៉"): []}
            _1l111l111l_opy_[bstack1lll1ll1111_opy_][bstack1l_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭៊")].append(bstack1l111l11l1_opy_[bstack1l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭់")])
        _1l111l111l_opy_[bstack1lll1ll1111_opy_ + bstack1l_opy_ (u"ࠩ࠰ࠫ៌") + hook_name] = bstack1l111l11l1_opy_
        bstack1lll1l1l111_opy_(node, bstack1l111l11l1_opy_, bstack1l_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫ៍"))
    elif event == bstack1l_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪ៎"):
        bstack11llll11l1_opy_ = node.nodeid + bstack1l_opy_ (u"ࠬ࠳ࠧ៏") + hook_name
        _1l111l111l_opy_[bstack11llll11l1_opy_][bstack1l_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ័")] = bstack1l11lll111_opy_()
        bstack1lll11l1l1l_opy_(_1l111l111l_opy_[bstack11llll11l1_opy_][bstack1l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ៑")])
        bstack1lll1l1l111_opy_(node, _1l111l111l_opy_[bstack11llll11l1_opy_], bstack1l_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦ្ࠪ"), bstack1lll11llll1_opy_=bstack1lll11ll111_opy_)
def bstack1lll1ll111l_opy_():
    global bstack1lll11l11ll_opy_
    if bstack1lllll1111_opy_():
        bstack1lll11l11ll_opy_ = bstack1l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩ࠭៓")
    else:
        bstack1lll11l11ll_opy_ = bstack1l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ។")
@bstack1llll1111l_opy_.bstack1lll1lllll1_opy_
def bstack1lll11l11l1_opy_():
    bstack1lll1ll111l_opy_()
    if bstack1111lllll_opy_():
        bstack1l111l1l_opy_(bstack1l1l1l1l_opy_)
    bstack111ll1l111_opy_ = bstack111ll11l1l_opy_(bstack1lll1l11l1l_opy_)
bstack1lll11l11l1_opy_()