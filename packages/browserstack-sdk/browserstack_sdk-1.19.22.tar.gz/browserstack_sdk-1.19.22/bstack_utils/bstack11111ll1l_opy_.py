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
import re
from bstack_utils.bstack1111ll1ll_opy_ import bstack1llllll11ll_opy_
def bstack1llllll111l_opy_(fixture_name):
    if fixture_name.startswith(bstack1ll11l_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᑁ")):
        return bstack1ll11l_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧᑂ")
    elif fixture_name.startswith(bstack1ll11l_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᑃ")):
        return bstack1ll11l_opy_ (u"ࠨࡵࡨࡸࡺࡶ࠭࡮ࡱࡧࡹࡱ࡫ࠧᑄ")
    elif fixture_name.startswith(bstack1ll11l_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᑅ")):
        return bstack1ll11l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧᑆ")
    elif fixture_name.startswith(bstack1ll11l_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᑇ")):
        return bstack1ll11l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭࡮ࡱࡧࡹࡱ࡫ࠧᑈ")
def bstack1lllllll11l_opy_(fixture_name):
    return bool(re.match(bstack1ll11l_opy_ (u"࠭࡞ࡠࡺࡸࡲ࡮ࡺ࡟ࠩࡵࡨࡸࡺࡶࡼࡵࡧࡤࡶࡩࡵࡷ࡯ࠫࡢࠬ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࢂ࡭ࡰࡦࡸࡰࡪ࠯࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠ࠰࠭ࠫᑉ"), fixture_name))
def bstack1llllll11l1_opy_(fixture_name):
    return bool(re.match(bstack1ll11l_opy_ (u"ࠧ࡟ࡡࡻࡹࡳ࡯ࡴࡠࠪࡶࡩࡹࡻࡰࡽࡶࡨࡥࡷࡪ࡯ࡸࡰࠬࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࠴ࠪࠨᑊ"), fixture_name))
def bstack1lllll1llll_opy_(fixture_name):
    return bool(re.match(bstack1ll11l_opy_ (u"ࠨࡠࡢࡼࡺࡴࡩࡵࡡࠫࡷࡪࡺࡵࡱࡾࡷࡩࡦࡸࡤࡰࡹࡱ࠭ࡤࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࠴ࠪࠨᑋ"), fixture_name))
def bstack1llllll1ll1_opy_(fixture_name):
    if fixture_name.startswith(bstack1ll11l_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᑌ")):
        return bstack1ll11l_opy_ (u"ࠪࡷࡪࡺࡵࡱ࠯ࡩࡹࡳࡩࡴࡪࡱࡱࠫᑍ"), bstack1ll11l_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩᑎ")
    elif fixture_name.startswith(bstack1ll11l_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᑏ")):
        return bstack1ll11l_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲ࡳ࡯ࡥࡷ࡯ࡩࠬᑐ"), bstack1ll11l_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏࠫᑑ")
    elif fixture_name.startswith(bstack1ll11l_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᑒ")):
        return bstack1ll11l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱ࠱࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭ᑓ"), bstack1ll11l_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧᑔ")
    elif fixture_name.startswith(bstack1ll11l_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᑕ")):
        return bstack1ll11l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭࡮ࡱࡧࡹࡱ࡫ࠧᑖ"), bstack1ll11l_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡇࡌࡍࠩᑗ")
    return None, None
def bstack1llllll1lll_opy_(hook_name):
    if hook_name in [bstack1ll11l_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ᑘ"), bstack1ll11l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪᑙ")]:
        return hook_name.capitalize()
    return hook_name
def bstack1lllllll1ll_opy_(hook_name):
    if hook_name in [bstack1ll11l_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࠪᑚ"), bstack1ll11l_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡩࡹ࡮࡯ࡥࠩᑛ")]:
        return bstack1ll11l_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩᑜ")
    elif hook_name in [bstack1ll11l_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠫᑝ"), bstack1ll11l_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠫᑞ")]:
        return bstack1ll11l_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏࠫᑟ")
    elif hook_name in [bstack1ll11l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠬᑠ"), bstack1ll11l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧࠫᑡ")]:
        return bstack1ll11l_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧᑢ")
    elif hook_name in [bstack1ll11l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪ࠭ᑣ"), bstack1ll11l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡤ࡮ࡤࡷࡸ࠭ᑤ")]:
        return bstack1ll11l_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡇࡌࡍࠩᑥ")
    return hook_name
def bstack1llllll1111_opy_(node, scenario):
    if hasattr(node, bstack1ll11l_opy_ (u"ࠧࡤࡣ࡯ࡰࡸࡶࡥࡤࠩᑦ")):
        parts = node.nodeid.rsplit(bstack1ll11l_opy_ (u"ࠣ࡝ࠥᑧ"))
        params = parts[-1]
        return bstack1ll11l_opy_ (u"ࠤࡾࢁࠥࡡࡻࡾࠤᑨ").format(scenario.name, params)
    return scenario.name
def bstack1llllll1l11_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack1ll11l_opy_ (u"ࠪࡧࡦࡲ࡬ࡴࡲࡨࡧࠬᑩ")):
            examples = list(node.callspec.params[bstack1ll11l_opy_ (u"ࠫࡤࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡨࡼࡦࡳࡰ࡭ࡧࠪᑪ")].values())
        return examples
    except:
        return []
def bstack1lllllll1l1_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack1llllllll11_opy_(report):
    try:
        status = bstack1ll11l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᑫ")
        if report.passed or (report.failed and hasattr(report, bstack1ll11l_opy_ (u"ࠨࡷࡢࡵࡻࡪࡦ࡯࡬ࠣᑬ"))):
            status = bstack1ll11l_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᑭ")
        elif report.skipped:
            status = bstack1ll11l_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩᑮ")
        bstack1llllll11ll_opy_(status)
    except:
        pass
def bstack1l1llll111_opy_(status):
    try:
        bstack1lllllll111_opy_ = bstack1ll11l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᑯ")
        if status == bstack1ll11l_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᑰ"):
            bstack1lllllll111_opy_ = bstack1ll11l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᑱ")
        elif status == bstack1ll11l_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ᑲ"):
            bstack1lllllll111_opy_ = bstack1ll11l_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧᑳ")
        bstack1llllll11ll_opy_(bstack1lllllll111_opy_)
    except:
        pass
def bstack1llllll1l1l_opy_(item=None, report=None, summary=None, extra=None):
    return