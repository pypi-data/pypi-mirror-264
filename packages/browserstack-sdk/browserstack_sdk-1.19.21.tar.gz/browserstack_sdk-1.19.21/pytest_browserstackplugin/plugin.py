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
from browserstack_sdk.__init__ import (bstack1l1lll1l_opy_, bstack111ll111l_opy_, update, bstack1111l11l1_opy_,
                                       bstack1ll1l1ll1l_opy_, bstack1l1ll11l_opy_, bstack1l1ll111l_opy_, bstack1lll111l1l_opy_,
                                       bstack11l11l111_opy_, bstack1lll1lll1_opy_, bstack1ll11llll_opy_, bstack111111l1_opy_,
                                       bstack11l111lll_opy_, getAccessibilityResults, getAccessibilityResultsSummary, perform_scan, bstack1ll11lll_opy_)
from browserstack_sdk.bstack11l11l1ll_opy_ import bstack1l1lll1lll_opy_
from browserstack_sdk._version import __version__
from bstack_utils import bstack1ll1l1ll_opy_
from bstack_utils.capture import bstack11lll1l1l1_opy_
from bstack_utils.config import Config
from bstack_utils.constants import bstack1ll1l1ll11_opy_, bstack1llll11ll1_opy_, bstack1llllll1l_opy_, \
    bstack111l1llll_opy_
from bstack_utils.helper import bstack1lll11l111_opy_, bstack1l11l1llll_opy_, bstack11l1111111_opy_, bstack1l1l1llll_opy_, \
    bstack11l11ll11l_opy_, \
    bstack11l11l11ll_opy_, bstack111l11l1_opy_, bstack111l11lll_opy_, bstack11l11ll1l1_opy_, bstack1ll1l11l1_opy_, Notset, \
    bstack1ll111ll11_opy_, bstack11l11llll1_opy_, bstack111lllll1l_opy_, Result, bstack111lll11ll_opy_, bstack11l11l111l_opy_, bstack1l111l1111_opy_, \
    bstack111l111l_opy_, bstack1l1l111ll_opy_, bstack111ll1l11_opy_, bstack11l111l11l_opy_
from bstack_utils.bstack111ll111ll_opy_ import bstack111l1llll1_opy_
from bstack_utils.messages import bstack11l1ll1l1_opy_, bstack111l1l111_opy_, bstack1lll11l11_opy_, bstack1ll1111l1_opy_, bstack1lllll11ll_opy_, \
    bstack11ll11lll_opy_, bstack1l1ll1l11_opy_, bstack1111ll111_opy_, bstack1ll1l111_opy_, bstack1l1lllll1_opy_, \
    bstack11ll111l_opy_, bstack1lll111lll_opy_
from bstack_utils.proxy import bstack1ll1l11lll_opy_, bstack1lll1l11l_opy_
from bstack_utils.bstack1lll1l1l1_opy_ import bstack1llllll1l11_opy_, bstack1lllll1l1ll_opy_, bstack1llllll1l1l_opy_, bstack1lllllll111_opy_, \
    bstack1lllll1llll_opy_, bstack1lllll1ll1l_opy_, bstack1llllll1111_opy_, bstack111ll1111_opy_, bstack1llllll111l_opy_
from bstack_utils.bstack11ll11ll_opy_ import bstack11l11111l_opy_
from bstack_utils.bstack1l1l1ll11l_opy_ import bstack11l111l1l_opy_, bstack11lllll1_opy_, bstack1lllllll11_opy_, \
    bstack1ll11lll1l_opy_, bstack1l1l1111_opy_
from bstack_utils.bstack1l111l1l11_opy_ import bstack1l111lll11_opy_
from bstack_utils.bstack1llll1ll1l_opy_ import bstack1ll1ll111l_opy_
import bstack_utils.bstack1ll1ll11l_opy_ as bstack11lllll1l_opy_
from bstack_utils.bstack1lllll11l1_opy_ import bstack1lllll11l1_opy_
bstack1l1l1l1l11_opy_ = None
bstack111l11l1l_opy_ = None
bstack1lllll1lll_opy_ = None
bstack1l11llll11_opy_ = None
bstack1l11llllll_opy_ = None
bstack1ll1l11ll_opy_ = None
bstack1l1ll1l1l_opy_ = None
bstack1lll1ll1ll_opy_ = None
bstack11l1l1ll_opy_ = None
bstack11111l11l_opy_ = None
bstack111l1111_opy_ = None
bstack1llll111ll_opy_ = None
bstack1llll1ll1_opy_ = None
bstack1ll1llll_opy_ = bstack1llll1l_opy_ (u"࠭ࠧᗑ")
CONFIG = {}
bstack1l1l11111l_opy_ = False
bstack111lll1l_opy_ = bstack1llll1l_opy_ (u"ࠧࠨᗒ")
bstack11ll1ll11_opy_ = bstack1llll1l_opy_ (u"ࠨࠩᗓ")
bstack1ll11l111_opy_ = False
bstack1lll11l11l_opy_ = []
bstack1ll1l11l1l_opy_ = bstack1ll1l1ll11_opy_
bstack1lll111ll1l_opy_ = bstack1llll1l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩᗔ")
bstack1lll1l1l11l_opy_ = False
bstack1ll1lllll1_opy_ = {}
bstack1l1111ll_opy_ = False
logger = bstack1ll1l1ll_opy_.get_logger(__name__, bstack1ll1l11l1l_opy_)
store = {
    bstack1llll1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧᗕ"): []
}
bstack1lll1l1ll11_opy_ = False
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_1l111lllll_opy_ = {}
current_test_uuid = None
def bstack1l1l1lll1_opy_(page, bstack1l1l1lllll_opy_):
    try:
        page.evaluate(bstack1llll1l_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧᗖ"),
                      bstack1llll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠩᗗ") + json.dumps(
                          bstack1l1l1lllll_opy_) + bstack1llll1l_opy_ (u"ࠨࡽࡾࠤᗘ"))
    except Exception as e:
        print(bstack1llll1l_opy_ (u"ࠢࡦࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠢࡾࢁࠧᗙ"), e)
def bstack11111111l_opy_(page, message, level):
    try:
        page.evaluate(bstack1llll1l_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤᗚ"), bstack1llll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧᗛ") + json.dumps(
            message) + bstack1llll1l_opy_ (u"ࠪ࠰ࠧࡲࡥࡷࡧ࡯ࠦ࠿࠭ᗜ") + json.dumps(level) + bstack1llll1l_opy_ (u"ࠫࢂࢃࠧᗝ"))
    except Exception as e:
        print(bstack1llll1l_opy_ (u"ࠧ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡣࡱࡲࡴࡺࡡࡵ࡫ࡲࡲࠥࢁࡽࠣᗞ"), e)
def pytest_configure(config):
    bstack1l1lll1ll1_opy_ = Config.bstack11ll1ll1_opy_()
    config.args = bstack1ll1ll111l_opy_.bstack1lll1llll1l_opy_(config.args)
    bstack1l1lll1ll1_opy_.bstack1llll1lll1_opy_(bstack111ll1l11_opy_(config.getoption(bstack1llll1l_opy_ (u"࠭ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪᗟ"))))
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    bstack1lll11l1111_opy_ = item.config.getoption(bstack1llll1l_opy_ (u"ࠧࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩᗠ"))
    plugins = item.config.getoption(bstack1llll1l_opy_ (u"ࠣࡲ࡯ࡹ࡬࡯࡮ࡴࠤᗡ"))
    report = outcome.get_result()
    bstack1lll11l11ll_opy_(item, call, report)
    if bstack1llll1l_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵࡡࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡱ࡮ࡸ࡫࡮ࡴࠢᗢ") not in plugins or bstack1ll1l11l1_opy_():
        return
    summary = []
    driver = getattr(item, bstack1llll1l_opy_ (u"ࠥࡣࡩࡸࡩࡷࡧࡵࠦᗣ"), None)
    page = getattr(item, bstack1llll1l_opy_ (u"ࠦࡤࡶࡡࡨࡧࠥᗤ"), None)
    try:
        if (driver == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None):
        bstack1lll1l1l1ll_opy_(item, report, summary, bstack1lll11l1111_opy_)
    if (page is not None):
        bstack1lll11l1lll_opy_(item, report, summary, bstack1lll11l1111_opy_)
def bstack1lll1l1l1ll_opy_(item, report, summary, bstack1lll11l1111_opy_):
    if report.when == bstack1llll1l_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫᗥ") and report.skipped:
        bstack1llllll111l_opy_(report)
    if report.when in [bstack1llll1l_opy_ (u"ࠨࡳࡦࡶࡸࡴࠧᗦ"), bstack1llll1l_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࠤᗧ")]:
        return
    if not bstack11l1111111_opy_():
        return
    try:
        if (str(bstack1lll11l1111_opy_).lower() != bstack1llll1l_opy_ (u"ࠨࡶࡵࡹࡪ࠭ᗨ")):
            item._driver.execute_script(
                bstack1llll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿ࠦࠧᗩ") + json.dumps(
                    report.nodeid) + bstack1llll1l_opy_ (u"ࠪࢁࢂ࠭ᗪ"))
        os.environ[bstack1llll1l_opy_ (u"ࠫࡕ࡟ࡔࡆࡕࡗࡣ࡙ࡋࡓࡕࡡࡑࡅࡒࡋࠧᗫ")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack1llll1l_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡱࡦࡸ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫࠺ࠡࡽ࠳ࢁࠧᗬ").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1llll1l_opy_ (u"ࠨࡷࡢࡵࡻࡪࡦ࡯࡬ࠣᗭ")))
    bstack1l1l111lll_opy_ = bstack1llll1l_opy_ (u"ࠢࠣᗮ")
    bstack1llllll111l_opy_(report)
    if not passed:
        try:
            bstack1l1l111lll_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack1llll1l_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡤࡦࡶࡨࡶࡲ࡯࡮ࡦࠢࡩࡥ࡮ࡲࡵࡳࡧࠣࡶࡪࡧࡳࡰࡰ࠽ࠤࢀ࠶ࡽࠣᗯ").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack1l1l111lll_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack1llll1l_opy_ (u"ࠤࡺࡥࡸࡾࡦࡢ࡫࡯ࠦᗰ")))
        bstack1l1l111lll_opy_ = bstack1llll1l_opy_ (u"ࠥࠦᗱ")
        if not passed:
            try:
                bstack1l1l111lll_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1llll1l_opy_ (u"ࠦ࡜ࡇࡒࡏࡋࡑࡋ࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡧࡩࡹ࡫ࡲ࡮࡫ࡱࡩࠥ࡬ࡡࡪ࡮ࡸࡶࡪࠦࡲࡦࡣࡶࡳࡳࡀࠠࡼ࠲ࢀࠦᗲ").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack1l1l111lll_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack1llll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣ࡫ࡱࡪࡴࠨࠬࠡ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡦࡤࡸࡦࠨ࠺ࠡࠩᗳ")
                    + json.dumps(bstack1llll1l_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠧࠢᗴ"))
                    + bstack1llll1l_opy_ (u"ࠢ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿࠥᗵ")
                )
            else:
                item._driver.execute_script(
                    bstack1llll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦࡪࡸࡲࡰࡴࠥ࠰ࠥࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡪࡡࡵࡣࠥ࠾ࠥ࠭ᗶ")
                    + json.dumps(str(bstack1l1l111lll_opy_))
                    + bstack1llll1l_opy_ (u"ࠤ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࠧᗷ")
                )
        except Exception as e:
            summary.append(bstack1llll1l_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡣࡱࡲࡴࡺࡡࡵࡧ࠽ࠤࢀ࠶ࡽࠣᗸ").format(e))
def bstack1lll11ll11l_opy_(test_name, error_message):
    try:
        bstack1lll1l1lll1_opy_ = []
        bstack1l1l11l11_opy_ = os.environ.get(bstack1llll1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫᗹ"), bstack1llll1l_opy_ (u"ࠬ࠶ࠧᗺ"))
        bstack1l1llll111_opy_ = {bstack1llll1l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᗻ"): test_name, bstack1llll1l_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ᗼ"): error_message, bstack1llll1l_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧᗽ"): bstack1l1l11l11_opy_}
        bstack1lll11l1l1l_opy_ = os.path.join(tempfile.gettempdir(), bstack1llll1l_opy_ (u"ࠩࡳࡻࡤࡶࡹࡵࡧࡶࡸࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧᗾ"))
        if os.path.exists(bstack1lll11l1l1l_opy_):
            with open(bstack1lll11l1l1l_opy_) as f:
                bstack1lll1l1lll1_opy_ = json.load(f)
        bstack1lll1l1lll1_opy_.append(bstack1l1llll111_opy_)
        with open(bstack1lll11l1l1l_opy_, bstack1llll1l_opy_ (u"ࠪࡻࠬᗿ")) as f:
            json.dump(bstack1lll1l1lll1_opy_, f)
    except Exception as e:
        logger.debug(bstack1llll1l_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡰࡦࡴࡶ࡭ࡸࡺࡩ࡯ࡩࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡱࡻࡷࡩࡸࡺࠠࡦࡴࡵࡳࡷࡹ࠺ࠡࠩᘀ") + str(e))
def bstack1lll11l1lll_opy_(item, report, summary, bstack1lll11l1111_opy_):
    if report.when in [bstack1llll1l_opy_ (u"ࠧࡹࡥࡵࡷࡳࠦᘁ"), bstack1llll1l_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࠣᘂ")]:
        return
    if (str(bstack1lll11l1111_opy_).lower() != bstack1llll1l_opy_ (u"ࠧࡵࡴࡸࡩࠬᘃ")):
        bstack1l1l1lll1_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1llll1l_opy_ (u"ࠣࡹࡤࡷࡽ࡬ࡡࡪ࡮ࠥᘄ")))
    bstack1l1l111lll_opy_ = bstack1llll1l_opy_ (u"ࠤࠥᘅ")
    bstack1llllll111l_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack1l1l111lll_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1llll1l_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡦࡨࡸࡪࡸ࡭ࡪࡰࡨࠤ࡫ࡧࡩ࡭ࡷࡵࡩࠥࡸࡥࡢࡵࡲࡲ࠿ࠦࡻ࠱ࡿࠥᘆ").format(e)
                )
        try:
            if passed:
                bstack1l1l1111_opy_(getattr(item, bstack1llll1l_opy_ (u"ࠫࡤࡶࡡࡨࡧࠪᘇ"), None), bstack1llll1l_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧᘈ"))
            else:
                error_message = bstack1llll1l_opy_ (u"࠭ࠧᘉ")
                if bstack1l1l111lll_opy_:
                    bstack11111111l_opy_(item._page, str(bstack1l1l111lll_opy_), bstack1llll1l_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨᘊ"))
                    bstack1l1l1111_opy_(getattr(item, bstack1llll1l_opy_ (u"ࠨࡡࡳࡥ࡬࡫ࠧᘋ"), None), bstack1llll1l_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤᘌ"), str(bstack1l1l111lll_opy_))
                    error_message = str(bstack1l1l111lll_opy_)
                else:
                    bstack1l1l1111_opy_(getattr(item, bstack1llll1l_opy_ (u"ࠪࡣࡵࡧࡧࡦࠩᘍ"), None), bstack1llll1l_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦᘎ"))
                bstack1lll11ll11l_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack1llll1l_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡹࡵࡪࡡࡵࡧࠣࡷࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࢁ࠰ࡾࠤᘏ").format(e))
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
    parser.addoption(bstack1llll1l_opy_ (u"ࠨ࠭࠮ࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥᘐ"), default=bstack1llll1l_opy_ (u"ࠢࡇࡣ࡯ࡷࡪࠨᘑ"), help=bstack1llll1l_opy_ (u"ࠣࡃࡸࡸࡴࡳࡡࡵ࡫ࡦࠤࡸ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠢᘒ"))
    parser.addoption(bstack1llll1l_opy_ (u"ࠤ࠰࠱ࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠣᘓ"), default=bstack1llll1l_opy_ (u"ࠥࡊࡦࡲࡳࡦࠤᘔ"), help=bstack1llll1l_opy_ (u"ࠦࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡩࠠࡴࡧࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠥᘕ"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack1llll1l_opy_ (u"ࠧ࠳࠭ࡥࡴ࡬ࡺࡪࡸࠢᘖ"), action=bstack1llll1l_opy_ (u"ࠨࡳࡵࡱࡵࡩࠧᘗ"), default=bstack1llll1l_opy_ (u"ࠢࡤࡪࡵࡳࡲ࡫ࠢᘘ"),
                         help=bstack1llll1l_opy_ (u"ࠣࡆࡵ࡭ࡻ࡫ࡲࠡࡶࡲࠤࡷࡻ࡮ࠡࡶࡨࡷࡹࡹࠢᘙ"))
def bstack1l1111l1l1_opy_(log):
    if not (log[bstack1llll1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᘚ")] and log[bstack1llll1l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᘛ")].strip()):
        return
    active = bstack1l111ll111_opy_()
    log = {
        bstack1llll1l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪᘜ"): log[bstack1llll1l_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫᘝ")],
        bstack1llll1l_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩᘞ"): datetime.datetime.utcnow().isoformat() + bstack1llll1l_opy_ (u"࡛ࠧࠩᘟ"),
        bstack1llll1l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᘠ"): log[bstack1llll1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᘡ")],
    }
    if active:
        if active[bstack1llll1l_opy_ (u"ࠪࡸࡾࡶࡥࠨᘢ")] == bstack1llll1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩᘣ"):
            log[bstack1llll1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᘤ")] = active[bstack1llll1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᘥ")]
        elif active[bstack1llll1l_opy_ (u"ࠧࡵࡻࡳࡩࠬᘦ")] == bstack1llll1l_opy_ (u"ࠨࡶࡨࡷࡹ࠭ᘧ"):
            log[bstack1llll1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᘨ")] = active[bstack1llll1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᘩ")]
    bstack1ll1ll111l_opy_.bstack11ll1ll1l_opy_([log])
def bstack1l111ll111_opy_():
    if len(store[bstack1llll1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨᘪ")]) > 0 and store[bstack1llll1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩᘫ")][-1]:
        return {
            bstack1llll1l_opy_ (u"࠭ࡴࡺࡲࡨࠫᘬ"): bstack1llll1l_opy_ (u"ࠧࡩࡱࡲ࡯ࠬᘭ"),
            bstack1llll1l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᘮ"): store[bstack1llll1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ᘯ")][-1]
        }
    if store.get(bstack1llll1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧᘰ"), None):
        return {
            bstack1llll1l_opy_ (u"ࠫࡹࡿࡰࡦࠩᘱ"): bstack1llll1l_opy_ (u"ࠬࡺࡥࡴࡶࠪᘲ"),
            bstack1llll1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᘳ"): store[bstack1llll1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫᘴ")]
        }
    return None
bstack11llll1ll1_opy_ = bstack11lll1l1l1_opy_(bstack1l1111l1l1_opy_)
def pytest_runtest_call(item):
    try:
        global CONFIG
        global bstack1lll1l1l11l_opy_
        item._1lll1l11ll1_opy_ = True
        bstack11l1lll1l_opy_ = bstack11lllll1l_opy_.bstack11l1ll11_opy_(CONFIG, bstack11l11l11ll_opy_(item.own_markers))
        item._a11y_test_case = bstack11l1lll1l_opy_
        if bstack1lll1l1l11l_opy_:
            driver = getattr(item, bstack1llll1l_opy_ (u"ࠨࡡࡧࡶ࡮ࡼࡥࡳࠩᘵ"), None)
            item._a11y_started = bstack11lllll1l_opy_.bstack1l1l11l111_opy_(driver, bstack11l1lll1l_opy_)
        if not bstack1ll1ll111l_opy_.on() or bstack1lll111ll1l_opy_ != bstack1llll1l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩᘶ"):
            return
        global current_test_uuid, bstack11llll1ll1_opy_
        bstack11llll1ll1_opy_.start()
        bstack1l111lll1l_opy_ = {
            bstack1llll1l_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᘷ"): uuid4().__str__(),
            bstack1llll1l_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᘸ"): datetime.datetime.utcnow().isoformat() + bstack1llll1l_opy_ (u"ࠬࡠࠧᘹ")
        }
        current_test_uuid = bstack1l111lll1l_opy_[bstack1llll1l_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᘺ")]
        store[bstack1llll1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫᘻ")] = bstack1l111lll1l_opy_[bstack1llll1l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᘼ")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _1l111lllll_opy_[item.nodeid] = {**_1l111lllll_opy_[item.nodeid], **bstack1l111lll1l_opy_}
        bstack1lll1l11l1l_opy_(item, _1l111lllll_opy_[item.nodeid], bstack1llll1l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪᘽ"))
    except Exception as err:
        print(bstack1llll1l_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡵࡹࡳࡺࡥࡴࡶࡢࡧࡦࡲ࡬࠻ࠢࡾࢁࠬᘾ"), str(err))
def pytest_runtest_setup(item):
    global bstack1lll1l1ll11_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack11l11ll1l1_opy_():
        atexit.register(bstack1l1llll11l_opy_)
        if not bstack1lll1l1ll11_opy_:
            try:
                bstack1lll11llll1_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack11l111l11l_opy_():
                    bstack1lll11llll1_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack1lll11llll1_opy_:
                    signal.signal(s, bstack1lll11l1ll1_opy_)
                bstack1lll1l1ll11_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack1llll1l_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡲࡦࡩ࡬ࡷࡹ࡫ࡲࠡࡵ࡬࡫ࡳࡧ࡬ࠡࡪࡤࡲࡩࡲࡥࡳࡵ࠽ࠤࠧᘿ") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack1llllll1l11_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack1llll1l_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᙀ")
    try:
        if not bstack1ll1ll111l_opy_.on():
            return
        bstack11llll1ll1_opy_.start()
        uuid = uuid4().__str__()
        bstack1l111lll1l_opy_ = {
            bstack1llll1l_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᙁ"): uuid,
            bstack1llll1l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᙂ"): datetime.datetime.utcnow().isoformat() + bstack1llll1l_opy_ (u"ࠨ࡜ࠪᙃ"),
            bstack1llll1l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧᙄ"): bstack1llll1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨᙅ"),
            bstack1llll1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧᙆ"): bstack1llll1l_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪᙇ"),
            bstack1llll1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡳࡧ࡭ࡦࠩᙈ"): bstack1llll1l_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ᙉ")
        }
        threading.current_thread().current_hook_uuid = uuid
        threading.current_thread().current_test_item = item
        store[bstack1llll1l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬᙊ")] = item
        store[bstack1llll1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ᙋ")] = [uuid]
        if not _1l111lllll_opy_.get(item.nodeid, None):
            _1l111lllll_opy_[item.nodeid] = {bstack1llll1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩᙌ"): [], bstack1llll1l_opy_ (u"ࠫ࡫࡯ࡸࡵࡷࡵࡩࡸ࠭ᙍ"): []}
        _1l111lllll_opy_[item.nodeid][bstack1llll1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫᙎ")].append(bstack1l111lll1l_opy_[bstack1llll1l_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᙏ")])
        _1l111lllll_opy_[item.nodeid + bstack1llll1l_opy_ (u"ࠧ࠮ࡵࡨࡸࡺࡶࠧᙐ")] = bstack1l111lll1l_opy_
        bstack1lll11l11l1_opy_(item, bstack1l111lll1l_opy_, bstack1llll1l_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩᙑ"))
    except Exception as err:
        print(bstack1llll1l_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡴࡸࡲࡹ࡫ࡳࡵࡡࡶࡩࡹࡻࡰ࠻ࠢࡾࢁࠬᙒ"), str(err))
def pytest_runtest_teardown(item):
    try:
        global bstack1ll1lllll1_opy_
        if CONFIG.get(bstack1llll1l_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩᙓ"), False):
            if CONFIG.get(bstack1llll1l_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࡆࡥࡵࡺࡵࡳࡧࡐࡳࡩ࡫ࠧᙔ"), bstack1llll1l_opy_ (u"ࠧࡧࡵࡵࡱࠥᙕ")) == bstack1llll1l_opy_ (u"ࠨࡴࡦࡵࡷࡧࡦࡹࡥࠣᙖ"):
                bstack1lll1l1l1l1_opy_ = bstack1lll11l111_opy_(threading.current_thread(), bstack1llll1l_opy_ (u"ࠧࡱࡧࡵࡧࡾ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪᙗ"), None)
                bstack11lll111l_opy_ = bstack1lll1l1l1l1_opy_ + bstack1llll1l_opy_ (u"ࠣ࠯ࡷࡩࡸࡺࡣࡢࡵࡨࠦᙘ")
                driver = getattr(item, bstack1llll1l_opy_ (u"ࠩࡢࡨࡷ࡯ࡶࡦࡴࠪᙙ"), None)
                PercySDK.screenshot(driver, bstack11lll111l_opy_)
        if getattr(item, bstack1llll1l_opy_ (u"ࠪࡣࡦ࠷࠱ࡺࡡࡶࡸࡦࡸࡴࡦࡦࠪᙚ"), False):
            bstack1l1lll1lll_opy_.bstack11ll11111_opy_(getattr(item, bstack1llll1l_opy_ (u"ࠫࡤࡪࡲࡪࡸࡨࡶࠬᙛ"), None), bstack1ll1lllll1_opy_, logger, item)
        if not bstack1ll1ll111l_opy_.on():
            return
        bstack1l111lll1l_opy_ = {
            bstack1llll1l_opy_ (u"ࠬࡻࡵࡪࡦࠪᙜ"): uuid4().__str__(),
            bstack1llll1l_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᙝ"): datetime.datetime.utcnow().isoformat() + bstack1llll1l_opy_ (u"࡛ࠧࠩᙞ"),
            bstack1llll1l_opy_ (u"ࠨࡶࡼࡴࡪ࠭ᙟ"): bstack1llll1l_opy_ (u"ࠩ࡫ࡳࡴࡱࠧᙠ"),
            bstack1llll1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭ᙡ"): bstack1llll1l_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠨᙢ"),
            bstack1llll1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡲࡦࡳࡥࠨᙣ"): bstack1llll1l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨᙤ")
        }
        _1l111lllll_opy_[item.nodeid + bstack1llll1l_opy_ (u"ࠧ࠮ࡶࡨࡥࡷࡪ࡯ࡸࡰࠪᙥ")] = bstack1l111lll1l_opy_
        bstack1lll11l11l1_opy_(item, bstack1l111lll1l_opy_, bstack1llll1l_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩᙦ"))
    except Exception as err:
        print(bstack1llll1l_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡴࡸࡲࡹ࡫ࡳࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱ࠾ࠥࢁࡽࠨᙧ"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if not bstack1ll1ll111l_opy_.on():
        yield
        return
    start_time = datetime.datetime.now()
    if bstack1lllllll111_opy_(fixturedef.argname):
        store[bstack1llll1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡲࡵࡤࡶ࡮ࡨࡣ࡮ࡺࡥ࡮ࠩᙨ")] = request.node
    elif bstack1lllll1llll_opy_(fixturedef.argname):
        store[bstack1llll1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡩ࡬ࡢࡵࡶࡣ࡮ࡺࡥ࡮ࠩᙩ")] = request.node
    outcome = yield
    try:
        fixture = {
            bstack1llll1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᙪ"): fixturedef.argname,
            bstack1llll1l_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᙫ"): bstack11l11ll11l_opy_(outcome),
            bstack1llll1l_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩᙬ"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        current_test_item = store[bstack1llll1l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬ᙭")]
        if not _1l111lllll_opy_.get(current_test_item.nodeid, None):
            _1l111lllll_opy_[current_test_item.nodeid] = {bstack1llll1l_opy_ (u"ࠩࡩ࡭ࡽࡺࡵࡳࡧࡶࠫ᙮"): []}
        _1l111lllll_opy_[current_test_item.nodeid][bstack1llll1l_opy_ (u"ࠪࡪ࡮ࡾࡴࡶࡴࡨࡷࠬᙯ")].append(fixture)
    except Exception as err:
        logger.debug(bstack1llll1l_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡪ࡮ࡾࡴࡶࡴࡨࡣࡸ࡫ࡴࡶࡲ࠽ࠤࢀࢃࠧᙰ"), str(err))
if bstack1ll1l11l1_opy_() and bstack1ll1ll111l_opy_.on():
    def pytest_bdd_before_step(request, step):
        try:
            _1l111lllll_opy_[request.node.nodeid][bstack1llll1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨᙱ")].bstack1llll1l1111_opy_(id(step))
        except Exception as err:
            print(bstack1llll1l_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡥࡩ࡫ࡵࡲࡦࡡࡶࡸࡪࡶ࠺ࠡࡽࢀࠫᙲ"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        try:
            _1l111lllll_opy_[request.node.nodeid][bstack1llll1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪᙳ")].bstack1l111l1ll1_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack1llll1l_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡸࡺࡥࡱࡡࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠬᙴ"), str(err))
    def pytest_bdd_after_step(request, step):
        try:
            bstack1l111l1l11_opy_: bstack1l111lll11_opy_ = _1l111lllll_opy_[request.node.nodeid][bstack1llll1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᙵ")]
            bstack1l111l1l11_opy_.bstack1l111l1ll1_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack1llll1l_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡽࡹ࡫ࡳࡵࡡࡥࡨࡩࡥࡳࡵࡧࡳࡣࡪࡸࡲࡰࡴ࠽ࠤࢀࢃࠧᙶ"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack1lll111ll1l_opy_
        try:
            if not bstack1ll1ll111l_opy_.on() or bstack1lll111ll1l_opy_ != bstack1llll1l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠨᙷ"):
                return
            global bstack11llll1ll1_opy_
            bstack11llll1ll1_opy_.start()
            driver = bstack1lll11l111_opy_(threading.current_thread(), bstack1llll1l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫᙸ"), None)
            if not _1l111lllll_opy_.get(request.node.nodeid, None):
                _1l111lllll_opy_[request.node.nodeid] = {}
            bstack1l111l1l11_opy_ = bstack1l111lll11_opy_.bstack1llll111ll1_opy_(
                scenario, feature, request.node,
                name=bstack1lllll1ll1l_opy_(request.node, scenario),
                bstack11llllllll_opy_=bstack1l1l1llll_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack1llll1l_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠳ࡣࡶࡥࡸࡱࡧ࡫ࡲࠨᙹ"),
                tags=bstack1llllll1111_opy_(feature, scenario),
                bstack1l11l11l11_opy_=bstack1ll1ll111l_opy_.bstack11lllll11l_opy_(driver) if driver and driver.session_id else {}
            )
            _1l111lllll_opy_[request.node.nodeid][bstack1llll1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪᙺ")] = bstack1l111l1l11_opy_
            bstack1lll11lll1l_opy_(bstack1l111l1l11_opy_.uuid)
            bstack1ll1ll111l_opy_.bstack1l111l11l1_opy_(bstack1llll1l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩᙻ"), bstack1l111l1l11_opy_)
        except Exception as err:
            print(bstack1llll1l_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡤࡧࡨࡤࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵ࠺ࠡࡽࢀࠫᙼ"), str(err))
def bstack1lll1l1ll1l_opy_(bstack1lll1l11l11_opy_):
    if bstack1lll1l11l11_opy_ in store[bstack1llll1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧᙽ")]:
        store[bstack1llll1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨᙾ")].remove(bstack1lll1l11l11_opy_)
def bstack1lll11lll1l_opy_(bstack1lll11l111l_opy_):
    store[bstack1llll1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩᙿ")] = bstack1lll11l111l_opy_
    threading.current_thread().current_test_uuid = bstack1lll11l111l_opy_
@bstack1ll1ll111l_opy_.bstack1lll1lllll1_opy_
def bstack1lll11l11ll_opy_(item, call, report):
    global bstack1lll111ll1l_opy_
    bstack1l11l111_opy_ = bstack1l1l1llll_opy_()
    if hasattr(report, bstack1llll1l_opy_ (u"࠭ࡳࡵࡱࡳࠫ ")):
        bstack1l11l111_opy_ = bstack111lll11ll_opy_(report.stop)
    if hasattr(report, bstack1llll1l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࠭ᚁ")):
        bstack1l11l111_opy_ = bstack111lll11ll_opy_(report.start)
    try:
        if getattr(report, bstack1llll1l_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭ᚂ"), bstack1llll1l_opy_ (u"ࠩࠪᚃ")) == bstack1llll1l_opy_ (u"ࠪࡧࡦࡲ࡬ࠨᚄ"):
            bstack11llll1ll1_opy_.reset()
        if getattr(report, bstack1llll1l_opy_ (u"ࠫࡼ࡮ࡥ࡯ࠩᚅ"), bstack1llll1l_opy_ (u"ࠬ࠭ᚆ")) == bstack1llll1l_opy_ (u"࠭ࡣࡢ࡮࡯ࠫᚇ"):
            if bstack1lll111ll1l_opy_ == bstack1llll1l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧᚈ"):
                _1l111lllll_opy_[item.nodeid][bstack1llll1l_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᚉ")] = bstack1l11l111_opy_
                bstack1lll1l11l1l_opy_(item, _1l111lllll_opy_[item.nodeid], bstack1llll1l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫᚊ"), report, call)
                store[bstack1llll1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧᚋ")] = None
            elif bstack1lll111ll1l_opy_ == bstack1llll1l_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠣᚌ"):
                bstack1l111l1l11_opy_ = _1l111lllll_opy_[item.nodeid][bstack1llll1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨᚍ")]
                bstack1l111l1l11_opy_.set(hooks=_1l111lllll_opy_[item.nodeid].get(bstack1llll1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬᚎ"), []))
                exception, bstack11lll11ll1_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack11lll11ll1_opy_ = [call.excinfo.exconly(), getattr(report, bstack1llll1l_opy_ (u"ࠧ࡭ࡱࡱ࡫ࡷ࡫ࡰࡳࡶࡨࡼࡹ࠭ᚏ"), bstack1llll1l_opy_ (u"ࠨࠩᚐ"))]
                bstack1l111l1l11_opy_.stop(time=bstack1l11l111_opy_, result=Result(result=getattr(report, bstack1llll1l_opy_ (u"ࠩࡲࡹࡹࡩ࡯࡮ࡧࠪᚑ"), bstack1llll1l_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᚒ")), exception=exception, bstack11lll11ll1_opy_=bstack11lll11ll1_opy_))
                bstack1ll1ll111l_opy_.bstack1l111l11l1_opy_(bstack1llll1l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᚓ"), _1l111lllll_opy_[item.nodeid][bstack1llll1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨᚔ")])
        elif getattr(report, bstack1llll1l_opy_ (u"࠭ࡷࡩࡧࡱࠫᚕ"), bstack1llll1l_opy_ (u"ࠧࠨᚖ")) in [bstack1llll1l_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧᚗ"), bstack1llll1l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫᚘ")]:
            bstack11llll1l1l_opy_ = item.nodeid + bstack1llll1l_opy_ (u"ࠪ࠱ࠬᚙ") + getattr(report, bstack1llll1l_opy_ (u"ࠫࡼ࡮ࡥ࡯ࠩᚚ"), bstack1llll1l_opy_ (u"ࠬ࠭᚛"))
            if getattr(report, bstack1llll1l_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ᚜"), False):
                hook_type = bstack1llll1l_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬ᚝") if getattr(report, bstack1llll1l_opy_ (u"ࠨࡹ࡫ࡩࡳ࠭᚞"), bstack1llll1l_opy_ (u"ࠩࠪ᚟")) == bstack1llll1l_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩᚠ") else bstack1llll1l_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠨᚡ")
                _1l111lllll_opy_[bstack11llll1l1l_opy_] = {
                    bstack1llll1l_opy_ (u"ࠬࡻࡵࡪࡦࠪᚢ"): uuid4().__str__(),
                    bstack1llll1l_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᚣ"): bstack1l11l111_opy_,
                    bstack1llll1l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪᚤ"): hook_type
                }
            _1l111lllll_opy_[bstack11llll1l1l_opy_][bstack1llll1l_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᚥ")] = bstack1l11l111_opy_
            bstack1lll1l1ll1l_opy_(_1l111lllll_opy_[bstack11llll1l1l_opy_][bstack1llll1l_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᚦ")])
            bstack1lll11l11l1_opy_(item, _1l111lllll_opy_[bstack11llll1l1l_opy_], bstack1llll1l_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᚧ"), report, call)
            if getattr(report, bstack1llll1l_opy_ (u"ࠫࡼ࡮ࡥ࡯ࠩᚨ"), bstack1llll1l_opy_ (u"ࠬ࠭ᚩ")) == bstack1llll1l_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬᚪ"):
                if getattr(report, bstack1llll1l_opy_ (u"ࠧࡰࡷࡷࡧࡴࡳࡥࠨᚫ"), bstack1llll1l_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᚬ")) == bstack1llll1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᚭ"):
                    bstack1l111lll1l_opy_ = {
                        bstack1llll1l_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᚮ"): uuid4().__str__(),
                        bstack1llll1l_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᚯ"): bstack1l1l1llll_opy_(),
                        bstack1llll1l_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᚰ"): bstack1l1l1llll_opy_()
                    }
                    _1l111lllll_opy_[item.nodeid] = {**_1l111lllll_opy_[item.nodeid], **bstack1l111lll1l_opy_}
                    bstack1lll1l11l1l_opy_(item, _1l111lllll_opy_[item.nodeid], bstack1llll1l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧᚱ"))
                    bstack1lll1l11l1l_opy_(item, _1l111lllll_opy_[item.nodeid], bstack1llll1l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩᚲ"), report, call)
    except Exception as err:
        print(bstack1llll1l_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡩࡣࡱࡨࡱ࡫࡟ࡰ࠳࠴ࡽࡤࡺࡥࡴࡶࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡿࢂ࠭ᚳ"), str(err))
def bstack1lll1l11111_opy_(test, bstack1l111lll1l_opy_, result=None, call=None, bstack1111l1l1_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack1l111l1l11_opy_ = {
        bstack1llll1l_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᚴ"): bstack1l111lll1l_opy_[bstack1llll1l_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᚵ")],
        bstack1llll1l_opy_ (u"ࠫࡹࡿࡰࡦࠩᚶ"): bstack1llll1l_opy_ (u"ࠬࡺࡥࡴࡶࠪᚷ"),
        bstack1llll1l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᚸ"): test.name,
        bstack1llll1l_opy_ (u"ࠧࡣࡱࡧࡽࠬᚹ"): {
            bstack1llll1l_opy_ (u"ࠨ࡮ࡤࡲ࡬࠭ᚺ"): bstack1llll1l_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩᚻ"),
            bstack1llll1l_opy_ (u"ࠪࡧࡴࡪࡥࠨᚼ"): inspect.getsource(test.obj)
        },
        bstack1llll1l_opy_ (u"ࠫ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨᚽ"): test.name,
        bstack1llll1l_opy_ (u"ࠬࡹࡣࡰࡲࡨࠫᚾ"): test.name,
        bstack1llll1l_opy_ (u"࠭ࡳࡤࡱࡳࡩࡸ࠭ᚿ"): bstack1ll1ll111l_opy_.bstack1l111111ll_opy_(test),
        bstack1llll1l_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪᛀ"): file_path,
        bstack1llll1l_opy_ (u"ࠨ࡮ࡲࡧࡦࡺࡩࡰࡰࠪᛁ"): file_path,
        bstack1llll1l_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᛂ"): bstack1llll1l_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫᛃ"),
        bstack1llll1l_opy_ (u"ࠫࡻࡩ࡟ࡧ࡫࡯ࡩࡵࡧࡴࡩࠩᛄ"): file_path,
        bstack1llll1l_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᛅ"): bstack1l111lll1l_opy_[bstack1llll1l_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᛆ")],
        bstack1llll1l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪᛇ"): bstack1llll1l_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴࠨᛈ"),
        bstack1llll1l_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡔࡨࡶࡺࡴࡐࡢࡴࡤࡱࠬᛉ"): {
            bstack1llll1l_opy_ (u"ࠪࡶࡪࡸࡵ࡯ࡡࡱࡥࡲ࡫ࠧᛊ"): test.nodeid
        },
        bstack1llll1l_opy_ (u"ࠫࡹࡧࡧࡴࠩᛋ"): bstack11l11l11ll_opy_(test.own_markers)
    }
    if bstack1111l1l1_opy_ in [bstack1llll1l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙࡫ࡪࡲࡳࡩࡩ࠭ᛌ"), bstack1llll1l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨᛍ")]:
        bstack1l111l1l11_opy_[bstack1llll1l_opy_ (u"ࠧ࡮ࡧࡷࡥࠬᛎ")] = {
            bstack1llll1l_opy_ (u"ࠨࡨ࡬ࡼࡹࡻࡲࡦࡵࠪᛏ"): bstack1l111lll1l_opy_.get(bstack1llll1l_opy_ (u"ࠩࡩ࡭ࡽࡺࡵࡳࡧࡶࠫᛐ"), [])
        }
    if bstack1111l1l1_opy_ == bstack1llll1l_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡰ࡯ࡰࡱࡧࡧࠫᛑ"):
        bstack1l111l1l11_opy_[bstack1llll1l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᛒ")] = bstack1llll1l_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ᛓ")
        bstack1l111l1l11_opy_[bstack1llll1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬᛔ")] = bstack1l111lll1l_opy_[bstack1llll1l_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ᛕ")]
        bstack1l111l1l11_opy_[bstack1llll1l_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᛖ")] = bstack1l111lll1l_opy_[bstack1llll1l_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᛗ")]
    if result:
        bstack1l111l1l11_opy_[bstack1llll1l_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᛘ")] = result.outcome
        bstack1l111l1l11_opy_[bstack1llll1l_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬᛙ")] = result.duration * 1000
        bstack1l111l1l11_opy_[bstack1llll1l_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᛚ")] = bstack1l111lll1l_opy_[bstack1llll1l_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᛛ")]
        if result.failed:
            bstack1l111l1l11_opy_[bstack1llll1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࡠࡶࡼࡴࡪ࠭ᛜ")] = bstack1ll1ll111l_opy_.bstack11ll1l11l1_opy_(call.excinfo.typename)
            bstack1l111l1l11_opy_[bstack1llll1l_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩᛝ")] = bstack1ll1ll111l_opy_.bstack1lll1ll111l_opy_(call.excinfo, result)
        bstack1l111l1l11_opy_[bstack1llll1l_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨᛞ")] = bstack1l111lll1l_opy_[bstack1llll1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩᛟ")]
    if outcome:
        bstack1l111l1l11_opy_[bstack1llll1l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᛠ")] = bstack11l11ll11l_opy_(outcome)
        bstack1l111l1l11_opy_[bstack1llll1l_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡢࡱࡸ࠭ᛡ")] = 0
        bstack1l111l1l11_opy_[bstack1llll1l_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᛢ")] = bstack1l111lll1l_opy_[bstack1llll1l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᛣ")]
        if bstack1l111l1l11_opy_[bstack1llll1l_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᛤ")] == bstack1llll1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᛥ"):
            bstack1l111l1l11_opy_[bstack1llll1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩᛦ")] = bstack1llll1l_opy_ (u"࡚ࠫࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠬᛧ")  # bstack1lll1l111l1_opy_
            bstack1l111l1l11_opy_[bstack1llll1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭ᛨ")] = [{bstack1llll1l_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩᛩ"): [bstack1llll1l_opy_ (u"ࠧࡴࡱࡰࡩࠥ࡫ࡲࡳࡱࡵࠫᛪ")]}]
        bstack1l111l1l11_opy_[bstack1llll1l_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ᛫")] = bstack1l111lll1l_opy_[bstack1llll1l_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ᛬")]
    return bstack1l111l1l11_opy_
def bstack1lll11l1l11_opy_(test, bstack11lllllll1_opy_, bstack1111l1l1_opy_, result, call, outcome, bstack1lll111lll1_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack11lllllll1_opy_[bstack1llll1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭᛭")]
    hook_name = bstack11lllllll1_opy_[bstack1llll1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡱࡥࡲ࡫ࠧᛮ")]
    hook_data = {
        bstack1llll1l_opy_ (u"ࠬࡻࡵࡪࡦࠪᛯ"): bstack11lllllll1_opy_[bstack1llll1l_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᛰ")],
        bstack1llll1l_opy_ (u"ࠧࡵࡻࡳࡩࠬᛱ"): bstack1llll1l_opy_ (u"ࠨࡪࡲࡳࡰ࠭ᛲ"),
        bstack1llll1l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᛳ"): bstack1llll1l_opy_ (u"ࠪࡿࢂ࠭ᛴ").format(bstack1lllll1l1ll_opy_(hook_name)),
        bstack1llll1l_opy_ (u"ࠫࡧࡵࡤࡺࠩᛵ"): {
            bstack1llll1l_opy_ (u"ࠬࡲࡡ࡯ࡩࠪᛶ"): bstack1llll1l_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ᛷ"),
            bstack1llll1l_opy_ (u"ࠧࡤࡱࡧࡩࠬᛸ"): None
        },
        bstack1llll1l_opy_ (u"ࠨࡵࡦࡳࡵ࡫ࠧ᛹"): test.name,
        bstack1llll1l_opy_ (u"ࠩࡶࡧࡴࡶࡥࡴࠩ᛺"): bstack1ll1ll111l_opy_.bstack1l111111ll_opy_(test, hook_name),
        bstack1llll1l_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭᛻"): file_path,
        bstack1llll1l_opy_ (u"ࠫࡱࡵࡣࡢࡶ࡬ࡳࡳ࠭᛼"): file_path,
        bstack1llll1l_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ᛽"): bstack1llll1l_opy_ (u"࠭ࡰࡦࡰࡧ࡭ࡳ࡭ࠧ᛾"),
        bstack1llll1l_opy_ (u"ࠧࡷࡥࡢࡪ࡮ࡲࡥࡱࡣࡷ࡬ࠬ᛿"): file_path,
        bstack1llll1l_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᜀ"): bstack11lllllll1_opy_[bstack1llll1l_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᜁ")],
        bstack1llll1l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ᜂ"): bstack1llll1l_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷ࠱ࡨࡻࡣࡶ࡯ࡥࡩࡷ࠭ᜃ") if bstack1lll111ll1l_opy_ == bstack1llll1l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠩᜄ") else bstack1llll1l_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠭ᜅ"),
        bstack1llll1l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪᜆ"): hook_type
    }
    bstack1lll1l111ll_opy_ = bstack11lll1ll1l_opy_(_1l111lllll_opy_.get(test.nodeid, None))
    if bstack1lll1l111ll_opy_:
        hook_data[bstack1llll1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢ࡭ࡩ࠭ᜇ")] = bstack1lll1l111ll_opy_
    if result:
        hook_data[bstack1llll1l_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᜈ")] = result.outcome
        hook_data[bstack1llll1l_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡠ࡯ࡶࠫᜉ")] = result.duration * 1000
        hook_data[bstack1llll1l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᜊ")] = bstack11lllllll1_opy_[bstack1llll1l_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᜋ")]
        if result.failed:
            hook_data[bstack1llll1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬᜌ")] = bstack1ll1ll111l_opy_.bstack11ll1l11l1_opy_(call.excinfo.typename)
            hook_data[bstack1llll1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨᜍ")] = bstack1ll1ll111l_opy_.bstack1lll1ll111l_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack1llll1l_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᜎ")] = bstack11l11ll11l_opy_(outcome)
        hook_data[bstack1llll1l_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪᜏ")] = 100
        hook_data[bstack1llll1l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᜐ")] = bstack11lllllll1_opy_[bstack1llll1l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᜑ")]
        if hook_data[bstack1llll1l_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᜒ")] == bstack1llll1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᜓ"):
            hook_data[bstack1llll1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࡠࡶࡼࡴࡪ᜔࠭")] = bstack1llll1l_opy_ (u"ࠨࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳ᜕ࠩ")  # bstack1lll1l111l1_opy_
            hook_data[bstack1llll1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪ᜖")] = [{bstack1llll1l_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭᜗"): [bstack1llll1l_opy_ (u"ࠫࡸࡵ࡭ࡦࠢࡨࡶࡷࡵࡲࠨ᜘")]}]
    if bstack1lll111lll1_opy_:
        hook_data[bstack1llll1l_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ᜙")] = bstack1lll111lll1_opy_.result
        hook_data[bstack1llll1l_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧ᜚")] = bstack11l11llll1_opy_(bstack11lllllll1_opy_[bstack1llll1l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ᜛")], bstack11lllllll1_opy_[bstack1llll1l_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭᜜")])
        hook_data[bstack1llll1l_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ᜝")] = bstack11lllllll1_opy_[bstack1llll1l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ᜞")]
        if hook_data[bstack1llll1l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᜟ")] == bstack1llll1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᜠ"):
            hook_data[bstack1llll1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬᜡ")] = bstack1ll1ll111l_opy_.bstack11ll1l11l1_opy_(bstack1lll111lll1_opy_.exception_type)
            hook_data[bstack1llll1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨᜢ")] = [{bstack1llll1l_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫᜣ"): bstack111lllll1l_opy_(bstack1lll111lll1_opy_.exception)}]
    return hook_data
def bstack1lll1l11l1l_opy_(test, bstack1l111lll1l_opy_, bstack1111l1l1_opy_, result=None, call=None, outcome=None):
    bstack1l111l1l11_opy_ = bstack1lll1l11111_opy_(test, bstack1l111lll1l_opy_, result, call, bstack1111l1l1_opy_, outcome)
    driver = getattr(test, bstack1llll1l_opy_ (u"ࠩࡢࡨࡷ࡯ࡶࡦࡴࠪᜤ"), None)
    if bstack1111l1l1_opy_ == bstack1llll1l_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫᜥ") and driver:
        bstack1l111l1l11_opy_[bstack1llll1l_opy_ (u"ࠫ࡮ࡴࡴࡦࡩࡵࡥࡹ࡯࡯࡯ࡵࠪᜦ")] = bstack1ll1ll111l_opy_.bstack11lllll11l_opy_(driver)
    if bstack1111l1l1_opy_ == bstack1llll1l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙࡫ࡪࡲࡳࡩࡩ࠭ᜧ"):
        bstack1111l1l1_opy_ = bstack1llll1l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨᜨ")
    bstack1l1111llll_opy_ = {
        bstack1llll1l_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫᜩ"): bstack1111l1l1_opy_,
        bstack1llll1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪᜪ"): bstack1l111l1l11_opy_
    }
    bstack1ll1ll111l_opy_.bstack1l111ll1l1_opy_(bstack1l1111llll_opy_)
def bstack1lll11l11l1_opy_(test, bstack1l111lll1l_opy_, bstack1111l1l1_opy_, result=None, call=None, outcome=None, bstack1lll111lll1_opy_=None):
    hook_data = bstack1lll11l1l11_opy_(test, bstack1l111lll1l_opy_, bstack1111l1l1_opy_, result, call, outcome, bstack1lll111lll1_opy_)
    bstack1l1111llll_opy_ = {
        bstack1llll1l_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭ᜫ"): bstack1111l1l1_opy_,
        bstack1llll1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࠬᜬ"): hook_data
    }
    bstack1ll1ll111l_opy_.bstack1l111ll1l1_opy_(bstack1l1111llll_opy_)
def bstack11lll1ll1l_opy_(bstack1l111lll1l_opy_):
    if not bstack1l111lll1l_opy_:
        return None
    if bstack1l111lll1l_opy_.get(bstack1llll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧᜭ"), None):
        return getattr(bstack1l111lll1l_opy_[bstack1llll1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨᜮ")], bstack1llll1l_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᜯ"), None)
    return bstack1l111lll1l_opy_.get(bstack1llll1l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᜰ"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    yield
    try:
        if not bstack1ll1ll111l_opy_.on():
            return
        places = [bstack1llll1l_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧᜱ"), bstack1llll1l_opy_ (u"ࠩࡦࡥࡱࡲࠧᜲ"), bstack1llll1l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࠬᜳ")]
        bstack11lllll1ll_opy_ = []
        for bstack1lll1l11lll_opy_ in places:
            records = caplog.get_records(bstack1lll1l11lll_opy_)
            bstack1lll11lllll_opy_ = bstack1llll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧ᜴ࠫ") if bstack1lll1l11lll_opy_ == bstack1llll1l_opy_ (u"ࠬࡩࡡ࡭࡮ࠪ᜵") else bstack1llll1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭᜶")
            bstack1lll111ll11_opy_ = request.node.nodeid + (bstack1llll1l_opy_ (u"ࠧࠨ᜷") if bstack1lll1l11lll_opy_ == bstack1llll1l_opy_ (u"ࠨࡥࡤࡰࡱ࠭᜸") else bstack1llll1l_opy_ (u"ࠩ࠰ࠫ᜹") + bstack1lll1l11lll_opy_)
            bstack1lll11l111l_opy_ = bstack11lll1ll1l_opy_(_1l111lllll_opy_.get(bstack1lll111ll11_opy_, None))
            if not bstack1lll11l111l_opy_:
                continue
            for record in records:
                if bstack11l11l111l_opy_(record.message):
                    continue
                bstack11lllll1ll_opy_.append({
                    bstack1llll1l_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭᜺"): datetime.datetime.utcfromtimestamp(record.created).isoformat() + bstack1llll1l_opy_ (u"ࠫ࡟࠭᜻"),
                    bstack1llll1l_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ᜼"): record.levelname,
                    bstack1llll1l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ᜽"): record.message,
                    bstack1lll11lllll_opy_: bstack1lll11l111l_opy_
                })
        if len(bstack11lllll1ll_opy_) > 0:
            bstack1ll1ll111l_opy_.bstack11ll1ll1l_opy_(bstack11lllll1ll_opy_)
    except Exception as err:
        print(bstack1llll1l_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡦࡥࡲࡲࡩࡥࡦࡪࡺࡷࡹࡷ࡫࠺ࠡࡽࢀࠫ᜾"), str(err))
def bstack111l1l11_opy_(sequence, driver_command, response=None, driver = None, args = None):
    global bstack1l1111ll_opy_
    bstack1ll11lllll_opy_ = bstack1lll11l111_opy_(threading.current_thread(), bstack1llll1l_opy_ (u"ࠨ࡫ࡶࡅ࠶࠷ࡹࡕࡧࡶࡸࠬ᜿"), None) and bstack1lll11l111_opy_(
            threading.current_thread(), bstack1llll1l_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨᝀ"), None)
    bstack11111lll_opy_ = getattr(driver, bstack1llll1l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡄ࠵࠶ࡿࡓࡩࡱࡸࡰࡩ࡙ࡣࡢࡰࠪᝁ"), None) != None and getattr(driver, bstack1llll1l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡅ࠶࠷ࡹࡔࡪࡲࡹࡱࡪࡓࡤࡣࡱࠫᝂ"), None) == True
    if sequence == bstack1llll1l_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࠬᝃ") and driver != None:
      if not bstack1l1111ll_opy_ and bstack11l1111111_opy_() and bstack1llll1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᝄ") in CONFIG and CONFIG[bstack1llll1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᝅ")] == True and bstack1lllll11l1_opy_.bstack1llll1l11_opy_(driver_command) and (bstack11111lll_opy_ or bstack1ll11lllll_opy_) and not bstack1ll11lll_opy_(args):
        try:
          bstack1l1111ll_opy_ = True
          logger.debug(bstack1llll1l_opy_ (u"ࠨࡒࡨࡶ࡫ࡵࡲ࡮࡫ࡱ࡫ࠥࡹࡣࡢࡰࠣࡪࡴࡸࠠࡼࡿࠪᝆ").format(driver_command))
          logger.debug(perform_scan(driver, driver_command=driver_command))
        except Exception as err:
          logger.debug(bstack1llll1l_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡶࡥࡳࡨࡲࡶࡲࠦࡳࡤࡣࡱࠤࢀࢃࠧᝇ").format(str(err)))
        bstack1l1111ll_opy_ = False
    if sequence == bstack1llll1l_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩᝈ"):
        if driver_command == bstack1llll1l_opy_ (u"ࠫࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠨᝉ"):
            bstack1ll1ll111l_opy_.bstack1l11l1lll1_opy_({
                bstack1llll1l_opy_ (u"ࠬ࡯࡭ࡢࡩࡨࠫᝊ"): response[bstack1llll1l_opy_ (u"࠭ࡶࡢ࡮ࡸࡩࠬᝋ")],
                bstack1llll1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᝌ"): store[bstack1llll1l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬᝍ")]
            })
def bstack1l1llll11l_opy_():
    global bstack1lll11l11l_opy_
    bstack1ll1l1ll_opy_.bstack11l1ll1l_opy_()
    logging.shutdown()
    bstack1ll1ll111l_opy_.bstack1l1111ll11_opy_()
    for driver in bstack1lll11l11l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1lll11l1ll1_opy_(*args):
    global bstack1lll11l11l_opy_
    bstack1ll1ll111l_opy_.bstack1l1111ll11_opy_()
    for driver in bstack1lll11l11l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1ll1l1111l_opy_(self, *args, **kwargs):
    bstack1l1l111l1l_opy_ = bstack1l1l1l1l11_opy_(self, *args, **kwargs)
    bstack1ll1ll111l_opy_.bstack1ll11111_opy_(self)
    return bstack1l1l111l1l_opy_
def bstack1111l1l1l_opy_(framework_name):
    global bstack1ll1llll_opy_
    global bstack1l1111lll_opy_
    bstack1ll1llll_opy_ = framework_name
    logger.info(bstack1lll111lll_opy_.format(bstack1ll1llll_opy_.split(bstack1llll1l_opy_ (u"ࠩ࠰ࠫᝎ"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack11l1111111_opy_():
            Service.start = bstack1l1ll111l_opy_
            Service.stop = bstack1lll111l1l_opy_
            webdriver.Remote.__init__ = bstack1l1l11ll1_opy_
            webdriver.Remote.get = bstack1llll11ll_opy_
            if not isinstance(os.getenv(bstack1llll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓ࡝࡙ࡋࡓࡕࡡࡓࡅࡗࡇࡌࡍࡇࡏࠫᝏ")), str):
                return
            WebDriver.close = bstack11l11l111_opy_
            WebDriver.quit = bstack11ll11l1l_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.get_accessibility_results = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
        if not bstack11l1111111_opy_() and bstack1ll1ll111l_opy_.on():
            webdriver.Remote.__init__ = bstack1ll1l1111l_opy_
        bstack1l1111lll_opy_ = True
    except Exception as e:
        pass
    bstack1ll1lll1l_opy_()
    if os.environ.get(bstack1llll1l_opy_ (u"ࠫࡘࡋࡌࡆࡐࡌ࡙ࡒࡥࡏࡓࡡࡓࡐࡆ࡟ࡗࡓࡋࡊࡌ࡙ࡥࡉࡏࡕࡗࡅࡑࡒࡅࡅࠩᝐ")):
        bstack1l1111lll_opy_ = eval(os.environ.get(bstack1llll1l_opy_ (u"࡙ࠬࡅࡍࡇࡑࡍ࡚ࡓ࡟ࡐࡔࡢࡔࡑࡇ࡙ࡘࡔࡌࡋࡍ࡚࡟ࡊࡐࡖࡘࡆࡒࡌࡆࡆࠪᝑ")))
    if not bstack1l1111lll_opy_:
        bstack1ll11llll_opy_(bstack1llll1l_opy_ (u"ࠨࡐࡢࡥ࡮ࡥ࡬࡫ࡳࠡࡰࡲࡸࠥ࡯࡮ࡴࡶࡤࡰࡱ࡫ࡤࠣᝒ"), bstack11ll111l_opy_)
    if bstack1ll1l1lll1_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            RemoteConnection._get_proxy_url = bstack1ll1llll11_opy_
        except Exception as e:
            logger.error(bstack11ll11lll_opy_.format(str(e)))
    if bstack1llll1l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧᝓ") in str(framework_name).lower():
        if not bstack11l1111111_opy_():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack1ll1l1ll1l_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack1l1ll11l_opy_
            Config.getoption = bstack1l111ll1_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack11llll1l1_opy_
        except Exception as e:
            pass
def bstack11ll11l1l_opy_(self):
    global bstack1ll1llll_opy_
    global bstack1lll11ll1_opy_
    global bstack111l11l1l_opy_
    try:
        if bstack1llll1l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ᝔") in bstack1ll1llll_opy_ and self.session_id != None and bstack1lll11l111_opy_(threading.current_thread(), bstack1llll1l_opy_ (u"ࠩࡷࡩࡸࡺࡓࡵࡣࡷࡹࡸ࠭᝕"), bstack1llll1l_opy_ (u"ࠪࠫ᝖")) != bstack1llll1l_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬ᝗"):
            bstack111llll11_opy_ = bstack1llll1l_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ᝘") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1llll1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭᝙")
            bstack1l1l111ll_opy_(logger, True)
            if self != None:
                bstack1ll11lll1l_opy_(self, bstack111llll11_opy_, bstack1llll1l_opy_ (u"ࠧ࠭ࠢࠪ᝚").join(threading.current_thread().bstackTestErrorMessages))
        item = store.get(bstack1llll1l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬ᝛"), None)
        if item is not None and bstack1lll1l1l11l_opy_:
            bstack1l1lll1lll_opy_.bstack11ll11111_opy_(self, bstack1ll1lllll1_opy_, logger, item)
        threading.current_thread().testStatus = bstack1llll1l_opy_ (u"ࠩࠪ᝜")
    except Exception as e:
        logger.debug(bstack1llll1l_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡ࡯ࡤࡶࡰ࡯࡮ࡨࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࠦ᝝") + str(e))
    bstack111l11l1l_opy_(self)
    self.session_id = None
def bstack1l1l11ll1_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack1lll11ll1_opy_
    global bstack1111111ll_opy_
    global bstack1ll11l111_opy_
    global bstack1ll1llll_opy_
    global bstack1l1l1l1l11_opy_
    global bstack1lll11l11l_opy_
    global bstack111lll1l_opy_
    global bstack11ll1ll11_opy_
    global bstack1lll1l1l11l_opy_
    global bstack1ll1lllll1_opy_
    CONFIG[bstack1llll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭᝞")] = str(bstack1ll1llll_opy_) + str(__version__)
    command_executor = bstack111l11lll_opy_(bstack111lll1l_opy_)
    logger.debug(bstack1ll1111l1_opy_.format(command_executor))
    proxy = bstack11l111lll_opy_(CONFIG, proxy)
    bstack1l1l11l11_opy_ = 0
    try:
        if bstack1ll11l111_opy_ is True:
            bstack1l1l11l11_opy_ = int(os.environ.get(bstack1llll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬ᝟")))
    except:
        bstack1l1l11l11_opy_ = 0
    bstack1lll1ll1_opy_ = bstack1l1lll1l_opy_(CONFIG, bstack1l1l11l11_opy_)
    logger.debug(bstack1111ll111_opy_.format(str(bstack1lll1ll1_opy_)))
    bstack1ll1lllll1_opy_ = CONFIG.get(bstack1llll1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᝠ"))[bstack1l1l11l11_opy_]
    if bstack1llll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫᝡ") in CONFIG and CONFIG[bstack1llll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬᝢ")]:
        bstack1lllllll11_opy_(bstack1lll1ll1_opy_, bstack11ll1ll11_opy_)
    if bstack11lllll1l_opy_.bstack1ll1l1l1l1_opy_(CONFIG, bstack1l1l11l11_opy_) and bstack11lllll1l_opy_.bstack11l1llll1_opy_(bstack1lll1ll1_opy_, options):
        bstack1lll1l1l11l_opy_ = True
        bstack11lllll1l_opy_.set_capabilities(bstack1lll1ll1_opy_, CONFIG)
    if desired_capabilities:
        bstack1ll1lll111_opy_ = bstack111ll111l_opy_(desired_capabilities)
        bstack1ll1lll111_opy_[bstack1llll1l_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩᝣ")] = bstack1ll111ll11_opy_(CONFIG)
        bstack111l1ll1_opy_ = bstack1l1lll1l_opy_(bstack1ll1lll111_opy_)
        if bstack111l1ll1_opy_:
            bstack1lll1ll1_opy_ = update(bstack111l1ll1_opy_, bstack1lll1ll1_opy_)
        desired_capabilities = None
    if options:
        bstack1lll1lll1_opy_(options, bstack1lll1ll1_opy_)
    if not options:
        options = bstack1111l11l1_opy_(bstack1lll1ll1_opy_)
    if proxy and bstack111l11l1_opy_() >= version.parse(bstack1llll1l_opy_ (u"ࠪ࠸࠳࠷࠰࠯࠲ࠪᝤ")):
        options.proxy(proxy)
    if options and bstack111l11l1_opy_() >= version.parse(bstack1llll1l_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪᝥ")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack111l11l1_opy_() < version.parse(bstack1llll1l_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫᝦ")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack1lll1ll1_opy_)
    logger.info(bstack1lll11l11_opy_)
    if bstack111l11l1_opy_() >= version.parse(bstack1llll1l_opy_ (u"࠭࠴࠯࠳࠳࠲࠵࠭ᝧ")):
        bstack1l1l1l1l11_opy_(self, command_executor=command_executor,
                  options=options, keep_alive=keep_alive, file_detector=file_detector)
    elif bstack111l11l1_opy_() >= version.parse(bstack1llll1l_opy_ (u"ࠧ࠴࠰࠻࠲࠵࠭ᝨ")):
        bstack1l1l1l1l11_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities, options=options,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    elif bstack111l11l1_opy_() >= version.parse(bstack1llll1l_opy_ (u"ࠨ࠴࠱࠹࠸࠴࠰ࠨᝩ")):
        bstack1l1l1l1l11_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    else:
        bstack1l1l1l1l11_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive)
    try:
        bstack1lll1l11_opy_ = bstack1llll1l_opy_ (u"ࠩࠪᝪ")
        if bstack111l11l1_opy_() >= version.parse(bstack1llll1l_opy_ (u"ࠪ࠸࠳࠶࠮࠱ࡤ࠴ࠫᝫ")):
            bstack1lll1l11_opy_ = self.caps.get(bstack1llll1l_opy_ (u"ࠦࡴࡶࡴࡪ࡯ࡤࡰࡍࡻࡢࡖࡴ࡯ࠦᝬ"))
        else:
            bstack1lll1l11_opy_ = self.capabilities.get(bstack1llll1l_opy_ (u"ࠧࡵࡰࡵ࡫ࡰࡥࡱࡎࡵࡣࡗࡵࡰࠧ᝭"))
        if bstack1lll1l11_opy_:
            bstack111l111l_opy_(bstack1lll1l11_opy_)
            if bstack111l11l1_opy_() <= version.parse(bstack1llll1l_opy_ (u"࠭࠳࠯࠳࠶࠲࠵࠭ᝮ")):
                self.command_executor._url = bstack1llll1l_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣᝯ") + bstack111lll1l_opy_ + bstack1llll1l_opy_ (u"ࠣ࠼࠻࠴࠴ࡽࡤ࠰ࡪࡸࡦࠧᝰ")
            else:
                self.command_executor._url = bstack1llll1l_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦ᝱") + bstack1lll1l11_opy_ + bstack1llll1l_opy_ (u"ࠥ࠳ࡼࡪ࠯ࡩࡷࡥࠦᝲ")
            logger.debug(bstack111l1l111_opy_.format(bstack1lll1l11_opy_))
        else:
            logger.debug(bstack11l1ll1l1_opy_.format(bstack1llll1l_opy_ (u"ࠦࡔࡶࡴࡪ࡯ࡤࡰࠥࡎࡵࡣࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨࠧᝳ")))
    except Exception as e:
        logger.debug(bstack11l1ll1l1_opy_.format(e))
    bstack1lll11ll1_opy_ = self.session_id
    if bstack1llll1l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ᝴") in bstack1ll1llll_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        item = store.get(bstack1llll1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪ᝵"), None)
        if item:
            bstack1lll11ll1l1_opy_ = getattr(item, bstack1llll1l_opy_ (u"ࠧࡠࡶࡨࡷࡹࡥࡣࡢࡵࡨࡣࡸࡺࡡࡳࡶࡨࡨࠬ᝶"), False)
            if not getattr(item, bstack1llll1l_opy_ (u"ࠨࡡࡧࡶ࡮ࡼࡥࡳࠩ᝷"), None) and bstack1lll11ll1l1_opy_:
                setattr(store[bstack1llll1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭᝸")], bstack1llll1l_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫ᝹"), self)
        bstack1ll1ll111l_opy_.bstack1ll11111_opy_(self)
    bstack1lll11l11l_opy_.append(self)
    if bstack1llll1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ᝺") in CONFIG and bstack1llll1l_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ᝻") in CONFIG[bstack1llll1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ᝼")][bstack1l1l11l11_opy_]:
        bstack1111111ll_opy_ = CONFIG[bstack1llll1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ᝽")][bstack1l1l11l11_opy_][bstack1llll1l_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭᝾")]
    logger.debug(bstack1l1lllll1_opy_.format(bstack1lll11ll1_opy_))
def bstack1llll11ll_opy_(self, url):
    global bstack11l1l1ll_opy_
    global CONFIG
    try:
        bstack11lllll1_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack1ll1l111_opy_.format(str(err)))
    try:
        bstack11l1l1ll_opy_(self, url)
    except Exception as e:
        try:
            bstack1l1lll11_opy_ = str(e)
            if any(err_msg in bstack1l1lll11_opy_ for err_msg in bstack1llllll1l_opy_):
                bstack11lllll1_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack1ll1l111_opy_.format(str(err)))
        raise e
def bstack1l1l1ll1ll_opy_(item, when):
    global bstack1llll111ll_opy_
    try:
        bstack1llll111ll_opy_(item, when)
    except Exception as e:
        pass
def bstack11llll1l1_opy_(item, call, rep):
    global bstack1llll1ll1_opy_
    global bstack1lll11l11l_opy_
    name = bstack1llll1l_opy_ (u"ࠩࠪ᝿")
    try:
        if rep.when == bstack1llll1l_opy_ (u"ࠪࡧࡦࡲ࡬ࠨក"):
            bstack1lll11ll1_opy_ = threading.current_thread().bstackSessionId
            bstack1lll11l1111_opy_ = item.config.getoption(bstack1llll1l_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ខ"))
            try:
                if (str(bstack1lll11l1111_opy_).lower() != bstack1llll1l_opy_ (u"ࠬࡺࡲࡶࡧࠪគ")):
                    name = str(rep.nodeid)
                    bstack1llll11l1_opy_ = bstack11l111l1l_opy_(bstack1llll1l_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧឃ"), name, bstack1llll1l_opy_ (u"ࠧࠨង"), bstack1llll1l_opy_ (u"ࠨࠩច"), bstack1llll1l_opy_ (u"ࠩࠪឆ"), bstack1llll1l_opy_ (u"ࠪࠫជ"))
                    os.environ[bstack1llll1l_opy_ (u"ࠫࡕ࡟ࡔࡆࡕࡗࡣ࡙ࡋࡓࡕࡡࡑࡅࡒࡋࠧឈ")] = name
                    for driver in bstack1lll11l11l_opy_:
                        if bstack1lll11ll1_opy_ == driver.session_id:
                            driver.execute_script(bstack1llll11l1_opy_)
            except Exception as e:
                logger.debug(bstack1llll1l_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠦࡦࡰࡴࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡴࡧࡶࡷ࡮ࡵ࡮࠻ࠢࡾࢁࠬញ").format(str(e)))
            try:
                bstack111ll1111_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack1llll1l_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧដ"):
                    status = bstack1llll1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧឋ") if rep.outcome.lower() == bstack1llll1l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨឌ") else bstack1llll1l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩឍ")
                    reason = bstack1llll1l_opy_ (u"ࠪࠫណ")
                    if status == bstack1llll1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫត"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack1llll1l_opy_ (u"ࠬ࡯࡮ࡧࡱࠪថ") if status == bstack1llll1l_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ទ") else bstack1llll1l_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ធ")
                    data = name + bstack1llll1l_opy_ (u"ࠨࠢࡳࡥࡸࡹࡥࡥࠣࠪន") if status == bstack1llll1l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩប") else name + bstack1llll1l_opy_ (u"ࠪࠤ࡫ࡧࡩ࡭ࡧࡧࠥࠥ࠭ផ") + reason
                    bstack1l1llllll_opy_ = bstack11l111l1l_opy_(bstack1llll1l_opy_ (u"ࠫࡦࡴ࡮ࡰࡶࡤࡸࡪ࠭ព"), bstack1llll1l_opy_ (u"ࠬ࠭ភ"), bstack1llll1l_opy_ (u"࠭ࠧម"), bstack1llll1l_opy_ (u"ࠧࠨយ"), level, data)
                    for driver in bstack1lll11l11l_opy_:
                        if bstack1lll11ll1_opy_ == driver.session_id:
                            driver.execute_script(bstack1l1llllll_opy_)
            except Exception as e:
                logger.debug(bstack1llll1l_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡩ࡯࡯ࡶࡨࡼࡹࠦࡦࡰࡴࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡴࡧࡶࡷ࡮ࡵ࡮࠻ࠢࡾࢁࠬរ").format(str(e)))
    except Exception as e:
        logger.debug(bstack1llll1l_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡴࡢࡶࡨࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹ࡫ࡳࡵࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࡿࢂ࠭ល").format(str(e)))
    bstack1llll1ll1_opy_(item, call, rep)
notset = Notset()
def bstack1l111ll1_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack111l1111_opy_
    if str(name).lower() == bstack1llll1l_opy_ (u"ࠪࡨࡷ࡯ࡶࡦࡴࠪវ"):
        return bstack1llll1l_opy_ (u"ࠦࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠥឝ")
    else:
        return bstack111l1111_opy_(self, name, default, skip)
def bstack1ll1llll11_opy_(self):
    global CONFIG
    global bstack1l1ll1l1l_opy_
    try:
        proxy = bstack1ll1l11lll_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack1llll1l_opy_ (u"ࠬ࠴ࡰࡢࡥࠪឞ")):
                proxies = bstack1lll1l11l_opy_(proxy, bstack111l11lll_opy_())
                if len(proxies) > 0:
                    protocol, bstack11l111l11_opy_ = proxies.popitem()
                    if bstack1llll1l_opy_ (u"ࠨ࠺࠰࠱ࠥស") in bstack11l111l11_opy_:
                        return bstack11l111l11_opy_
                    else:
                        return bstack1llll1l_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣហ") + bstack11l111l11_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack1llll1l_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡵࡸ࡯ࡹࡻࠣࡹࡷࡲࠠ࠻ࠢࡾࢁࠧឡ").format(str(e)))
    return bstack1l1ll1l1l_opy_(self)
def bstack1ll1l1lll1_opy_():
    return (bstack1llll1l_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬអ") in CONFIG or bstack1llll1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧឣ") in CONFIG) and bstack1l11l1llll_opy_() and bstack111l11l1_opy_() >= version.parse(
        bstack1llll11ll1_opy_)
def bstack11111l1l1_opy_(self,
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
    global bstack1111111ll_opy_
    global bstack1ll11l111_opy_
    global bstack1ll1llll_opy_
    CONFIG[bstack1llll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭ឤ")] = str(bstack1ll1llll_opy_) + str(__version__)
    bstack1l1l11l11_opy_ = 0
    try:
        if bstack1ll11l111_opy_ is True:
            bstack1l1l11l11_opy_ = int(os.environ.get(bstack1llll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬឥ")))
    except:
        bstack1l1l11l11_opy_ = 0
    CONFIG[bstack1llll1l_opy_ (u"ࠨࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧឦ")] = True
    bstack1lll1ll1_opy_ = bstack1l1lll1l_opy_(CONFIG, bstack1l1l11l11_opy_)
    logger.debug(bstack1111ll111_opy_.format(str(bstack1lll1ll1_opy_)))
    if CONFIG.get(bstack1llll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫឧ")):
        bstack1lllllll11_opy_(bstack1lll1ll1_opy_, bstack11ll1ll11_opy_)
    if bstack1llll1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫឨ") in CONFIG and bstack1llll1l_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧឩ") in CONFIG[bstack1llll1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ឪ")][bstack1l1l11l11_opy_]:
        bstack1111111ll_opy_ = CONFIG[bstack1llll1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧឫ")][bstack1l1l11l11_opy_][bstack1llll1l_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪឬ")]
    import urllib
    import json
    bstack11l11l11_opy_ = bstack1llll1l_opy_ (u"࠭ࡷࡴࡵ࠽࠳࠴ࡩࡤࡱ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡁࡦࡥࡵࡹ࠽ࠨឭ") + urllib.parse.quote(json.dumps(bstack1lll1ll1_opy_))
    browser = self.connect(bstack11l11l11_opy_)
    return browser
def bstack1ll1lll1l_opy_():
    global bstack1l1111lll_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        BrowserType.launch = bstack11111l1l1_opy_
        bstack1l1111lll_opy_ = True
    except Exception as e:
        pass
def bstack1lll11ll111_opy_():
    global CONFIG
    global bstack1l1l11111l_opy_
    global bstack111lll1l_opy_
    global bstack11ll1ll11_opy_
    global bstack1ll11l111_opy_
    global bstack1ll1l11l1l_opy_
    CONFIG = json.loads(os.environ.get(bstack1llll1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌ࠭ឮ")))
    bstack1l1l11111l_opy_ = eval(os.environ.get(bstack1llll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩឯ")))
    bstack111lll1l_opy_ = os.environ.get(bstack1llll1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡊࡘࡆࡤ࡛ࡒࡍࠩឰ"))
    bstack111111l1_opy_(CONFIG, bstack1l1l11111l_opy_)
    bstack1ll1l11l1l_opy_ = bstack1ll1l1ll_opy_.bstack1ll1l111l_opy_(CONFIG, bstack1ll1l11l1l_opy_)
    global bstack1l1l1l1l11_opy_
    global bstack111l11l1l_opy_
    global bstack1lllll1lll_opy_
    global bstack1l11llll11_opy_
    global bstack1l11llllll_opy_
    global bstack1ll1l11ll_opy_
    global bstack1lll1ll1ll_opy_
    global bstack11l1l1ll_opy_
    global bstack1l1ll1l1l_opy_
    global bstack111l1111_opy_
    global bstack1llll111ll_opy_
    global bstack1llll1ll1_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack1l1l1l1l11_opy_ = webdriver.Remote.__init__
        bstack111l11l1l_opy_ = WebDriver.quit
        bstack1lll1ll1ll_opy_ = WebDriver.close
        bstack11l1l1ll_opy_ = WebDriver.get
    except Exception as e:
        pass
    if (bstack1llll1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ឱ") in CONFIG or bstack1llll1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨឲ") in CONFIG) and bstack1l11l1llll_opy_():
        if bstack111l11l1_opy_() < version.parse(bstack1llll11ll1_opy_):
            logger.error(bstack1l1ll1l11_opy_.format(bstack111l11l1_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                bstack1l1ll1l1l_opy_ = RemoteConnection._get_proxy_url
            except Exception as e:
                logger.error(bstack11ll11lll_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack111l1111_opy_ = Config.getoption
        from _pytest import runner
        bstack1llll111ll_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warn(e, bstack1lllll11ll_opy_)
    try:
        from pytest_bdd import reporting
        bstack1llll1ll1_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstack1llll1l_opy_ (u"ࠬࡖ࡬ࡦࡣࡶࡩࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡴࠦࡲࡶࡰࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡧࡶࡸࡸ࠭ឳ"))
    bstack11ll1ll11_opy_ = CONFIG.get(bstack1llll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ឴"), {}).get(bstack1llll1l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ឵"))
    bstack1ll11l111_opy_ = True
    bstack1111l1l1l_opy_(bstack111l1llll_opy_)
if (bstack11l11ll1l1_opy_()):
    bstack1lll11ll111_opy_()
@bstack1l111l1111_opy_(class_method=False)
def bstack1lll111llll_opy_(hook_name, event, bstack1lll11lll11_opy_=None):
    if hook_name not in [bstack1llll1l_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩា"), bstack1llll1l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭ិ"), bstack1llll1l_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࠩី"), bstack1llll1l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪ࠭ឹ"), bstack1llll1l_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡨࡲࡡࡴࡵࠪឺ"), bstack1llll1l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡥ࡯ࡥࡸࡹࠧុ"), bstack1llll1l_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡦࡶ࡫ࡳࡩ࠭ូ"), bstack1llll1l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡪࡺࡨࡰࡦࠪួ")]:
        return
    node = store[bstack1llll1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠ࡫ࡷࡩࡲ࠭ើ")]
    if hook_name in [bstack1llll1l_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࠩឿ"), bstack1llll1l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪ࠭ៀ")]:
        node = store[bstack1llll1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥ࡭ࡰࡦࡸࡰࡪࡥࡩࡵࡧࡰࠫេ")]
    elif hook_name in [bstack1llll1l_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠫែ"), bstack1llll1l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡦࡰࡦࡹࡳࠨៃ")]:
        node = store[bstack1llll1l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡦࡰࡦࡹࡳࡠ࡫ࡷࡩࡲ࠭ោ")]
    if event == bstack1llll1l_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࠩៅ"):
        hook_type = bstack1llllll1l1l_opy_(hook_name)
        uuid = uuid4().__str__()
        bstack11lllllll1_opy_ = {
            bstack1llll1l_opy_ (u"ࠪࡹࡺ࡯ࡤࠨំ"): uuid,
            bstack1llll1l_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨះ"): bstack1l1l1llll_opy_(),
            bstack1llll1l_opy_ (u"ࠬࡺࡹࡱࡧࠪៈ"): bstack1llll1l_opy_ (u"࠭ࡨࡰࡱ࡮ࠫ៉"),
            bstack1llll1l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪ៊"): hook_type,
            bstack1llll1l_opy_ (u"ࠨࡪࡲࡳࡰࡥ࡮ࡢ࡯ࡨࠫ់"): hook_name
        }
        store[bstack1llll1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭៌")].append(uuid)
        bstack1lll1l1l111_opy_ = node.nodeid
        if hook_type == bstack1llll1l_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠨ៍"):
            if not _1l111lllll_opy_.get(bstack1lll1l1l111_opy_, None):
                _1l111lllll_opy_[bstack1lll1l1l111_opy_] = {bstack1llll1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ៎"): []}
            _1l111lllll_opy_[bstack1lll1l1l111_opy_][bstack1llll1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ៏")].append(bstack11lllllll1_opy_[bstack1llll1l_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ័")])
        _1l111lllll_opy_[bstack1lll1l1l111_opy_ + bstack1llll1l_opy_ (u"ࠧ࠮ࠩ៑") + hook_name] = bstack11lllllll1_opy_
        bstack1lll11l11l1_opy_(node, bstack11lllllll1_opy_, bstack1llll1l_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥ្ࠩ"))
    elif event == bstack1llll1l_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࠨ៓"):
        bstack11llll1l1l_opy_ = node.nodeid + bstack1llll1l_opy_ (u"ࠪ࠱ࠬ។") + hook_name
        _1l111lllll_opy_[bstack11llll1l1l_opy_][bstack1llll1l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ៕")] = bstack1l1l1llll_opy_()
        bstack1lll1l1ll1l_opy_(_1l111lllll_opy_[bstack11llll1l1l_opy_][bstack1llll1l_opy_ (u"ࠬࡻࡵࡪࡦࠪ៖")])
        bstack1lll11l11l1_opy_(node, _1l111lllll_opy_[bstack11llll1l1l_opy_], bstack1llll1l_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨៗ"), bstack1lll111lll1_opy_=bstack1lll11lll11_opy_)
def bstack1lll1l1111l_opy_():
    global bstack1lll111ll1l_opy_
    if bstack1ll1l11l1_opy_():
        bstack1lll111ll1l_opy_ = bstack1llll1l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠫ៘")
    else:
        bstack1lll111ll1l_opy_ = bstack1llll1l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ៙")
@bstack1ll1ll111l_opy_.bstack1lll1lllll1_opy_
def bstack1lll11ll1ll_opy_():
    bstack1lll1l1111l_opy_()
    if bstack1l11l1llll_opy_():
        bstack11l11111l_opy_(bstack111l1l11_opy_)
    bstack111ll111ll_opy_ = bstack111l1llll1_opy_(bstack1lll111llll_opy_)
bstack1lll11ll1ll_opy_()