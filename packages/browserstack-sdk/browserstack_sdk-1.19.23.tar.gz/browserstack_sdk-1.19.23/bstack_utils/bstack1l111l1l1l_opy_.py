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
from uuid import uuid4
from bstack_utils.helper import bstack1l11lll111_opy_, bstack11l1111lll_opy_
from bstack_utils.bstack1lll1ll1_opy_ import bstack1lllllll111_opy_
class bstack1l111ll11l_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, bstack11lllll111_opy_=None, framework=None, tags=[], scope=[], bstack1llll1l1ll1_opy_=None, bstack1llll1ll11l_opy_=True, bstack1llll1l1l11_opy_=None, bstack11lllllll_opy_=None, result=None, duration=None, bstack11llllll11_opy_=None, meta={}):
        self.bstack11llllll11_opy_ = bstack11llllll11_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1llll1ll11l_opy_:
            self.uuid = uuid4().__str__()
        self.bstack11lllll111_opy_ = bstack11lllll111_opy_
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack1llll1l1ll1_opy_ = bstack1llll1l1ll1_opy_
        self.bstack1llll1l1l11_opy_ = bstack1llll1l1l11_opy_
        self.bstack11lllllll_opy_ = bstack11lllllll_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
    def bstack1l111l1lll_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack1llll1l11l1_opy_(self):
        bstack1llll11l1ll_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack1l_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨᒪ"): bstack1llll11l1ll_opy_,
            bstack1l_opy_ (u"࠭࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠨᒫ"): bstack1llll11l1ll_opy_,
            bstack1l_opy_ (u"ࠧࡷࡥࡢࡪ࡮ࡲࡥࡱࡣࡷ࡬ࠬᒬ"): bstack1llll11l1ll_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack1l_opy_ (u"ࠣࡗࡱࡩࡽࡶࡥࡤࡶࡨࡨࠥࡧࡲࡨࡷࡰࡩࡳࡺ࠺ࠡࠤᒭ") + key)
            setattr(self, key, val)
    def bstack1llll1l1lll_opy_(self):
        return {
            bstack1l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᒮ"): self.name,
            bstack1l_opy_ (u"ࠪࡦࡴࡪࡹࠨᒯ"): {
                bstack1l_opy_ (u"ࠫࡱࡧ࡮ࡨࠩᒰ"): bstack1l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬᒱ"),
                bstack1l_opy_ (u"࠭ࡣࡰࡦࡨࠫᒲ"): self.code
            },
            bstack1l_opy_ (u"ࠧࡴࡥࡲࡴࡪࡹࠧᒳ"): self.scope,
            bstack1l_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭ᒴ"): self.tags,
            bstack1l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬᒵ"): self.framework,
            bstack1l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᒶ"): self.bstack11lllll111_opy_
        }
    def bstack1llll1l1l1l_opy_(self):
        return {
         bstack1l_opy_ (u"ࠫࡲ࡫ࡴࡢࠩᒷ"): self.meta
        }
    def bstack1llll11l1l1_opy_(self):
        return {
            bstack1l_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡗ࡫ࡲࡶࡰࡓࡥࡷࡧ࡭ࠨᒸ"): {
                bstack1l_opy_ (u"࠭ࡲࡦࡴࡸࡲࡤࡴࡡ࡮ࡧࠪᒹ"): self.bstack1llll1l1ll1_opy_
            }
        }
    def bstack1llll1l111l_opy_(self, bstack1llll11ll11_opy_, details):
        step = next(filter(lambda st: st[bstack1l_opy_ (u"ࠧࡪࡦࠪᒺ")] == bstack1llll11ll11_opy_, self.meta[bstack1l_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᒻ")]), None)
        step.update(details)
    def bstack1llll1l1111_opy_(self, bstack1llll11ll11_opy_):
        step = next(filter(lambda st: st[bstack1l_opy_ (u"ࠩ࡬ࡨࠬᒼ")] == bstack1llll11ll11_opy_, self.meta[bstack1l_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᒽ")]), None)
        step.update({
            bstack1l_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᒾ"): bstack1l11lll111_opy_()
        })
    def bstack11llllllll_opy_(self, bstack1llll11ll11_opy_, result, duration=None):
        bstack1llll1l1l11_opy_ = bstack1l11lll111_opy_()
        if bstack1llll11ll11_opy_ is not None and self.meta.get(bstack1l_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᒿ")):
            step = next(filter(lambda st: st[bstack1l_opy_ (u"࠭ࡩࡥࠩᓀ")] == bstack1llll11ll11_opy_, self.meta[bstack1l_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᓁ")]), None)
            step.update({
                bstack1l_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᓂ"): bstack1llll1l1l11_opy_,
                bstack1l_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫᓃ"): duration if duration else bstack11l1111lll_opy_(step[bstack1l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᓄ")], bstack1llll1l1l11_opy_),
                bstack1l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᓅ"): result.result,
                bstack1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭ᓆ"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1llll11llll_opy_):
        if self.meta.get(bstack1l_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᓇ")):
            self.meta[bstack1l_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᓈ")].append(bstack1llll11llll_opy_)
        else:
            self.meta[bstack1l_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᓉ")] = [ bstack1llll11llll_opy_ ]
    def bstack1llll11l111_opy_(self):
        return {
            bstack1l_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᓊ"): self.bstack1l111l1lll_opy_(),
            **self.bstack1llll1l1lll_opy_(),
            **self.bstack1llll1l11l1_opy_(),
            **self.bstack1llll1l1l1l_opy_()
        }
    def bstack1llll1ll111_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack1l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᓋ"): self.bstack1llll1l1l11_opy_,
            bstack1l_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬᓌ"): self.duration,
            bstack1l_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᓍ"): self.result.result
        }
        if data[bstack1l_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᓎ")] == bstack1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᓏ"):
            data[bstack1l_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧᓐ")] = self.result.bstack11ll1l1l1l_opy_()
            data[bstack1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪᓑ")] = [{bstack1l_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭ᓒ"): self.result.bstack111lllllll_opy_()}]
        return data
    def bstack1llll11ll1l_opy_(self):
        return {
            bstack1l_opy_ (u"ࠫࡺࡻࡩࡥࠩᓓ"): self.bstack1l111l1lll_opy_(),
            **self.bstack1llll1l1lll_opy_(),
            **self.bstack1llll1l11l1_opy_(),
            **self.bstack1llll1ll111_opy_(),
            **self.bstack1llll1l1l1l_opy_()
        }
    def bstack1l11l1111l_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack1l_opy_ (u"࡙ࠬࡴࡢࡴࡷࡩࡩ࠭ᓔ") in event:
            return self.bstack1llll11l111_opy_()
        elif bstack1l_opy_ (u"࠭ࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨᓕ") in event:
            return self.bstack1llll11ll1l_opy_()
    def bstack11lllll1ll_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1llll1l1l11_opy_ = time if time else bstack1l11lll111_opy_()
        self.duration = duration if duration else bstack11l1111lll_opy_(self.bstack11lllll111_opy_, self.bstack1llll1l1l11_opy_)
        if result:
            self.result = result
class bstack11llll1111_opy_(bstack1l111ll11l_opy_):
    def __init__(self, hooks=[], bstack1l111lll1l_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack1l111lll1l_opy_ = bstack1l111lll1l_opy_
        super().__init__(*args, **kwargs, bstack11lllllll_opy_=bstack1l_opy_ (u"ࠧࡵࡧࡶࡸࠬᓖ"))
    @classmethod
    def bstack1llll11lll1_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1l_opy_ (u"ࠨ࡫ࡧࠫᓗ"): id(step),
                bstack1l_opy_ (u"ࠩࡷࡩࡽࡺࠧᓘ"): step.name,
                bstack1l_opy_ (u"ࠪ࡯ࡪࡿࡷࡰࡴࡧࠫᓙ"): step.keyword,
            })
        return bstack11llll1111_opy_(
            **kwargs,
            meta={
                bstack1l_opy_ (u"ࠫ࡫࡫ࡡࡵࡷࡵࡩࠬᓚ"): {
                    bstack1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᓛ"): feature.name,
                    bstack1l_opy_ (u"࠭ࡰࡢࡶ࡫ࠫᓜ"): feature.filename,
                    bstack1l_opy_ (u"ࠧࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬᓝ"): feature.description
                },
                bstack1l_opy_ (u"ࠨࡵࡦࡩࡳࡧࡲࡪࡱࠪᓞ"): {
                    bstack1l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᓟ"): scenario.name
                },
                bstack1l_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᓠ"): steps,
                bstack1l_opy_ (u"ࠫࡪࡾࡡ࡮ࡲ࡯ࡩࡸ࠭ᓡ"): bstack1lllllll111_opy_(test)
            }
        )
    def bstack1llll1l11ll_opy_(self):
        return {
            bstack1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫᓢ"): self.hooks
        }
    def bstack1llll11l11l_opy_(self):
        if self.bstack1l111lll1l_opy_:
            return {
                bstack1l_opy_ (u"࠭ࡩ࡯ࡶࡨ࡫ࡷࡧࡴࡪࡱࡱࡷࠬᓣ"): self.bstack1l111lll1l_opy_
            }
        return {}
    def bstack1llll11ll1l_opy_(self):
        return {
            **super().bstack1llll11ll1l_opy_(),
            **self.bstack1llll1l11ll_opy_()
        }
    def bstack1llll11l111_opy_(self):
        return {
            **super().bstack1llll11l111_opy_(),
            **self.bstack1llll11l11l_opy_()
        }
    def bstack11lllll1ll_opy_(self):
        return bstack1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩᓤ")
class bstack1l11111l11_opy_(bstack1l111ll11l_opy_):
    def __init__(self, hook_type, *args, **kwargs):
        self.hook_type = hook_type
        super().__init__(*args, **kwargs, bstack11lllllll_opy_=bstack1l_opy_ (u"ࠨࡪࡲࡳࡰ࠭ᓥ"))
    def bstack1l111111ll_opy_(self):
        return self.hook_type
    def bstack1llll1ll1l1_opy_(self):
        return {
            bstack1l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬᓦ"): self.hook_type
        }
    def bstack1llll11ll1l_opy_(self):
        return {
            **super().bstack1llll11ll1l_opy_(),
            **self.bstack1llll1ll1l1_opy_()
        }
    def bstack1llll11l111_opy_(self):
        return {
            **super().bstack1llll11l111_opy_(),
            **self.bstack1llll1ll1l1_opy_()
        }
    def bstack11lllll1ll_opy_(self):
        return bstack1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࠬᓧ")