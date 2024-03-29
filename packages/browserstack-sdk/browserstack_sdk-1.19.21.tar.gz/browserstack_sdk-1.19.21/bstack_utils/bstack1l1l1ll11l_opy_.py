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
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.helper import bstack111lll1ll1_opy_, bstack11l11ll11_opy_, bstack1lll11l111_opy_, bstack11lll1ll_opy_, \
    bstack11l11ll111_opy_
def bstack1l1llll11l_opy_(bstack1llll1l1lll_opy_):
    for driver in bstack1llll1l1lll_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1ll11lll1l_opy_(driver, status, reason=bstack1llll1l_opy_ (u"ࠩࠪᑶ")):
    bstack1l1lll1ll1_opy_ = Config.bstack11ll1ll1_opy_()
    if bstack1l1lll1ll1_opy_.bstack11ll1lll11_opy_():
        return
    bstack1llll11l1_opy_ = bstack11l111l1l_opy_(bstack1llll1l_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭ᑷ"), bstack1llll1l_opy_ (u"ࠫࠬᑸ"), status, reason, bstack1llll1l_opy_ (u"ࠬ࠭ᑹ"), bstack1llll1l_opy_ (u"࠭ࠧᑺ"))
    driver.execute_script(bstack1llll11l1_opy_)
def bstack1l1l1111_opy_(page, status, reason=bstack1llll1l_opy_ (u"ࠧࠨᑻ")):
    try:
        if page is None:
            return
        bstack1l1lll1ll1_opy_ = Config.bstack11ll1ll1_opy_()
        if bstack1l1lll1ll1_opy_.bstack11ll1lll11_opy_():
            return
        bstack1llll11l1_opy_ = bstack11l111l1l_opy_(bstack1llll1l_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫᑼ"), bstack1llll1l_opy_ (u"ࠩࠪᑽ"), status, reason, bstack1llll1l_opy_ (u"ࠪࠫᑾ"), bstack1llll1l_opy_ (u"ࠫࠬᑿ"))
        page.evaluate(bstack1llll1l_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨᒀ"), bstack1llll11l1_opy_)
    except Exception as e:
        print(bstack1llll1l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡧࡱࡵࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡽࢀࠦᒁ"), e)
def bstack11l111l1l_opy_(type, name, status, reason, bstack1l1llll1l_opy_, bstack1l1l11ll1l_opy_):
    bstack11l1llll_opy_ = {
        bstack1llll1l_opy_ (u"ࠧࡢࡥࡷ࡭ࡴࡴࠧᒂ"): type,
        bstack1llll1l_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᒃ"): {}
    }
    if type == bstack1llll1l_opy_ (u"ࠩࡤࡲࡳࡵࡴࡢࡶࡨࠫᒄ"):
        bstack11l1llll_opy_[bstack1llll1l_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ᒅ")][bstack1llll1l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪᒆ")] = bstack1l1llll1l_opy_
        bstack11l1llll_opy_[bstack1llll1l_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨᒇ")][bstack1llll1l_opy_ (u"࠭ࡤࡢࡶࡤࠫᒈ")] = json.dumps(str(bstack1l1l11ll1l_opy_))
    if type == bstack1llll1l_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨᒉ"):
        bstack11l1llll_opy_[bstack1llll1l_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᒊ")][bstack1llll1l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᒋ")] = name
    if type == bstack1llll1l_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭ᒌ"):
        bstack11l1llll_opy_[bstack1llll1l_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᒍ")][bstack1llll1l_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬᒎ")] = status
        if status == bstack1llll1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᒏ") and str(reason) != bstack1llll1l_opy_ (u"ࠢࠣᒐ"):
            bstack11l1llll_opy_[bstack1llll1l_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᒑ")][bstack1llll1l_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩᒒ")] = json.dumps(str(reason))
    bstack1l11l1ll1_opy_ = bstack1llll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠨᒓ").format(json.dumps(bstack11l1llll_opy_))
    return bstack1l11l1ll1_opy_
def bstack11lllll1_opy_(url, config, logger, bstack111l111l1_opy_=False):
    hostname = bstack11l11ll11_opy_(url)
    is_private = bstack11lll1ll_opy_(hostname)
    try:
        if is_private or bstack111l111l1_opy_:
            file_path = bstack111lll1ll1_opy_(bstack1llll1l_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫᒔ"), bstack1llll1l_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫᒕ"), logger)
            if os.environ.get(bstack1llll1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡓࡕࡔࡠࡕࡈࡘࡤࡋࡒࡓࡑࡕࠫᒖ")) and eval(
                    os.environ.get(bstack1llll1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡔࡏࡕࡡࡖࡉ࡙ࡥࡅࡓࡔࡒࡖࠬᒗ"))):
                return
            if (bstack1llll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬᒘ") in config and not config[bstack1llll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ᒙ")]):
                os.environ[bstack1llll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡐࡒࡘࡤ࡙ࡅࡕࡡࡈࡖࡗࡕࡒࠨᒚ")] = str(True)
                bstack1llll1ll111_opy_ = {bstack1llll1l_opy_ (u"ࠫ࡭ࡵࡳࡵࡰࡤࡱࡪ࠭ᒛ"): hostname}
                bstack11l11ll111_opy_(bstack1llll1l_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫᒜ"), bstack1llll1l_opy_ (u"࠭࡮ࡶࡦࡪࡩࡤࡲ࡯ࡤࡣ࡯ࠫᒝ"), bstack1llll1ll111_opy_, logger)
    except Exception as e:
        pass
def bstack1lllllll11_opy_(caps, bstack1llll1ll11l_opy_):
    if bstack1llll1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᒞ") in caps:
        caps[bstack1llll1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᒟ")][bstack1llll1l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࠨᒠ")] = True
        if bstack1llll1ll11l_opy_:
            caps[bstack1llll1l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᒡ")][bstack1llll1l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᒢ")] = bstack1llll1ll11l_opy_
    else:
        caps[bstack1llll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࠪᒣ")] = True
        if bstack1llll1ll11l_opy_:
            caps[bstack1llll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᒤ")] = bstack1llll1ll11l_opy_
def bstack1lllll1lll1_opy_(bstack1l111l1l1l_opy_):
    bstack1llll1ll1l1_opy_ = bstack1lll11l111_opy_(threading.current_thread(), bstack1llll1l_opy_ (u"ࠧࡵࡧࡶࡸࡘࡺࡡࡵࡷࡶࠫᒥ"), bstack1llll1l_opy_ (u"ࠨࠩᒦ"))
    if bstack1llll1ll1l1_opy_ == bstack1llll1l_opy_ (u"ࠩࠪᒧ") or bstack1llll1ll1l1_opy_ == bstack1llll1l_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫᒨ"):
        threading.current_thread().testStatus = bstack1l111l1l1l_opy_
    else:
        if bstack1l111l1l1l_opy_ == bstack1llll1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᒩ"):
            threading.current_thread().testStatus = bstack1l111l1l1l_opy_