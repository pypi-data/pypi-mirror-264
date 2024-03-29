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
import datetime
import json
import logging
import os
import threading
from bstack_utils.helper import bstack11ll1l1111_opy_, bstack1lll11111_opy_, get_host_info, bstack11l1ll1ll1_opy_, bstack11ll11111l_opy_, bstack11l11l1l1l_opy_, \
    bstack111ll1l1ll_opy_, bstack11l1111l11_opy_, bstack1ll1l11l_opy_, bstack111ll1lll1_opy_, bstack111ll1l11_opy_, bstack1l111l1111_opy_
from bstack_utils.bstack1lllll1111l_opy_ import bstack1lllll111l1_opy_
from bstack_utils.bstack1l111l1l11_opy_ import bstack1l1111111l_opy_
import bstack_utils.bstack1ll1ll11l_opy_ as bstack11lllll1l_opy_
from bstack_utils.constants import bstack11l1l1l111_opy_
bstack1llll11111l_opy_ = [
    bstack1llll1l_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨᓨ"), bstack1llll1l_opy_ (u"ࠬࡉࡂࡕࡕࡨࡷࡸ࡯࡯࡯ࡅࡵࡩࡦࡺࡥࡥࠩᓩ"), bstack1llll1l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨᓪ"), bstack1llll1l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨᓫ"),
    bstack1llll1l_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪᓬ"), bstack1llll1l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪᓭ"), bstack1llll1l_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫᓮ")
]
bstack1lll1ll1111_opy_ = bstack1llll1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡩ࡯࡭࡮ࡨࡧࡹࡵࡲ࠮ࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫᓯ")
logger = logging.getLogger(__name__)
class bstack1ll1ll111l_opy_:
    bstack1lllll1111l_opy_ = None
    bs_config = None
    @classmethod
    @bstack1l111l1111_opy_(class_method=True)
    def launch(cls, bs_config, bstack1llll1111ll_opy_):
        cls.bs_config = bs_config
        cls.bstack1lll1l1llll_opy_()
        bstack11ll11ll1l_opy_ = bstack11l1ll1ll1_opy_(bs_config)
        bstack11l1llll1l_opy_ = bstack11ll11111l_opy_(bs_config)
        bstack1l1lll1l11_opy_ = False
        bstack11l1l1111_opy_ = False
        if bstack1llll1l_opy_ (u"ࠬࡧࡰࡱࠩᓰ") in bs_config:
            bstack1l1lll1l11_opy_ = True
        else:
            bstack11l1l1111_opy_ = True
        bstack1l11l111l_opy_ = {
            bstack1llll1l_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ᓱ"): cls.bstack11ll1l111_opy_(bstack1llll1111ll_opy_.get(bstack1llll1l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡹࡸ࡫ࡤࠨᓲ"), bstack1llll1l_opy_ (u"ࠨࠩᓳ"))) and cls.bstack1llll1111l1_opy_(bstack1llll1111ll_opy_.get(bstack1llll1l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡻࡳࡦࡦࠪᓴ"), bstack1llll1l_opy_ (u"ࠪࠫᓵ"))),
            bstack1llll1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᓶ"): bstack11lllll1l_opy_.bstack11l11lll_opy_(bs_config),
            bstack1llll1l_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫᓷ"): bs_config.get(bstack1llll1l_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬᓸ"), False),
            bstack1llll1l_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩᓹ"): bstack11l1l1111_opy_,
            bstack1llll1l_opy_ (u"ࠨࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠧᓺ"): bstack1l1lll1l11_opy_
        }
        data = {
            bstack1llll1l_opy_ (u"ࠩࡩࡳࡷࡳࡡࡵࠩᓻ"): bstack1llll1l_opy_ (u"ࠪ࡮ࡸࡵ࡮ࠨᓼ"),
            bstack1llll1l_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡤࡴࡡ࡮ࡧࠪᓽ"): bs_config.get(bstack1llll1l_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪᓾ"), bstack1llll1l_opy_ (u"࠭ࠧᓿ")),
            bstack1llll1l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᔀ"): bs_config.get(bstack1llll1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫᔁ"), os.path.basename(os.path.abspath(os.getcwd()))),
            bstack1llll1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᔂ"): bs_config.get(bstack1llll1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᔃ")),
            bstack1llll1l_opy_ (u"ࠫࡩ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩᔄ"): bs_config.get(bstack1llll1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡈࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨᔅ"), bstack1llll1l_opy_ (u"࠭ࠧᔆ")),
            bstack1llll1l_opy_ (u"ࠧࡴࡶࡤࡶࡹࡥࡴࡪ࡯ࡨࠫᔇ"): datetime.datetime.now().isoformat(),
            bstack1llll1l_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭ᔈ"): bstack11l11l1l1l_opy_(bs_config),
            bstack1llll1l_opy_ (u"ࠩ࡫ࡳࡸࡺ࡟ࡪࡰࡩࡳࠬᔉ"): get_host_info(),
            bstack1llll1l_opy_ (u"ࠪࡧ࡮ࡥࡩ࡯ࡨࡲࠫᔊ"): bstack1lll11111_opy_(),
            bstack1llll1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢࡶࡺࡴ࡟ࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫᔋ"): os.environ.get(bstack1llll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇ࡛ࡉࡍࡆࡢࡖ࡚ࡔ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫᔌ")),
            bstack1llll1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩࡥࡴࡦࡵࡷࡷࡤࡸࡥࡳࡷࡱࠫᔍ"): os.environ.get(bstack1llll1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࠬᔎ"), False),
            bstack1llll1l_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࡡࡦࡳࡳࡺࡲࡰ࡮ࠪᔏ"): bstack11ll1l1111_opy_(),
            bstack1llll1l_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࡢࡱࡦࡶࠧᔐ"): bstack1l11l111l_opy_,
            bstack1llll1l_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࡢࡺࡪࡸࡳࡪࡱࡱࠫᔑ"): {
                bstack1llll1l_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡎࡢ࡯ࡨࠫᔒ"): bstack1llll1111ll_opy_.get(bstack1llll1l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪ࠭ᔓ"), bstack1llll1l_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠭ᔔ")),
                bstack1llll1l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭࡙ࡩࡷࡹࡩࡰࡰࠪᔕ"): bstack1llll1111ll_opy_.get(bstack1llll1l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᔖ")),
                bstack1llll1l_opy_ (u"ࠩࡶࡨࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᔗ"): bstack1llll1111ll_opy_.get(bstack1llll1l_opy_ (u"ࠪࡷࡩࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᔘ"))
            }
        }
        config = {
            bstack1llll1l_opy_ (u"ࠫࡦࡻࡴࡩࠩᔙ"): (bstack11ll11ll1l_opy_, bstack11l1llll1l_opy_),
            bstack1llll1l_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭ᔚ"): cls.default_headers()
        }
        response = bstack1ll1l11l_opy_(bstack1llll1l_opy_ (u"࠭ࡐࡐࡕࡗࠫᔛ"), cls.request_url(bstack1llll1l_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡷ࡬ࡰࡩࡹࠧᔜ")), data, config)
        if response.status_code != 200:
            os.environ[bstack1llll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ᔝ")] = bstack1llll1l_opy_ (u"ࠩࡱࡹࡱࡲࠧᔞ")
            os.environ[bstack1llll1l_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡃࡐࡏࡓࡐࡊ࡚ࡅࡅࠩᔟ")] = bstack1llll1l_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪᔠ")
            os.environ[bstack1llll1l_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡍ࡛࡙࠭ᔡ")] = bstack1llll1l_opy_ (u"࠭࡮ࡶ࡮࡯ࠫᔢ")
            os.environ[bstack1llll1l_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉ࠭ᔣ")] = bstack1llll1l_opy_ (u"ࠣࡰࡸࡰࡱࠨᔤ")
            os.environ[bstack1llll1l_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡁࡍࡎࡒ࡛ࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࡕࠪᔥ")] = bstack1llll1l_opy_ (u"ࠥࡲࡺࡲ࡬ࠣᔦ")
            bstack1lll1lll111_opy_ = response.json()
            if bstack1lll1lll111_opy_ and bstack1lll1lll111_opy_[bstack1llll1l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᔧ")]:
                error_message = bstack1lll1lll111_opy_[bstack1llll1l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᔨ")]
                if bstack1lll1lll111_opy_[bstack1llll1l_opy_ (u"࠭ࡥࡳࡴࡲࡶ࡙ࡿࡰࡦࠩᔩ")] == bstack1llll1l_opy_ (u"ࠧࡆࡔࡕࡓࡗࡥࡉࡏࡘࡄࡐࡎࡊ࡟ࡄࡔࡈࡈࡊࡔࡔࡊࡃࡏࡗࠬᔪ"):
                    logger.error(error_message)
                elif bstack1lll1lll111_opy_[bstack1llll1l_opy_ (u"ࠨࡧࡵࡶࡴࡸࡔࡺࡲࡨࠫᔫ")] == bstack1llll1l_opy_ (u"ࠩࡈࡖࡗࡕࡒࡠࡃࡆࡇࡊ࡙ࡓࡠࡆࡈࡒࡎࡋࡄࠨᔬ"):
                    logger.info(error_message)
                elif bstack1lll1lll111_opy_[bstack1llll1l_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࡖࡼࡴࡪ࠭ᔭ")] == bstack1llll1l_opy_ (u"ࠫࡊࡘࡒࡐࡔࡢࡗࡉࡑ࡟ࡅࡇࡓࡖࡊࡉࡁࡕࡇࡇࠫᔮ"):
                    logger.error(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack1llll1l_opy_ (u"ࠧࡊࡡࡵࡣࠣࡹࡵࡲ࡯ࡢࡦࠣࡸࡴࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯࡚ࠥࡥࡴࡶࠣࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠣࡪࡦ࡯࡬ࡦࡦࠣࡨࡺ࡫ࠠࡵࡱࠣࡷࡴࡳࡥࠡࡧࡵࡶࡴࡸࠢᔯ"))
            return [None, None, None]
        bstack1lll1lll111_opy_ = response.json()
        os.environ[bstack1llll1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫᔰ")] = bstack1lll1lll111_opy_[bstack1llll1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩᔱ")]
        if cls.bstack11ll1l111_opy_(bstack1llll1111ll_opy_.get(bstack1llll1l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡺࡹࡥࡥࠩᔲ"), bstack1llll1l_opy_ (u"ࠩࠪᔳ"))) is True and cls.bstack1llll1111l1_opy_(bstack1llll1111ll_opy_.get(bstack1llll1l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡵࡴࡧࡧࠫᔴ"), bstack1llll1l_opy_ (u"ࠫࠬᔵ"))):
            logger.debug(bstack1llll1l_opy_ (u"࡚ࠬࡥࡴࡶࠣࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠣࡆࡺ࡯࡬ࡥࠢࡦࡶࡪࡧࡴࡪࡱࡱࠤࡘࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬ࠢࠩᔶ"))
            os.environ[bstack1llll1l_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡆࡓࡒࡖࡌࡆࡖࡈࡈࠬᔷ")] = bstack1llll1l_opy_ (u"ࠧࡵࡴࡸࡩࠬᔸ")
            if bstack1lll1lll111_opy_.get(bstack1llll1l_opy_ (u"ࠨ࡬ࡺࡸࠬᔹ")):
                os.environ[bstack1llll1l_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡊࡘࡖࠪᔺ")] = bstack1lll1lll111_opy_[bstack1llll1l_opy_ (u"ࠪ࡮ࡼࡺࠧᔻ")]
                os.environ[bstack1llll1l_opy_ (u"ࠫࡈࡘࡅࡅࡇࡑࡘࡎࡇࡌࡔࡡࡉࡓࡗࡥࡃࡓࡃࡖࡌࡤࡘࡅࡑࡑࡕࡘࡎࡔࡇࠨᔼ")] = json.dumps({
                    bstack1llll1l_opy_ (u"ࠬࡻࡳࡦࡴࡱࡥࡲ࡫ࠧᔽ"): bstack11ll11ll1l_opy_,
                    bstack1llll1l_opy_ (u"࠭ࡰࡢࡵࡶࡻࡴࡸࡤࠨᔾ"): bstack11l1llll1l_opy_
                })
            if bstack1lll1lll111_opy_.get(bstack1llll1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩᔿ")):
                os.environ[bstack1llll1l_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡍࡇࡓࡉࡇࡇࡣࡎࡊࠧᕀ")] = bstack1lll1lll111_opy_[bstack1llll1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫᕁ")]
            if bstack1lll1lll111_opy_.get(bstack1llll1l_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡡࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧᕂ")):
                os.environ[bstack1llll1l_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡃࡏࡐࡔ࡝࡟ࡔࡅࡕࡉࡊࡔࡓࡉࡑࡗࡗࠬᕃ")] = str(bstack1lll1lll111_opy_[bstack1llll1l_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡣࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩᕄ")])
        return [bstack1lll1lll111_opy_[bstack1llll1l_opy_ (u"࠭ࡪࡸࡶࠪᕅ")], bstack1lll1lll111_opy_[bstack1llll1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩᕆ")], bstack1lll1lll111_opy_[bstack1llll1l_opy_ (u"ࠨࡣ࡯ࡰࡴࡽ࡟ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࡷࠬᕇ")]]
    @classmethod
    @bstack1l111l1111_opy_(class_method=True)
    def stop(cls):
        if not cls.on():
            return
        if os.environ[bstack1llll1l_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡊࡘࡖࠪᕈ")] == bstack1llll1l_opy_ (u"ࠥࡲࡺࡲ࡬ࠣᕉ") or os.environ[bstack1llll1l_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡉࡃࡖࡌࡊࡊ࡟ࡊࡆࠪᕊ")] == bstack1llll1l_opy_ (u"ࠧࡴࡵ࡭࡮ࠥᕋ"):
            print(bstack1llll1l_opy_ (u"࠭ࡅ࡙ࡅࡈࡔ࡙ࡏࡏࡏࠢࡌࡒࠥࡹࡴࡰࡲࡅࡹ࡮ࡲࡤࡖࡲࡶࡸࡷ࡫ࡡ࡮ࠢࡕࡉࡖ࡛ࡅࡔࡖࠣࡘࡔࠦࡔࡆࡕࡗࠤࡔࡈࡓࡆࡔ࡙ࡅࡇࡏࡌࡊࡖ࡜ࠤ࠿ࠦࡍࡪࡵࡶ࡭ࡳ࡭ࠠࡢࡷࡷ࡬ࡪࡴࡴࡪࡥࡤࡸ࡮ࡵ࡮ࠡࡶࡲ࡯ࡪࡴࠧᕌ"))
            return {
                bstack1llll1l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧᕍ"): bstack1llll1l_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧᕎ"),
                bstack1llll1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᕏ"): bstack1llll1l_opy_ (u"ࠪࡘࡴࡱࡥ࡯࠱ࡥࡹ࡮ࡲࡤࡊࡆࠣ࡭ࡸࠦࡵ࡯ࡦࡨࡪ࡮ࡴࡥࡥ࠮ࠣࡦࡺ࡯࡬ࡥࠢࡦࡶࡪࡧࡴࡪࡱࡱࠤࡲ࡯ࡧࡩࡶࠣ࡬ࡦࡼࡥࠡࡨࡤ࡭ࡱ࡫ࡤࠨᕐ")
            }
        else:
            cls.bstack1lllll1111l_opy_.shutdown()
            data = {
                bstack1llll1l_opy_ (u"ࠫࡸࡺ࡯ࡱࡡࡷ࡭ࡲ࡫ࠧᕑ"): datetime.datetime.now().isoformat()
            }
            config = {
                bstack1llll1l_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭ᕒ"): cls.default_headers()
            }
            bstack11l11l1111_opy_ = bstack1llll1l_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡢࡶ࡫࡯ࡨࡸ࠵ࡻࡾ࠱ࡶࡸࡴࡶࠧᕓ").format(os.environ[bstack1llll1l_opy_ (u"ࠢࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉࠨᕔ")])
            bstack1lll1ll1l11_opy_ = cls.request_url(bstack11l11l1111_opy_)
            response = bstack1ll1l11l_opy_(bstack1llll1l_opy_ (u"ࠨࡒࡘࡘࠬᕕ"), bstack1lll1ll1l11_opy_, data, config)
            if not response.ok:
                raise Exception(bstack1llll1l_opy_ (u"ࠤࡖࡸࡴࡶࠠࡳࡧࡴࡹࡪࡹࡴࠡࡰࡲࡸࠥࡵ࡫ࠣᕖ"))
    @classmethod
    def bstack1l1111ll11_opy_(cls):
        if cls.bstack1lllll1111l_opy_ is None:
            return
        cls.bstack1lllll1111l_opy_.shutdown()
    @classmethod
    def bstack111l11111_opy_(cls):
        if cls.on():
            print(
                bstack1llll1l_opy_ (u"࡚ࠪ࡮ࡹࡩࡵࠢ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡢࡶ࡫࡯ࡨࡸ࠵ࡻࡾࠢࡷࡳࠥࡼࡩࡦࡹࠣࡦࡺ࡯࡬ࡥࠢࡵࡩࡵࡵࡲࡵ࠮ࠣ࡭ࡳࡹࡩࡨࡪࡷࡷ࠱ࠦࡡ࡯ࡦࠣࡱࡦࡴࡹࠡ࡯ࡲࡶࡪࠦࡤࡦࡤࡸ࡫࡬࡯࡮ࡨࠢ࡬ࡲ࡫ࡵࡲ࡮ࡣࡷ࡭ࡴࡴࠠࡢ࡮࡯ࠤࡦࡺࠠࡰࡰࡨࠤࡵࡲࡡࡤࡧࠤࡠࡳ࠭ᕗ").format(os.environ[bstack1llll1l_opy_ (u"ࠦࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡉࡃࡖࡌࡊࡊ࡟ࡊࡆࠥᕘ")]))
    @classmethod
    def bstack1lll1l1llll_opy_(cls):
        if cls.bstack1lllll1111l_opy_ is not None:
            return
        cls.bstack1lllll1111l_opy_ = bstack1lllll111l1_opy_(cls.bstack1lll1lll11l_opy_)
        cls.bstack1lllll1111l_opy_.start()
    @classmethod
    def bstack1l111ll1l1_opy_(cls, bstack11llll111l_opy_, bstack1lll1ll11ll_opy_=bstack1llll1l_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡨࡡࡵࡥ࡫ࠫᕙ")):
        if not cls.on():
            return
        bstack1111l1l1_opy_ = bstack11llll111l_opy_[bstack1llll1l_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪᕚ")]
        bstack1lll1ll1l1l_opy_ = {
            bstack1llll1l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨᕛ"): bstack1llll1l_opy_ (u"ࠨࡖࡨࡷࡹࡥࡓࡵࡣࡵࡸࡤ࡛ࡰ࡭ࡱࡤࡨࠬᕜ"),
            bstack1llll1l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫᕝ"): bstack1llll1l_opy_ (u"ࠪࡘࡪࡹࡴࡠࡇࡱࡨࡤ࡛ࡰ࡭ࡱࡤࡨࠬᕞ"),
            bstack1llll1l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡱࡩࡱࡲࡨࡨࠬᕟ"): bstack1llll1l_opy_ (u"࡚ࠬࡥࡴࡶࡢࡗࡰ࡯ࡰࡱࡧࡧࡣ࡚ࡶ࡬ࡰࡣࡧࠫᕠ"),
            bstack1llll1l_opy_ (u"࠭ࡌࡰࡩࡆࡶࡪࡧࡴࡦࡦࠪᕡ"): bstack1llll1l_opy_ (u"ࠧࡍࡱࡪࡣ࡚ࡶ࡬ࡰࡣࡧࠫᕢ"),
            bstack1llll1l_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩᕣ"): bstack1llll1l_opy_ (u"ࠩࡋࡳࡴࡱ࡟ࡔࡶࡤࡶࡹࡥࡕࡱ࡮ࡲࡥࡩ࠭ᕤ"),
            bstack1llll1l_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᕥ"): bstack1llll1l_opy_ (u"ࠫࡍࡵ࡯࡬ࡡࡈࡲࡩࡥࡕࡱ࡮ࡲࡥࡩ࠭ᕦ"),
            bstack1llll1l_opy_ (u"ࠬࡉࡂࡕࡕࡨࡷࡸ࡯࡯࡯ࡅࡵࡩࡦࡺࡥࡥࠩᕧ"): bstack1llll1l_opy_ (u"࠭ࡃࡃࡖࡢ࡙ࡵࡲ࡯ࡢࡦࠪᕨ")
        }.get(bstack1111l1l1_opy_)
        if bstack1lll1ll11ll_opy_ == bstack1llll1l_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡣࡷࡧ࡭࠭ᕩ"):
            cls.bstack1lll1l1llll_opy_()
            cls.bstack1lllll1111l_opy_.add(bstack11llll111l_opy_)
        elif bstack1lll1ll11ll_opy_ == bstack1llll1l_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭ᕪ"):
            cls.bstack1lll1lll11l_opy_([bstack11llll111l_opy_], bstack1lll1ll11ll_opy_)
    @classmethod
    @bstack1l111l1111_opy_(class_method=True)
    def bstack1lll1lll11l_opy_(cls, bstack11llll111l_opy_, bstack1lll1ll11ll_opy_=bstack1llll1l_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡥࡥࡹࡩࡨࠨᕫ")):
        config = {
            bstack1llll1l_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫᕬ"): cls.default_headers()
        }
        response = bstack1ll1l11l_opy_(bstack1llll1l_opy_ (u"ࠫࡕࡕࡓࡕࠩᕭ"), cls.request_url(bstack1lll1ll11ll_opy_), bstack11llll111l_opy_, config)
        bstack11ll11lll1_opy_ = response.json()
    @classmethod
    @bstack1l111l1111_opy_(class_method=True)
    def bstack11ll1ll1l_opy_(cls, bstack11lllll1ll_opy_):
        bstack1lll1lll1ll_opy_ = []
        for log in bstack11lllll1ll_opy_:
            bstack1lll1lll1l1_opy_ = {
                bstack1llll1l_opy_ (u"ࠬࡱࡩ࡯ࡦࠪᕮ"): bstack1llll1l_opy_ (u"࠭ࡔࡆࡕࡗࡣࡑࡕࡇࠨᕯ"),
                bstack1llll1l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ᕰ"): log[bstack1llll1l_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧᕱ")],
                bstack1llll1l_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬᕲ"): log[bstack1llll1l_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ᕳ")],
                bstack1llll1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡡࡵࡩࡸࡶ࡯࡯ࡵࡨࠫᕴ"): {},
                bstack1llll1l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᕵ"): log[bstack1llll1l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᕶ")],
            }
            if bstack1llll1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᕷ") in log:
                bstack1lll1lll1l1_opy_[bstack1llll1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᕸ")] = log[bstack1llll1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᕹ")]
            elif bstack1llll1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᕺ") in log:
                bstack1lll1lll1l1_opy_[bstack1llll1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᕻ")] = log[bstack1llll1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᕼ")]
            bstack1lll1lll1ll_opy_.append(bstack1lll1lll1l1_opy_)
        cls.bstack1l111ll1l1_opy_({
            bstack1llll1l_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪᕽ"): bstack1llll1l_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫᕾ"),
            bstack1llll1l_opy_ (u"ࠨ࡮ࡲ࡫ࡸ࠭ᕿ"): bstack1lll1lll1ll_opy_
        })
    @classmethod
    @bstack1l111l1111_opy_(class_method=True)
    def bstack1lll1ll11l1_opy_(cls, steps):
        bstack1lll1ll1ll1_opy_ = []
        for step in steps:
            bstack1lll1llll11_opy_ = {
                bstack1llll1l_opy_ (u"ࠩ࡮࡭ࡳࡪࠧᖀ"): bstack1llll1l_opy_ (u"ࠪࡘࡊ࡙ࡔࡠࡕࡗࡉࡕ࠭ᖁ"),
                bstack1llll1l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪᖂ"): step[bstack1llll1l_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫᖃ")],
                bstack1llll1l_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩᖄ"): step[bstack1llll1l_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪᖅ")],
                bstack1llll1l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᖆ"): step[bstack1llll1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᖇ")],
                bstack1llll1l_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࠬᖈ"): step[bstack1llll1l_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳ࠭ᖉ")]
            }
            if bstack1llll1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᖊ") in step:
                bstack1lll1llll11_opy_[bstack1llll1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᖋ")] = step[bstack1llll1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᖌ")]
            elif bstack1llll1l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᖍ") in step:
                bstack1lll1llll11_opy_[bstack1llll1l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᖎ")] = step[bstack1llll1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᖏ")]
            bstack1lll1ll1ll1_opy_.append(bstack1lll1llll11_opy_)
        cls.bstack1l111ll1l1_opy_({
            bstack1llll1l_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨᖐ"): bstack1llll1l_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩᖑ"),
            bstack1llll1l_opy_ (u"࠭࡬ࡰࡩࡶࠫᖒ"): bstack1lll1ll1ll1_opy_
        })
    @classmethod
    @bstack1l111l1111_opy_(class_method=True)
    def bstack1l11l1lll1_opy_(cls, screenshot):
        cls.bstack1l111ll1l1_opy_({
            bstack1llll1l_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫᖓ"): bstack1llll1l_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬᖔ"),
            bstack1llll1l_opy_ (u"ࠩ࡯ࡳ࡬ࡹࠧᖕ"): [{
                bstack1llll1l_opy_ (u"ࠪ࡯࡮ࡴࡤࠨᖖ"): bstack1llll1l_opy_ (u"࡙ࠫࡋࡓࡕࡡࡖࡇࡗࡋࡅࡏࡕࡋࡓ࡙࠭ᖗ"),
                bstack1llll1l_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨᖘ"): datetime.datetime.utcnow().isoformat() + bstack1llll1l_opy_ (u"࡚࠭ࠨᖙ"),
                bstack1llll1l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᖚ"): screenshot[bstack1llll1l_opy_ (u"ࠨ࡫ࡰࡥ࡬࡫ࠧᖛ")],
                bstack1llll1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᖜ"): screenshot[bstack1llll1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᖝ")]
            }]
        }, bstack1lll1ll11ll_opy_=bstack1llll1l_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩᖞ"))
    @classmethod
    @bstack1l111l1111_opy_(class_method=True)
    def bstack1ll11111_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack1l111ll1l1_opy_({
            bstack1llll1l_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩᖟ"): bstack1llll1l_opy_ (u"࠭ࡃࡃࡖࡖࡩࡸࡹࡩࡰࡰࡆࡶࡪࡧࡴࡦࡦࠪᖠ"),
            bstack1llll1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩᖡ"): {
                bstack1llll1l_opy_ (u"ࠣࡷࡸ࡭ࡩࠨᖢ"): cls.current_test_uuid(),
                bstack1llll1l_opy_ (u"ࠤ࡬ࡲࡹ࡫ࡧࡳࡣࡷ࡭ࡴࡴࡳࠣᖣ"): cls.bstack11lllll11l_opy_(driver)
            }
        })
    @classmethod
    def on(cls):
        if os.environ.get(bstack1llll1l_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡋ࡙ࡗࠫᖤ"), None) is None or os.environ[bstack1llll1l_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡌ࡚ࡘࠬᖥ")] == bstack1llll1l_opy_ (u"ࠧࡴࡵ࡭࡮ࠥᖦ"):
            return False
        return True
    @classmethod
    def bstack11ll1l111_opy_(cls, framework=bstack1llll1l_opy_ (u"ࠨࠢᖧ")):
        bstack1lll1llllll_opy_ = framework in bstack11l1l1l111_opy_
        return bstack111ll1l11_opy_(cls.bs_config.get(bstack1llll1l_opy_ (u"ࠧࡵࡧࡶࡸࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫᖨ"), bstack1lll1llllll_opy_))
    @classmethod
    def bstack1llll1111l1_opy_(cls, framework):
        return framework in bstack11l1l1l111_opy_
    @staticmethod
    def request_url(url):
        return bstack1llll1l_opy_ (u"ࠨࡽࢀ࠳ࢀࢃࠧᖩ").format(bstack1lll1ll1111_opy_, url)
    @staticmethod
    def default_headers():
        headers = {
            bstack1llll1l_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨᖪ"): bstack1llll1l_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ᖫ"),
            bstack1llll1l_opy_ (u"ࠫ࡝࠳ࡂࡔࡖࡄࡇࡐ࠳ࡔࡆࡕࡗࡓࡕ࡙ࠧᖬ"): bstack1llll1l_opy_ (u"ࠬࡺࡲࡶࡧࠪᖭ")
        }
        if os.environ.get(bstack1llll1l_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡎ࡜࡚ࠧᖮ"), None):
            headers[bstack1llll1l_opy_ (u"ࠧࡂࡷࡷ࡬ࡴࡸࡩࡻࡣࡷ࡭ࡴࡴࠧᖯ")] = bstack1llll1l_opy_ (u"ࠨࡄࡨࡥࡷ࡫ࡲࠡࡽࢀࠫᖰ").format(os.environ[bstack1llll1l_opy_ (u"ࠤࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡊࡘࡖࠥᖱ")])
        return headers
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack1llll1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧᖲ"), None)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack1llll1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨᖳ"), None)
    @staticmethod
    def bstack1l111ll111_opy_():
        if getattr(threading.current_thread(), bstack1llll1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩᖴ"), None):
            return {
                bstack1llll1l_opy_ (u"࠭ࡴࡺࡲࡨࠫᖵ"): bstack1llll1l_opy_ (u"ࠧࡵࡧࡶࡸࠬᖶ"),
                bstack1llll1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᖷ"): getattr(threading.current_thread(), bstack1llll1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ᖸ"), None)
            }
        if getattr(threading.current_thread(), bstack1llll1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧᖹ"), None):
            return {
                bstack1llll1l_opy_ (u"ࠫࡹࡿࡰࡦࠩᖺ"): bstack1llll1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪᖻ"),
                bstack1llll1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᖼ"): getattr(threading.current_thread(), bstack1llll1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫᖽ"), None)
            }
        return None
    @staticmethod
    def bstack11lllll11l_opy_(driver):
        return {
            bstack11l1111l11_opy_(): bstack111ll1l1ll_opy_(driver)
        }
    @staticmethod
    def bstack1lll1ll111l_opy_(exception_info, report):
        return [{bstack1llll1l_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫᖾ"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack11ll1l11l1_opy_(typename):
        if bstack1llll1l_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࠧᖿ") in typename:
            return bstack1llll1l_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࡋࡲࡳࡱࡵࠦᗀ")
        return bstack1llll1l_opy_ (u"࡚ࠦࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠧᗁ")
    @staticmethod
    def bstack1lll1lllll1_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1ll1ll111l_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack1l111111ll_opy_(test, hook_name=None):
        bstack1llll111111_opy_ = test.parent
        if hook_name in [bstack1llll1l_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡨࡲࡡࡴࡵࠪᗂ"), bstack1llll1l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡥ࡯ࡥࡸࡹࠧᗃ"), bstack1llll1l_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪ࠭ᗄ"), bstack1llll1l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠪᗅ")]:
            bstack1llll111111_opy_ = test
        scope = []
        while bstack1llll111111_opy_ is not None:
            scope.append(bstack1llll111111_opy_.name)
            bstack1llll111111_opy_ = bstack1llll111111_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1lll1ll1lll_opy_(hook_type):
        if hook_type == bstack1llll1l_opy_ (u"ࠤࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠢᗆ"):
            return bstack1llll1l_opy_ (u"ࠥࡗࡪࡺࡵࡱࠢ࡫ࡳࡴࡱࠢᗇ")
        elif hook_type == bstack1llll1l_opy_ (u"ࠦࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠣᗈ"):
            return bstack1llll1l_opy_ (u"࡚ࠧࡥࡢࡴࡧࡳࡼࡴࠠࡩࡱࡲ࡯ࠧᗉ")
    @staticmethod
    def bstack1lll1llll1l_opy_(bstack1ll1ll111_opy_):
        try:
            if not bstack1ll1ll111l_opy_.on():
                return bstack1ll1ll111_opy_
            if os.environ.get(bstack1llll1l_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࠦᗊ"), None) == bstack1llll1l_opy_ (u"ࠢࡵࡴࡸࡩࠧᗋ"):
                tests = os.environ.get(bstack1llll1l_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓࡥࡔࡆࡕࡗࡗࠧᗌ"), None)
                if tests is None or tests == bstack1llll1l_opy_ (u"ࠤࡱࡹࡱࡲࠢᗍ"):
                    return bstack1ll1ll111_opy_
                bstack1ll1ll111_opy_ = tests.split(bstack1llll1l_opy_ (u"ࠪ࠰ࠬᗎ"))
                return bstack1ll1ll111_opy_
        except Exception as exc:
            print(bstack1llll1l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡶࡪࡸࡵ࡯ࠢ࡫ࡥࡳࡪ࡬ࡦࡴ࠽ࠤࠧᗏ"), str(exc))
        return bstack1ll1ll111_opy_
    @classmethod
    def bstack1l111l11l1_opy_(cls, event: str, bstack11llll111l_opy_: bstack1l1111111l_opy_):
        bstack1l1111llll_opy_ = {
            bstack1llll1l_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩᗐ"): event,
            bstack11llll111l_opy_.bstack1l11111l11_opy_(): bstack11llll111l_opy_.bstack11llll1l11_opy_(event)
        }
        bstack1ll1ll111l_opy_.bstack1l111ll1l1_opy_(bstack1l1111llll_opy_)