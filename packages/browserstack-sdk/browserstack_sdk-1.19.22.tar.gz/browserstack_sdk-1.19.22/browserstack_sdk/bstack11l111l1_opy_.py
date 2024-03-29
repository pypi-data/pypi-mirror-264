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
import os
import json
import logging
logger = logging.getLogger(__name__)
class BrowserStackSdk:
    def get_current_platform():
        bstack1l111ll1l_opy_ = {}
        bstack1l11l11ll1_opy_ = os.environ.get(bstack1ll11l_opy_ (u"ࠩࡆ࡙ࡗࡘࡅࡏࡖࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡊࡁࡕࡃࠪഛ"), bstack1ll11l_opy_ (u"ࠪࠫജ"))
        if not bstack1l11l11ll1_opy_:
            return bstack1l111ll1l_opy_
        try:
            bstack1l11l11lll_opy_ = json.loads(bstack1l11l11ll1_opy_)
            if bstack1ll11l_opy_ (u"ࠦࡴࡹࠢഝ") in bstack1l11l11lll_opy_:
                bstack1l111ll1l_opy_[bstack1ll11l_opy_ (u"ࠧࡵࡳࠣഞ")] = bstack1l11l11lll_opy_[bstack1ll11l_opy_ (u"ࠨ࡯ࡴࠤട")]
            if bstack1ll11l_opy_ (u"ࠢࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠦഠ") in bstack1l11l11lll_opy_ or bstack1ll11l_opy_ (u"ࠣࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠦഡ") in bstack1l11l11lll_opy_:
                bstack1l111ll1l_opy_[bstack1ll11l_opy_ (u"ࠤࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠧഢ")] = bstack1l11l11lll_opy_.get(bstack1ll11l_opy_ (u"ࠥࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠢണ"), bstack1l11l11lll_opy_.get(bstack1ll11l_opy_ (u"ࠦࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠢത")))
            if bstack1ll11l_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࠨഥ") in bstack1l11l11lll_opy_ or bstack1ll11l_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠦദ") in bstack1l11l11lll_opy_:
                bstack1l111ll1l_opy_[bstack1ll11l_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠧധ")] = bstack1l11l11lll_opy_.get(bstack1ll11l_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࠤന"), bstack1l11l11lll_opy_.get(bstack1ll11l_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠢഩ")))
            if bstack1ll11l_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧപ") in bstack1l11l11lll_opy_ or bstack1ll11l_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠧഫ") in bstack1l11l11lll_opy_:
                bstack1l111ll1l_opy_[bstack1ll11l_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳࠨബ")] = bstack1l11l11lll_opy_.get(bstack1ll11l_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣഭ"), bstack1l11l11lll_opy_.get(bstack1ll11l_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠣമ")))
            if bstack1ll11l_opy_ (u"ࠣࡦࡨࡺ࡮ࡩࡥࠣയ") in bstack1l11l11lll_opy_ or bstack1ll11l_opy_ (u"ࠤࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪࠨര") in bstack1l11l11lll_opy_:
                bstack1l111ll1l_opy_[bstack1ll11l_opy_ (u"ࠥࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠢറ")] = bstack1l11l11lll_opy_.get(bstack1ll11l_opy_ (u"ࠦࡩ࡫ࡶࡪࡥࡨࠦല"), bstack1l11l11lll_opy_.get(bstack1ll11l_opy_ (u"ࠧࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠤള")))
            if bstack1ll11l_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠣഴ") in bstack1l11l11lll_opy_ or bstack1ll11l_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪࠨവ") in bstack1l11l11lll_opy_:
                bstack1l111ll1l_opy_[bstack1ll11l_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠢശ")] = bstack1l11l11lll_opy_.get(bstack1ll11l_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࠦഷ"), bstack1l11l11lll_opy_.get(bstack1ll11l_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠤസ")))
            if bstack1ll11l_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡥࡶࡦࡴࡶ࡭ࡴࡴࠢഹ") in bstack1l11l11lll_opy_ or bstack1ll11l_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢഺ") in bstack1l11l11lll_opy_:
                bstack1l111ll1l_opy_[bstack1ll11l_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮഻ࠣ")] = bstack1l11l11lll_opy_.get(bstack1ll11l_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡࡹࡩࡷࡹࡩࡰࡰ഼ࠥ"), bstack1l11l11lll_opy_.get(bstack1ll11l_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠥഽ")))
            if bstack1ll11l_opy_ (u"ࠤࡦࡹࡸࡺ࡯࡮ࡘࡤࡶ࡮ࡧࡢ࡭ࡧࡶࠦാ") in bstack1l11l11lll_opy_:
                bstack1l111ll1l_opy_[bstack1ll11l_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯࡙ࡥࡷ࡯ࡡࡣ࡮ࡨࡷࠧി")] = bstack1l11l11lll_opy_[bstack1ll11l_opy_ (u"ࠦࡨࡻࡳࡵࡱࡰ࡚ࡦࡸࡩࡢࡤ࡯ࡩࡸࠨീ")]
        except Exception as error:
            logger.error(bstack1ll11l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡥࡸࡶࡷ࡫࡮ࡵࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤࡩࡧࡴࡢ࠼ࠣࠦു") +  str(error))
        return bstack1l111ll1l_opy_