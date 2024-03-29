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
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.helper import bstack111lll11l1_opy_, bstack1ll1111ll_opy_, bstack11lll11ll_opy_, bstack11l11lll_opy_, \
    bstack11l111ll11_opy_
def bstack1l1l111l1l_opy_(bstack1llll1llll1_opy_):
    for driver in bstack1llll1llll1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1lll1l11ll_opy_(driver, status, reason=bstack1l_opy_ (u"ࠩࠪᑶ")):
    bstack1l1l1l1l1l_opy_ = Config.bstack1l1l1lll1l_opy_()
    if bstack1l1l1l1l1l_opy_.bstack11ll1ll11l_opy_():
        return
    bstack11l1l1l11_opy_ = bstack1lllllll1l_opy_(bstack1l_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭ᑷ"), bstack1l_opy_ (u"ࠫࠬᑸ"), status, reason, bstack1l_opy_ (u"ࠬ࠭ᑹ"), bstack1l_opy_ (u"࠭ࠧᑺ"))
    driver.execute_script(bstack11l1l1l11_opy_)
def bstack1lll1ll11l_opy_(page, status, reason=bstack1l_opy_ (u"ࠧࠨᑻ")):
    try:
        if page is None:
            return
        bstack1l1l1l1l1l_opy_ = Config.bstack1l1l1lll1l_opy_()
        if bstack1l1l1l1l1l_opy_.bstack11ll1ll11l_opy_():
            return
        bstack11l1l1l11_opy_ = bstack1lllllll1l_opy_(bstack1l_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫᑼ"), bstack1l_opy_ (u"ࠩࠪᑽ"), status, reason, bstack1l_opy_ (u"ࠪࠫᑾ"), bstack1l_opy_ (u"ࠫࠬᑿ"))
        page.evaluate(bstack1l_opy_ (u"ࠧࡥࠠ࠾ࡀࠣࡿࢂࠨᒀ"), bstack11l1l1l11_opy_)
    except Exception as e:
        print(bstack1l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡧࡱࡵࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡽࢀࠦᒁ"), e)
def bstack1lllllll1l_opy_(type, name, status, reason, bstack1111111ll_opy_, bstack1l1l1l11ll_opy_):
    bstack11l1ll1l_opy_ = {
        bstack1l_opy_ (u"ࠧࡢࡥࡷ࡭ࡴࡴࠧᒂ"): type,
        bstack1l_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᒃ"): {}
    }
    if type == bstack1l_opy_ (u"ࠩࡤࡲࡳࡵࡴࡢࡶࡨࠫᒄ"):
        bstack11l1ll1l_opy_[bstack1l_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ᒅ")][bstack1l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪᒆ")] = bstack1111111ll_opy_
        bstack11l1ll1l_opy_[bstack1l_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨᒇ")][bstack1l_opy_ (u"࠭ࡤࡢࡶࡤࠫᒈ")] = json.dumps(str(bstack1l1l1l11ll_opy_))
    if type == bstack1l_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨᒉ"):
        bstack11l1ll1l_opy_[bstack1l_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᒊ")][bstack1l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᒋ")] = name
    if type == bstack1l_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭ᒌ"):
        bstack11l1ll1l_opy_[bstack1l_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᒍ")][bstack1l_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬᒎ")] = status
        if status == bstack1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᒏ") and str(reason) != bstack1l_opy_ (u"ࠢࠣᒐ"):
            bstack11l1ll1l_opy_[bstack1l_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᒑ")][bstack1l_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩᒒ")] = json.dumps(str(reason))
    bstack1lll1l1l1_opy_ = bstack1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠨᒓ").format(json.dumps(bstack11l1ll1l_opy_))
    return bstack1lll1l1l1_opy_
def bstack11l1ll111_opy_(url, config, logger, bstack1lll111l_opy_=False):
    hostname = bstack1ll1111ll_opy_(url)
    is_private = bstack11l11lll_opy_(hostname)
    try:
        if is_private or bstack1lll111l_opy_:
            file_path = bstack111lll11l1_opy_(bstack1l_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫᒔ"), bstack1l_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫᒕ"), logger)
            if os.environ.get(bstack1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡓࡕࡔࡠࡕࡈࡘࡤࡋࡒࡓࡑࡕࠫᒖ")) and eval(
                    os.environ.get(bstack1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡔࡏࡕࡡࡖࡉ࡙ࡥࡅࡓࡔࡒࡖࠬᒗ"))):
                return
            if (bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬᒘ") in config and not config[bstack1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ᒙ")]):
                os.environ[bstack1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡐࡒࡘࡤ࡙ࡅࡕࡡࡈࡖࡗࡕࡒࠨᒚ")] = str(True)
                bstack1llll1lll1l_opy_ = {bstack1l_opy_ (u"ࠫ࡭ࡵࡳࡵࡰࡤࡱࡪ࠭ᒛ"): hostname}
                bstack11l111ll11_opy_(bstack1l_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫᒜ"), bstack1l_opy_ (u"࠭࡮ࡶࡦࡪࡩࡤࡲ࡯ࡤࡣ࡯ࠫᒝ"), bstack1llll1lll1l_opy_, logger)
    except Exception as e:
        pass
def bstack1111l1111_opy_(caps, bstack1llll1lll11_opy_):
    if bstack1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᒞ") in caps:
        caps[bstack1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᒟ")][bstack1l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࠨᒠ")] = True
        if bstack1llll1lll11_opy_:
            caps[bstack1l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᒡ")][bstack1l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᒢ")] = bstack1llll1lll11_opy_
    else:
        caps[bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࠪᒣ")] = True
        if bstack1llll1lll11_opy_:
            caps[bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᒤ")] = bstack1llll1lll11_opy_
def bstack1llllll1l11_opy_(bstack11lll11lll_opy_):
    bstack1llll1ll1ll_opy_ = bstack11lll11ll_opy_(threading.current_thread(), bstack1l_opy_ (u"ࠧࡵࡧࡶࡸࡘࡺࡡࡵࡷࡶࠫᒥ"), bstack1l_opy_ (u"ࠨࠩᒦ"))
    if bstack1llll1ll1ll_opy_ == bstack1l_opy_ (u"ࠩࠪᒧ") or bstack1llll1ll1ll_opy_ == bstack1l_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫᒨ"):
        threading.current_thread().testStatus = bstack11lll11lll_opy_
    else:
        if bstack11lll11lll_opy_ == bstack1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᒩ"):
            threading.current_thread().testStatus = bstack11lll11lll_opy_