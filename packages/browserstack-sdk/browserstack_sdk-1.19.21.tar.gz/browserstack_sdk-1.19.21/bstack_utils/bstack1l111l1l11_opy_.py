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
from uuid import uuid4
from bstack_utils.helper import bstack1l1l1llll_opy_, bstack11l11llll1_opy_
from bstack_utils.bstack1lll1l1l1_opy_ import bstack1lllll1ll11_opy_
class bstack1l1111111l_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, bstack11llllllll_opy_=None, framework=None, tags=[], scope=[], bstack1llll11ll11_opy_=None, bstack1llll11l11l_opy_=True, bstack1llll11l111_opy_=None, bstack1111l1l1_opy_=None, result=None, duration=None, bstack1l111l1lll_opy_=None, meta={}):
        self.bstack1l111l1lll_opy_ = bstack1l111l1lll_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1llll11l11l_opy_:
            self.uuid = uuid4().__str__()
        self.bstack11llllllll_opy_ = bstack11llllllll_opy_
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack1llll11ll11_opy_ = bstack1llll11ll11_opy_
        self.bstack1llll11l111_opy_ = bstack1llll11l111_opy_
        self.bstack1111l1l1_opy_ = bstack1111l1l1_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
    def bstack1l111l111l_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack1llll1l1ll1_opy_(self):
        bstack1llll1l11l1_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack1llll1l_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨᒪ"): bstack1llll1l11l1_opy_,
            bstack1llll1l_opy_ (u"࠭࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠨᒫ"): bstack1llll1l11l1_opy_,
            bstack1llll1l_opy_ (u"ࠧࡷࡥࡢࡪ࡮ࡲࡥࡱࡣࡷ࡬ࠬᒬ"): bstack1llll1l11l1_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack1llll1l_opy_ (u"ࠣࡗࡱࡩࡽࡶࡥࡤࡶࡨࡨࠥࡧࡲࡨࡷࡰࡩࡳࡺ࠺ࠡࠤᒭ") + key)
            setattr(self, key, val)
    def bstack1llll11llll_opy_(self):
        return {
            bstack1llll1l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᒮ"): self.name,
            bstack1llll1l_opy_ (u"ࠪࡦࡴࡪࡹࠨᒯ"): {
                bstack1llll1l_opy_ (u"ࠫࡱࡧ࡮ࡨࠩᒰ"): bstack1llll1l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬᒱ"),
                bstack1llll1l_opy_ (u"࠭ࡣࡰࡦࡨࠫᒲ"): self.code
            },
            bstack1llll1l_opy_ (u"ࠧࡴࡥࡲࡴࡪࡹࠧᒳ"): self.scope,
            bstack1llll1l_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭ᒴ"): self.tags,
            bstack1llll1l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬᒵ"): self.framework,
            bstack1llll1l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᒶ"): self.bstack11llllllll_opy_
        }
    def bstack1llll1l1l1l_opy_(self):
        return {
         bstack1llll1l_opy_ (u"ࠫࡲ࡫ࡴࡢࠩᒷ"): self.meta
        }
    def bstack1llll11ll1l_opy_(self):
        return {
            bstack1llll1l_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡗ࡫ࡲࡶࡰࡓࡥࡷࡧ࡭ࠨᒸ"): {
                bstack1llll1l_opy_ (u"࠭ࡲࡦࡴࡸࡲࡤࡴࡡ࡮ࡧࠪᒹ"): self.bstack1llll11ll11_opy_
            }
        }
    def bstack1llll11l1ll_opy_(self, bstack1llll111l11_opy_, details):
        step = next(filter(lambda st: st[bstack1llll1l_opy_ (u"ࠧࡪࡦࠪᒺ")] == bstack1llll111l11_opy_, self.meta[bstack1llll1l_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᒻ")]), None)
        step.update(details)
    def bstack1llll1l1111_opy_(self, bstack1llll111l11_opy_):
        step = next(filter(lambda st: st[bstack1llll1l_opy_ (u"ࠩ࡬ࡨࠬᒼ")] == bstack1llll111l11_opy_, self.meta[bstack1llll1l_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᒽ")]), None)
        step.update({
            bstack1llll1l_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᒾ"): bstack1l1l1llll_opy_()
        })
    def bstack1l111l1ll1_opy_(self, bstack1llll111l11_opy_, result, duration=None):
        bstack1llll11l111_opy_ = bstack1l1l1llll_opy_()
        if bstack1llll111l11_opy_ is not None and self.meta.get(bstack1llll1l_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᒿ")):
            step = next(filter(lambda st: st[bstack1llll1l_opy_ (u"࠭ࡩࡥࠩᓀ")] == bstack1llll111l11_opy_, self.meta[bstack1llll1l_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᓁ")]), None)
            step.update({
                bstack1llll1l_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᓂ"): bstack1llll11l111_opy_,
                bstack1llll1l_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫᓃ"): duration if duration else bstack11l11llll1_opy_(step[bstack1llll1l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᓄ")], bstack1llll11l111_opy_),
                bstack1llll1l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᓅ"): result.result,
                bstack1llll1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭ᓆ"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1llll1l111l_opy_):
        if self.meta.get(bstack1llll1l_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᓇ")):
            self.meta[bstack1llll1l_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᓈ")].append(bstack1llll1l111l_opy_)
        else:
            self.meta[bstack1llll1l_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᓉ")] = [ bstack1llll1l111l_opy_ ]
    def bstack1llll11lll1_opy_(self):
        return {
            bstack1llll1l_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᓊ"): self.bstack1l111l111l_opy_(),
            **self.bstack1llll11llll_opy_(),
            **self.bstack1llll1l1ll1_opy_(),
            **self.bstack1llll1l1l1l_opy_()
        }
    def bstack1llll111l1l_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack1llll1l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᓋ"): self.bstack1llll11l111_opy_,
            bstack1llll1l_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬᓌ"): self.duration,
            bstack1llll1l_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᓍ"): self.result.result
        }
        if data[bstack1llll1l_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᓎ")] == bstack1llll1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᓏ"):
            data[bstack1llll1l_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧᓐ")] = self.result.bstack11ll1l11l1_opy_()
            data[bstack1llll1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪᓑ")] = [{bstack1llll1l_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭ᓒ"): self.result.bstack11l111l1l1_opy_()}]
        return data
    def bstack1llll1l11ll_opy_(self):
        return {
            bstack1llll1l_opy_ (u"ࠫࡺࡻࡩࡥࠩᓓ"): self.bstack1l111l111l_opy_(),
            **self.bstack1llll11llll_opy_(),
            **self.bstack1llll1l1ll1_opy_(),
            **self.bstack1llll111l1l_opy_(),
            **self.bstack1llll1l1l1l_opy_()
        }
    def bstack11llll1l11_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack1llll1l_opy_ (u"࡙ࠬࡴࡢࡴࡷࡩࡩ࠭ᓔ") in event:
            return self.bstack1llll11lll1_opy_()
        elif bstack1llll1l_opy_ (u"࠭ࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨᓕ") in event:
            return self.bstack1llll1l11ll_opy_()
    def bstack1l11111l11_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1llll11l111_opy_ = time if time else bstack1l1l1llll_opy_()
        self.duration = duration if duration else bstack11l11llll1_opy_(self.bstack11llllllll_opy_, self.bstack1llll11l111_opy_)
        if result:
            self.result = result
class bstack1l111lll11_opy_(bstack1l1111111l_opy_):
    def __init__(self, hooks=[], bstack1l11l11l11_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack1l11l11l11_opy_ = bstack1l11l11l11_opy_
        super().__init__(*args, **kwargs, bstack1111l1l1_opy_=bstack1llll1l_opy_ (u"ࠧࡵࡧࡶࡸࠬᓖ"))
    @classmethod
    def bstack1llll111ll1_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1llll1l_opy_ (u"ࠨ࡫ࡧࠫᓗ"): id(step),
                bstack1llll1l_opy_ (u"ࠩࡷࡩࡽࡺࠧᓘ"): step.name,
                bstack1llll1l_opy_ (u"ࠪ࡯ࡪࡿࡷࡰࡴࡧࠫᓙ"): step.keyword,
            })
        return bstack1l111lll11_opy_(
            **kwargs,
            meta={
                bstack1llll1l_opy_ (u"ࠫ࡫࡫ࡡࡵࡷࡵࡩࠬᓚ"): {
                    bstack1llll1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᓛ"): feature.name,
                    bstack1llll1l_opy_ (u"࠭ࡰࡢࡶ࡫ࠫᓜ"): feature.filename,
                    bstack1llll1l_opy_ (u"ࠧࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬᓝ"): feature.description
                },
                bstack1llll1l_opy_ (u"ࠨࡵࡦࡩࡳࡧࡲࡪࡱࠪᓞ"): {
                    bstack1llll1l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᓟ"): scenario.name
                },
                bstack1llll1l_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᓠ"): steps,
                bstack1llll1l_opy_ (u"ࠫࡪࡾࡡ࡮ࡲ࡯ࡩࡸ࠭ᓡ"): bstack1lllll1ll11_opy_(test)
            }
        )
    def bstack1llll11l1l1_opy_(self):
        return {
            bstack1llll1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫᓢ"): self.hooks
        }
    def bstack1llll1l1l11_opy_(self):
        if self.bstack1l11l11l11_opy_:
            return {
                bstack1llll1l_opy_ (u"࠭ࡩ࡯ࡶࡨ࡫ࡷࡧࡴࡪࡱࡱࡷࠬᓣ"): self.bstack1l11l11l11_opy_
            }
        return {}
    def bstack1llll1l11ll_opy_(self):
        return {
            **super().bstack1llll1l11ll_opy_(),
            **self.bstack1llll11l1l1_opy_()
        }
    def bstack1llll11lll1_opy_(self):
        return {
            **super().bstack1llll11lll1_opy_(),
            **self.bstack1llll1l1l11_opy_()
        }
    def bstack1l11111l11_opy_(self):
        return bstack1llll1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩᓤ")
class bstack11lllll111_opy_(bstack1l1111111l_opy_):
    def __init__(self, hook_type, *args, **kwargs):
        self.hook_type = hook_type
        super().__init__(*args, **kwargs, bstack1111l1l1_opy_=bstack1llll1l_opy_ (u"ࠨࡪࡲࡳࡰ࠭ᓥ"))
    def bstack1l111llll1_opy_(self):
        return self.hook_type
    def bstack1llll111lll_opy_(self):
        return {
            bstack1llll1l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬᓦ"): self.hook_type
        }
    def bstack1llll1l11ll_opy_(self):
        return {
            **super().bstack1llll1l11ll_opy_(),
            **self.bstack1llll111lll_opy_()
        }
    def bstack1llll11lll1_opy_(self):
        return {
            **super().bstack1llll11lll1_opy_(),
            **self.bstack1llll111lll_opy_()
        }
    def bstack1l11111l11_opy_(self):
        return bstack1llll1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࠬᓧ")