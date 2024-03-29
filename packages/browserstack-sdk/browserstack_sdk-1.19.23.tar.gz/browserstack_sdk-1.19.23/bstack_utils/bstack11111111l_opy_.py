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
import json
import requests
import logging
from urllib.parse import urlparse
from datetime import datetime
from bstack_utils.constants import bstack11ll11l111_opy_ as bstack11ll11l1l1_opy_
from bstack_utils.bstack1lll11111_opy_ import bstack1lll11111_opy_
from bstack_utils.helper import bstack1l11lll111_opy_, bstack1l1ll1111l_opy_, bstack11l1ll1lll_opy_, bstack11l1llllll_opy_, bstack111llll1l_opy_, get_host_info, bstack11ll11lll1_opy_, bstack1l1l1l11_opy_, bstack11llll1l11_opy_
from browserstack_sdk._version import __version__
logger = logging.getLogger(__name__)
@bstack11llll1l11_opy_(class_method=False)
def _11ll11l11l_opy_(driver, bstack11lll1ll_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack1l_opy_ (u"ࠨࡱࡶࡣࡳࡧ࡭ࡦࠩา"): caps.get(bstack1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠨำ"), None),
        bstack1l_opy_ (u"ࠪࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠧิ"): bstack11lll1ll_opy_.get(bstack1l_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠧี"), None),
        bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥ࡮ࡢ࡯ࡨࠫึ"): caps.get(bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫื"), None),
        bstack1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ุࠩ"): caps.get(bstack1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ูࠩ"), None)
    }
  except Exception as error:
    logger.debug(bstack1l_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡨࡨࡸࡨ࡮ࡩ࡯ࡩࠣࡴࡱࡧࡴࡧࡱࡵࡱࠥࡪࡥࡵࡣ࡬ࡰࡸࠦࡷࡪࡶ࡫ࠤࡪࡸࡲࡰࡴࠣ࠾ฺࠥ࠭") + str(error))
  return response
def bstack11llll1ll_opy_(config):
  return config.get(bstack1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ฻"), False) or any([p.get(bstack1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ฼"), False) == True for p in config.get(bstack1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ฽"), [])])
def bstack1ll1ll11_opy_(config, bstack1ll1l1lll1_opy_):
  try:
    if not bstack1l1ll1111l_opy_(config):
      return False
    bstack11l1llll11_opy_ = config.get(bstack1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭฾"), False)
    bstack11ll11ll11_opy_ = config[bstack1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ฿")][bstack1ll1l1lll1_opy_].get(bstack1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨเ"), None)
    if bstack11ll11ll11_opy_ != None:
      bstack11l1llll11_opy_ = bstack11ll11ll11_opy_
    bstack11ll11l1ll_opy_ = os.getenv(bstack1l_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧแ")) is not None and len(os.getenv(bstack1l_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨโ"))) > 0 and os.getenv(bstack1l_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩใ")) != bstack1l_opy_ (u"ࠬࡴࡵ࡭࡮ࠪไ")
    return bstack11l1llll11_opy_ and bstack11ll11l1ll_opy_
  except Exception as error:
    logger.debug(bstack1l_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡼࡥࡳ࡫ࡩࡽ࡮ࡴࡧࠡࡶ࡫ࡩࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡷࡪࡶ࡫ࠤࡪࡸࡲࡰࡴࠣ࠾ࠥ࠭ๅ") + str(error))
  return False
def bstack1ll1l111l_opy_(bstack11ll1l111l_opy_, test_tags):
  bstack11ll1l111l_opy_ = os.getenv(bstack1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨๆ"))
  if bstack11ll1l111l_opy_ is None:
    return True
  bstack11ll1l111l_opy_ = json.loads(bstack11ll1l111l_opy_)
  try:
    include_tags = bstack11ll1l111l_opy_[bstack1l_opy_ (u"ࠨ࡫ࡱࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭็")] if bstack1l_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫่ࠧ") in bstack11ll1l111l_opy_ and isinstance(bstack11ll1l111l_opy_[bstack1l_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨ้")], list) else []
    exclude_tags = bstack11ll1l111l_opy_[bstack1l_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦ๊ࠩ")] if bstack1l_opy_ (u"ࠬ࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧ๋ࠪ") in bstack11ll1l111l_opy_ and isinstance(bstack11ll1l111l_opy_[bstack1l_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫ์")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack1l_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡼࡡ࡭࡫ࡧࡥࡹ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡬࡯ࡳࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡥࡩ࡫ࡵࡲࡦࠢࡶࡧࡦࡴ࡮ࡪࡰࡪ࠲ࠥࡋࡲࡳࡱࡵࠤ࠿ࠦࠢํ") + str(error))
  return False
def bstack1llll111ll_opy_(config, bstack11ll11ll1l_opy_, bstack11ll111lll_opy_, bstack11ll1l1111_opy_):
  bstack11ll11llll_opy_ = bstack11l1ll1lll_opy_(config)
  bstack11l1lll11l_opy_ = bstack11l1llllll_opy_(config)
  if bstack11ll11llll_opy_ is None or bstack11l1lll11l_opy_ is None:
    logger.error(bstack1l_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡶࡺࡴࠠࡧࡱࡵࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࠺ࠡࡏ࡬ࡷࡸ࡯࡮ࡨࠢࡤࡹࡹ࡮ࡥ࡯ࡶ࡬ࡧࡦࡺࡩࡰࡰࠣࡸࡴࡱࡥ࡯ࠩ๎"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪ๏"), bstack1l_opy_ (u"ࠪࡿࢂ࠭๐")))
    data = {
        bstack1l_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩ๑"): config[bstack1l_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪ๒")],
        bstack1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ๓"): config.get(bstack1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ๔"), os.path.basename(os.getcwd())),
        bstack1l_opy_ (u"ࠨࡵࡷࡥࡷࡺࡔࡪ࡯ࡨࠫ๕"): bstack1l11lll111_opy_(),
        bstack1l_opy_ (u"ࠩࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧ๖"): config.get(bstack1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡆࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭๗"), bstack1l_opy_ (u"ࠫࠬ๘")),
        bstack1l_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬ๙"): {
            bstack1l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡐࡤࡱࡪ࠭๚"): bstack11ll11ll1l_opy_,
            bstack1l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭࡙ࡩࡷࡹࡩࡰࡰࠪ๛"): bstack11ll111lll_opy_,
            bstack1l_opy_ (u"ࠨࡵࡧ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬ๜"): __version__,
            bstack1l_opy_ (u"ࠩ࡯ࡥࡳ࡭ࡵࡢࡩࡨࠫ๝"): bstack1l_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ๞"),
            bstack1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ๟"): bstack1l_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠧ๠"),
            bstack1l_opy_ (u"࠭ࡴࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭๡"): bstack11ll1l1111_opy_
        },
        bstack1l_opy_ (u"ࠧࡴࡧࡷࡸ࡮ࡴࡧࡴࠩ๢"): settings,
        bstack1l_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࡅࡲࡲࡹࡸ࡯࡭ࠩ๣"): bstack11ll11lll1_opy_(),
        bstack1l_opy_ (u"ࠩࡦ࡭ࡎࡴࡦࡰࠩ๤"): bstack111llll1l_opy_(),
        bstack1l_opy_ (u"ࠪ࡬ࡴࡹࡴࡊࡰࡩࡳࠬ๥"): get_host_info(),
        bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭๦"): bstack1l1ll1111l_opy_(config)
    }
    headers = {
        bstack1l_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫ๧"): bstack1l_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩ๨"),
    }
    config = {
        bstack1l_opy_ (u"ࠧࡢࡷࡷ࡬ࠬ๩"): (bstack11ll11llll_opy_, bstack11l1lll11l_opy_),
        bstack1l_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩ๪"): headers
    }
    response = bstack1l1l1l11_opy_(bstack1l_opy_ (u"ࠩࡓࡓࡘ࡚ࠧ๫"), bstack11ll11l1l1_opy_ + bstack1l_opy_ (u"ࠪ࠳ࡻ࠸࠯ࡵࡧࡶࡸࡤࡸࡵ࡯ࡵࠪ๬"), data, config)
    bstack11l1lll1ll_opy_ = response.json()
    if bstack11l1lll1ll_opy_[bstack1l_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬ๭")]:
      parsed = json.loads(os.getenv(bstack1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭๮"), bstack1l_opy_ (u"࠭ࡻࡾࠩ๯")))
      parsed[bstack1l_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ๰")] = bstack11l1lll1ll_opy_[bstack1l_opy_ (u"ࠨࡦࡤࡸࡦ࠭๱")][bstack1l_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ๲")]
      os.environ[bstack1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫ๳")] = json.dumps(parsed)
      bstack1lll11111_opy_.bstack11ll1111ll_opy_(bstack11l1lll1ll_opy_[bstack1l_opy_ (u"ࠫࡩࡧࡴࡢࠩ๴")][bstack1l_opy_ (u"ࠬࡹࡣࡳ࡫ࡳࡸࡸ࠭๵")])
      bstack1lll11111_opy_.bstack11l1lll111_opy_(bstack11l1lll1ll_opy_[bstack1l_opy_ (u"࠭ࡤࡢࡶࡤࠫ๶")][bstack1l_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡴࠩ๷")])
      bstack1lll11111_opy_.store()
      return bstack11l1lll1ll_opy_[bstack1l_opy_ (u"ࠨࡦࡤࡸࡦ࠭๸")][bstack1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡖࡲ࡯ࡪࡴࠧ๹")], bstack11l1lll1ll_opy_[bstack1l_opy_ (u"ࠪࡨࡦࡺࡡࠨ๺")][bstack1l_opy_ (u"ࠫ࡮ࡪࠧ๻")]
    else:
      logger.error(bstack1l_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡳࡷࡱࡲ࡮ࡴࡧࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱ࠾ࠥ࠭๼") + bstack11l1lll1ll_opy_[bstack1l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ๽")])
      if bstack11l1lll1ll_opy_[bstack1l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ๾")] == bstack1l_opy_ (u"ࠨࡋࡱࡺࡦࡲࡩࡥࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡥࡹ࡯࡯࡯ࠢࡳࡥࡸࡹࡥࡥ࠰ࠪ๿"):
        for bstack11l1lll1l1_opy_ in bstack11l1lll1ll_opy_[bstack1l_opy_ (u"ࠩࡨࡶࡷࡵࡲࡴࠩ຀")]:
          logger.error(bstack11l1lll1l1_opy_[bstack1l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫກ")])
      return None, None
  except Exception as error:
    logger.error(bstack1l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡶࡨࡷࡹࠦࡲࡶࡰࠣࡪࡴࡸࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰ࠽ࠤࠧຂ") +  str(error))
    return None, None
def bstack111111lll_opy_():
  if os.getenv(bstack1l_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪ຃")) is None:
    return {
        bstack1l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ຄ"): bstack1l_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭຅"),
        bstack1l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩຆ"): bstack1l_opy_ (u"ࠩࡅࡹ࡮ࡲࡤࠡࡥࡵࡩࡦࡺࡩࡰࡰࠣ࡬ࡦࡪࠠࡧࡣ࡬ࡰࡪࡪ࠮ࠨງ")
    }
  data = {bstack1l_opy_ (u"ࠪࡩࡳࡪࡔࡪ࡯ࡨࠫຈ"): bstack1l11lll111_opy_()}
  headers = {
      bstack1l_opy_ (u"ࠫࡆࡻࡴࡩࡱࡵ࡭ࡿࡧࡴࡪࡱࡱࠫຉ"): bstack1l_opy_ (u"ࠬࡈࡥࡢࡴࡨࡶࠥ࠭ຊ") + os.getenv(bstack1l_opy_ (u"ࠨࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠦ຋")),
      bstack1l_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭ຌ"): bstack1l_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫຍ")
  }
  response = bstack1l1l1l11_opy_(bstack1l_opy_ (u"ࠩࡓ࡙࡙࠭ຎ"), bstack11ll11l1l1_opy_ + bstack1l_opy_ (u"ࠪ࠳ࡹ࡫ࡳࡵࡡࡵࡹࡳࡹ࠯ࡴࡶࡲࡴࠬຏ"), data, { bstack1l_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬຐ"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack1l_opy_ (u"ࠧࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡖࡨࡷࡹࠦࡒࡶࡰࠣࡱࡦࡸ࡫ࡦࡦࠣࡥࡸࠦࡣࡰ࡯ࡳࡰࡪࡺࡥࡥࠢࡤࡸࠥࠨຑ") + datetime.utcnow().isoformat() + bstack1l_opy_ (u"࡚࠭ࠨຒ"))
      return {bstack1l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧຓ"): bstack1l_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩດ"), bstack1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪຕ"): bstack1l_opy_ (u"ࠪࠫຖ")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack1l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦ࡭ࡢࡴ࡮࡭ࡳ࡭ࠠࡤࡱࡰࡴࡱ࡫ࡴࡪࡱࡱࠤࡴ࡬ࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡘࡪࡹࡴࠡࡔࡸࡲ࠿ࠦࠢທ") + str(error))
    return {
        bstack1l_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬຘ"): bstack1l_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬນ"),
        bstack1l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨບ"): str(error)
    }
def bstack11ll1l111_opy_(caps, options):
  try:
    bstack11l1lllll1_opy_ = caps.get(bstack1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩປ"), {}).get(bstack1l_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭ຜ"), caps.get(bstack1l_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࠪຝ"), bstack1l_opy_ (u"ࠫࠬພ")))
    if bstack11l1lllll1_opy_:
      logger.warn(bstack1l_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡳࡷࡱࠤࡴࡴ࡬ࡺࠢࡲࡲࠥࡊࡥࡴ࡭ࡷࡳࡵࠦࡢࡳࡱࡺࡷࡪࡸࡳ࠯ࠤຟ"))
      return False
    browser = caps.get(bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫຠ"), bstack1l_opy_ (u"ࠧࠨມ")).lower()
    if browser != bstack1l_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨຢ"):
      logger.warn(bstack1l_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡷࡻ࡮ࠡࡱࡱࡰࡾࠦ࡯࡯ࠢࡆ࡬ࡷࡵ࡭ࡦࠢࡥࡶࡴࡽࡳࡦࡴࡶ࠲ࠧຣ"))
      return False
    browser_version = caps.get(bstack1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ຤"), caps.get(bstack1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ລ")))
    if browser_version and browser_version != bstack1l_opy_ (u"ࠬࡲࡡࡵࡧࡶࡸࠬ຦") and int(browser_version.split(bstack1l_opy_ (u"࠭࠮ࠨວ"))[0]) <= 94:
      logger.warn(bstack1l_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡵࡹࡳࠦ࡯࡯࡮ࡼࠤࡴࡴࠠࡄࡪࡵࡳࡲ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࡪࡶࡪࡧࡴࡦࡴࠣࡸ࡭ࡧ࡮ࠡ࠻࠷࠲ࠧຨ"))
      return False
    if not options is None:
      bstack11ll111ll1_opy_ = options.to_capabilities().get(bstack1l_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ຩ"), {})
      if bstack1l_opy_ (u"ࠩ࠰࠱࡭࡫ࡡࡥ࡮ࡨࡷࡸ࠭ສ") in bstack11ll111ll1_opy_.get(bstack1l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨຫ"), []):
        logger.warn(bstack1l_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦ࡮ࡰࡶࠣࡶࡺࡴࠠࡰࡰࠣࡰࡪ࡭ࡡࡤࡻࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧ࠱ࠤࡘࡽࡩࡵࡥ࡫ࠤࡹࡵࠠ࡯ࡧࡺࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨࠤࡴࡸࠠࡢࡸࡲ࡭ࡩࠦࡵࡴ࡫ࡱ࡫ࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩ࠳ࠨຬ"))
        return False
    return True
  except Exception as error:
    logger.debug(bstack1l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡻࡧ࡬ࡪࡦࡤࡸࡪࠦࡡ࠲࠳ࡼࠤࡸࡻࡰࡱࡱࡵࡸࠥࡀࠢອ") + str(error))
    return False
def set_capabilities(caps, config):
  try:
    bstack11l1ll1ll1_opy_ = config.get(bstack1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ຮ"), {})
    bstack11l1ll1ll1_opy_[bstack1l_opy_ (u"ࠧࡢࡷࡷ࡬࡙ࡵ࡫ࡦࡰࠪຯ")] = os.getenv(bstack1l_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ະ"))
    bstack11ll111111_opy_ = json.loads(os.getenv(bstack1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪັ"), bstack1l_opy_ (u"ࠪࡿࢂ࠭າ"))).get(bstack1l_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬຳ"))
    caps[bstack1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬິ")] = True
    if bstack1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧີ") in caps:
      caps[bstack1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨຶ")][bstack1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨື")] = bstack11l1ll1ll1_opy_
      caps[bstack1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵຸࠪ")][bstack1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵູࠪ")][bstack1l_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲ຺ࠬ")] = bstack11ll111111_opy_
    else:
      caps[bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫົ")] = bstack11l1ll1ll1_opy_
      caps[bstack1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬຼ")][bstack1l_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨຽ")] = bstack11ll111111_opy_
  except Exception as error:
    logger.debug(bstack1l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡷࡪࡺࡴࡪࡰࡪࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹ࠮ࠡࡇࡵࡶࡴࡸ࠺ࠡࠤ຾") +  str(error))
def bstack1111ll11_opy_(driver, bstack11ll111l1l_opy_):
  try:
    setattr(driver, bstack1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯ࠩ຿"), True)
    session = driver.session_id
    if session:
      bstack11ll1111l1_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack11ll1111l1_opy_ = False
      bstack11ll1111l1_opy_ = url.scheme in [bstack1l_opy_ (u"ࠥ࡬ࡹࡺࡰࠣເ"), bstack1l_opy_ (u"ࠦ࡭ࡺࡴࡱࡵࠥແ")]
      if bstack11ll1111l1_opy_:
        if bstack11ll111l1l_opy_:
          logger.info(bstack1l_opy_ (u"࡙ࠧࡥࡵࡷࡳࠤ࡫ࡵࡲࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡶࡨࡷࡹ࡯࡮ࡨࠢ࡫ࡥࡸࠦࡳࡵࡣࡵࡸࡪࡪ࠮ࠡࡃࡸࡸࡴࡳࡡࡵࡧࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡥࡹࡧࡦࡹࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡣࡧࡪ࡭ࡳࠦ࡭ࡰ࡯ࡨࡲࡹࡧࡲࡪ࡮ࡼ࠲ࠧໂ"))
      return bstack11ll111l1l_opy_
  except Exception as e:
    logger.error(bstack1l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡴࡢࡴࡷ࡭ࡳ࡭ࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡸࡩࡡ࡯ࠢࡩࡳࡷࠦࡴࡩ࡫ࡶࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫࠺ࠡࠤໃ") + str(e))
    return False
def bstack1l1l1111ll_opy_(driver, class_name, name, module_name, path, bstack11lll1ll_opy_):
  try:
    bstack11ll1ll111_opy_ = [class_name] if not class_name is None else []
    bstack11l1llll1l_opy_ = {
        bstack1l_opy_ (u"ࠢࡴࡣࡹࡩࡗ࡫ࡳࡶ࡮ࡷࡷࠧໄ"): True,
        bstack1l_opy_ (u"ࠣࡶࡨࡷࡹࡊࡥࡵࡣ࡬ࡰࡸࠨ໅"): {
            bstack1l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢໆ"): name,
            bstack1l_opy_ (u"ࠥࡸࡪࡹࡴࡓࡷࡱࡍࡩࠨ໇"): os.environ.get(bstack1l_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤ࡚ࡅࡔࡖࡢࡖ࡚ࡔ࡟ࡊࡆ່ࠪ")),
            bstack1l_opy_ (u"ࠧ࡬ࡩ࡭ࡧࡓࡥࡹ࡮້ࠢ"): str(path),
            bstack1l_opy_ (u"ࠨࡳࡤࡱࡳࡩࡑ࡯ࡳࡵࠤ໊"): [module_name, *bstack11ll1ll111_opy_, name],
        },
        bstack1l_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠤ໋"): _11ll11l11l_opy_(driver, bstack11lll1ll_opy_)
    }
    logger.debug(bstack1l_opy_ (u"ࠨࡒࡨࡶ࡫ࡵࡲ࡮࡫ࡱ࡫ࠥࡹࡣࡢࡰࠣࡦࡪ࡬࡯ࡳࡧࠣࡷࡦࡼࡩ࡯ࡩࠣࡶࡪࡹࡵ࡭ࡶࡶࠫ໌"))
    logger.debug(driver.execute_async_script(bstack1lll11111_opy_.perform_scan, {bstack1l_opy_ (u"ࠤࡰࡩࡹ࡮࡯ࡥࠤໍ"): name}))
    logger.debug(driver.execute_async_script(bstack1lll11111_opy_.bstack11ll11111l_opy_, bstack11l1llll1l_opy_))
    logger.info(bstack1l_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡸࡪࡹࡴࡪࡰࡪࠤ࡫ࡵࡲࠡࡶ࡫࡭ࡸࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢ࡫ࡥࡸࠦࡥ࡯ࡦࡨࡨ࠳ࠨ໎"))
  except Exception as bstack11ll111l11_opy_:
    logger.error(bstack1l_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠥࡩ࡯ࡶ࡮ࡧࠤࡳࡵࡴࠡࡤࡨࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡪࠠࡧࡱࡵࠤࡹ࡮ࡥࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨ࠾ࠥࠨ໏") + str(path) + bstack1l_opy_ (u"ࠧࠦࡅࡳࡴࡲࡶࠥࡀࠢ໐") + str(bstack11ll111l11_opy_))