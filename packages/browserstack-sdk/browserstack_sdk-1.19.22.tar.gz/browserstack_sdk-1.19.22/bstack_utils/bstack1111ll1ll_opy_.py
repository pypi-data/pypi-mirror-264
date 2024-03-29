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
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.helper import bstack111lll11ll_opy_, bstack1llll1ll_opy_, bstack1l1l111l1l_opy_, bstack1lll1ll1l_opy_, \
    bstack11l11111ll_opy_
def bstack1l1l111lll_opy_(bstack1llll1ll1ll_opy_):
    for driver in bstack1llll1ll1ll_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1111ll11_opy_(driver, status, reason=bstack1ll11l_opy_ (u"ࠩࠪᑶ")):
    bstack1l11l111l_opy_ = Config.bstack1l11llll1l_opy_()
    if bstack1l11l111l_opy_.bstack11lll1111l_opy_():
        return
    bstack11111lll_opy_ = bstack1ll11lllll_opy_(bstack1ll11l_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭ᑷ"), bstack1ll11l_opy_ (u"ࠫࠬᑸ"), status, reason, bstack1ll11l_opy_ (u"ࠬ࠭ᑹ"), bstack1ll11l_opy_ (u"࠭ࠧᑺ"))
    driver.execute_script(bstack11111lll_opy_)
def bstack11l1ll11l_opy_(page, status, reason=bstack1ll11l_opy_ (u"ࠧࠨᑻ")):
    try:
        if page is None:
            return
        bstack1l11l111l_opy_ = Config.bstack1l11llll1l_opy_()
        if bstack1l11l111l_opy_.bstack11lll1111l_opy_():
            return
        bstack11111lll_opy_ = bstack1ll11lllll_opy_(bstack1ll11l_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫᑼ"), bstack1ll11l_opy_ (u"ࠩࠪᑽ"), status, reason, bstack1ll11l_opy_ (u"ࠪࠫᑾ"), bstack1ll11l_opy_ (u"ࠫࠬᑿ"))
        page.evaluate(bstack1ll11l_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨᒀ"), bstack11111lll_opy_)
    except Exception as e:
        print(bstack1ll11l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡧࡱࡵࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡽࢀࠦᒁ"), e)
def bstack1ll11lllll_opy_(type, name, status, reason, bstack1ll1lll11l_opy_, bstack11l1llll_opy_):
    bstack111lll1l1_opy_ = {
        bstack1ll11l_opy_ (u"ࠧࡢࡥࡷ࡭ࡴࡴࠧᒂ"): type,
        bstack1ll11l_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᒃ"): {}
    }
    if type == bstack1ll11l_opy_ (u"ࠩࡤࡲࡳࡵࡴࡢࡶࡨࠫᒄ"):
        bstack111lll1l1_opy_[bstack1ll11l_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ᒅ")][bstack1ll11l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪᒆ")] = bstack1ll1lll11l_opy_
        bstack111lll1l1_opy_[bstack1ll11l_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨᒇ")][bstack1ll11l_opy_ (u"࠭ࡤࡢࡶࡤࠫᒈ")] = json.dumps(str(bstack11l1llll_opy_))
    if type == bstack1ll11l_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨᒉ"):
        bstack111lll1l1_opy_[bstack1ll11l_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᒊ")][bstack1ll11l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᒋ")] = name
    if type == bstack1ll11l_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭ᒌ"):
        bstack111lll1l1_opy_[bstack1ll11l_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᒍ")][bstack1ll11l_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬᒎ")] = status
        if status == bstack1ll11l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᒏ") and str(reason) != bstack1ll11l_opy_ (u"ࠢࠣᒐ"):
            bstack111lll1l1_opy_[bstack1ll11l_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᒑ")][bstack1ll11l_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩᒒ")] = json.dumps(str(reason))
    bstack1l1111111_opy_ = bstack1ll11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠨᒓ").format(json.dumps(bstack111lll1l1_opy_))
    return bstack1l1111111_opy_
def bstack1lll1ll1l1_opy_(url, config, logger, bstack1ll11llll1_opy_=False):
    hostname = bstack1llll1ll_opy_(url)
    is_private = bstack1lll1ll1l_opy_(hostname)
    try:
        if is_private or bstack1ll11llll1_opy_:
            file_path = bstack111lll11ll_opy_(bstack1ll11l_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫᒔ"), bstack1ll11l_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫᒕ"), logger)
            if os.environ.get(bstack1ll11l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡓࡕࡔࡠࡕࡈࡘࡤࡋࡒࡓࡑࡕࠫᒖ")) and eval(
                    os.environ.get(bstack1ll11l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡔࡏࡕࡡࡖࡉ࡙ࡥࡅࡓࡔࡒࡖࠬᒗ"))):
                return
            if (bstack1ll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬᒘ") in config and not config[bstack1ll11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ᒙ")]):
                os.environ[bstack1ll11l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡐࡒࡘࡤ࡙ࡅࡕࡡࡈࡖࡗࡕࡒࠨᒚ")] = str(True)
                bstack1llll1lll11_opy_ = {bstack1ll11l_opy_ (u"ࠫ࡭ࡵࡳࡵࡰࡤࡱࡪ࠭ᒛ"): hostname}
                bstack11l11111ll_opy_(bstack1ll11l_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫᒜ"), bstack1ll11l_opy_ (u"࠭࡮ࡶࡦࡪࡩࡤࡲ࡯ࡤࡣ࡯ࠫᒝ"), bstack1llll1lll11_opy_, logger)
    except Exception as e:
        pass
def bstack1l111l11l_opy_(caps, bstack1llll1llll1_opy_):
    if bstack1ll11l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᒞ") in caps:
        caps[bstack1ll11l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᒟ")][bstack1ll11l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࠨᒠ")] = True
        if bstack1llll1llll1_opy_:
            caps[bstack1ll11l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᒡ")][bstack1ll11l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᒢ")] = bstack1llll1llll1_opy_
    else:
        caps[bstack1ll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࠪᒣ")] = True
        if bstack1llll1llll1_opy_:
            caps[bstack1ll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᒤ")] = bstack1llll1llll1_opy_
def bstack1llllll11ll_opy_(bstack1l11111lll_opy_):
    bstack1llll1lll1l_opy_ = bstack1l1l111l1l_opy_(threading.current_thread(), bstack1ll11l_opy_ (u"ࠧࡵࡧࡶࡸࡘࡺࡡࡵࡷࡶࠫᒥ"), bstack1ll11l_opy_ (u"ࠨࠩᒦ"))
    if bstack1llll1lll1l_opy_ == bstack1ll11l_opy_ (u"ࠩࠪᒧ") or bstack1llll1lll1l_opy_ == bstack1ll11l_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫᒨ"):
        threading.current_thread().testStatus = bstack1l11111lll_opy_
    else:
        if bstack1l11111lll_opy_ == bstack1ll11l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᒩ"):
            threading.current_thread().testStatus = bstack1l11111lll_opy_