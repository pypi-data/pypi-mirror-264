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
import datetime
import json
import logging
import os
import threading
from bstack_utils.helper import bstack11ll11lll1_opy_, bstack111llll1l_opy_, get_host_info, bstack11l1ll1lll_opy_, bstack11l1llllll_opy_, bstack111ll1l1ll_opy_, \
    bstack11l11l1111_opy_, bstack111llll11l_opy_, bstack1l1l1l11_opy_, bstack11l11l1l1l_opy_, bstack11l1l1lll_opy_, bstack11llll1l11_opy_
from bstack_utils.bstack1lllll1l1l1_opy_ import bstack1lllll1lll1_opy_
from bstack_utils.bstack1l111l1l1l_opy_ import bstack1l111ll11l_opy_
import bstack_utils.bstack11111111l_opy_ as bstack1ll1l11l1l_opy_
from bstack_utils.constants import bstack11l1l1l111_opy_
bstack1lll1llll11_opy_ = [
    bstack1l_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨᓨ"), bstack1l_opy_ (u"ࠬࡉࡂࡕࡕࡨࡷࡸ࡯࡯࡯ࡅࡵࡩࡦࡺࡥࡥࠩᓩ"), bstack1l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨᓪ"), bstack1l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨᓫ"),
    bstack1l_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪᓬ"), bstack1l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪᓭ"), bstack1l_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫᓮ")
]
bstack1lll1llllll_opy_ = bstack1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡩ࡯࡭࡮ࡨࡧࡹࡵࡲ࠮ࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫᓯ")
logger = logging.getLogger(__name__)
class bstack1llll1111l_opy_:
    bstack1lllll1l1l1_opy_ = None
    bs_config = None
    @classmethod
    @bstack11llll1l11_opy_(class_method=True)
    def launch(cls, bs_config, bstack1llll111l11_opy_):
        cls.bs_config = bs_config
        cls.bstack1lll1lll1ll_opy_()
        bstack11ll11llll_opy_ = bstack11l1ll1lll_opy_(bs_config)
        bstack11l1lll11l_opy_ = bstack11l1llllll_opy_(bs_config)
        bstack1lll1lll11_opy_ = False
        bstack1l11llllll_opy_ = False
        if bstack1l_opy_ (u"ࠬࡧࡰࡱࠩᓰ") in bs_config:
            bstack1lll1lll11_opy_ = True
        else:
            bstack1l11llllll_opy_ = True
        bstack111l111ll_opy_ = {
            bstack1l_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ᓱ"): cls.bstack1l111l1ll_opy_() and cls.bstack1llll111lll_opy_(bstack1llll111l11_opy_.get(bstack1l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡹࡸ࡫ࡤࠨᓲ"), bstack1l_opy_ (u"ࠨࠩᓳ"))),
            bstack1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᓴ"): bstack1ll1l11l1l_opy_.bstack11llll1ll_opy_(bs_config),
            bstack1l_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩᓵ"): bs_config.get(bstack1l_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪᓶ"), False),
            bstack1l_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧᓷ"): bstack1l11llllll_opy_,
            bstack1l_opy_ (u"࠭ࡡࡱࡲࡢࡥࡺࡺ࡯࡮ࡣࡷࡩࠬᓸ"): bstack1lll1lll11_opy_
        }
        data = {
            bstack1l_opy_ (u"ࠧࡧࡱࡵࡱࡦࡺࠧᓹ"): bstack1l_opy_ (u"ࠨ࡬ࡶࡳࡳ࠭ᓺ"),
            bstack1l_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡢࡲࡦࡳࡥࠨᓻ"): bs_config.get(bstack1l_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨᓼ"), bstack1l_opy_ (u"ࠫࠬᓽ")),
            bstack1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᓾ"): bs_config.get(bstack1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩᓿ"), os.path.basename(os.path.abspath(os.getcwd()))),
            bstack1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪᔀ"): bs_config.get(bstack1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪᔁ")),
            bstack1l_opy_ (u"ࠩࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧᔂ"): bs_config.get(bstack1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡆࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭ᔃ"), bstack1l_opy_ (u"ࠫࠬᔄ")),
            bstack1l_opy_ (u"ࠬࡹࡴࡢࡴࡷࡣࡹ࡯࡭ࡦࠩᔅ"): datetime.datetime.now().isoformat(),
            bstack1l_opy_ (u"࠭ࡴࡢࡩࡶࠫᔆ"): bstack111ll1l1ll_opy_(bs_config),
            bstack1l_opy_ (u"ࠧࡩࡱࡶࡸࡤ࡯࡮ࡧࡱࠪᔇ"): get_host_info(),
            bstack1l_opy_ (u"ࠨࡥ࡬ࡣ࡮ࡴࡦࡰࠩᔈ"): bstack111llll1l_opy_(),
            bstack1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡴࡸࡲࡤ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩᔉ"): os.environ.get(bstack1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅ࡙ࡎࡒࡄࡠࡔࡘࡒࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩᔊ")),
            bstack1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࡣࡹ࡫ࡳࡵࡵࡢࡶࡪࡸࡵ࡯ࠩᔋ"): os.environ.get(bstack1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࠪᔌ"), False),
            bstack1l_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴ࡟ࡤࡱࡱࡸࡷࡵ࡬ࠨᔍ"): bstack11ll11lll1_opy_(),
            bstack1l_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࡠ࡯ࡤࡴࠬᔎ"): bstack111l111ll_opy_,
            bstack1l_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᔏ"): {
                bstack1l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡓࡧ࡭ࡦࠩᔐ"): bstack1llll111l11_opy_.get(bstack1l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࠫᔑ"), bstack1l_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷࠫᔒ")),
                bstack1l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᔓ"): bstack1llll111l11_opy_.get(bstack1l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪᔔ")),
                bstack1l_opy_ (u"ࠧࡴࡦ࡮࡚ࡪࡸࡳࡪࡱࡱࠫᔕ"): bstack1llll111l11_opy_.get(bstack1l_opy_ (u"ࠨࡵࡧ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᔖ"))
            }
        }
        config = {
            bstack1l_opy_ (u"ࠩࡤࡹࡹ࡮ࠧᔗ"): (bstack11ll11llll_opy_, bstack11l1lll11l_opy_),
            bstack1l_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫᔘ"): cls.default_headers()
        }
        response = bstack1l1l1l11_opy_(bstack1l_opy_ (u"ࠫࡕࡕࡓࡕࠩᔙ"), cls.request_url(bstack1l_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡨࡵࡪ࡮ࡧࡷࠬᔚ")), data, config)
        if response.status_code != 200:
            os.environ[bstack1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫᔛ")] = bstack1l_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬᔜ")
            os.environ[bstack1l_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡈࡕࡍࡑࡎࡈࡘࡊࡊࠧᔝ")] = bstack1l_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨᔞ")
            os.environ[bstack1l_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡋ࡙ࡗࠫᔟ")] = bstack1l_opy_ (u"ࠫࡳࡻ࡬࡭ࠩᔠ")
            os.environ[bstack1l_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡊࡄࡗࡍࡋࡄࡠࡋࡇࠫᔡ")] = bstack1l_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦᔢ")
            os.environ[bstack1l_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡆࡒࡌࡐ࡙ࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࡓࠨᔣ")] = bstack1l_opy_ (u"ࠣࡰࡸࡰࡱࠨᔤ")
            bstack1llll111111_opy_ = response.json()
            if bstack1llll111111_opy_ and bstack1llll111111_opy_[bstack1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᔥ")]:
                error_message = bstack1llll111111_opy_[bstack1l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᔦ")]
                if bstack1llll111111_opy_[bstack1l_opy_ (u"ࠫࡪࡸࡲࡰࡴࡗࡽࡵ࡫ࠧᔧ")] == bstack1l_opy_ (u"ࠬࡋࡒࡓࡑࡕࡣࡎࡔࡖࡂࡎࡌࡈࡤࡉࡒࡆࡆࡈࡒ࡙ࡏࡁࡍࡕࠪᔨ"):
                    logger.error(error_message)
                elif bstack1llll111111_opy_[bstack1l_opy_ (u"࠭ࡥࡳࡴࡲࡶ࡙ࡿࡰࡦࠩᔩ")] == bstack1l_opy_ (u"ࠧࡆࡔࡕࡓࡗࡥࡁࡄࡅࡈࡗࡘࡥࡄࡆࡐࡌࡉࡉ࠭ᔪ"):
                    logger.info(error_message)
                elif bstack1llll111111_opy_[bstack1l_opy_ (u"ࠨࡧࡵࡶࡴࡸࡔࡺࡲࡨࠫᔫ")] == bstack1l_opy_ (u"ࠩࡈࡖࡗࡕࡒࡠࡕࡇࡏࡤࡊࡅࡑࡔࡈࡇࡆ࡚ࡅࡅࠩᔬ"):
                    logger.error(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack1l_opy_ (u"ࠥࡈࡦࡺࡡࠡࡷࡳࡰࡴࡧࡤࠡࡶࡲࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡘࡪࡹࡴࠡࡑࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡦࡸࡩࠥࡺ࡯ࠡࡵࡲࡱࡪࠦࡥࡳࡴࡲࡶࠧᔭ"))
            return [None, None, None]
        bstack1llll111111_opy_ = response.json()
        os.environ[bstack1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩᔮ")] = bstack1llll111111_opy_[bstack1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧᔯ")]
        if cls.bstack1l111l1ll_opy_() is True and cls.bstack1llll111lll_opy_(bstack1llll111l11_opy_.get(bstack1l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡸࡷࡪࡪࠧᔰ"), bstack1l_opy_ (u"ࠧࠨᔱ"))):
            logger.debug(bstack1l_opy_ (u"ࠨࡖࡨࡷࡹࠦࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾࠦࡂࡶ࡫࡯ࡨࠥࡩࡲࡦࡣࡷ࡭ࡴࡴࠠࡔࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࠥࠬᔲ"))
            os.environ[bstack1l_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡉࡏࡎࡒࡏࡉ࡙ࡋࡄࠨᔳ")] = bstack1l_opy_ (u"ࠪࡸࡷࡻࡥࠨᔴ")
            if bstack1llll111111_opy_.get(bstack1l_opy_ (u"ࠫ࡯ࡽࡴࠨᔵ")):
                os.environ[bstack1l_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡍ࡛࡙࠭ᔶ")] = bstack1llll111111_opy_[bstack1l_opy_ (u"࠭ࡪࡸࡶࠪᔷ")]
                os.environ[bstack1l_opy_ (u"ࠧࡄࡔࡈࡈࡊࡔࡔࡊࡃࡏࡗࡤࡌࡏࡓࡡࡆࡖࡆ࡙ࡈࡠࡔࡈࡔࡔࡘࡔࡊࡐࡊࠫᔸ")] = json.dumps({
                    bstack1l_opy_ (u"ࠨࡷࡶࡩࡷࡴࡡ࡮ࡧࠪᔹ"): bstack11ll11llll_opy_,
                    bstack1l_opy_ (u"ࠩࡳࡥࡸࡹࡷࡰࡴࡧࠫᔺ"): bstack11l1lll11l_opy_
                })
            if bstack1llll111111_opy_.get(bstack1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬᔻ")):
                os.environ[bstack1l_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡉࡃࡖࡌࡊࡊ࡟ࡊࡆࠪᔼ")] = bstack1llll111111_opy_[bstack1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧᔽ")]
            if bstack1llll111111_opy_.get(bstack1l_opy_ (u"࠭ࡡ࡭࡮ࡲࡻࡤࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪᔾ")):
                os.environ[bstack1l_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡆࡒࡌࡐ࡙ࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࡓࠨᔿ")] = str(bstack1llll111111_opy_[bstack1l_opy_ (u"ࠨࡣ࡯ࡰࡴࡽ࡟ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࡷࠬᕀ")])
        return [bstack1llll111111_opy_[bstack1l_opy_ (u"ࠩ࡭ࡻࡹ࠭ᕁ")], bstack1llll111111_opy_[bstack1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬᕂ")], bstack1llll111111_opy_[bstack1l_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡢࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨᕃ")]]
    @classmethod
    @bstack11llll1l11_opy_(class_method=True)
    def stop(cls):
        if not cls.on():
            return
        if os.environ[bstack1l_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡍ࡛࡙࠭ᕄ")] == bstack1l_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦᕅ") or os.environ[bstack1l_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉ࠭ᕆ")] == bstack1l_opy_ (u"ࠣࡰࡸࡰࡱࠨᕇ"):
            print(bstack1l_opy_ (u"ࠩࡈ࡜ࡈࡋࡐࡕࡋࡒࡒࠥࡏࡎࠡࡵࡷࡳࡵࡈࡵࡪ࡮ࡧ࡙ࡵࡹࡴࡳࡧࡤࡱࠥࡘࡅࡒࡗࡈࡗ࡙ࠦࡔࡐࠢࡗࡉࡘ࡚ࠠࡐࡄࡖࡉࡗ࡜ࡁࡃࡋࡏࡍ࡙࡟ࠠ࠻ࠢࡐ࡭ࡸࡹࡩ࡯ࡩࠣࡥࡺࡺࡨࡦࡰࡷ࡭ࡨࡧࡴࡪࡱࡱࠤࡹࡵ࡫ࡦࡰࠪᕈ"))
            return {
                bstack1l_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪᕉ"): bstack1l_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᕊ"),
                bstack1l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᕋ"): bstack1l_opy_ (u"࠭ࡔࡰ࡭ࡨࡲ࠴ࡨࡵࡪ࡮ࡧࡍࡉࠦࡩࡴࠢࡸࡲࡩ࡫ࡦࡪࡰࡨࡨ࠱ࠦࡢࡶ࡫࡯ࡨࠥࡩࡲࡦࡣࡷ࡭ࡴࡴࠠ࡮࡫ࡪ࡬ࡹࠦࡨࡢࡸࡨࠤ࡫ࡧࡩ࡭ࡧࡧࠫᕌ")
            }
        else:
            cls.bstack1lllll1l1l1_opy_.shutdown()
            data = {
                bstack1l_opy_ (u"ࠧࡴࡶࡲࡴࡤࡺࡩ࡮ࡧࠪᕍ"): datetime.datetime.now().isoformat()
            }
            config = {
                bstack1l_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩᕎ"): cls.default_headers()
            }
            bstack11l111l111_opy_ = bstack1l_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁ࠴ࡹࡴࡰࡲࠪᕏ").format(os.environ[bstack1l_opy_ (u"ࠥࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡈࡂࡕࡋࡉࡉࡥࡉࡅࠤᕐ")])
            bstack1lll1ll1l11_opy_ = cls.request_url(bstack11l111l111_opy_)
            response = bstack1l1l1l11_opy_(bstack1l_opy_ (u"ࠫࡕ࡛ࡔࠨᕑ"), bstack1lll1ll1l11_opy_, data, config)
            if not response.ok:
                raise Exception(bstack1l_opy_ (u"࡙ࠧࡴࡰࡲࠣࡶࡪࡷࡵࡦࡵࡷࠤࡳࡵࡴࠡࡱ࡮ࠦᕒ"))
    @classmethod
    def bstack11lll1l1ll_opy_(cls):
        if cls.bstack1lllll1l1l1_opy_ is None:
            return
        cls.bstack1lllll1l1l1_opy_.shutdown()
    @classmethod
    def bstack1l1lll1ll_opy_(cls):
        if cls.on():
            print(
                bstack1l_opy_ (u"࠭ࡖࡪࡵ࡬ࡸࠥ࡮ࡴࡵࡲࡶ࠾࠴࠵࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁࠥࡺ࡯ࠡࡸ࡬ࡩࡼࠦࡢࡶ࡫࡯ࡨࠥࡸࡥࡱࡱࡵࡸ࠱ࠦࡩ࡯ࡵ࡬࡫࡭ࡺࡳ࠭ࠢࡤࡲࡩࠦ࡭ࡢࡰࡼࠤࡲࡵࡲࡦࠢࡧࡩࡧࡻࡧࡨ࡫ࡱ࡫ࠥ࡯࡮ࡧࡱࡵࡱࡦࡺࡩࡰࡰࠣࡥࡱࡲࠠࡢࡶࠣࡳࡳ࡫ࠠࡱ࡮ࡤࡧࡪࠧ࡜࡯ࠩᕓ").format(os.environ[bstack1l_opy_ (u"ࠢࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉࠨᕔ")]))
    @classmethod
    def bstack1lll1lll1ll_opy_(cls):
        if cls.bstack1lllll1l1l1_opy_ is not None:
            return
        cls.bstack1lllll1l1l1_opy_ = bstack1lllll1lll1_opy_(cls.bstack1lll1llll1l_opy_)
        cls.bstack1lllll1l1l1_opy_.start()
    @classmethod
    def bstack1l111lll11_opy_(cls, bstack1l11l11111_opy_, bstack1llll111l1l_opy_=bstack1l_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡤࡤࡸࡨ࡮ࠧᕕ")):
        if not cls.on():
            return
        bstack11lllllll_opy_ = bstack1l11l11111_opy_[bstack1l_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭ᕖ")]
        bstack1lll1lll111_opy_ = {
            bstack1l_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫᕗ"): bstack1l_opy_ (u"࡙ࠫ࡫ࡳࡵࡡࡖࡸࡦࡸࡴࡠࡗࡳࡰࡴࡧࡤࠨᕘ"),
            bstack1l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧᕙ"): bstack1l_opy_ (u"࠭ࡔࡦࡵࡷࡣࡊࡴࡤࡠࡗࡳࡰࡴࡧࡤࠨᕚ"),
            bstack1l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨᕛ"): bstack1l_opy_ (u"ࠨࡖࡨࡷࡹࡥࡓ࡬࡫ࡳࡴࡪࡪ࡟ࡖࡲ࡯ࡳࡦࡪࠧᕜ"),
            bstack1l_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭ᕝ"): bstack1l_opy_ (u"ࠪࡐࡴ࡭࡟ࡖࡲ࡯ࡳࡦࡪࠧᕞ"),
            bstack1l_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬᕟ"): bstack1l_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡢࡗࡹࡧࡲࡵࡡࡘࡴࡱࡵࡡࡥࠩᕠ"),
            bstack1l_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨᕡ"): bstack1l_opy_ (u"ࠧࡉࡱࡲ࡯ࡤࡋ࡮ࡥࡡࡘࡴࡱࡵࡡࡥࠩᕢ"),
            bstack1l_opy_ (u"ࠨࡅࡅࡘࡘ࡫ࡳࡴ࡫ࡲࡲࡈࡸࡥࡢࡶࡨࡨࠬᕣ"): bstack1l_opy_ (u"ࠩࡆࡆ࡙ࡥࡕࡱ࡮ࡲࡥࡩ࠭ᕤ")
        }.get(bstack11lllllll_opy_)
        if bstack1llll111l1l_opy_ == bstack1l_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡦࡦࡺࡣࡩࠩᕥ"):
            cls.bstack1lll1lll1ll_opy_()
            cls.bstack1lllll1l1l1_opy_.add(bstack1l11l11111_opy_)
        elif bstack1llll111l1l_opy_ == bstack1l_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩᕦ"):
            cls.bstack1lll1llll1l_opy_([bstack1l11l11111_opy_], bstack1llll111l1l_opy_)
    @classmethod
    @bstack11llll1l11_opy_(class_method=True)
    def bstack1lll1llll1l_opy_(cls, bstack1l11l11111_opy_, bstack1llll111l1l_opy_=bstack1l_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡨࡡࡵࡥ࡫ࠫᕧ")):
        config = {
            bstack1l_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧᕨ"): cls.default_headers()
        }
        response = bstack1l1l1l11_opy_(bstack1l_opy_ (u"ࠧࡑࡑࡖࡘࠬᕩ"), cls.request_url(bstack1llll111l1l_opy_), bstack1l11l11111_opy_, config)
        bstack11l1lll1ll_opy_ = response.json()
    @classmethod
    @bstack11llll1l11_opy_(class_method=True)
    def bstack1ll1l1lll_opy_(cls, bstack11lll1llll_opy_):
        bstack1lll1lll1l1_opy_ = []
        for log in bstack11lll1llll_opy_:
            bstack1lll1lll11l_opy_ = {
                bstack1l_opy_ (u"ࠨ࡭࡬ࡲࡩ࠭ᕪ"): bstack1l_opy_ (u"ࠩࡗࡉࡘ࡚࡟ࡍࡑࡊࠫᕫ"),
                bstack1l_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩᕬ"): log[bstack1l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪᕭ")],
                bstack1l_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨᕮ"): log[bstack1l_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩᕯ")],
                bstack1l_opy_ (u"ࠧࡩࡶࡷࡴࡤࡸࡥࡴࡲࡲࡲࡸ࡫ࠧᕰ"): {},
                bstack1l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᕱ"): log[bstack1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᕲ")],
            }
            if bstack1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᕳ") in log:
                bstack1lll1lll11l_opy_[bstack1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᕴ")] = log[bstack1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᕵ")]
            elif bstack1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᕶ") in log:
                bstack1lll1lll11l_opy_[bstack1l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᕷ")] = log[bstack1l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᕸ")]
            bstack1lll1lll1l1_opy_.append(bstack1lll1lll11l_opy_)
        cls.bstack1l111lll11_opy_({
            bstack1l_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭ᕹ"): bstack1l_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧᕺ"),
            bstack1l_opy_ (u"ࠫࡱࡵࡧࡴࠩᕻ"): bstack1lll1lll1l1_opy_
        })
    @classmethod
    @bstack11llll1l11_opy_(class_method=True)
    def bstack1lll1ll1lll_opy_(cls, steps):
        bstack1llll1111ll_opy_ = []
        for step in steps:
            bstack1lll1ll1l1l_opy_ = {
                bstack1l_opy_ (u"ࠬࡱࡩ࡯ࡦࠪᕼ"): bstack1l_opy_ (u"࠭ࡔࡆࡕࡗࡣࡘ࡚ࡅࡑࠩᕽ"),
                bstack1l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ᕾ"): step[bstack1l_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧᕿ")],
                bstack1l_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬᖀ"): step[bstack1l_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ᖁ")],
                bstack1l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᖂ"): step[bstack1l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᖃ")],
                bstack1l_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠨᖄ"): step[bstack1l_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩᖅ")]
            }
            if bstack1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᖆ") in step:
                bstack1lll1ll1l1l_opy_[bstack1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᖇ")] = step[bstack1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᖈ")]
            elif bstack1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᖉ") in step:
                bstack1lll1ll1l1l_opy_[bstack1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᖊ")] = step[bstack1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᖋ")]
            bstack1llll1111ll_opy_.append(bstack1lll1ll1l1l_opy_)
        cls.bstack1l111lll11_opy_({
            bstack1l_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫᖌ"): bstack1l_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬᖍ"),
            bstack1l_opy_ (u"ࠩ࡯ࡳ࡬ࡹࠧᖎ"): bstack1llll1111ll_opy_
        })
    @classmethod
    @bstack11llll1l11_opy_(class_method=True)
    def bstack11l1lll11_opy_(cls, screenshot):
        cls.bstack1l111lll11_opy_({
            bstack1l_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧᖏ"): bstack1l_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨᖐ"),
            bstack1l_opy_ (u"ࠬࡲ࡯ࡨࡵࠪᖑ"): [{
                bstack1l_opy_ (u"࠭࡫ࡪࡰࡧࠫᖒ"): bstack1l_opy_ (u"ࠧࡕࡇࡖࡘࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࠩᖓ"),
                bstack1l_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫᖔ"): datetime.datetime.utcnow().isoformat() + bstack1l_opy_ (u"ࠩ࡝ࠫᖕ"),
                bstack1l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᖖ"): screenshot[bstack1l_opy_ (u"ࠫ࡮ࡳࡡࡨࡧࠪᖗ")],
                bstack1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᖘ"): screenshot[bstack1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᖙ")]
            }]
        }, bstack1llll111l1l_opy_=bstack1l_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࡷࠬᖚ"))
    @classmethod
    @bstack11llll1l11_opy_(class_method=True)
    def bstack11l1lll1_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack1l111lll11_opy_({
            bstack1l_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬᖛ"): bstack1l_opy_ (u"ࠩࡆࡆ࡙࡙ࡥࡴࡵ࡬ࡳࡳࡉࡲࡦࡣࡷࡩࡩ࠭ᖜ"),
            bstack1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬᖝ"): {
                bstack1l_opy_ (u"ࠦࡺࡻࡩࡥࠤᖞ"): cls.current_test_uuid(),
                bstack1l_opy_ (u"ࠧ࡯࡮ࡵࡧࡪࡶࡦࡺࡩࡰࡰࡶࠦᖟ"): cls.bstack1l111l1111_opy_(driver)
            }
        })
    @classmethod
    def on(cls):
        if os.environ.get(bstack1l_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡎ࡜࡚ࠧᖠ"), None) is None or os.environ[bstack1l_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡏ࡝ࡔࠨᖡ")] == bstack1l_opy_ (u"ࠣࡰࡸࡰࡱࠨᖢ"):
            return False
        return True
    @classmethod
    def bstack1l111l1ll_opy_(cls):
        return bstack11l1l1lll_opy_(cls.bs_config.get(bstack1l_opy_ (u"ࠩࡷࡩࡸࡺࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ᖣ"), False))
    @classmethod
    def bstack1llll111lll_opy_(cls, framework):
        return framework in bstack11l1l1l111_opy_
    @staticmethod
    def request_url(url):
        return bstack1l_opy_ (u"ࠪࡿࢂ࠵ࡻࡾࠩᖤ").format(bstack1lll1llllll_opy_, url)
    @staticmethod
    def default_headers():
        headers = {
            bstack1l_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪᖥ"): bstack1l_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨᖦ"),
            bstack1l_opy_ (u"࠭ࡘ࠮ࡄࡖࡘࡆࡉࡋ࠮ࡖࡈࡗ࡙ࡕࡐࡔࠩᖧ"): bstack1l_opy_ (u"ࠧࡵࡴࡸࡩࠬᖨ")
        }
        if os.environ.get(bstack1l_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡐࡗࡕࠩᖩ"), None):
            headers[bstack1l_opy_ (u"ࠩࡄࡹࡹ࡮࡯ࡳ࡫ࡽࡥࡹ࡯࡯࡯ࠩᖪ")] = bstack1l_opy_ (u"ࠪࡆࡪࡧࡲࡦࡴࠣࡿࢂ࠭ᖫ").format(os.environ[bstack1l_opy_ (u"ࠦࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡌ࡚ࡘࠧᖬ")])
        return headers
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩᖭ"), None)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪᖮ"), None)
    @staticmethod
    def bstack1l1111l111_opy_():
        if getattr(threading.current_thread(), bstack1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫᖯ"), None):
            return {
                bstack1l_opy_ (u"ࠨࡶࡼࡴࡪ࠭ᖰ"): bstack1l_opy_ (u"ࠩࡷࡩࡸࡺࠧᖱ"),
                bstack1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᖲ"): getattr(threading.current_thread(), bstack1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨᖳ"), None)
            }
        if getattr(threading.current_thread(), bstack1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩᖴ"), None):
            return {
                bstack1l_opy_ (u"࠭ࡴࡺࡲࡨࠫᖵ"): bstack1l_opy_ (u"ࠧࡩࡱࡲ࡯ࠬᖶ"),
                bstack1l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᖷ"): getattr(threading.current_thread(), bstack1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭ᖸ"), None)
            }
        return None
    @staticmethod
    def bstack1l111l1111_opy_(driver):
        return {
            bstack111llll11l_opy_(): bstack11l11l1111_opy_(driver)
        }
    @staticmethod
    def bstack1llll11111l_opy_(exception_info, report):
        return [{bstack1l_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭ᖹ"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack11ll1l1l1l_opy_(typename):
        if bstack1l_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࠢᖺ") in typename:
            return bstack1l_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࡆࡴࡵࡳࡷࠨᖻ")
        return bstack1l_opy_ (u"ࠨࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠢᖼ")
    @staticmethod
    def bstack1lll1lllll1_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1llll1111l_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack1l1111ll1l_opy_(test, hook_name=None):
        bstack1llll111ll1_opy_ = test.parent
        if hook_name in [bstack1l_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡣ࡭ࡣࡶࡷࠬᖽ"), bstack1l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠩᖾ"), bstack1l_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࠨᖿ"), bstack1l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳ࡯ࡥࡷ࡯ࡩࠬᗀ")]:
            bstack1llll111ll1_opy_ = test
        scope = []
        while bstack1llll111ll1_opy_ is not None:
            scope.append(bstack1llll111ll1_opy_.name)
            bstack1llll111ll1_opy_ = bstack1llll111ll1_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1lll1ll1ll1_opy_(hook_type):
        if hook_type == bstack1l_opy_ (u"ࠦࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠤᗁ"):
            return bstack1l_opy_ (u"࡙ࠧࡥࡵࡷࡳࠤ࡭ࡵ࡯࡬ࠤᗂ")
        elif hook_type == bstack1l_opy_ (u"ࠨࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠥᗃ"):
            return bstack1l_opy_ (u"ࠢࡕࡧࡤࡶࡩࡵࡷ࡯ࠢ࡫ࡳࡴࡱࠢᗄ")
    @staticmethod
    def bstack1llll1111l1_opy_(bstack1l1lll1ll1_opy_):
        try:
            if not bstack1llll1111l_opy_.on():
                return bstack1l1lll1ll1_opy_
            if os.environ.get(bstack1l_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓࠨᗅ"), None) == bstack1l_opy_ (u"ࠤࡷࡶࡺ࡫ࠢᗆ"):
                tests = os.environ.get(bstack1l_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࡠࡖࡈࡗ࡙࡙ࠢᗇ"), None)
                if tests is None or tests == bstack1l_opy_ (u"ࠦࡳࡻ࡬࡭ࠤᗈ"):
                    return bstack1l1lll1ll1_opy_
                bstack1l1lll1ll1_opy_ = tests.split(bstack1l_opy_ (u"ࠬ࠲ࠧᗉ"))
                return bstack1l1lll1ll1_opy_
        except Exception as exc:
            print(bstack1l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡸࡥࡳࡷࡱࠤ࡭ࡧ࡮ࡥ࡮ࡨࡶ࠿ࠦࠢᗊ"), str(exc))
        return bstack1l1lll1ll1_opy_
    @classmethod
    def bstack1l111ll1ll_opy_(cls, event: str, bstack1l11l11111_opy_: bstack1l111ll11l_opy_):
        bstack1l11l111l1_opy_ = {
            bstack1l_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫᗋ"): event,
            bstack1l11l11111_opy_.bstack11lllll1ll_opy_(): bstack1l11l11111_opy_.bstack1l11l1111l_opy_(event)
        }
        bstack1llll1111l_opy_.bstack1l111lll11_opy_(bstack1l11l111l1_opy_)