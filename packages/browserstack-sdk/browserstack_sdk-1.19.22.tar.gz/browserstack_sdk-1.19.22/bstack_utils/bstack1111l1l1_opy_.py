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
class bstack11l1ll1l1l_opy_(object):
  bstack111ll1111_opy_ = os.path.join(os.path.expanduser(bstack1ll11l_opy_ (u"࠭ࡾࠨ໑")), bstack1ll11l_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ໒"))
  bstack11l1ll111l_opy_ = os.path.join(bstack111ll1111_opy_, bstack1ll11l_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵ࠱࡮ࡸࡵ࡮ࠨ໓"))
  bstack11l1ll1111_opy_ = None
  perform_scan = None
  bstack1l1ll11ll_opy_ = None
  bstack1ll11ll11l_opy_ = None
  bstack11ll11l1ll_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack1ll11l_opy_ (u"ࠩ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠫ໔")):
      cls.instance = super(bstack11l1ll1l1l_opy_, cls).__new__(cls)
      cls.instance.bstack11l1ll11l1_opy_()
    return cls.instance
  def bstack11l1ll11l1_opy_(self):
    try:
      with open(self.bstack11l1ll111l_opy_, bstack1ll11l_opy_ (u"ࠪࡶࠬ໕")) as bstack1lll11ll11_opy_:
        bstack11l1ll1l11_opy_ = bstack1lll11ll11_opy_.read()
        data = json.loads(bstack11l1ll1l11_opy_)
        if bstack1ll11l_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡸ࠭໖") in data:
          self.bstack11ll11l11l_opy_(data[bstack1ll11l_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹࠧ໗")])
        if bstack1ll11l_opy_ (u"࠭ࡳࡤࡴ࡬ࡴࡹࡹࠧ໘") in data:
          self.bstack11ll11ll11_opy_(data[bstack1ll11l_opy_ (u"ࠧࡴࡥࡵ࡭ࡵࡺࡳࠨ໙")])
    except:
      pass
  def bstack11ll11ll11_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts[bstack1ll11l_opy_ (u"ࠨࡵࡦࡥࡳ࠭໚")]
      self.bstack1l1ll11ll_opy_ = scripts[bstack1ll11l_opy_ (u"ࠩࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸ࠭໛")]
      self.bstack1ll11ll11l_opy_ = scripts[bstack1ll11l_opy_ (u"ࠪ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࡓࡶ࡯ࡰࡥࡷࡿࠧໜ")]
      self.bstack11ll11l1ll_opy_ = scripts[bstack1ll11l_opy_ (u"ࠫࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠩໝ")]
  def bstack11ll11l11l_opy_(self, bstack11l1ll1111_opy_):
    if bstack11l1ll1111_opy_ != None and len(bstack11l1ll1111_opy_) != 0:
      self.bstack11l1ll1111_opy_ = bstack11l1ll1111_opy_
  def store(self):
    try:
      with open(self.bstack11l1ll111l_opy_, bstack1ll11l_opy_ (u"ࠬࡽࠧໞ")) as file:
        json.dump({
          bstack1ll11l_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪࡳࠣໟ"): self.bstack11l1ll1111_opy_,
          bstack1ll11l_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࡳࠣ໠"): {
            bstack1ll11l_opy_ (u"ࠣࡵࡦࡥࡳࠨ໡"): self.perform_scan,
            bstack1ll11l_opy_ (u"ࠤࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸࠨ໢"): self.bstack1l1ll11ll_opy_,
            bstack1ll11l_opy_ (u"ࠥ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࡓࡶ࡯ࡰࡥࡷࡿࠢ໣"): self.bstack1ll11ll11l_opy_,
            bstack1ll11l_opy_ (u"ࠦࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠤ໤"): self.bstack11ll11l1ll_opy_
          }
        }, file)
    except:
      pass
  def bstack1llll1l11_opy_(self, bstack11l1ll11ll_opy_):
    try:
      return any(command.get(bstack1ll11l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ໥")) == bstack11l1ll11ll_opy_ for command in self.bstack11l1ll1111_opy_)
    except:
      return False
bstack1111l1l1_opy_ = bstack11l1ll1l1l_opy_()