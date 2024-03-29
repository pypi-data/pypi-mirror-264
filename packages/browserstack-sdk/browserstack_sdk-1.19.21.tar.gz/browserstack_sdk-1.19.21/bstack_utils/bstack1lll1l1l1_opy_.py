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
import re
from bstack_utils.bstack1l1l1ll11l_opy_ import bstack1lllll1lll1_opy_
def bstack1llllll1ll1_opy_(fixture_name):
    if fixture_name.startswith(bstack1llll1l_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᑁ")):
        return bstack1llll1l_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧᑂ")
    elif fixture_name.startswith(bstack1llll1l_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᑃ")):
        return bstack1llll1l_opy_ (u"ࠨࡵࡨࡸࡺࡶ࠭࡮ࡱࡧࡹࡱ࡫ࠧᑄ")
    elif fixture_name.startswith(bstack1llll1l_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᑅ")):
        return bstack1llll1l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧᑆ")
    elif fixture_name.startswith(bstack1llll1l_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᑇ")):
        return bstack1llll1l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭࡮ࡱࡧࡹࡱ࡫ࠧᑈ")
def bstack1llllll11ll_opy_(fixture_name):
    return bool(re.match(bstack1llll1l_opy_ (u"࠭࡞ࡠࡺࡸࡲ࡮ࡺ࡟ࠩࡵࡨࡸࡺࡶࡼࡵࡧࡤࡶࡩࡵࡷ࡯ࠫࡢࠬ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࢂ࡭ࡰࡦࡸࡰࡪ࠯࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠ࠰࠭ࠫᑉ"), fixture_name))
def bstack1lllllll111_opy_(fixture_name):
    return bool(re.match(bstack1llll1l_opy_ (u"ࠧ࡟ࡡࡻࡹࡳ࡯ࡴࡠࠪࡶࡩࡹࡻࡰࡽࡶࡨࡥࡷࡪ࡯ࡸࡰࠬࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࠴ࠪࠨᑊ"), fixture_name))
def bstack1lllll1llll_opy_(fixture_name):
    return bool(re.match(bstack1llll1l_opy_ (u"ࠨࡠࡢࡼࡺࡴࡩࡵࡡࠫࡷࡪࡺࡵࡱࡾࡷࡩࡦࡸࡤࡰࡹࡱ࠭ࡤࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࠴ࠪࠨᑋ"), fixture_name))
def bstack1llllll1lll_opy_(fixture_name):
    if fixture_name.startswith(bstack1llll1l_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᑌ")):
        return bstack1llll1l_opy_ (u"ࠪࡷࡪࡺࡵࡱ࠯ࡩࡹࡳࡩࡴࡪࡱࡱࠫᑍ"), bstack1llll1l_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩᑎ")
    elif fixture_name.startswith(bstack1llll1l_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᑏ")):
        return bstack1llll1l_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲ࡳ࡯ࡥࡷ࡯ࡩࠬᑐ"), bstack1llll1l_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏࠫᑑ")
    elif fixture_name.startswith(bstack1llll1l_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᑒ")):
        return bstack1llll1l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱ࠱࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭ᑓ"), bstack1llll1l_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧᑔ")
    elif fixture_name.startswith(bstack1llll1l_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᑕ")):
        return bstack1llll1l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭࡮ࡱࡧࡹࡱ࡫ࠧᑖ"), bstack1llll1l_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡇࡌࡍࠩᑗ")
    return None, None
def bstack1lllll1l1ll_opy_(hook_name):
    if hook_name in [bstack1llll1l_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ᑘ"), bstack1llll1l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪᑙ")]:
        return hook_name.capitalize()
    return hook_name
def bstack1llllll1l1l_opy_(hook_name):
    if hook_name in [bstack1llll1l_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࠪᑚ"), bstack1llll1l_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡩࡹ࡮࡯ࡥࠩᑛ")]:
        return bstack1llll1l_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩᑜ")
    elif hook_name in [bstack1llll1l_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲࡵࡤࡶ࡮ࡨࠫᑝ"), bstack1llll1l_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡩ࡬ࡢࡵࡶࠫᑞ")]:
        return bstack1llll1l_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏࠫᑟ")
    elif hook_name in [bstack1llll1l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠬᑠ"), bstack1llll1l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧࠫᑡ")]:
        return bstack1llll1l_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧᑢ")
    elif hook_name in [bstack1llll1l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪ࠭ᑣ"), bstack1llll1l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡤ࡮ࡤࡷࡸ࠭ᑤ")]:
        return bstack1llll1l_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡇࡌࡍࠩᑥ")
    return hook_name
def bstack1lllll1ll1l_opy_(node, scenario):
    if hasattr(node, bstack1llll1l_opy_ (u"ࠧࡤࡣ࡯ࡰࡸࡶࡥࡤࠩᑦ")):
        parts = node.nodeid.rsplit(bstack1llll1l_opy_ (u"ࠣ࡝ࠥᑧ"))
        params = parts[-1]
        return bstack1llll1l_opy_ (u"ࠤࡾࢁࠥࡡࡻࡾࠤᑨ").format(scenario.name, params)
    return scenario.name
def bstack1lllll1ll11_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack1llll1l_opy_ (u"ࠪࡧࡦࡲ࡬ࡴࡲࡨࡧࠬᑩ")):
            examples = list(node.callspec.params[bstack1llll1l_opy_ (u"ࠫࡤࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡨࡼࡦࡳࡰ࡭ࡧࠪᑪ")].values())
        return examples
    except:
        return []
def bstack1llllll1111_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack1llllll111l_opy_(report):
    try:
        status = bstack1llll1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᑫ")
        if report.passed or (report.failed and hasattr(report, bstack1llll1l_opy_ (u"ࠨࡷࡢࡵࡻࡪࡦ࡯࡬ࠣᑬ"))):
            status = bstack1llll1l_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᑭ")
        elif report.skipped:
            status = bstack1llll1l_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩᑮ")
        bstack1lllll1lll1_opy_(status)
    except:
        pass
def bstack111ll1111_opy_(status):
    try:
        bstack1llllll11l1_opy_ = bstack1llll1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᑯ")
        if status == bstack1llll1l_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᑰ"):
            bstack1llllll11l1_opy_ = bstack1llll1l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᑱ")
        elif status == bstack1llll1l_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ᑲ"):
            bstack1llllll11l1_opy_ = bstack1llll1l_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧᑳ")
        bstack1lllll1lll1_opy_(bstack1llllll11l1_opy_)
    except:
        pass
def bstack1llllll1l11_opy_(item=None, report=None, summary=None, extra=None):
    return