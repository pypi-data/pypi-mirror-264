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
from uuid import uuid4
from bstack_utils.helper import bstack1ll111ll11_opy_, bstack111lllll11_opy_
from bstack_utils.bstack11111ll1l_opy_ import bstack1llllll1l11_opy_
class bstack11llll11ll_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, bstack11lllll1ll_opy_=None, framework=None, tags=[], scope=[], bstack1llll11l1ll_opy_=None, bstack1llll11ll11_opy_=True, bstack1llll1ll1l1_opy_=None, bstack1ll1ll1l1_opy_=None, result=None, duration=None, bstack1l11111l1l_opy_=None, meta={}):
        self.bstack1l11111l1l_opy_ = bstack1l11111l1l_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1llll11ll11_opy_:
            self.uuid = uuid4().__str__()
        self.bstack11lllll1ll_opy_ = bstack11lllll1ll_opy_
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack1llll11l1ll_opy_ = bstack1llll11l1ll_opy_
        self.bstack1llll1ll1l1_opy_ = bstack1llll1ll1l1_opy_
        self.bstack1ll1ll1l1_opy_ = bstack1ll1ll1l1_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
    def bstack11lll1ll1l_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack1llll1ll11l_opy_(self):
        bstack1llll1l1lll_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack1ll11l_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨᒪ"): bstack1llll1l1lll_opy_,
            bstack1ll11l_opy_ (u"࠭࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠨᒫ"): bstack1llll1l1lll_opy_,
            bstack1ll11l_opy_ (u"ࠧࡷࡥࡢࡪ࡮ࡲࡥࡱࡣࡷ࡬ࠬᒬ"): bstack1llll1l1lll_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack1ll11l_opy_ (u"ࠣࡗࡱࡩࡽࡶࡥࡤࡶࡨࡨࠥࡧࡲࡨࡷࡰࡩࡳࡺ࠺ࠡࠤᒭ") + key)
            setattr(self, key, val)
    def bstack1llll1ll111_opy_(self):
        return {
            bstack1ll11l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᒮ"): self.name,
            bstack1ll11l_opy_ (u"ࠪࡦࡴࡪࡹࠨᒯ"): {
                bstack1ll11l_opy_ (u"ࠫࡱࡧ࡮ࡨࠩᒰ"): bstack1ll11l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬᒱ"),
                bstack1ll11l_opy_ (u"࠭ࡣࡰࡦࡨࠫᒲ"): self.code
            },
            bstack1ll11l_opy_ (u"ࠧࡴࡥࡲࡴࡪࡹࠧᒳ"): self.scope,
            bstack1ll11l_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭ᒴ"): self.tags,
            bstack1ll11l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬᒵ"): self.framework,
            bstack1ll11l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᒶ"): self.bstack11lllll1ll_opy_
        }
    def bstack1llll11l1l1_opy_(self):
        return {
         bstack1ll11l_opy_ (u"ࠫࡲ࡫ࡴࡢࠩᒷ"): self.meta
        }
    def bstack1llll1l1l11_opy_(self):
        return {
            bstack1ll11l_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡗ࡫ࡲࡶࡰࡓࡥࡷࡧ࡭ࠨᒸ"): {
                bstack1ll11l_opy_ (u"࠭ࡲࡦࡴࡸࡲࡤࡴࡡ࡮ࡧࠪᒹ"): self.bstack1llll11l1ll_opy_
            }
        }
    def bstack1llll11ll1l_opy_(self, bstack1llll1l1111_opy_, details):
        step = next(filter(lambda st: st[bstack1ll11l_opy_ (u"ࠧࡪࡦࠪᒺ")] == bstack1llll1l1111_opy_, self.meta[bstack1ll11l_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᒻ")]), None)
        step.update(details)
    def bstack1llll11l11l_opy_(self, bstack1llll1l1111_opy_):
        step = next(filter(lambda st: st[bstack1ll11l_opy_ (u"ࠩ࡬ࡨࠬᒼ")] == bstack1llll1l1111_opy_, self.meta[bstack1ll11l_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᒽ")]), None)
        step.update({
            bstack1ll11l_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᒾ"): bstack1ll111ll11_opy_()
        })
    def bstack1l111l1111_opy_(self, bstack1llll1l1111_opy_, result, duration=None):
        bstack1llll1ll1l1_opy_ = bstack1ll111ll11_opy_()
        if bstack1llll1l1111_opy_ is not None and self.meta.get(bstack1ll11l_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᒿ")):
            step = next(filter(lambda st: st[bstack1ll11l_opy_ (u"࠭ࡩࡥࠩᓀ")] == bstack1llll1l1111_opy_, self.meta[bstack1ll11l_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᓁ")]), None)
            step.update({
                bstack1ll11l_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᓂ"): bstack1llll1ll1l1_opy_,
                bstack1ll11l_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫᓃ"): duration if duration else bstack111lllll11_opy_(step[bstack1ll11l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᓄ")], bstack1llll1ll1l1_opy_),
                bstack1ll11l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᓅ"): result.result,
                bstack1ll11l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭ᓆ"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1llll11l111_opy_):
        if self.meta.get(bstack1ll11l_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᓇ")):
            self.meta[bstack1ll11l_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᓈ")].append(bstack1llll11l111_opy_)
        else:
            self.meta[bstack1ll11l_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᓉ")] = [ bstack1llll11l111_opy_ ]
    def bstack1llll1l11l1_opy_(self):
        return {
            bstack1ll11l_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᓊ"): self.bstack11lll1ll1l_opy_(),
            **self.bstack1llll1ll111_opy_(),
            **self.bstack1llll1ll11l_opy_(),
            **self.bstack1llll11l1l1_opy_()
        }
    def bstack1llll1l111l_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack1ll11l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᓋ"): self.bstack1llll1ll1l1_opy_,
            bstack1ll11l_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬᓌ"): self.duration,
            bstack1ll11l_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᓍ"): self.result.result
        }
        if data[bstack1ll11l_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᓎ")] == bstack1ll11l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᓏ"):
            data[bstack1ll11l_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧᓐ")] = self.result.bstack11ll1l1l11_opy_()
            data[bstack1ll11l_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪᓑ")] = [{bstack1ll11l_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭ᓒ"): self.result.bstack11l11ll1ll_opy_()}]
        return data
    def bstack1llll11llll_opy_(self):
        return {
            bstack1ll11l_opy_ (u"ࠫࡺࡻࡩࡥࠩᓓ"): self.bstack11lll1ll1l_opy_(),
            **self.bstack1llll1ll111_opy_(),
            **self.bstack1llll1ll11l_opy_(),
            **self.bstack1llll1l111l_opy_(),
            **self.bstack1llll11l1l1_opy_()
        }
    def bstack1l1111l1l1_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack1ll11l_opy_ (u"࡙ࠬࡴࡢࡴࡷࡩࡩ࠭ᓔ") in event:
            return self.bstack1llll1l11l1_opy_()
        elif bstack1ll11l_opy_ (u"࠭ࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨᓕ") in event:
            return self.bstack1llll11llll_opy_()
    def bstack11llll1ll1_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1llll1ll1l1_opy_ = time if time else bstack1ll111ll11_opy_()
        self.duration = duration if duration else bstack111lllll11_opy_(self.bstack11lllll1ll_opy_, self.bstack1llll1ll1l1_opy_)
        if result:
            self.result = result
class bstack1l111ll111_opy_(bstack11llll11ll_opy_):
    def __init__(self, hooks=[], bstack11llll1111_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack11llll1111_opy_ = bstack11llll1111_opy_
        super().__init__(*args, **kwargs, bstack1ll1ll1l1_opy_=bstack1ll11l_opy_ (u"ࠧࡵࡧࡶࡸࠬᓖ"))
    @classmethod
    def bstack1llll1l11ll_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1ll11l_opy_ (u"ࠨ࡫ࡧࠫᓗ"): id(step),
                bstack1ll11l_opy_ (u"ࠩࡷࡩࡽࡺࠧᓘ"): step.name,
                bstack1ll11l_opy_ (u"ࠪ࡯ࡪࡿࡷࡰࡴࡧࠫᓙ"): step.keyword,
            })
        return bstack1l111ll111_opy_(
            **kwargs,
            meta={
                bstack1ll11l_opy_ (u"ࠫ࡫࡫ࡡࡵࡷࡵࡩࠬᓚ"): {
                    bstack1ll11l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᓛ"): feature.name,
                    bstack1ll11l_opy_ (u"࠭ࡰࡢࡶ࡫ࠫᓜ"): feature.filename,
                    bstack1ll11l_opy_ (u"ࠧࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬᓝ"): feature.description
                },
                bstack1ll11l_opy_ (u"ࠨࡵࡦࡩࡳࡧࡲࡪࡱࠪᓞ"): {
                    bstack1ll11l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᓟ"): scenario.name
                },
                bstack1ll11l_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᓠ"): steps,
                bstack1ll11l_opy_ (u"ࠫࡪࡾࡡ࡮ࡲ࡯ࡩࡸ࠭ᓡ"): bstack1llllll1l11_opy_(test)
            }
        )
    def bstack1llll1l1ll1_opy_(self):
        return {
            bstack1ll11l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫᓢ"): self.hooks
        }
    def bstack1llll11lll1_opy_(self):
        if self.bstack11llll1111_opy_:
            return {
                bstack1ll11l_opy_ (u"࠭ࡩ࡯ࡶࡨ࡫ࡷࡧࡴࡪࡱࡱࡷࠬᓣ"): self.bstack11llll1111_opy_
            }
        return {}
    def bstack1llll11llll_opy_(self):
        return {
            **super().bstack1llll11llll_opy_(),
            **self.bstack1llll1l1ll1_opy_()
        }
    def bstack1llll1l11l1_opy_(self):
        return {
            **super().bstack1llll1l11l1_opy_(),
            **self.bstack1llll11lll1_opy_()
        }
    def bstack11llll1ll1_opy_(self):
        return bstack1ll11l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩᓤ")
class bstack1l111l1ll1_opy_(bstack11llll11ll_opy_):
    def __init__(self, hook_type, *args, **kwargs):
        self.hook_type = hook_type
        super().__init__(*args, **kwargs, bstack1ll1ll1l1_opy_=bstack1ll11l_opy_ (u"ࠨࡪࡲࡳࡰ࠭ᓥ"))
    def bstack1l111ll1l1_opy_(self):
        return self.hook_type
    def bstack1llll1l1l1l_opy_(self):
        return {
            bstack1ll11l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬᓦ"): self.hook_type
        }
    def bstack1llll11llll_opy_(self):
        return {
            **super().bstack1llll11llll_opy_(),
            **self.bstack1llll1l1l1l_opy_()
        }
    def bstack1llll1l11l1_opy_(self):
        return {
            **super().bstack1llll1l11l1_opy_(),
            **self.bstack1llll1l1l1l_opy_()
        }
    def bstack11llll1ll1_opy_(self):
        return bstack1ll11l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࠬᓧ")