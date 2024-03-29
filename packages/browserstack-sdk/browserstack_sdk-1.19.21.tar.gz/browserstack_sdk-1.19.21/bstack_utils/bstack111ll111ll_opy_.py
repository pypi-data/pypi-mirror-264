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
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result
def _111l1ll1l1_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack111l1llll1_opy_:
    def __init__(self, handler):
        self._111ll11ll1_opy_ = {}
        self._111ll11111_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        self._111ll11ll1_opy_[bstack1llll1l_opy_ (u"ࠨࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫጞ")] = Module._111l1ll11l_opy_
        self._111ll11ll1_opy_[bstack1llll1l_opy_ (u"ࠩࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪጟ")] = Module._111ll11l1l_opy_
        self._111ll11ll1_opy_[bstack1llll1l_opy_ (u"ࠪࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࠪጠ")] = Class._111l1l1lll_opy_
        self._111ll11ll1_opy_[bstack1llll1l_opy_ (u"ࠫࡲ࡫ࡴࡩࡱࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࠬጡ")] = Class._111l1lll1l_opy_
        Module._111l1ll11l_opy_ = self.bstack111ll1l111_opy_(bstack1llll1l_opy_ (u"ࠬ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨጢ"))
        Module._111ll11l1l_opy_ = self.bstack111ll1l111_opy_(bstack1llll1l_opy_ (u"࠭࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧጣ"))
        Class._111l1l1lll_opy_ = self.bstack111ll1l111_opy_(bstack1llll1l_opy_ (u"ࠧࡤ࡮ࡤࡷࡸࡥࡦࡪࡺࡷࡹࡷ࡫ࠧጤ"))
        Class._111l1lll1l_opy_ = self.bstack111ll1l111_opy_(bstack1llll1l_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࠩጥ"))
    def bstack111ll11lll_opy_(self, bstack111l1ll111_opy_, hook_type):
        meth = getattr(bstack111l1ll111_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._111ll11111_opy_[hook_type] = meth
            setattr(bstack111l1ll111_opy_, hook_type, self.bstack111ll11l11_opy_(hook_type))
    def bstack111ll111l1_opy_(self, instance, bstack111ll1l11l_opy_):
        if bstack111ll1l11l_opy_ == bstack1llll1l_opy_ (u"ࠤࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠧጦ"):
            self.bstack111ll11lll_opy_(instance.obj, bstack1llll1l_opy_ (u"ࠥࡷࡪࡺࡵࡱࡡࡩࡹࡳࡩࡴࡪࡱࡱࠦጧ"))
            self.bstack111ll11lll_opy_(instance.obj, bstack1llll1l_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠣጨ"))
        if bstack111ll1l11l_opy_ == bstack1llll1l_opy_ (u"ࠧࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪࠨጩ"):
            self.bstack111ll11lll_opy_(instance.obj, bstack1llll1l_opy_ (u"ࠨࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࠧጪ"))
            self.bstack111ll11lll_opy_(instance.obj, bstack1llll1l_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࠤጫ"))
        if bstack111ll1l11l_opy_ == bstack1llll1l_opy_ (u"ࠣࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠣጬ"):
            self.bstack111ll11lll_opy_(instance.obj, bstack1llll1l_opy_ (u"ࠤࡶࡩࡹࡻࡰࡠࡥ࡯ࡥࡸࡹࠢጭ"))
            self.bstack111ll11lll_opy_(instance.obj, bstack1llll1l_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࡤࡩ࡬ࡢࡵࡶࠦጮ"))
        if bstack111ll1l11l_opy_ == bstack1llll1l_opy_ (u"ࠦࡲ࡫ࡴࡩࡱࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࠧጯ"):
            self.bstack111ll11lll_opy_(instance.obj, bstack1llll1l_opy_ (u"ࠧࡹࡥࡵࡷࡳࡣࡲ࡫ࡴࡩࡱࡧࠦጰ"))
            self.bstack111ll11lll_opy_(instance.obj, bstack1llll1l_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡨࡸ࡭ࡵࡤࠣጱ"))
    @staticmethod
    def bstack111l1lll11_opy_(hook_type, func, args):
        if hook_type in [bstack1llll1l_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡦࡶ࡫ࡳࡩ࠭ጲ"), bstack1llll1l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡪࡺࡨࡰࡦࠪጳ")]:
            _111l1ll1l1_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack111ll11l11_opy_(self, hook_type):
        def bstack111ll1111l_opy_(arg=None):
            self.handler(hook_type, bstack1llll1l_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࠩጴ"))
            result = None
            exception = None
            try:
                self.bstack111l1lll11_opy_(hook_type, self._111ll11111_opy_[hook_type], (arg,))
                result = Result(result=bstack1llll1l_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪጵ"))
            except Exception as e:
                result = Result(result=bstack1llll1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫጶ"), exception=e)
                self.handler(hook_type, bstack1llll1l_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫጷ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1llll1l_opy_ (u"࠭ࡡࡧࡶࡨࡶࠬጸ"), result)
        def bstack111l1lllll_opy_(this, arg=None):
            self.handler(hook_type, bstack1llll1l_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫ࠧጹ"))
            result = None
            exception = None
            try:
                self.bstack111l1lll11_opy_(hook_type, self._111ll11111_opy_[hook_type], (this, arg))
                result = Result(result=bstack1llll1l_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨጺ"))
            except Exception as e:
                result = Result(result=bstack1llll1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩጻ"), exception=e)
                self.handler(hook_type, bstack1llll1l_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࠩጼ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1llll1l_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪጽ"), result)
        if hook_type in [bstack1llll1l_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲ࡫ࡴࡩࡱࡧࠫጾ"), bstack1llll1l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡨࡸ࡭ࡵࡤࠨጿ")]:
            return bstack111l1lllll_opy_
        return bstack111ll1111l_opy_
    def bstack111ll1l111_opy_(self, bstack111ll1l11l_opy_):
        def bstack111l1ll1ll_opy_(this, *args, **kwargs):
            self.bstack111ll111l1_opy_(this, bstack111ll1l11l_opy_)
            self._111ll11ll1_opy_[bstack111ll1l11l_opy_](this, *args, **kwargs)
        return bstack111l1ll1ll_opy_