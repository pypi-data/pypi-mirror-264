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
import os
import json
import logging
logger = logging.getLogger(__name__)
class BrowserStackSdk:
    def get_current_platform():
        bstack1llllll111_opy_ = {}
        bstack1l11l11ll1_opy_ = os.environ.get(bstack1llll1l_opy_ (u"ࠩࡆ࡙ࡗࡘࡅࡏࡖࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡊࡁࡕࡃࠪഛ"), bstack1llll1l_opy_ (u"ࠪࠫജ"))
        if not bstack1l11l11ll1_opy_:
            return bstack1llllll111_opy_
        try:
            bstack1l11l11lll_opy_ = json.loads(bstack1l11l11ll1_opy_)
            if bstack1llll1l_opy_ (u"ࠦࡴࡹࠢഝ") in bstack1l11l11lll_opy_:
                bstack1llllll111_opy_[bstack1llll1l_opy_ (u"ࠧࡵࡳࠣഞ")] = bstack1l11l11lll_opy_[bstack1llll1l_opy_ (u"ࠨ࡯ࡴࠤട")]
            if bstack1llll1l_opy_ (u"ࠢࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠦഠ") in bstack1l11l11lll_opy_ or bstack1llll1l_opy_ (u"ࠣࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠦഡ") in bstack1l11l11lll_opy_:
                bstack1llllll111_opy_[bstack1llll1l_opy_ (u"ࠤࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠧഢ")] = bstack1l11l11lll_opy_.get(bstack1llll1l_opy_ (u"ࠥࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠢണ"), bstack1l11l11lll_opy_.get(bstack1llll1l_opy_ (u"ࠦࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠢത")))
            if bstack1llll1l_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࠨഥ") in bstack1l11l11lll_opy_ or bstack1llll1l_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠦദ") in bstack1l11l11lll_opy_:
                bstack1llllll111_opy_[bstack1llll1l_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠧധ")] = bstack1l11l11lll_opy_.get(bstack1llll1l_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࠤന"), bstack1l11l11lll_opy_.get(bstack1llll1l_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠢഩ")))
            if bstack1llll1l_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧപ") in bstack1l11l11lll_opy_ or bstack1llll1l_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠧഫ") in bstack1l11l11lll_opy_:
                bstack1llllll111_opy_[bstack1llll1l_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳࠨബ")] = bstack1l11l11lll_opy_.get(bstack1llll1l_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣഭ"), bstack1l11l11lll_opy_.get(bstack1llll1l_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠣമ")))
            if bstack1llll1l_opy_ (u"ࠣࡦࡨࡺ࡮ࡩࡥࠣയ") in bstack1l11l11lll_opy_ or bstack1llll1l_opy_ (u"ࠤࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪࠨര") in bstack1l11l11lll_opy_:
                bstack1llllll111_opy_[bstack1llll1l_opy_ (u"ࠥࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠢറ")] = bstack1l11l11lll_opy_.get(bstack1llll1l_opy_ (u"ࠦࡩ࡫ࡶࡪࡥࡨࠦല"), bstack1l11l11lll_opy_.get(bstack1llll1l_opy_ (u"ࠧࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠤള")))
            if bstack1llll1l_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠣഴ") in bstack1l11l11lll_opy_ or bstack1llll1l_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪࠨവ") in bstack1l11l11lll_opy_:
                bstack1llllll111_opy_[bstack1llll1l_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠢശ")] = bstack1l11l11lll_opy_.get(bstack1llll1l_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࠦഷ"), bstack1l11l11lll_opy_.get(bstack1llll1l_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠤസ")))
            if bstack1llll1l_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡥࡶࡦࡴࡶ࡭ࡴࡴࠢഹ") in bstack1l11l11lll_opy_ or bstack1llll1l_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢഺ") in bstack1l11l11lll_opy_:
                bstack1llllll111_opy_[bstack1llll1l_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮഻ࠣ")] = bstack1l11l11lll_opy_.get(bstack1llll1l_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡࡹࡩࡷࡹࡩࡰࡰ഼ࠥ"), bstack1l11l11lll_opy_.get(bstack1llll1l_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠥഽ")))
            if bstack1llll1l_opy_ (u"ࠤࡦࡹࡸࡺ࡯࡮ࡘࡤࡶ࡮ࡧࡢ࡭ࡧࡶࠦാ") in bstack1l11l11lll_opy_:
                bstack1llllll111_opy_[bstack1llll1l_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯࡙ࡥࡷ࡯ࡡࡣ࡮ࡨࡷࠧി")] = bstack1l11l11lll_opy_[bstack1llll1l_opy_ (u"ࠦࡨࡻࡳࡵࡱࡰ࡚ࡦࡸࡩࡢࡤ࡯ࡩࡸࠨീ")]
        except Exception as error:
            logger.error(bstack1llll1l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡥࡸࡶࡷ࡫࡮ࡵࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤࡩࡧࡴࡢ࠼ࠣࠦു") +  str(error))
        return bstack1llllll111_opy_