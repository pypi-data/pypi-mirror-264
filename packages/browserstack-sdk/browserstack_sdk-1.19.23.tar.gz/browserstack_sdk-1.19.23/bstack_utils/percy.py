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
import re
import sys
import json
import time
import shutil
import tempfile
import requests
import subprocess
from threading import Thread
from os.path import expanduser
from bstack_utils.constants import *
from requests.auth import HTTPBasicAuth
from bstack_utils.helper import bstack1111l1l1_opy_, bstack1l1l1l11_opy_
class bstack1ll1111lll_opy_:
  working_dir = os.getcwd()
  bstack1l1ll1l11l_opy_ = False
  config = {}
  binary_path = bstack1l_opy_ (u"ࠧࠨᎷ")
  bstack11111l1l11_opy_ = bstack1l_opy_ (u"ࠨࠩᎸ")
  bstack11lllll11_opy_ = False
  bstack111l111111_opy_ = None
  bstack1111llllll_opy_ = {}
  bstack1111l1ll1l_opy_ = 300
  bstack11111ll111_opy_ = False
  logger = None
  bstack1111llll1l_opy_ = False
  bstack1111l1l111_opy_ = bstack1l_opy_ (u"ࠩࠪᎹ")
  bstack11111l1l1l_opy_ = {
    bstack1l_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪᎺ") : 1,
    bstack1l_opy_ (u"ࠫ࡫࡯ࡲࡦࡨࡲࡼࠬᎻ") : 2,
    bstack1l_opy_ (u"ࠬ࡫ࡤࡨࡧࠪᎼ") : 3,
    bstack1l_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠭Ꮍ") : 4
  }
  def __init__(self) -> None: pass
  def bstack111l1111ll_opy_(self):
    bstack1111l1lll1_opy_ = bstack1l_opy_ (u"ࠧࠨᎾ")
    bstack111l111l1l_opy_ = sys.platform
    bstack1111l1l1l1_opy_ = bstack1l_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧᎿ")
    if re.match(bstack1l_opy_ (u"ࠤࡧࡥࡷࡽࡩ࡯ࡾࡰࡥࡨࠦ࡯ࡴࠤᏀ"), bstack111l111l1l_opy_) != None:
      bstack1111l1lll1_opy_ = bstack11l1l11l11_opy_ + bstack1l_opy_ (u"ࠥ࠳ࡵ࡫ࡲࡤࡻ࠰ࡳࡸࡾ࠮ࡻ࡫ࡳࠦᏁ")
      self.bstack1111l1l111_opy_ = bstack1l_opy_ (u"ࠫࡲࡧࡣࠨᏂ")
    elif re.match(bstack1l_opy_ (u"ࠧࡳࡳࡸ࡫ࡱࢀࡲࡹࡹࡴࡾࡰ࡭ࡳ࡭ࡷࡽࡥࡼ࡫ࡼ࡯࡮ࡽࡤࡦࡧࡼ࡯࡮ࡽࡹ࡬ࡲࡨ࡫ࡼࡦ࡯ࡦࢀࡼ࡯࡮࠴࠴ࠥᏃ"), bstack111l111l1l_opy_) != None:
      bstack1111l1lll1_opy_ = bstack11l1l11l11_opy_ + bstack1l_opy_ (u"ࠨ࠯ࡱࡧࡵࡧࡾ࠳ࡷࡪࡰ࠱ࡾ࡮ࡶࠢᏄ")
      bstack1111l1l1l1_opy_ = bstack1l_opy_ (u"ࠢࡱࡧࡵࡧࡾ࠴ࡥࡹࡧࠥᏅ")
      self.bstack1111l1l111_opy_ = bstack1l_opy_ (u"ࠨࡹ࡬ࡲࠬᏆ")
    else:
      bstack1111l1lll1_opy_ = bstack11l1l11l11_opy_ + bstack1l_opy_ (u"ࠤ࠲ࡴࡪࡸࡣࡺ࠯࡯࡭ࡳࡻࡸ࠯ࡼ࡬ࡴࠧᏇ")
      self.bstack1111l1l111_opy_ = bstack1l_opy_ (u"ࠪࡰ࡮ࡴࡵࡹࠩᏈ")
    return bstack1111l1lll1_opy_, bstack1111l1l1l1_opy_
  def bstack111l111l11_opy_(self):
    try:
      bstack111l11111l_opy_ = [os.path.join(expanduser(bstack1l_opy_ (u"ࠦࢃࠨᏉ")), bstack1l_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬᏊ")), self.working_dir, tempfile.gettempdir()]
      for path in bstack111l11111l_opy_:
        if(self.bstack1111ll11ll_opy_(path)):
          return path
      raise bstack1l_opy_ (u"ࠨࡕ࡯ࡣ࡯ࡦࡪࠦࡴࡰࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠥᏋ")
    except Exception as e:
      self.logger.error(bstack1l_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡪ࡮ࡴࡤࠡࡣࡹࡥ࡮ࡲࡡࡣ࡮ࡨࠤࡵࡧࡴࡩࠢࡩࡳࡷࠦࡰࡦࡴࡦࡽࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࠲ࠦࡻࡾࠤᏌ").format(e))
  def bstack1111ll11ll_opy_(self, path):
    try:
      if not os.path.exists(path):
        os.makedirs(path)
      return True
    except:
      return False
  def bstack1111llll11_opy_(self, bstack1111l1lll1_opy_, bstack1111l1l1l1_opy_):
    try:
      bstack1111l11l11_opy_ = self.bstack111l111l11_opy_()
      bstack111l111ll1_opy_ = os.path.join(bstack1111l11l11_opy_, bstack1l_opy_ (u"ࠨࡲࡨࡶࡨࡿ࠮ࡻ࡫ࡳࠫᏍ"))
      bstack11111ll1l1_opy_ = os.path.join(bstack1111l11l11_opy_, bstack1111l1l1l1_opy_)
      if os.path.exists(bstack11111ll1l1_opy_):
        self.logger.info(bstack1l_opy_ (u"ࠤࡓࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠡࡨࡲࡹࡳࡪࠠࡪࡰࠣࡿࢂ࠲ࠠࡴ࡭࡬ࡴࡵ࡯࡮ࡨࠢࡧࡳࡼࡴ࡬ࡰࡣࡧࠦᏎ").format(bstack11111ll1l1_opy_))
        return bstack11111ll1l1_opy_
      if os.path.exists(bstack111l111ll1_opy_):
        self.logger.info(bstack1l_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡽ࡭ࡵࠦࡦࡰࡷࡱࡨࠥ࡯࡮ࠡࡽࢀ࠰ࠥࡻ࡮ࡻ࡫ࡳࡴ࡮ࡴࡧࠣᏏ").format(bstack111l111ll1_opy_))
        return self.bstack1111l1llll_opy_(bstack111l111ll1_opy_, bstack1111l1l1l1_opy_)
      self.logger.info(bstack1l_opy_ (u"ࠦࡉࡵࡷ࡯࡮ࡲࡥࡩ࡯࡮ࡨࠢࡳࡩࡷࡩࡹࠡࡤ࡬ࡲࡦࡸࡹࠡࡨࡵࡳࡲࠦࡻࡾࠤᏐ").format(bstack1111l1lll1_opy_))
      response = bstack1l1l1l11_opy_(bstack1l_opy_ (u"ࠬࡍࡅࡕࠩᏑ"), bstack1111l1lll1_opy_, {}, {})
      if response.status_code == 200:
        with open(bstack111l111ll1_opy_, bstack1l_opy_ (u"࠭ࡷࡣࠩᏒ")) as file:
          file.write(response.content)
        self.logger.info(bstack1l_opy_ (u"ࠢࡅࡱࡺࡲࡱࡵࡡࡥࡧࡧࠤࡵ࡫ࡲࡤࡻࠣࡦ࡮ࡴࡡࡳࡻࠣࡥࡳࡪࠠࡴࡣࡹࡩࡩࠦࡡࡵࠢࡾࢁࠧᏓ").format(bstack111l111ll1_opy_))
        return self.bstack1111l1llll_opy_(bstack111l111ll1_opy_, bstack1111l1l1l1_opy_)
      else:
        raise(bstack1l_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡩࡵࡷ࡯࡮ࡲࡥࡩࠦࡴࡩࡧࠣࡪ࡮ࡲࡥ࠯ࠢࡖࡸࡦࡺࡵࡴࠢࡦࡳࡩ࡫࠺ࠡࡽࢀࠦᏔ").format(response.status_code))
    except Exception as e:
      self.logger.error(bstack1l_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠠࡱࡧࡵࡧࡾࠦࡢࡪࡰࡤࡶࡾࡀࠠࡼࡿࠥᏕ").format(e))
  def bstack11111lll11_opy_(self, bstack1111l1lll1_opy_, bstack1111l1l1l1_opy_):
    try:
      retry = 2
      bstack11111ll1l1_opy_ = None
      bstack1111l1ll11_opy_ = False
      while retry > 0:
        bstack11111ll1l1_opy_ = self.bstack1111llll11_opy_(bstack1111l1lll1_opy_, bstack1111l1l1l1_opy_)
        bstack1111l1ll11_opy_ = self.bstack1111lll11l_opy_(bstack1111l1lll1_opy_, bstack1111l1l1l1_opy_, bstack11111ll1l1_opy_)
        if bstack1111l1ll11_opy_:
          break
        retry -= 1
      return bstack11111ll1l1_opy_, bstack1111l1ll11_opy_
    except Exception as e:
      self.logger.error(bstack1l_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡧࡦࡶࠣࡴࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠢࡳࡥࡹ࡮ࠢᏖ").format(e))
    return bstack11111ll1l1_opy_, False
  def bstack1111lll11l_opy_(self, bstack1111l1lll1_opy_, bstack1111l1l1l1_opy_, bstack11111ll1l1_opy_, bstack1111l11l1l_opy_ = 0):
    if bstack1111l11l1l_opy_ > 1:
      return False
    if bstack11111ll1l1_opy_ == None or os.path.exists(bstack11111ll1l1_opy_) == False:
      self.logger.warn(bstack1l_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡴࡦࡺࡨࠡࡰࡲࡸࠥ࡬࡯ࡶࡰࡧ࠰ࠥࡸࡥࡵࡴࡼ࡭ࡳ࡭ࠠࡥࡱࡺࡲࡱࡵࡡࡥࠤᏗ"))
      return False
    bstack1111l11111_opy_ = bstack1l_opy_ (u"ࠧࡤ࠮ࠫࡂࡳࡩࡷࡩࡹ࡝࠱ࡦࡰ࡮ࠦ࡜ࡥ࠰࡟ࡨ࠰࠴࡜ࡥ࠭ࠥᏘ")
    command = bstack1l_opy_ (u"࠭ࡻࡾࠢ࠰࠱ࡻ࡫ࡲࡴ࡫ࡲࡲࠬᏙ").format(bstack11111ll1l1_opy_)
    bstack1111lll111_opy_ = subprocess.check_output(command, shell=True, text=True)
    if re.match(bstack1111l11111_opy_, bstack1111lll111_opy_) != None:
      return True
    else:
      self.logger.error(bstack1l_opy_ (u"ࠢࡑࡧࡵࡧࡾࠦࡶࡦࡴࡶ࡭ࡴࡴࠠࡤࡪࡨࡧࡰࠦࡦࡢ࡫࡯ࡩࡩࠨᏚ"))
      return False
  def bstack1111l1llll_opy_(self, bstack111l111ll1_opy_, bstack1111l1l1l1_opy_):
    try:
      working_dir = os.path.dirname(bstack111l111ll1_opy_)
      shutil.unpack_archive(bstack111l111ll1_opy_, working_dir)
      bstack11111ll1l1_opy_ = os.path.join(working_dir, bstack1111l1l1l1_opy_)
      os.chmod(bstack11111ll1l1_opy_, 0o755)
      return bstack11111ll1l1_opy_
    except Exception as e:
      self.logger.error(bstack1l_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡺࡴࡺࡪࡲࠣࡴࡪࡸࡣࡺࠢࡥ࡭ࡳࡧࡲࡺࠤᏛ"))
  def bstack11111lll1l_opy_(self):
    try:
      percy = str(self.config.get(bstack1l_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨᏜ"), bstack1l_opy_ (u"ࠥࡪࡦࡲࡳࡦࠤᏝ"))).lower()
      if percy != bstack1l_opy_ (u"ࠦࡹࡸࡵࡦࠤᏞ"):
        return False
      self.bstack11lllll11_opy_ = True
      return True
    except Exception as e:
      self.logger.error(bstack1l_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡦࡨࡸࡪࡩࡴࠡࡲࡨࡶࡨࡿࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢᏟ").format(e))
  def bstack11111lllll_opy_(self):
    try:
      bstack11111lllll_opy_ = str(self.config.get(bstack1l_opy_ (u"࠭ࡰࡦࡴࡦࡽࡈࡧࡰࡵࡷࡵࡩࡒࡵࡤࡦࠩᏠ"), bstack1l_opy_ (u"ࠢࡢࡷࡷࡳࠧᏡ"))).lower()
      return bstack11111lllll_opy_
    except Exception as e:
      self.logger.error(bstack1l_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡩ࡫ࡴࡦࡥࡷࠤࡵ࡫ࡲࡤࡻࠣࡧࡦࡶࡴࡶࡴࡨࠤࡲࡵࡤࡦ࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤᏢ").format(e))
  def init(self, bstack1l1ll1l11l_opy_, config, logger):
    self.bstack1l1ll1l11l_opy_ = bstack1l1ll1l11l_opy_
    self.config = config
    self.logger = logger
    if not self.bstack11111lll1l_opy_():
      return
    self.bstack1111llllll_opy_ = config.get(bstack1l_opy_ (u"ࠩࡳࡩࡷࡩࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᏣ"), {})
    self.bstack1111ll1lll_opy_ = config.get(bstack1l_opy_ (u"ࠪࡴࡪࡸࡣࡺࡅࡤࡴࡹࡻࡲࡦࡏࡲࡨࡪ࠭Ꮴ"), bstack1l_opy_ (u"ࠦࡦࡻࡴࡰࠤᏥ"))
    try:
      bstack1111l1lll1_opy_, bstack1111l1l1l1_opy_ = self.bstack111l1111ll_opy_()
      bstack11111ll1l1_opy_, bstack1111l1ll11_opy_ = self.bstack11111lll11_opy_(bstack1111l1lll1_opy_, bstack1111l1l1l1_opy_)
      if bstack1111l1ll11_opy_:
        self.binary_path = bstack11111ll1l1_opy_
        thread = Thread(target=self.bstack1111l1l1ll_opy_)
        thread.start()
      else:
        self.bstack1111llll1l_opy_ = True
        self.logger.error(bstack1l_opy_ (u"ࠧࡏ࡮ࡷࡣ࡯࡭ࡩࠦࡰࡦࡴࡦࡽࠥࡶࡡࡵࡪࠣࡪࡴࡻ࡮ࡥࠢ࠰ࠤࢀࢃࠬࠡࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺࡡࡳࡶࠣࡔࡪࡸࡣࡺࠤᏦ").format(bstack11111ll1l1_opy_))
    except Exception as e:
      self.logger.error(bstack1l_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡲࡨࡶࡨࡿࠬࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࢀࢃࠢᏧ").format(e))
  def bstack11111l1lll_opy_(self):
    try:
      logfile = os.path.join(self.working_dir, bstack1l_opy_ (u"ࠧ࡭ࡱࡪࠫᏨ"), bstack1l_opy_ (u"ࠨࡲࡨࡶࡨࡿ࠮࡭ࡱࡪࠫᏩ"))
      os.makedirs(os.path.dirname(logfile)) if not os.path.exists(os.path.dirname(logfile)) else None
      self.logger.debug(bstack1l_opy_ (u"ࠤࡓࡹࡸ࡮ࡩ࡯ࡩࠣࡴࡪࡸࡣࡺࠢ࡯ࡳ࡬ࡹࠠࡢࡶࠣࡿࢂࠨᏪ").format(logfile))
      self.bstack11111l1l11_opy_ = logfile
    except Exception as e:
      self.logger.error(bstack1l_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡦࡶࠣࡴࡪࡸࡣࡺࠢ࡯ࡳ࡬ࠦࡰࡢࡶ࡫࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦᏫ").format(e))
  def bstack1111l1l1ll_opy_(self):
    bstack11111l11ll_opy_ = self.bstack11111llll1_opy_()
    if bstack11111l11ll_opy_ == None:
      self.bstack1111llll1l_opy_ = True
      self.logger.error(bstack1l_opy_ (u"ࠦࡕ࡫ࡲࡤࡻࠣࡸࡴࡱࡥ࡯ࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨ࠱ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡲࡨࡶࡨࡿࠢᏬ"))
      return False
    command_args = [bstack1l_opy_ (u"ࠧࡧࡰࡱ࠼ࡨࡼࡪࡩ࠺ࡴࡶࡤࡶࡹࠨᏭ") if self.bstack1l1ll1l11l_opy_ else bstack1l_opy_ (u"࠭ࡥࡹࡧࡦ࠾ࡸࡺࡡࡳࡶࠪᏮ")]
    bstack1111l1111l_opy_ = self.bstack1111l11lll_opy_()
    if bstack1111l1111l_opy_ != None:
      command_args.append(bstack1l_opy_ (u"ࠢ࠮ࡥࠣࡿࢂࠨᏯ").format(bstack1111l1111l_opy_))
    env = os.environ.copy()
    env[bstack1l_opy_ (u"ࠣࡒࡈࡖࡈ࡟࡟ࡕࡑࡎࡉࡓࠨᏰ")] = bstack11111l11ll_opy_
    bstack1111ll1111_opy_ = [self.binary_path]
    self.bstack11111l1lll_opy_()
    self.bstack111l111111_opy_ = self.bstack1111ll11l1_opy_(bstack1111ll1111_opy_ + command_args, env)
    self.logger.debug(bstack1l_opy_ (u"ࠤࡖࡸࡦࡸࡴࡪࡰࡪࠤࡍ࡫ࡡ࡭ࡶ࡫ࠤࡈ࡮ࡥࡤ࡭ࠥᏱ"))
    bstack1111l11l1l_opy_ = 0
    while self.bstack111l111111_opy_.poll() == None:
      bstack1111l111ll_opy_ = self.bstack11111ll11l_opy_()
      if bstack1111l111ll_opy_:
        self.logger.debug(bstack1l_opy_ (u"ࠥࡌࡪࡧ࡬ࡵࡪࠣࡇ࡭࡫ࡣ࡬ࠢࡶࡹࡨࡩࡥࡴࡵࡩࡹࡱࠨᏲ"))
        self.bstack11111ll111_opy_ = True
        return True
      bstack1111l11l1l_opy_ += 1
      self.logger.debug(bstack1l_opy_ (u"ࠦࡍ࡫ࡡ࡭ࡶ࡫ࠤࡈ࡮ࡥࡤ࡭ࠣࡖࡪࡺࡲࡺࠢ࠰ࠤࢀࢃࠢᏳ").format(bstack1111l11l1l_opy_))
      time.sleep(2)
    self.logger.error(bstack1l_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡵࡷࡥࡷࡺࠠࡱࡧࡵࡧࡾ࠲ࠠࡉࡧࡤࡰࡹ࡮ࠠࡄࡪࡨࡧࡰࠦࡆࡢ࡫࡯ࡩࡩࠦࡡࡧࡶࡨࡶࠥࢁࡽࠡࡣࡷࡸࡪࡳࡰࡵࡵࠥᏴ").format(bstack1111l11l1l_opy_))
    self.bstack1111llll1l_opy_ = True
    return False
  def bstack11111ll11l_opy_(self, bstack1111l11l1l_opy_ = 0):
    try:
      if bstack1111l11l1l_opy_ > 10:
        return False
      bstack1111ll1l1l_opy_ = os.environ.get(bstack1l_opy_ (u"࠭ࡐࡆࡔࡆ࡝ࡤ࡙ࡅࡓࡘࡈࡖࡤࡇࡄࡅࡔࡈࡗࡘ࠭Ᏽ"), bstack1l_opy_ (u"ࠧࡩࡶࡷࡴ࠿࠵࠯࡭ࡱࡦࡥࡱ࡮࡯ࡴࡶ࠽࠹࠸࠹࠸ࠨ᏶"))
      bstack1111ll1ll1_opy_ = bstack1111ll1l1l_opy_ + bstack11l11lllll_opy_
      response = requests.get(bstack1111ll1ll1_opy_)
      return True if response.json() else False
    except:
      return False
  def bstack11111llll1_opy_(self):
    bstack11111l1ll1_opy_ = bstack1l_opy_ (u"ࠨࡣࡳࡴࠬ᏷") if self.bstack1l1ll1l11l_opy_ else bstack1l_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫᏸ")
    bstack11l111l111_opy_ = bstack1l_opy_ (u"ࠥࡥࡵ࡯࠯ࡢࡲࡳࡣࡵ࡫ࡲࡤࡻ࠲࡫ࡪࡺ࡟ࡱࡴࡲ࡮ࡪࡩࡴࡠࡶࡲ࡯ࡪࡴ࠿࡯ࡣࡰࡩࡂࢁࡽࠧࡶࡼࡴࡪࡃࡻࡾࠤᏹ").format(self.config[bstack1l_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩᏺ")], bstack11111l1ll1_opy_)
    uri = bstack1111l1l1_opy_(bstack11l111l111_opy_)
    try:
      response = bstack1l1l1l11_opy_(bstack1l_opy_ (u"ࠬࡍࡅࡕࠩᏻ"), uri, {}, {bstack1l_opy_ (u"࠭ࡡࡶࡶ࡫ࠫᏼ"): (self.config[bstack1l_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩᏽ")], self.config[bstack1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ᏾")])})
      if response.status_code == 200:
        bstack1111l111l1_opy_ = response.json()
        if bstack1l_opy_ (u"ࠤࡷࡳࡰ࡫࡮ࠣ᏿") in bstack1111l111l1_opy_:
          return bstack1111l111l1_opy_[bstack1l_opy_ (u"ࠥࡸࡴࡱࡥ࡯ࠤ᐀")]
        else:
          raise bstack1l_opy_ (u"࡙ࠫࡵ࡫ࡦࡰࠣࡒࡴࡺࠠࡇࡱࡸࡲࡩࠦ࠭ࠡࡽࢀࠫᐁ").format(bstack1111l111l1_opy_)
      else:
        raise bstack1l_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡨࡨࡸࡨ࡮ࠠࡱࡧࡵࡧࡾࠦࡴࡰ࡭ࡨࡲ࠱ࠦࡒࡦࡵࡳࡳࡳࡹࡥࠡࡵࡷࡥࡹࡻࡳࠡ࠯ࠣࡿࢂ࠲ࠠࡓࡧࡶࡴࡴࡴࡳࡦࠢࡅࡳࡩࡿࠠ࠮ࠢࡾࢁࠧᐂ").format(response.status_code, response.json())
    except Exception as e:
      self.logger.error(bstack1l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡱࡧࡵࡧࡾࠦࡰࡳࡱ࡭ࡩࡨࡺࠢᐃ").format(e))
  def bstack1111l11lll_opy_(self):
    bstack111l1111l1_opy_ = os.path.join(tempfile.gettempdir(), bstack1l_opy_ (u"ࠢࡱࡧࡵࡧࡾࡉ࡯࡯ࡨ࡬࡫࠳ࡰࡳࡰࡰࠥᐄ"))
    try:
      if bstack1l_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࠩᐅ") not in self.bstack1111llllll_opy_:
        self.bstack1111llllll_opy_[bstack1l_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࠪᐆ")] = 2
      with open(bstack111l1111l1_opy_, bstack1l_opy_ (u"ࠪࡻࠬᐇ")) as fp:
        json.dump(self.bstack1111llllll_opy_, fp)
      return bstack111l1111l1_opy_
    except Exception as e:
      self.logger.error(bstack1l_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡤࡴࡨࡥࡹ࡫ࠠࡱࡧࡵࡧࡾࠦࡣࡰࡰࡩ࠰ࠥࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡽࢀࠦᐈ").format(e))
  def bstack1111ll11l1_opy_(self, cmd, env = os.environ.copy()):
    try:
      if self.bstack1111l1l111_opy_ == bstack1l_opy_ (u"ࠬࡽࡩ࡯ࠩᐉ"):
        bstack1111l11ll1_opy_ = [bstack1l_opy_ (u"࠭ࡣ࡮ࡦ࠱ࡩࡽ࡫ࠧᐊ"), bstack1l_opy_ (u"ࠧ࠰ࡥࠪᐋ")]
        cmd = bstack1111l11ll1_opy_ + cmd
      cmd = bstack1l_opy_ (u"ࠨࠢࠪᐌ").join(cmd)
      self.logger.debug(bstack1l_opy_ (u"ࠤࡕࡹࡳࡴࡩ࡯ࡩࠣࡿࢂࠨᐍ").format(cmd))
      with open(self.bstack11111l1l11_opy_, bstack1l_opy_ (u"ࠥࡥࠧᐎ")) as bstack1111lll1l1_opy_:
        process = subprocess.Popen(cmd, shell=True, stdout=bstack1111lll1l1_opy_, text=True, stderr=bstack1111lll1l1_opy_, env=env, universal_newlines=True)
      return process
    except Exception as e:
      self.bstack1111llll1l_opy_ = True
      self.logger.error(bstack1l_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡶࡤࡶࡹࠦࡰࡦࡴࡦࡽࠥࡽࡩࡵࡪࠣࡧࡲࡪࠠ࠮ࠢࡾࢁ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯࠼ࠣࡿࢂࠨᐏ").format(cmd, e))
  def shutdown(self):
    try:
      if self.bstack11111ll111_opy_:
        self.logger.info(bstack1l_opy_ (u"࡙ࠧࡴࡰࡲࡳ࡭ࡳ࡭ࠠࡑࡧࡵࡧࡾࠨᐐ"))
        cmd = [self.binary_path, bstack1l_opy_ (u"ࠨࡥࡹࡧࡦ࠾ࡸࡺ࡯ࡱࠤᐑ")]
        self.bstack1111ll11l1_opy_(cmd)
        self.bstack11111ll111_opy_ = False
    except Exception as e:
      self.logger.error(bstack1l_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡹࡵࡰࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡺ࡭ࡹ࡮ࠠࡤࡱࡰࡱࡦࡴࡤࠡ࠯ࠣࡿࢂ࠲ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰ࠽ࠤࢀࢃࠢᐒ").format(cmd, e))
  def bstack1l1l1l1lll_opy_(self):
    if not self.bstack11lllll11_opy_:
      return
    try:
      bstack1111l1l11l_opy_ = 0
      while not self.bstack11111ll111_opy_ and bstack1111l1l11l_opy_ < self.bstack1111l1ll1l_opy_:
        if self.bstack1111llll1l_opy_:
          self.logger.info(bstack1l_opy_ (u"ࠣࡒࡨࡶࡨࡿࠠࡴࡧࡷࡹࡵࠦࡦࡢ࡫࡯ࡩࡩࠨᐓ"))
          return
        time.sleep(1)
        bstack1111l1l11l_opy_ += 1
      os.environ[bstack1l_opy_ (u"ࠩࡓࡉࡗࡉ࡙ࡠࡄࡈࡗ࡙ࡥࡐࡍࡃࡗࡊࡔࡘࡍࠨᐔ")] = str(self.bstack11111ll1ll_opy_())
      self.logger.info(bstack1l_opy_ (u"ࠥࡔࡪࡸࡣࡺࠢࡶࡩࡹࡻࡰࠡࡥࡲࡱࡵࡲࡥࡵࡧࡧࠦᐕ"))
    except Exception as e:
      self.logger.error(bstack1l_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡴࡧࡷࡹࡵࠦࡰࡦࡴࡦࡽ࠱ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡾࢁࠧᐖ").format(e))
  def bstack11111ll1ll_opy_(self):
    if self.bstack1l1ll1l11l_opy_:
      return
    try:
      bstack1111lll1ll_opy_ = [platform[bstack1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪᐗ")].lower() for platform in self.config.get(bstack1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᐘ"), [])]
      bstack1111lllll1_opy_ = sys.maxsize
      bstack1111ll111l_opy_ = bstack1l_opy_ (u"ࠧࠨᐙ")
      for browser in bstack1111lll1ll_opy_:
        if browser in self.bstack11111l1l1l_opy_:
          bstack1111ll1l11_opy_ = self.bstack11111l1l1l_opy_[browser]
        if bstack1111ll1l11_opy_ < bstack1111lllll1_opy_:
          bstack1111lllll1_opy_ = bstack1111ll1l11_opy_
          bstack1111ll111l_opy_ = browser
      return bstack1111ll111l_opy_
    except Exception as e:
      self.logger.error(bstack1l_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡫࡯࡮ࡥࠢࡥࡩࡸࡺࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮࠮ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡻࡾࠤᐚ").format(e))