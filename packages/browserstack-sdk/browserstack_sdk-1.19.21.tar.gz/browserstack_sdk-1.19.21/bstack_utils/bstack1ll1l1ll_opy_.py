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
import sys
import logging
import tarfile
import io
import os
import requests
import re
from requests_toolbelt.multipart.encoder import MultipartEncoder
from bstack_utils.constants import bstack11l1l11l11_opy_
import tempfile
import json
bstack111l11l11l_opy_ = os.path.join(tempfile.gettempdir(), bstack1llll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡤࡦࡤࡸ࡫࠳ࡲ࡯ࡨࠩፀ"))
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack1llll1l_opy_ (u"ࠨ࡞ࡱࠩ࠭ࡧࡳࡤࡶ࡬ࡱࡪ࠯ࡳࠡ࡝ࠨࠬࡳࡧ࡭ࡦࠫࡶࡡࡠࠫࠨ࡭ࡧࡹࡩࡱࡴࡡ࡮ࡧࠬࡷࡢࠦ࠭ࠡࠧࠫࡱࡪࡹࡳࡢࡩࡨ࠭ࡸ࠭ፁ"),
      datefmt=bstack1llll1l_opy_ (u"ࠩࠨࡌ࠿ࠫࡍ࠻ࠧࡖࠫፂ"),
      stream=sys.stdout
    )
  return logger
def bstack111l1l11l1_opy_():
  global bstack111l11l11l_opy_
  if os.path.exists(bstack111l11l11l_opy_):
    os.remove(bstack111l11l11l_opy_)
def bstack11l1ll1l_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def bstack1ll1l111l_opy_(config, log_level):
  bstack111l11ll1l_opy_ = log_level
  if bstack1llll1l_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬፃ") in config:
    bstack111l11ll1l_opy_ = bstack11l1l11l11_opy_[config[bstack1llll1l_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭ፄ")]]
  if config.get(bstack1llll1l_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡇࡵࡵࡱࡆࡥࡵࡺࡵࡳࡧࡏࡳ࡬ࡹࠧፅ"), False):
    logging.getLogger().setLevel(bstack111l11ll1l_opy_)
    return bstack111l11ll1l_opy_
  global bstack111l11l11l_opy_
  bstack11l1ll1l_opy_()
  bstack111l11ll11_opy_ = logging.Formatter(
    fmt=bstack1llll1l_opy_ (u"࠭࡜࡯ࠧࠫࡥࡸࡩࡴࡪ࡯ࡨ࠭ࡸ࡛ࠦࠦࠪࡱࡥࡲ࡫ࠩࡴ࡟࡞ࠩ࠭ࡲࡥࡷࡧ࡯ࡲࡦࡳࡥࠪࡵࡠࠤ࠲ࠦࠥࠩ࡯ࡨࡷࡸࡧࡧࡦࠫࡶࠫፆ"),
    datefmt=bstack1llll1l_opy_ (u"ࠧࠦࡊ࠽ࠩࡒࡀࠥࡔࠩፇ")
  )
  bstack111l1l1l1l_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack111l11l11l_opy_)
  file_handler.setFormatter(bstack111l11ll11_opy_)
  bstack111l1l1l1l_opy_.setFormatter(bstack111l11ll11_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack111l1l1l1l_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack1llll1l_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯࠱ࡻࡪࡨࡤࡳ࡫ࡹࡩࡷ࠴ࡲࡦ࡯ࡲࡸࡪ࠴ࡲࡦ࡯ࡲࡸࡪࡥࡣࡰࡰࡱࡩࡨࡺࡩࡰࡰࠪፈ"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack111l1l1l1l_opy_.setLevel(bstack111l11ll1l_opy_)
  logging.getLogger().addHandler(bstack111l1l1l1l_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack111l11ll1l_opy_
def bstack111l11llll_opy_(config):
  try:
    bstack111l1l111l_opy_ = set([
      bstack1llll1l_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫፉ"), bstack1llll1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ፊ"), bstack1llll1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧፋ"), bstack1llll1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩፌ"), bstack1llll1l_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲ࡜ࡡࡳ࡫ࡤࡦࡱ࡫ࡳࠨፍ"),
      bstack1llll1l_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡛ࡳࡦࡴࠪፎ"), bstack1llll1l_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡢࡵࡶࠫፏ"), bstack1llll1l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡑࡴࡲࡼࡾ࡛ࡳࡦࡴࠪፐ"), bstack1llll1l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡒࡵࡳࡽࡿࡐࡢࡵࡶࠫፑ")
    ])
    bstack111l1l1l11_opy_ = bstack1llll1l_opy_ (u"ࠫࠬፒ")
    with open(bstack1llll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡾࡳ࡬ࠨፓ")) as bstack111l11lll1_opy_:
      bstack111l1l1111_opy_ = bstack111l11lll1_opy_.read()
      bstack111l1l1l11_opy_ = re.sub(bstack1llll1l_opy_ (u"ࡸࠧ࡟ࠪ࡟ࡷ࠰࠯࠿ࠤ࠰࠭ࠨࡡࡴࠧፔ"), bstack1llll1l_opy_ (u"ࠧࠨፕ"), bstack111l1l1111_opy_, flags=re.M)
      bstack111l1l1l11_opy_ = re.sub(
        bstack1llll1l_opy_ (u"ࡳࠩࡡࠬࡡࡹࠫࠪࡁࠫࠫፖ") + bstack1llll1l_opy_ (u"ࠩࡿࠫፗ").join(bstack111l1l111l_opy_) + bstack1llll1l_opy_ (u"ࠪ࠭࠳࠰ࠤࠨፘ"),
        bstack1llll1l_opy_ (u"ࡶࠬࡢ࠲࠻ࠢ࡞ࡖࡊࡊࡁࡄࡖࡈࡈࡢ࠭ፙ"),
        bstack111l1l1l11_opy_, flags=re.M | re.I
      )
    def bstack111l11l1ll_opy_(dic):
      bstack111l1l1ll1_opy_ = {}
      for key, value in dic.items():
        if key in bstack111l1l111l_opy_:
          bstack111l1l1ll1_opy_[key] = bstack1llll1l_opy_ (u"ࠬࡡࡒࡆࡆࡄࡇ࡙ࡋࡄ࡞ࠩፚ")
        else:
          if isinstance(value, dict):
            bstack111l1l1ll1_opy_[key] = bstack111l11l1ll_opy_(value)
          else:
            bstack111l1l1ll1_opy_[key] = value
      return bstack111l1l1ll1_opy_
    bstack111l1l1ll1_opy_ = bstack111l11l1ll_opy_(config)
    return {
      bstack1llll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠩ፛"): bstack111l1l1l11_opy_,
      bstack1llll1l_opy_ (u"ࠧࡧ࡫ࡱࡥࡱࡩ࡯࡯ࡨ࡬࡫࠳ࡰࡳࡰࡰࠪ፜"): json.dumps(bstack111l1l1ll1_opy_)
    }
  except Exception as e:
    return {}
def bstack11ll1ll1l_opy_(config):
  global bstack111l11l11l_opy_
  try:
    if config.get(bstack1llll1l_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡃࡸࡸࡴࡉࡡࡱࡶࡸࡶࡪࡒ࡯ࡨࡵࠪ፝"), False):
      return
    uuid = os.getenv(bstack1llll1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ፞"))
    if not uuid or uuid == bstack1llll1l_opy_ (u"ࠪࡲࡺࡲ࡬ࠨ፟"):
      return
    bstack111l1l11ll_opy_ = [bstack1llll1l_opy_ (u"ࠫࡷ࡫ࡱࡶ࡫ࡵࡩࡲ࡫࡮ࡵࡵ࠱ࡸࡽࡺࠧ፠"), bstack1llll1l_opy_ (u"ࠬࡖࡩࡱࡨ࡬ࡰࡪ࠭፡"), bstack1llll1l_opy_ (u"࠭ࡰࡺࡲࡵࡳ࡯࡫ࡣࡵ࠰ࡷࡳࡲࡲࠧ።"), bstack111l11l11l_opy_]
    bstack11l1ll1l_opy_()
    logging.shutdown()
    output_file = os.path.join(tempfile.gettempdir(), bstack1llll1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠭࡭ࡱࡪࡷ࠲࠭፣") + uuid + bstack1llll1l_opy_ (u"ࠨ࠰ࡷࡥࡷ࠴ࡧࡻࠩ፤"))
    with tarfile.open(output_file, bstack1llll1l_opy_ (u"ࠤࡺ࠾࡬ࢀࠢ፥")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack111l1l11ll_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack111l11llll_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack111l11l1l1_opy_ = data.encode()
        tarinfo.size = len(bstack111l11l1l1_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack111l11l1l1_opy_))
    bstack1l11ll1l_opy_ = MultipartEncoder(
      fields= {
        bstack1llll1l_opy_ (u"ࠪࡨࡦࡺࡡࠨ፦"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack1llll1l_opy_ (u"ࠫࡷࡨࠧ፧")), bstack1llll1l_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲ࡼ࠲࡭ࡺࡪࡲࠪ፨")),
        bstack1llll1l_opy_ (u"࠭ࡣ࡭࡫ࡨࡲࡹࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨ፩"): uuid
      }
    )
    response = requests.post(
      bstack1llll1l_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࡷࡳࡰࡴࡧࡤ࠮ࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡨࡲࡩࡦࡰࡷ࠱ࡱࡵࡧࡴ࠱ࡸࡴࡱࡵࡡࡥࠤ፪"),
      data=bstack1l11ll1l_opy_,
      headers={bstack1llll1l_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧ፫"): bstack1l11ll1l_opy_.content_type},
      auth=(config[bstack1llll1l_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ፬")], config[bstack1llll1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭፭")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack1llll1l_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣࡹࡵࡲ࡯ࡢࡦࠣࡰࡴ࡭ࡳ࠻ࠢࠪ፮") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack1llll1l_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸ࡫࡮ࡥ࡫ࡱ࡫ࠥࡲ࡯ࡨࡵ࠽ࠫ፯") + str(e))
  finally:
    try:
      bstack111l1l11l1_opy_()
    except:
      pass