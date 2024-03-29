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
import atexit
import os
import signal
import sys
import yaml
import requests
import logging
import threading
import socket
import datetime
import string
import random
import json
import collections.abc
import re
import multiprocessing
import traceback
import copy
import tempfile
from packaging import version
from browserstack.local import Local
from urllib.parse import urlparse
from dotenv import load_dotenv
from bstack_utils.constants import *
from bstack_utils.percy import *
from browserstack_sdk.bstack11l111l1_opy_ import *
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.bstack1ll1111l_opy_ import bstack111l1lll1_opy_
import time
import requests
def bstack1111l1ll1_opy_():
  global CONFIG
  headers = {
        bstack1ll11l_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩࡶ"): bstack1ll11l_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧࡷ"),
      }
  proxies = bstack1lllll11l1_opy_(CONFIG, bstack1ll11ll11_opy_)
  try:
    response = requests.get(bstack1ll11ll11_opy_, headers=headers, proxies=proxies, timeout=5)
    if response.json():
      bstack11111ll11_opy_ = response.json()[bstack1ll11l_opy_ (u"ࠬ࡮ࡵࡣࡵࠪࡸ")]
      logger.debug(bstack1l1l1l111_opy_.format(response.json()))
      return bstack11111ll11_opy_
    else:
      logger.debug(bstack1l1ll1ll1l_opy_.format(bstack1ll11l_opy_ (u"ࠨࡒࡦࡵࡳࡳࡳࡹࡥࠡࡌࡖࡓࡓࠦࡰࡢࡴࡶࡩࠥ࡫ࡲࡳࡱࡵࠤࠧࡹ")))
  except Exception as e:
    logger.debug(bstack1l1ll1ll1l_opy_.format(e))
def bstack11ll1l11l_opy_(hub_url):
  global CONFIG
  url = bstack1ll11l_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤࡺ")+  hub_url + bstack1ll11l_opy_ (u"ࠣ࠱ࡦ࡬ࡪࡩ࡫ࠣࡻ")
  headers = {
        bstack1ll11l_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨࡼ"): bstack1ll11l_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ࡽ"),
      }
  proxies = bstack1lllll11l1_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=5)
    latency = time.perf_counter() - start_time
    logger.debug(bstack11l1lllll_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack1ll111l1ll_opy_.format(hub_url, e))
def bstack1llll111ll_opy_():
  try:
    global bstack11l1ll1l_opy_
    bstack11111ll11_opy_ = bstack1111l1ll1_opy_()
    bstack111l11l1l_opy_ = []
    results = []
    for bstack1l11ll11l1_opy_ in bstack11111ll11_opy_:
      bstack111l11l1l_opy_.append(bstack11ll111l1_opy_(target=bstack11ll1l11l_opy_,args=(bstack1l11ll11l1_opy_,)))
    for t in bstack111l11l1l_opy_:
      t.start()
    for t in bstack111l11l1l_opy_:
      results.append(t.join())
    bstack1l1ll1l11l_opy_ = {}
    for item in results:
      hub_url = item[bstack1ll11l_opy_ (u"ࠫ࡭ࡻࡢࡠࡷࡵࡰࠬࡾ")]
      latency = item[bstack1ll11l_opy_ (u"ࠬࡲࡡࡵࡧࡱࡧࡾ࠭ࡿ")]
      bstack1l1ll1l11l_opy_[hub_url] = latency
    bstack1l1lll11_opy_ = min(bstack1l1ll1l11l_opy_, key= lambda x: bstack1l1ll1l11l_opy_[x])
    bstack11l1ll1l_opy_ = bstack1l1lll11_opy_
    logger.debug(bstack1llll1ll1l_opy_.format(bstack1l1lll11_opy_))
  except Exception as e:
    logger.debug(bstack1l11l1ll_opy_.format(e))
from bstack_utils.messages import *
from bstack_utils import bstack1llll1lll1_opy_
from bstack_utils.config import Config
from bstack_utils.helper import bstack1lll1lll1l_opy_, bstack11l1llll1_opy_, bstack111l1ll1_opy_, bstack1l1l111l1l_opy_, bstack11ll1l11_opy_, \
  Notset, bstack1l11lllll1_opy_, \
  bstack1ll1ll11ll_opy_, bstack1l1l1llll1_opy_, bstack1llll1l111_opy_, bstack1llll1111_opy_, bstack1ll11l1ll_opy_, bstack1llll1l1ll_opy_, \
  bstack1lll1lll11_opy_, \
  bstack1ll1ll11_opy_, bstack11lll1l1_opy_, bstack1l1ll11l1l_opy_, bstack11l11ll11_opy_, \
  bstack1l1l11l11l_opy_, bstack111l1l11_opy_, bstack1l11111l1_opy_
from bstack_utils.bstack1ll11lll1l_opy_ import bstack11lll1ll1_opy_
from bstack_utils.bstack1ll1lll11_opy_ import bstack111111l1_opy_
from bstack_utils.bstack1111ll1ll_opy_ import bstack1111ll11_opy_, bstack11l1ll11l_opy_
from bstack_utils.bstack1111l1111_opy_ import bstack1l111lll1_opy_
from bstack_utils.bstack1111l1l1_opy_ import bstack1111l1l1_opy_
from bstack_utils.proxy import bstack1lll1l1lll_opy_, bstack1lllll11l1_opy_, bstack1l1ll1l1l1_opy_, bstack1l1l1ll1ll_opy_
import bstack_utils.bstack1l11l1lll_opy_ as bstack1ll1lll1ll_opy_
from browserstack_sdk.bstack111ll11l_opy_ import *
from browserstack_sdk.bstack1ll11111l1_opy_ import *
from bstack_utils.bstack11111ll1l_opy_ import bstack1l1llll111_opy_
bstack1lll111l_opy_ = bstack1ll11l_opy_ (u"࠭ࠠࠡ࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࡠࡳࠦࠠࡪࡨࠫࡴࡦ࡭ࡥࠡ࠿ࡀࡁࠥࡼ࡯ࡪࡦࠣ࠴࠮ࠦࡻ࡝ࡰࠣࠤࠥࡺࡲࡺࡽ࡟ࡲࠥࡩ࡯࡯ࡵࡷࠤ࡫ࡹࠠ࠾ࠢࡵࡩࡶࡻࡩࡳࡧࠫࡠࠬ࡬ࡳ࡝ࠩࠬ࠿ࡡࡴࠠࠡࠢࠣࠤ࡫ࡹ࠮ࡢࡲࡳࡩࡳࡪࡆࡪ࡮ࡨࡗࡾࡴࡣࠩࡤࡶࡸࡦࡩ࡫ࡠࡲࡤࡸ࡭࠲ࠠࡋࡕࡒࡒ࠳ࡹࡴࡳ࡫ࡱ࡫࡮࡬ࡹࠩࡲࡢ࡭ࡳࡪࡥࡹࠫࠣ࠯ࠥࠨ࠺ࠣࠢ࠮ࠤࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡐࡓࡐࡐ࠱ࡴࡦࡸࡳࡦࠪࠫࡥࡼࡧࡩࡵࠢࡱࡩࡼࡖࡡࡨࡧ࠵࠲ࡪࡼࡡ࡭ࡷࡤࡸࡪ࠮ࠢࠩࠫࠣࡁࡃࠦࡻࡾࠤ࠯ࠤࡡ࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡧࡦࡶࡖࡩࡸࡹࡩࡰࡰࡇࡩࡹࡧࡩ࡭ࡵࠥࢁࡡ࠭ࠩࠪࠫ࡞ࠦ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠢ࡞ࠫࠣ࠯ࠥࠨࠬ࡝࡞ࡱࠦ࠮ࡢ࡮ࠡࠢࠣࠤࢂࡩࡡࡵࡥ࡫ࠬࡪࡾࠩࡼ࡞ࡱࠤࠥࠦࠠࡾ࡞ࡱࠤࠥࢃ࡜࡯ࠢࠣ࠳࠯ࠦ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࠣ࠮࠴࠭ࢀ")
bstack1ll1l11ll1_opy_ = bstack1ll11l_opy_ (u"ࠧ࡝ࡰ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࡡࡴࡣࡰࡰࡶࡸࠥࡨࡳࡵࡣࡦ࡯ࡤࡶࡡࡵࡪࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࡟ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠹࡝࡝ࡰࡦࡳࡳࡹࡴࠡࡤࡶࡸࡦࡩ࡫ࡠࡥࡤࡴࡸࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠳ࡠࡠࡳࡩ࡯࡯ࡵࡷࠤࡵࡥࡩ࡯ࡦࡨࡼࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠳࡟࡟ࡲࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡸࡲࡩࡤࡧࠫ࠴࠱ࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠴ࠫ࡟ࡲࡨࡵ࡮ࡴࡶࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫ࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤࠬ࠿ࡡࡴࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴࡬ࡢࡷࡱࡧ࡭ࠦ࠽ࠡࡣࡶࡽࡳࡩࠠࠩ࡮ࡤࡹࡳࡩࡨࡐࡲࡷ࡭ࡴࡴࡳࠪࠢࡀࡂࠥࢁ࡜࡯࡮ࡨࡸࠥࡩࡡࡱࡵ࠾ࡠࡳࡺࡲࡺࠢࡾࡠࡳࡩࡡࡱࡵࠣࡁࠥࡐࡓࡐࡐ࠱ࡴࡦࡸࡳࡦࠪࡥࡷࡹࡧࡣ࡬ࡡࡦࡥࡵࡹࠩ࡝ࡰࠣࠤࢂࠦࡣࡢࡶࡦ࡬࠭࡫ࡸࠪࠢࡾࡠࡳࠦࠠࠡࠢࢀࡠࡳࠦࠠࡳࡧࡷࡹࡷࡴࠠࡢࡹࡤ࡭ࡹࠦࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴ࡣࡰࡰࡱࡩࡨࡺࠨࡼ࡞ࡱࠤࠥࠦࠠࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷ࠾ࠥࡦࡷࡴࡵ࠽࠳࠴ࡩࡤࡱ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡁࡦࡥࡵࡹ࠽ࠥࡽࡨࡲࡨࡵࡤࡦࡗࡕࡍࡈࡵ࡭ࡱࡱࡱࡩࡳࡺࠨࡋࡕࡒࡒ࠳ࡹࡴࡳ࡫ࡱ࡫࡮࡬ࡹࠩࡥࡤࡴࡸ࠯ࠩࡾࡢ࠯ࡠࡳࠦࠠࠡࠢ࠱࠲࠳ࡲࡡࡶࡰࡦ࡬ࡔࡶࡴࡪࡱࡱࡷࡡࡴࠠࠡࡿࠬࡠࡳࢃ࡜࡯࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࡠࡳ࠭ࢁ")
from ._version import __version__
bstack1111111ll_opy_ = None
CONFIG = {}
bstack11ll1l1l_opy_ = {}
bstack1l1ll1l1_opy_ = {}
bstack1lll11111_opy_ = None
bstack1ll1l11111_opy_ = None
bstack1l11ll1l_opy_ = None
bstack11l111l11_opy_ = -1
bstack1111l11ll_opy_ = 0
bstack111ll1ll_opy_ = bstack1lllllllll_opy_
bstack1ll111l11l_opy_ = 1
bstack11l111111_opy_ = False
bstack1lll1ll111_opy_ = False
bstack11ll11ll1_opy_ = bstack1ll11l_opy_ (u"ࠨࠩࢂ")
bstack111l1l1l_opy_ = bstack1ll11l_opy_ (u"ࠩࠪࢃ")
bstack111l11111_opy_ = False
bstack1ll1l11l1_opy_ = True
bstack111ll1lll_opy_ = bstack1ll11l_opy_ (u"ࠪࠫࢄ")
bstack1l11l1l111_opy_ = []
bstack11l1ll1l_opy_ = bstack1ll11l_opy_ (u"ࠫࠬࢅ")
bstack1l1ll111ll_opy_ = False
bstack1l1l1l11l_opy_ = None
bstack1llllll11_opy_ = None
bstack1ll11l1ll1_opy_ = None
bstack111ll1ll1_opy_ = -1
bstack1l1l1llll_opy_ = os.path.join(os.path.expanduser(bstack1ll11l_opy_ (u"ࠬࢄࠧࢆ")), bstack1ll11l_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ࢇ"), bstack1ll11l_opy_ (u"ࠧ࠯ࡴࡲࡦࡴࡺ࠭ࡳࡧࡳࡳࡷࡺ࠭ࡩࡧ࡯ࡴࡪࡸ࠮࡫ࡵࡲࡲࠬ࢈"))
bstack1ll1llll1l_opy_ = 0
bstack1l1llll1ll_opy_ = []
bstack1l1l111l11_opy_ = []
bstack1ll1111ll_opy_ = []
bstack1ll11l1l1_opy_ = []
bstack1l1l111l_opy_ = bstack1ll11l_opy_ (u"ࠨࠩࢉ")
bstack1l111l11_opy_ = bstack1ll11l_opy_ (u"ࠩࠪࢊ")
bstack11111l1ll_opy_ = False
bstack1l1l1l1ll_opy_ = False
bstack1lll1l1l11_opy_ = {}
bstack1ll1l11ll_opy_ = None
bstack11l1111ll_opy_ = None
bstack1l1l1ll1l_opy_ = None
bstack1l1llll1l_opy_ = None
bstack11llll11l_opy_ = None
bstack1l1ll1lll1_opy_ = None
bstack1l1l1l1111_opy_ = None
bstack1ll1lllll1_opy_ = None
bstack1llll11111_opy_ = None
bstack1lll111lll_opy_ = None
bstack1ll1lll1l1_opy_ = None
bstack1l1l1ll111_opy_ = None
bstack1l11l1l1l1_opy_ = None
bstack1l11ll1111_opy_ = None
bstack111111l11_opy_ = None
bstack1llllll1l1_opy_ = None
bstack1l1ll1111_opy_ = None
bstack1ll111l11_opy_ = None
bstack1111llll_opy_ = None
bstack111111l1l_opy_ = None
bstack1lllll111_opy_ = None
bstack11ll11l1l_opy_ = False
bstack1lll1l1l_opy_ = bstack1ll11l_opy_ (u"ࠥࠦࢋ")
logger = bstack1llll1lll1_opy_.get_logger(__name__, bstack111ll1ll_opy_)
bstack1l11l111l_opy_ = Config.bstack1l11llll1l_opy_()
percy = bstack11ll11l1_opy_()
bstack1ll1111lll_opy_ = bstack111l1lll1_opy_()
def bstack1llll1lll_opy_():
  global CONFIG
  global bstack11111l1ll_opy_
  global bstack1l11l111l_opy_
  bstack1ll1111111_opy_ = bstack1l1l1111ll_opy_(CONFIG)
  if (bstack1ll11l_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ࢌ") in bstack1ll1111111_opy_ and str(bstack1ll1111111_opy_[bstack1ll11l_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧࢍ")]).lower() == bstack1ll11l_opy_ (u"࠭ࡴࡳࡷࡨࠫࢎ")):
    bstack11111l1ll_opy_ = True
  bstack1l11l111l_opy_.bstack111l1111l_opy_(bstack1ll1111111_opy_.get(bstack1ll11l_opy_ (u"ࠧࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫ࢏"), False))
def bstack1llllllll_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack1lll1l1ll_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1l11l1ll11_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstack1ll11l_opy_ (u"ࠣ࠯࠰ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡥࡲࡲ࡫࡯ࡧࡧ࡫࡯ࡩࠧ࢐") == args[i].lower() or bstack1ll11l_opy_ (u"ࠤ࠰࠱ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡴࡦࡪࡩࠥ࢑") == args[i].lower():
      path = args[i + 1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      global bstack111ll1lll_opy_
      bstack111ll1lll_opy_ += bstack1ll11l_opy_ (u"ࠪ࠱࠲ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡇࡴࡴࡦࡪࡩࡉ࡭ࡱ࡫ࠠࠨ࢒") + path
      return path
  return None
bstack1111l1ll_opy_ = re.compile(bstack1ll11l_opy_ (u"ࡶࠧ࠴ࠪࡀ࡞ࠧࡿ࠭࠴ࠪࡀࠫࢀ࠲࠯ࡅࠢ࢓"))
def bstack1lllll1ll1_opy_(loader, node):
  value = loader.construct_scalar(node)
  for group in bstack1111l1ll_opy_.findall(value):
    if group is not None and os.environ.get(group) is not None:
      value = value.replace(bstack1ll11l_opy_ (u"ࠧࠪࡻࠣ࢔") + group + bstack1ll11l_opy_ (u"ࠨࡽࠣ࢕"), os.environ.get(group))
  return value
def bstack1lll11ll1l_opy_():
  bstack1l111ll1_opy_ = bstack1l11l1ll11_opy_()
  if bstack1l111ll1_opy_ and os.path.exists(os.path.abspath(bstack1l111ll1_opy_)):
    fileName = bstack1l111ll1_opy_
  if bstack1ll11l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌࡥࡆࡊࡎࡈࠫ࢖") in os.environ and os.path.exists(
          os.path.abspath(os.environ[bstack1ll11l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍ࡟ࡇࡋࡏࡉࠬࢗ")])) and not bstack1ll11l_opy_ (u"ࠩࡩ࡭ࡱ࡫ࡎࡢ࡯ࡨࠫ࢘") in locals():
    fileName = os.environ[bstack1ll11l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࡡࡉࡍࡑࡋ࢙ࠧ")]
  if bstack1ll11l_opy_ (u"ࠫ࡫࡯࡬ࡦࡐࡤࡱࡪ࢚࠭") in locals():
    bstack1111_opy_ = os.path.abspath(fileName)
  else:
    bstack1111_opy_ = bstack1ll11l_opy_ (u"࢛ࠬ࠭")
  bstack1l1l1ll11l_opy_ = os.getcwd()
  bstack111llllll_opy_ = bstack1ll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠩ࢜")
  bstack1l1l1l111l_opy_ = bstack1ll11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹࡢ࡯࡯ࠫ࢝")
  while (not os.path.exists(bstack1111_opy_)) and bstack1l1l1ll11l_opy_ != bstack1ll11l_opy_ (u"ࠣࠤ࢞"):
    bstack1111_opy_ = os.path.join(bstack1l1l1ll11l_opy_, bstack111llllll_opy_)
    if not os.path.exists(bstack1111_opy_):
      bstack1111_opy_ = os.path.join(bstack1l1l1ll11l_opy_, bstack1l1l1l111l_opy_)
    if bstack1l1l1ll11l_opy_ != os.path.dirname(bstack1l1l1ll11l_opy_):
      bstack1l1l1ll11l_opy_ = os.path.dirname(bstack1l1l1ll11l_opy_)
    else:
      bstack1l1l1ll11l_opy_ = bstack1ll11l_opy_ (u"ࠤࠥ࢟")
  if not os.path.exists(bstack1111_opy_):
    bstack11l11l1l_opy_(
      bstack1lllll1lll_opy_.format(os.getcwd()))
  try:
    with open(bstack1111_opy_, bstack1ll11l_opy_ (u"ࠪࡶࠬࢠ")) as stream:
      yaml.add_implicit_resolver(bstack1ll11l_opy_ (u"ࠦࠦࡶࡡࡵࡪࡨࡼࠧࢡ"), bstack1111l1ll_opy_)
      yaml.add_constructor(bstack1ll11l_opy_ (u"ࠧࠧࡰࡢࡶ࡫ࡩࡽࠨࢢ"), bstack1lllll1ll1_opy_)
      config = yaml.load(stream, yaml.FullLoader)
      return config
  except:
    with open(bstack1111_opy_, bstack1ll11l_opy_ (u"࠭ࡲࠨࢣ")) as stream:
      try:
        config = yaml.safe_load(stream)
        return config
      except yaml.YAMLError as exc:
        bstack11l11l1l_opy_(bstack1ll1l11l11_opy_.format(str(exc)))
def bstack1l1l111l1_opy_(config):
  bstack1ll1111l1_opy_ = bstack11l111lll_opy_(config)
  for option in list(bstack1ll1111l1_opy_):
    if option.lower() in bstack1ll1l11l1l_opy_ and option != bstack1ll1l11l1l_opy_[option.lower()]:
      bstack1ll1111l1_opy_[bstack1ll1l11l1l_opy_[option.lower()]] = bstack1ll1111l1_opy_[option]
      del bstack1ll1111l1_opy_[option]
  return config
def bstack1l1l11ll11_opy_():
  global bstack1l1ll1l1_opy_
  for key, bstack1l11l11ll_opy_ in bstack1l11ll11_opy_.items():
    if isinstance(bstack1l11l11ll_opy_, list):
      for var in bstack1l11l11ll_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack1l1ll1l1_opy_[key] = os.environ[var]
          break
    elif bstack1l11l11ll_opy_ in os.environ and os.environ[bstack1l11l11ll_opy_] and str(os.environ[bstack1l11l11ll_opy_]).strip():
      bstack1l1ll1l1_opy_[key] = os.environ[bstack1l11l11ll_opy_]
  if bstack1ll11l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩࢤ") in os.environ:
    bstack1l1ll1l1_opy_[bstack1ll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬࢥ")] = {}
    bstack1l1ll1l1_opy_[bstack1ll11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢦ")][bstack1ll11l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࢧ")] = os.environ[bstack1ll11l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭ࢨ")]
def bstack1l11ll1l1_opy_():
  global bstack11ll1l1l_opy_
  global bstack111ll1lll_opy_
  for idx, val in enumerate(sys.argv):
    if idx < len(sys.argv) and bstack1ll11l_opy_ (u"ࠬ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨࢩ").lower() == val.lower():
      bstack11ll1l1l_opy_[bstack1ll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪࢪ")] = {}
      bstack11ll1l1l_opy_[bstack1ll11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫࢫ")][bstack1ll11l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࢬ")] = sys.argv[idx + 1]
      del sys.argv[idx:idx + 2]
      break
  for key, bstack11lll1ll_opy_ in bstack1l1lll11l1_opy_.items():
    if isinstance(bstack11lll1ll_opy_, list):
      for idx, val in enumerate(sys.argv):
        for var in bstack11lll1ll_opy_:
          if idx < len(sys.argv) and bstack1ll11l_opy_ (u"ࠩ࠰࠱ࠬࢭ") + var.lower() == val.lower() and not key in bstack11ll1l1l_opy_:
            bstack11ll1l1l_opy_[key] = sys.argv[idx + 1]
            bstack111ll1lll_opy_ += bstack1ll11l_opy_ (u"ࠪࠤ࠲࠳ࠧࢮ") + var + bstack1ll11l_opy_ (u"ࠫࠥ࠭ࢯ") + sys.argv[idx + 1]
            del sys.argv[idx:idx + 2]
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx < len(sys.argv) and bstack1ll11l_opy_ (u"ࠬ࠳࠭ࠨࢰ") + bstack11lll1ll_opy_.lower() == val.lower() and not key in bstack11ll1l1l_opy_:
          bstack11ll1l1l_opy_[key] = sys.argv[idx + 1]
          bstack111ll1lll_opy_ += bstack1ll11l_opy_ (u"࠭ࠠ࠮࠯ࠪࢱ") + bstack11lll1ll_opy_ + bstack1ll11l_opy_ (u"ࠧࠡࠩࢲ") + sys.argv[idx + 1]
          del sys.argv[idx:idx + 2]
def bstack11ll11111_opy_(config):
  bstack1lllll1l1_opy_ = config.keys()
  for bstack1l11ll1ll1_opy_, bstack111ll111_opy_ in bstack11ll1l1ll_opy_.items():
    if bstack111ll111_opy_ in bstack1lllll1l1_opy_:
      config[bstack1l11ll1ll1_opy_] = config[bstack111ll111_opy_]
      del config[bstack111ll111_opy_]
  for bstack1l11ll1ll1_opy_, bstack111ll111_opy_ in bstack1l1l1111_opy_.items():
    if isinstance(bstack111ll111_opy_, list):
      for bstack11lll11l_opy_ in bstack111ll111_opy_:
        if bstack11lll11l_opy_ in bstack1lllll1l1_opy_:
          config[bstack1l11ll1ll1_opy_] = config[bstack11lll11l_opy_]
          del config[bstack11lll11l_opy_]
          break
    elif bstack111ll111_opy_ in bstack1lllll1l1_opy_:
      config[bstack1l11ll1ll1_opy_] = config[bstack111ll111_opy_]
      del config[bstack111ll111_opy_]
  for bstack11lll11l_opy_ in list(config):
    for bstack1lll11lll_opy_ in bstack1ll1l1lll1_opy_:
      if bstack11lll11l_opy_.lower() == bstack1lll11lll_opy_.lower() and bstack11lll11l_opy_ != bstack1lll11lll_opy_:
        config[bstack1lll11lll_opy_] = config[bstack11lll11l_opy_]
        del config[bstack11lll11l_opy_]
  bstack1l1ll1ll1_opy_ = []
  if bstack1ll11l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫࢳ") in config:
    bstack1l1ll1ll1_opy_ = config[bstack1ll11l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬࢴ")]
  for platform in bstack1l1ll1ll1_opy_:
    for bstack11lll11l_opy_ in list(platform):
      for bstack1lll11lll_opy_ in bstack1ll1l1lll1_opy_:
        if bstack11lll11l_opy_.lower() == bstack1lll11lll_opy_.lower() and bstack11lll11l_opy_ != bstack1lll11lll_opy_:
          platform[bstack1lll11lll_opy_] = platform[bstack11lll11l_opy_]
          del platform[bstack11lll11l_opy_]
  for bstack1l11ll1ll1_opy_, bstack111ll111_opy_ in bstack1l1l1111_opy_.items():
    for platform in bstack1l1ll1ll1_opy_:
      if isinstance(bstack111ll111_opy_, list):
        for bstack11lll11l_opy_ in bstack111ll111_opy_:
          if bstack11lll11l_opy_ in platform:
            platform[bstack1l11ll1ll1_opy_] = platform[bstack11lll11l_opy_]
            del platform[bstack11lll11l_opy_]
            break
      elif bstack111ll111_opy_ in platform:
        platform[bstack1l11ll1ll1_opy_] = platform[bstack111ll111_opy_]
        del platform[bstack111ll111_opy_]
  for bstack11l1lll1_opy_ in bstack1111l11l1_opy_:
    if bstack11l1lll1_opy_ in config:
      if not bstack1111l11l1_opy_[bstack11l1lll1_opy_] in config:
        config[bstack1111l11l1_opy_[bstack11l1lll1_opy_]] = {}
      config[bstack1111l11l1_opy_[bstack11l1lll1_opy_]].update(config[bstack11l1lll1_opy_])
      del config[bstack11l1lll1_opy_]
  for platform in bstack1l1ll1ll1_opy_:
    for bstack11l1lll1_opy_ in bstack1111l11l1_opy_:
      if bstack11l1lll1_opy_ in list(platform):
        if not bstack1111l11l1_opy_[bstack11l1lll1_opy_] in platform:
          platform[bstack1111l11l1_opy_[bstack11l1lll1_opy_]] = {}
        platform[bstack1111l11l1_opy_[bstack11l1lll1_opy_]].update(platform[bstack11l1lll1_opy_])
        del platform[bstack11l1lll1_opy_]
  config = bstack1l1l111l1_opy_(config)
  return config
def bstack1ll1l1111l_opy_(config):
  global bstack111l1l1l_opy_
  if bstack1ll11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧࢵ") in config and str(config[bstack1ll11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨࢶ")]).lower() != bstack1ll11l_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫࢷ"):
    if not bstack1ll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪࢸ") in config:
      config[bstack1ll11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫࢹ")] = {}
    if not bstack1ll11l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࢺ") in config[bstack1ll11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢻ")]:
      bstack1ll111ll11_opy_ = datetime.datetime.now()
      bstack111111ll1_opy_ = bstack1ll111ll11_opy_.strftime(bstack1ll11l_opy_ (u"ࠪࠩࡩࡥࠥࡣࡡࠨࡌࠪࡓࠧࢼ"))
      hostname = socket.gethostname()
      bstack1l1llll11l_opy_ = bstack1ll11l_opy_ (u"ࠫࠬࢽ").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack1ll11l_opy_ (u"ࠬࢁࡽࡠࡽࢀࡣࢀࢃࠧࢾ").format(bstack111111ll1_opy_, hostname, bstack1l1llll11l_opy_)
      config[bstack1ll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪࢿ")][bstack1ll11l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࣀ")] = identifier
    bstack111l1l1l_opy_ = config[bstack1ll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬࣁ")][bstack1ll11l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࣂ")]
  return config
def bstack11111llll_opy_():
  bstack111l1llll_opy_ =  bstack1llll1111_opy_()[bstack1ll11l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠩࣃ")]
  return bstack111l1llll_opy_ if bstack111l1llll_opy_ else -1
def bstack11l11l111_opy_(bstack111l1llll_opy_):
  global CONFIG
  if not bstack1ll11l_opy_ (u"ࠫࠩࢁࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࢂ࠭ࣄ") in CONFIG[bstack1ll11l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࣅ")]:
    return
  CONFIG[bstack1ll11l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨࣆ")] = CONFIG[bstack1ll11l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࣇ")].replace(
    bstack1ll11l_opy_ (u"ࠨࠦࡾࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࡿࠪࣈ"),
    str(bstack111l1llll_opy_)
  )
def bstack11ll1llll_opy_():
  global CONFIG
  if not bstack1ll11l_opy_ (u"ࠩࠧࡿࡉࡇࡔࡆࡡࡗࡍࡒࡋࡽࠨࣉ") in CONFIG[bstack1ll11l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ࣊")]:
    return
  bstack1ll111ll11_opy_ = datetime.datetime.now()
  bstack111111ll1_opy_ = bstack1ll111ll11_opy_.strftime(bstack1ll11l_opy_ (u"ࠫࠪࡪ࠭ࠦࡤ࠰ࠩࡍࡀࠥࡎࠩ࣋"))
  CONFIG[bstack1ll11l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ࣌")] = CONFIG[bstack1ll11l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ࣍")].replace(
    bstack1ll11l_opy_ (u"ࠧࠥࡽࡇࡅ࡙ࡋ࡟ࡕࡋࡐࡉࢂ࠭࣎"),
    bstack111111ll1_opy_
  )
def bstack1lll11ll1_opy_():
  global CONFIG
  if bstack1ll11l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴ࣏ࠪ") in CONFIG and not bool(CONFIG[bstack1ll11l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵ࣐ࠫ")]):
    del CONFIG[bstack1ll11l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶ࣑ࠬ")]
    return
  if not bstack1ll11l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࣒࠭") in CONFIG:
    CONFIG[bstack1ll11l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸ࣓ࠧ")] = bstack1ll11l_opy_ (u"࠭ࠣࠥࡽࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࡾࠩࣔ")
  if bstack1ll11l_opy_ (u"ࠧࠥࡽࡇࡅ࡙ࡋ࡟ࡕࡋࡐࡉࢂ࠭ࣕ") in CONFIG[bstack1ll11l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࣖ")]:
    bstack11ll1llll_opy_()
    os.environ[bstack1ll11l_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡡࡆࡓࡒࡈࡉࡏࡇࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉ࠭ࣗ")] = CONFIG[bstack1ll11l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࣘ")]
  if not bstack1ll11l_opy_ (u"ࠫࠩࢁࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࢂ࠭ࣙ") in CONFIG[bstack1ll11l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࣚ")]:
    return
  bstack111l1llll_opy_ = bstack1ll11l_opy_ (u"࠭ࠧࣛ")
  bstack1l1ll1llll_opy_ = bstack11111llll_opy_()
  if bstack1l1ll1llll_opy_ != -1:
    bstack111l1llll_opy_ = bstack1ll11l_opy_ (u"ࠧࡄࡋࠣࠫࣜ") + str(bstack1l1ll1llll_opy_)
  if bstack111l1llll_opy_ == bstack1ll11l_opy_ (u"ࠨࠩࣝ"):
    bstack111ll11ll_opy_ = bstack1l1lll1ll1_opy_(CONFIG[bstack1ll11l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬࣞ")])
    if bstack111ll11ll_opy_ != -1:
      bstack111l1llll_opy_ = str(bstack111ll11ll_opy_)
  if bstack111l1llll_opy_:
    bstack11l11l111_opy_(bstack111l1llll_opy_)
    os.environ[bstack1ll11l_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡢࡇࡔࡓࡂࡊࡐࡈࡈࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧࣟ")] = CONFIG[bstack1ll11l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭࣠")]
def bstack1l1l1ll1_opy_(bstack1111l1lll_opy_, bstack111l1l111_opy_, path):
  bstack11lll1l1l_opy_ = {
    bstack1ll11l_opy_ (u"ࠬ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ࣡"): bstack111l1l111_opy_
  }
  if os.path.exists(path):
    bstack1lll1lll1_opy_ = json.load(open(path, bstack1ll11l_opy_ (u"࠭ࡲࡣࠩ࣢")))
  else:
    bstack1lll1lll1_opy_ = {}
  bstack1lll1lll1_opy_[bstack1111l1lll_opy_] = bstack11lll1l1l_opy_
  with open(path, bstack1ll11l_opy_ (u"ࠢࡸࣣ࠭ࠥ")) as outfile:
    json.dump(bstack1lll1lll1_opy_, outfile)
def bstack1l1lll1ll1_opy_(bstack1111l1lll_opy_):
  bstack1111l1lll_opy_ = str(bstack1111l1lll_opy_)
  bstack111ll1111_opy_ = os.path.join(os.path.expanduser(bstack1ll11l_opy_ (u"ࠨࢀࠪࣤ")), bstack1ll11l_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩࣥ"))
  try:
    if not os.path.exists(bstack111ll1111_opy_):
      os.makedirs(bstack111ll1111_opy_)
    file_path = os.path.join(os.path.expanduser(bstack1ll11l_opy_ (u"ࠪࢂࣦࠬ")), bstack1ll11l_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫࣧ"), bstack1ll11l_opy_ (u"ࠬ࠴ࡢࡶ࡫࡯ࡨ࠲ࡴࡡ࡮ࡧ࠰ࡧࡦࡩࡨࡦ࠰࡭ࡷࡴࡴࠧࣨ"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack1ll11l_opy_ (u"࠭ࡷࠨࣩ")):
        pass
      with open(file_path, bstack1ll11l_opy_ (u"ࠢࡸ࠭ࠥ࣪")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack1ll11l_opy_ (u"ࠨࡴࠪ࣫")) as bstack1lll11ll11_opy_:
      bstack1llllll111_opy_ = json.load(bstack1lll11ll11_opy_)
    if bstack1111l1lll_opy_ in bstack1llllll111_opy_:
      bstack1l1l11ll1_opy_ = bstack1llllll111_opy_[bstack1111l1lll_opy_][bstack1ll11l_opy_ (u"ࠩ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭࣬")]
      bstack1l11ll111l_opy_ = int(bstack1l1l11ll1_opy_) + 1
      bstack1l1l1ll1_opy_(bstack1111l1lll_opy_, bstack1l11ll111l_opy_, file_path)
      return bstack1l11ll111l_opy_
    else:
      bstack1l1l1ll1_opy_(bstack1111l1lll_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack1111l1l11_opy_.format(str(e)))
    return -1
def bstack11111lll1_opy_(config):
  if not config[bstack1ll11l_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩ࣭ࠬ")] or not config[bstack1ll11l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿ࣮ࠧ")]:
    return True
  else:
    return False
def bstack1llll11ll_opy_(config, index=0):
  global bstack111l11111_opy_
  bstack1ll1llll11_opy_ = {}
  caps = bstack1ll1l1111_opy_ + bstack1l11l1l11l_opy_
  if bstack111l11111_opy_:
    caps += bstack1l1lll1l_opy_
  for key in config:
    if key in caps + [bstack1ll11l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ࣯")]:
      continue
    bstack1ll1llll11_opy_[key] = config[key]
  if bstack1ll11l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࣰࠩ") in config:
    for bstack11ll1111_opy_ in config[bstack1ll11l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࣱࠪ")][index]:
      if bstack11ll1111_opy_ in caps + [bstack1ll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪࣲ࠭"), bstack1ll11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪࣳ")]:
        continue
      bstack1ll1llll11_opy_[bstack11ll1111_opy_] = config[bstack1ll11l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ࣴ")][index][bstack11ll1111_opy_]
  bstack1ll1llll11_opy_[bstack1ll11l_opy_ (u"ࠫ࡭ࡵࡳࡵࡐࡤࡱࡪ࠭ࣵ")] = socket.gethostname()
  if bstack1ll11l_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳࣶ࠭") in bstack1ll1llll11_opy_:
    del (bstack1ll1llll11_opy_[bstack1ll11l_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧࣷ")])
  return bstack1ll1llll11_opy_
def bstack11llll11_opy_(config):
  global bstack111l11111_opy_
  bstack11ll11lll_opy_ = {}
  caps = bstack1l11l1l11l_opy_
  if bstack111l11111_opy_:
    caps += bstack1l1lll1l_opy_
  for key in caps:
    if key in config:
      bstack11ll11lll_opy_[key] = config[key]
  return bstack11ll11lll_opy_
def bstack11l11l1l1_opy_(bstack1ll1llll11_opy_, bstack11ll11lll_opy_):
  bstack11ll1ll1_opy_ = {}
  for key in bstack1ll1llll11_opy_.keys():
    if key in bstack11ll1l1ll_opy_:
      bstack11ll1ll1_opy_[bstack11ll1l1ll_opy_[key]] = bstack1ll1llll11_opy_[key]
    else:
      bstack11ll1ll1_opy_[key] = bstack1ll1llll11_opy_[key]
  for key in bstack11ll11lll_opy_:
    if key in bstack11ll1l1ll_opy_:
      bstack11ll1ll1_opy_[bstack11ll1l1ll_opy_[key]] = bstack11ll11lll_opy_[key]
    else:
      bstack11ll1ll1_opy_[key] = bstack11ll11lll_opy_[key]
  return bstack11ll1ll1_opy_
def bstack1lll1111ll_opy_(config, index=0):
  global bstack111l11111_opy_
  caps = {}
  config = copy.deepcopy(config)
  bstack111l1l1l1_opy_ = bstack1lll1lll1l_opy_(bstack1l1l1ll1l1_opy_, config, logger)
  bstack11ll11lll_opy_ = bstack11llll11_opy_(config)
  bstack111l11l1_opy_ = bstack1l11l1l11l_opy_
  bstack111l11l1_opy_ += bstack1ll1llll1_opy_
  bstack11ll11lll_opy_ = update(bstack11ll11lll_opy_, bstack111l1l1l1_opy_)
  if bstack111l11111_opy_:
    bstack111l11l1_opy_ += bstack1l1lll1l_opy_
  if bstack1ll11l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪࣸ") in config:
    if bstack1ll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪࣹ࠭") in config[bstack1ll11l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࣺࠬ")][index]:
      caps[bstack1ll11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨࣻ")] = config[bstack1ll11l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧࣼ")][index][bstack1ll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪࣽ")]
    if bstack1ll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧࣾ") in config[bstack1ll11l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪࣿ")][index]:
      caps[bstack1ll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩऀ")] = str(config[bstack1ll11l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬँ")][index][bstack1ll11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫं")])
    bstack1ll1l1ll11_opy_ = bstack1lll1lll1l_opy_(bstack1l1l1ll1l1_opy_, config[bstack1ll11l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧः")][index], logger)
    bstack111l11l1_opy_ += list(bstack1ll1l1ll11_opy_.keys())
    for bstack1lll11111l_opy_ in bstack111l11l1_opy_:
      if bstack1lll11111l_opy_ in config[bstack1ll11l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨऄ")][index]:
        if bstack1lll11111l_opy_ == bstack1ll11l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨअ"):
          try:
            bstack1ll1l1ll11_opy_[bstack1lll11111l_opy_] = str(config[bstack1ll11l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪआ")][index][bstack1lll11111l_opy_] * 1.0)
          except:
            bstack1ll1l1ll11_opy_[bstack1lll11111l_opy_] = str(config[bstack1ll11l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫइ")][index][bstack1lll11111l_opy_])
        else:
          bstack1ll1l1ll11_opy_[bstack1lll11111l_opy_] = config[bstack1ll11l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬई")][index][bstack1lll11111l_opy_]
        del (config[bstack1ll11l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭उ")][index][bstack1lll11111l_opy_])
    bstack11ll11lll_opy_ = update(bstack11ll11lll_opy_, bstack1ll1l1ll11_opy_)
  bstack1ll1llll11_opy_ = bstack1llll11ll_opy_(config, index)
  for bstack11lll11l_opy_ in bstack1l11l1l11l_opy_ + [bstack1ll11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩऊ"), bstack1ll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ऋ")] + list(bstack111l1l1l1_opy_.keys()):
    if bstack11lll11l_opy_ in bstack1ll1llll11_opy_:
      bstack11ll11lll_opy_[bstack11lll11l_opy_] = bstack1ll1llll11_opy_[bstack11lll11l_opy_]
      del (bstack1ll1llll11_opy_[bstack11lll11l_opy_])
  if bstack1l11lllll1_opy_(config):
    bstack1ll1llll11_opy_[bstack1ll11l_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ऌ")] = True
    caps.update(bstack11ll11lll_opy_)
    caps[bstack1ll11l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨऍ")] = bstack1ll1llll11_opy_
  else:
    bstack1ll1llll11_opy_[bstack1ll11l_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨऎ")] = False
    caps.update(bstack11l11l1l1_opy_(bstack1ll1llll11_opy_, bstack11ll11lll_opy_))
    if bstack1ll11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧए") in caps:
      caps[bstack1ll11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫऐ")] = caps[bstack1ll11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩऑ")]
      del (caps[bstack1ll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪऒ")])
    if bstack1ll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧओ") in caps:
      caps[bstack1ll11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩऔ")] = caps[bstack1ll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩक")]
      del (caps[bstack1ll11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪख")])
  return caps
def bstack1ll1l111_opy_():
  global bstack11l1ll1l_opy_
  if bstack1lll1l1ll_opy_() <= version.parse(bstack1ll11l_opy_ (u"ࠪ࠷࠳࠷࠳࠯࠲ࠪग")):
    if bstack11l1ll1l_opy_ != bstack1ll11l_opy_ (u"ࠫࠬघ"):
      return bstack1ll11l_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨङ") + bstack11l1ll1l_opy_ + bstack1ll11l_opy_ (u"ࠨ࠺࠹࠲࠲ࡻࡩ࠵ࡨࡶࡤࠥच")
    return bstack11111l111_opy_
  if bstack11l1ll1l_opy_ != bstack1ll11l_opy_ (u"ࠧࠨछ"):
    return bstack1ll11l_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࠥज") + bstack11l1ll1l_opy_ + bstack1ll11l_opy_ (u"ࠤ࠲ࡻࡩ࠵ࡨࡶࡤࠥझ")
  return bstack1ll1llll_opy_
def bstack11lll111_opy_(options):
  return hasattr(options, bstack1ll11l_opy_ (u"ࠪࡷࡪࡺ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶࡼࠫञ"))
def update(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = update(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack11llll1ll_opy_(options, bstack1ll11ll111_opy_):
  for bstack1l11l1ll1l_opy_ in bstack1ll11ll111_opy_:
    if bstack1l11l1ll1l_opy_ in [bstack1ll11l_opy_ (u"ࠫࡦࡸࡧࡴࠩट"), bstack1ll11l_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩठ")]:
      continue
    if bstack1l11l1ll1l_opy_ in options._experimental_options:
      options._experimental_options[bstack1l11l1ll1l_opy_] = update(options._experimental_options[bstack1l11l1ll1l_opy_],
                                                         bstack1ll11ll111_opy_[bstack1l11l1ll1l_opy_])
    else:
      options.add_experimental_option(bstack1l11l1ll1l_opy_, bstack1ll11ll111_opy_[bstack1l11l1ll1l_opy_])
  if bstack1ll11l_opy_ (u"࠭ࡡࡳࡩࡶࠫड") in bstack1ll11ll111_opy_:
    for arg in bstack1ll11ll111_opy_[bstack1ll11l_opy_ (u"ࠧࡢࡴࡪࡷࠬढ")]:
      options.add_argument(arg)
    del (bstack1ll11ll111_opy_[bstack1ll11l_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ण")])
  if bstack1ll11l_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭त") in bstack1ll11ll111_opy_:
    for ext in bstack1ll11ll111_opy_[bstack1ll11l_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧथ")]:
      options.add_extension(ext)
    del (bstack1ll11ll111_opy_[bstack1ll11l_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨद")])
def bstack1lll1lllll_opy_(options, bstack1lllll11_opy_):
  if bstack1ll11l_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫध") in bstack1lllll11_opy_:
    for bstack1l1l11ll_opy_ in bstack1lllll11_opy_[bstack1ll11l_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬन")]:
      if bstack1l1l11ll_opy_ in options._preferences:
        options._preferences[bstack1l1l11ll_opy_] = update(options._preferences[bstack1l1l11ll_opy_], bstack1lllll11_opy_[bstack1ll11l_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ऩ")][bstack1l1l11ll_opy_])
      else:
        options.set_preference(bstack1l1l11ll_opy_, bstack1lllll11_opy_[bstack1ll11l_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧप")][bstack1l1l11ll_opy_])
  if bstack1ll11l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧफ") in bstack1lllll11_opy_:
    for arg in bstack1lllll11_opy_[bstack1ll11l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨब")]:
      options.add_argument(arg)
def bstack1llll11ll1_opy_(options, bstack11ll11ll_opy_):
  if bstack1ll11l_opy_ (u"ࠫࡼ࡫ࡢࡷ࡫ࡨࡻࠬभ") in bstack11ll11ll_opy_:
    options.use_webview(bool(bstack11ll11ll_opy_[bstack1ll11l_opy_ (u"ࠬࡽࡥࡣࡸ࡬ࡩࡼ࠭म")]))
  bstack11llll1ll_opy_(options, bstack11ll11ll_opy_)
def bstack11l1l1l1l_opy_(options, bstack1l1ll1l1ll_opy_):
  for bstack11l1ll1l1_opy_ in bstack1l1ll1l1ll_opy_:
    if bstack11l1ll1l1_opy_ in [bstack1ll11l_opy_ (u"࠭ࡴࡦࡥ࡫ࡲࡴࡲ࡯ࡨࡻࡓࡶࡪࡼࡩࡦࡹࠪय"), bstack1ll11l_opy_ (u"ࠧࡢࡴࡪࡷࠬर")]:
      continue
    options.set_capability(bstack11l1ll1l1_opy_, bstack1l1ll1l1ll_opy_[bstack11l1ll1l1_opy_])
  if bstack1ll11l_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ऱ") in bstack1l1ll1l1ll_opy_:
    for arg in bstack1l1ll1l1ll_opy_[bstack1ll11l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧल")]:
      options.add_argument(arg)
  if bstack1ll11l_opy_ (u"ࠪࡸࡪࡩࡨ࡯ࡱ࡯ࡳ࡬ࡿࡐࡳࡧࡹ࡭ࡪࡽࠧळ") in bstack1l1ll1l1ll_opy_:
    options.bstack1l11111l_opy_(bool(bstack1l1ll1l1ll_opy_[bstack1ll11l_opy_ (u"ࠫࡹ࡫ࡣࡩࡰࡲࡰࡴ࡭ࡹࡑࡴࡨࡺ࡮࡫ࡷࠨऴ")]))
def bstack1ll11l1lll_opy_(options, bstack11111l11_opy_):
  for bstack1l1ll111l_opy_ in bstack11111l11_opy_:
    if bstack1l1ll111l_opy_ in [bstack1ll11l_opy_ (u"ࠬࡧࡤࡥ࡫ࡷ࡭ࡴࡴࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩव"), bstack1ll11l_opy_ (u"࠭ࡡࡳࡩࡶࠫश")]:
      continue
    options._options[bstack1l1ll111l_opy_] = bstack11111l11_opy_[bstack1l1ll111l_opy_]
  if bstack1ll11l_opy_ (u"ࠧࡢࡦࡧ࡭ࡹ࡯࡯࡯ࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫष") in bstack11111l11_opy_:
    for bstack1ll111111_opy_ in bstack11111l11_opy_[bstack1ll11l_opy_ (u"ࠨࡣࡧࡨ࡮ࡺࡩࡰࡰࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬस")]:
      options.bstack1lll1l11_opy_(
        bstack1ll111111_opy_, bstack11111l11_opy_[bstack1ll11l_opy_ (u"ࠩࡤࡨࡩ࡯ࡴࡪࡱࡱࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ह")][bstack1ll111111_opy_])
  if bstack1ll11l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨऺ") in bstack11111l11_opy_:
    for arg in bstack11111l11_opy_[bstack1ll11l_opy_ (u"ࠫࡦࡸࡧࡴࠩऻ")]:
      options.add_argument(arg)
def bstack11l1ll11_opy_(options, caps):
  if not hasattr(options, bstack1ll11l_opy_ (u"ࠬࡑࡅ़࡚ࠩ")):
    return
  if options.KEY == bstack1ll11l_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫऽ") and options.KEY in caps:
    bstack11llll1ll_opy_(options, caps[bstack1ll11l_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬा")])
  elif options.KEY == bstack1ll11l_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭ि") and options.KEY in caps:
    bstack1lll1lllll_opy_(options, caps[bstack1ll11l_opy_ (u"ࠩࡰࡳࡿࡀࡦࡪࡴࡨࡪࡴࡾࡏࡱࡶ࡬ࡳࡳࡹࠧी")])
  elif options.KEY == bstack1ll11l_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫࠱ࡳࡵࡺࡩࡰࡰࡶࠫु") and options.KEY in caps:
    bstack11l1l1l1l_opy_(options, caps[bstack1ll11l_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬࠲ࡴࡶࡴࡪࡱࡱࡷࠬू")])
  elif options.KEY == bstack1ll11l_opy_ (u"ࠬࡳࡳ࠻ࡧࡧ࡫ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ृ") and options.KEY in caps:
    bstack1llll11ll1_opy_(options, caps[bstack1ll11l_opy_ (u"࠭࡭ࡴ࠼ࡨࡨ࡬࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧॄ")])
  elif options.KEY == bstack1ll11l_opy_ (u"ࠧࡴࡧ࠽࡭ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ॅ") and options.KEY in caps:
    bstack1ll11l1lll_opy_(options, caps[bstack1ll11l_opy_ (u"ࠨࡵࡨ࠾࡮࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧॆ")])
def bstack1l11ll1lll_opy_(caps):
  global bstack111l11111_opy_
  if isinstance(os.environ.get(bstack1ll11l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪे")), str):
    bstack111l11111_opy_ = eval(os.getenv(bstack1ll11l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫै")))
  if bstack111l11111_opy_:
    if bstack1llllllll_opy_() < version.parse(bstack1ll11l_opy_ (u"ࠫ࠷࠴࠳࠯࠲ࠪॉ")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack1ll11l_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬॊ")
    if bstack1ll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫो") in caps:
      browser = caps[bstack1ll11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬौ")]
    elif bstack1ll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳ्ࠩ") in caps:
      browser = caps[bstack1ll11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪॎ")]
    browser = str(browser).lower()
    if browser == bstack1ll11l_opy_ (u"ࠪ࡭ࡵ࡮࡯࡯ࡧࠪॏ") or browser == bstack1ll11l_opy_ (u"ࠫ࡮ࡶࡡࡥࠩॐ"):
      browser = bstack1ll11l_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭ࠬ॑")
    if browser == bstack1ll11l_opy_ (u"࠭ࡳࡢ࡯ࡶࡹࡳ࡭॒ࠧ"):
      browser = bstack1ll11l_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧ॓")
    if browser not in [bstack1ll11l_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨ॔"), bstack1ll11l_opy_ (u"ࠩࡨࡨ࡬࡫ࠧॕ"), bstack1ll11l_opy_ (u"ࠪ࡭ࡪ࠭ॖ"), bstack1ll11l_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࠫॗ"), bstack1ll11l_opy_ (u"ࠬ࡬ࡩࡳࡧࡩࡳࡽ࠭क़")]:
      return None
    try:
      package = bstack1ll11l_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭࠯ࡹࡨࡦࡩࡸࡩࡷࡧࡵ࠲ࢀࢃ࠮ࡰࡲࡷ࡭ࡴࡴࡳࠨख़").format(browser)
      name = bstack1ll11l_opy_ (u"ࠧࡐࡲࡷ࡭ࡴࡴࡳࠨग़")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack11lll111_opy_(options):
        return None
      for bstack11lll11l_opy_ in caps.keys():
        options.set_capability(bstack11lll11l_opy_, caps[bstack11lll11l_opy_])
      bstack11l1ll11_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack11l11111_opy_(options, bstack1ll111l1l_opy_):
  if not bstack11lll111_opy_(options):
    return
  for bstack11lll11l_opy_ in bstack1ll111l1l_opy_.keys():
    if bstack11lll11l_opy_ in bstack1ll1llll1_opy_:
      continue
    if bstack11lll11l_opy_ in options._caps and type(options._caps[bstack11lll11l_opy_]) in [dict, list]:
      options._caps[bstack11lll11l_opy_] = update(options._caps[bstack11lll11l_opy_], bstack1ll111l1l_opy_[bstack11lll11l_opy_])
    else:
      options.set_capability(bstack11lll11l_opy_, bstack1ll111l1l_opy_[bstack11lll11l_opy_])
  bstack11l1ll11_opy_(options, bstack1ll111l1l_opy_)
  if bstack1ll11l_opy_ (u"ࠨ࡯ࡲࡾ࠿ࡪࡥࡣࡷࡪ࡫ࡪࡸࡁࡥࡦࡵࡩࡸࡹࠧज़") in options._caps:
    if options._caps[bstack1ll11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧड़")] and options._caps[bstack1ll11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨढ़")].lower() != bstack1ll11l_opy_ (u"ࠫ࡫࡯ࡲࡦࡨࡲࡼࠬफ़"):
      del options._caps[bstack1ll11l_opy_ (u"ࠬࡳ࡯ࡻ࠼ࡧࡩࡧࡻࡧࡨࡧࡵࡅࡩࡪࡲࡦࡵࡶࠫय़")]
def bstack1l1ll111l1_opy_(proxy_config):
  if bstack1ll11l_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪॠ") in proxy_config:
    proxy_config[bstack1ll11l_opy_ (u"ࠧࡴࡵ࡯ࡔࡷࡵࡸࡺࠩॡ")] = proxy_config[bstack1ll11l_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬॢ")]
    del (proxy_config[bstack1ll11l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ॣ")])
  if bstack1ll11l_opy_ (u"ࠪࡴࡷࡵࡸࡺࡖࡼࡴࡪ࠭।") in proxy_config and proxy_config[bstack1ll11l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡗࡽࡵ࡫ࠧ॥")].lower() != bstack1ll11l_opy_ (u"ࠬࡪࡩࡳࡧࡦࡸࠬ०"):
    proxy_config[bstack1ll11l_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡙ࡿࡰࡦࠩ१")] = bstack1ll11l_opy_ (u"ࠧ࡮ࡣࡱࡹࡦࡲࠧ२")
  if bstack1ll11l_opy_ (u"ࠨࡲࡵࡳࡽࡿࡁࡶࡶࡲࡧࡴࡴࡦࡪࡩࡘࡶࡱ࠭३") in proxy_config:
    proxy_config[bstack1ll11l_opy_ (u"ࠩࡳࡶࡴࡾࡹࡕࡻࡳࡩࠬ४")] = bstack1ll11l_opy_ (u"ࠪࡴࡦࡩࠧ५")
  return proxy_config
def bstack11l1l1ll1_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack1ll11l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࠪ६") in config:
    return proxy
  config[bstack1ll11l_opy_ (u"ࠬࡶࡲࡰࡺࡼࠫ७")] = bstack1l1ll111l1_opy_(config[bstack1ll11l_opy_ (u"࠭ࡰࡳࡱࡻࡽࠬ८")])
  if proxy == None:
    proxy = Proxy(config[bstack1ll11l_opy_ (u"ࠧࡱࡴࡲࡼࡾ࠭९")])
  return proxy
def bstack1l111llll_opy_(self):
  global CONFIG
  global bstack1l1l1ll111_opy_
  try:
    proxy = bstack1l1ll1l1l1_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack1ll11l_opy_ (u"ࠨ࠰ࡳࡥࡨ࠭॰")):
        proxies = bstack1lll1l1lll_opy_(proxy, bstack1ll1l111_opy_())
        if len(proxies) > 0:
          protocol, bstack1llll11lll_opy_ = proxies.popitem()
          if bstack1ll11l_opy_ (u"ࠤ࠽࠳࠴ࠨॱ") in bstack1llll11lll_opy_:
            return bstack1llll11lll_opy_
          else:
            return bstack1ll11l_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦॲ") + bstack1llll11lll_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack1ll11l_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡱࡴࡲࡼࡾࠦࡵࡳ࡮ࠣ࠾ࠥࢁࡽࠣॳ").format(str(e)))
  return bstack1l1l1ll111_opy_(self)
def bstack1l1l11l1_opy_():
  global CONFIG
  return bstack1l1l1ll1ll_opy_(CONFIG) and bstack1llll1l1ll_opy_() and bstack1lll1l1ll_opy_() >= version.parse(bstack1ll1l1lll_opy_)
def bstack1lll1ll11l_opy_():
  global CONFIG
  return (bstack1ll11l_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨॴ") in CONFIG or bstack1ll11l_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪॵ") in CONFIG) and bstack1lll1lll11_opy_()
def bstack11l111lll_opy_(config):
  bstack1ll1111l1_opy_ = {}
  if bstack1ll11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫॶ") in config:
    bstack1ll1111l1_opy_ = config[bstack1ll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬॷ")]
  if bstack1ll11l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨॸ") in config:
    bstack1ll1111l1_opy_ = config[bstack1ll11l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩॹ")]
  proxy = bstack1l1ll1l1l1_opy_(config)
  if proxy:
    if proxy.endswith(bstack1ll11l_opy_ (u"ࠫ࠳ࡶࡡࡤࠩॺ")) and os.path.isfile(proxy):
      bstack1ll1111l1_opy_[bstack1ll11l_opy_ (u"ࠬ࠳ࡰࡢࡥ࠰ࡪ࡮ࡲࡥࠨॻ")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack1ll11l_opy_ (u"࠭࠮ࡱࡣࡦࠫॼ")):
        proxies = bstack1lllll11l1_opy_(config, bstack1ll1l111_opy_())
        if len(proxies) > 0:
          protocol, bstack1llll11lll_opy_ = proxies.popitem()
          if bstack1ll11l_opy_ (u"ࠢ࠻࠱࠲ࠦॽ") in bstack1llll11lll_opy_:
            parsed_url = urlparse(bstack1llll11lll_opy_)
          else:
            parsed_url = urlparse(protocol + bstack1ll11l_opy_ (u"ࠣ࠼࠲࠳ࠧॾ") + bstack1llll11lll_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack1ll1111l1_opy_[bstack1ll11l_opy_ (u"ࠩࡳࡶࡴࡾࡹࡉࡱࡶࡸࠬॿ")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack1ll1111l1_opy_[bstack1ll11l_opy_ (u"ࠪࡴࡷࡵࡸࡺࡒࡲࡶࡹ࠭ঀ")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack1ll1111l1_opy_[bstack1ll11l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡘࡷࡪࡸࠧঁ")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack1ll1111l1_opy_[bstack1ll11l_opy_ (u"ࠬࡶࡲࡰࡺࡼࡔࡦࡹࡳࠨং")] = str(parsed_url.password)
  return bstack1ll1111l1_opy_
def bstack1l1l1111ll_opy_(config):
  if bstack1ll11l_opy_ (u"࠭ࡴࡦࡵࡷࡇࡴࡴࡴࡦࡺࡷࡓࡵࡺࡩࡰࡰࡶࠫঃ") in config:
    return config[bstack1ll11l_opy_ (u"ࠧࡵࡧࡶࡸࡈࡵ࡮ࡵࡧࡻࡸࡔࡶࡴࡪࡱࡱࡷࠬ঄")]
  return {}
def bstack1l111l11l_opy_(caps):
  global bstack111l1l1l_opy_
  if bstack1ll11l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩঅ") in caps:
    caps[bstack1ll11l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪআ")][bstack1ll11l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࠩই")] = True
    if bstack111l1l1l_opy_:
      caps[bstack1ll11l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬঈ")][bstack1ll11l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧউ")] = bstack111l1l1l_opy_
  else:
    caps[bstack1ll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࠫঊ")] = True
    if bstack111l1l1l_opy_:
      caps[bstack1ll11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨঋ")] = bstack111l1l1l_opy_
def bstack1111lll1_opy_():
  global CONFIG
  if bstack1ll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬঌ") in CONFIG and bstack1l11111l1_opy_(CONFIG[bstack1ll11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭঍")]):
    bstack1ll1111l1_opy_ = bstack11l111lll_opy_(CONFIG)
    bstack1l11llll1_opy_(CONFIG[bstack1ll11l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭঎")], bstack1ll1111l1_opy_)
def bstack1l11llll1_opy_(key, bstack1ll1111l1_opy_):
  global bstack1111111ll_opy_
  logger.info(bstack1l11lll1l1_opy_)
  try:
    bstack1111111ll_opy_ = Local()
    bstack1llll11l1l_opy_ = {bstack1ll11l_opy_ (u"ࠫࡰ࡫ࡹࠨএ"): key}
    bstack1llll11l1l_opy_.update(bstack1ll1111l1_opy_)
    logger.debug(bstack111ll1l1l_opy_.format(str(bstack1llll11l1l_opy_)))
    bstack1111111ll_opy_.start(**bstack1llll11l1l_opy_)
    if bstack1111111ll_opy_.isRunning():
      logger.info(bstack1ll1l1ll_opy_)
  except Exception as e:
    bstack11l11l1l_opy_(bstack11l1l11l_opy_.format(str(e)))
def bstack11l111ll_opy_():
  global bstack1111111ll_opy_
  if bstack1111111ll_opy_.isRunning():
    logger.info(bstack1l1lll1l1l_opy_)
    bstack1111111ll_opy_.stop()
  bstack1111111ll_opy_ = None
def bstack1l111lll_opy_(bstack1l11l1lll1_opy_=[]):
  global CONFIG
  bstack111llll11_opy_ = []
  bstack11l1l11ll_opy_ = [bstack1ll11l_opy_ (u"ࠬࡵࡳࠨঐ"), bstack1ll11l_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩ঑"), bstack1ll11l_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫ঒"), bstack1ll11l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪও"), bstack1ll11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧঔ"), bstack1ll11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫক")]
  try:
    for err in bstack1l11l1lll1_opy_:
      bstack1ll1l111l1_opy_ = {}
      for k in bstack11l1l11ll_opy_:
        val = CONFIG[bstack1ll11l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧখ")][int(err[bstack1ll11l_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫগ")])].get(k)
        if val:
          bstack1ll1l111l1_opy_[k] = val
      if(err[bstack1ll11l_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬঘ")] != bstack1ll11l_opy_ (u"ࠧࠨঙ")):
        bstack1ll1l111l1_opy_[bstack1ll11l_opy_ (u"ࠨࡶࡨࡷࡹࡹࠧচ")] = {
          err[bstack1ll11l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧছ")]: err[bstack1ll11l_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩজ")]
        }
        bstack111llll11_opy_.append(bstack1ll1l111l1_opy_)
  except Exception as e:
    logger.debug(bstack1ll11l_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡦࡰࡴࡰࡥࡹࡺࡩ࡯ࡩࠣࡨࡦࡺࡡࠡࡨࡲࡶࠥ࡫ࡶࡦࡰࡷ࠾ࠥ࠭ঝ") + str(e))
  finally:
    return bstack111llll11_opy_
def bstack1lll1111l1_opy_(file_name):
  bstack1ll111l1_opy_ = []
  try:
    bstack1ll1lll1_opy_ = os.path.join(tempfile.gettempdir(), file_name)
    if os.path.exists(bstack1ll1lll1_opy_):
      with open(bstack1ll1lll1_opy_) as f:
        bstack1ll1l1l1l_opy_ = json.load(f)
        bstack1ll111l1_opy_ = bstack1ll1l1l1l_opy_
      os.remove(bstack1ll1lll1_opy_)
    return bstack1ll111l1_opy_
  except Exception as e:
    logger.debug(bstack1ll11l_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡧ࡫ࡱࡨ࡮ࡴࡧࠡࡧࡵࡶࡴࡸࠠ࡭࡫ࡶࡸ࠿ࠦࠧঞ") + str(e))
def bstack1l1l111lll_opy_():
  global bstack1lll1l1l_opy_
  global bstack1l11l1l111_opy_
  global bstack1l1llll1ll_opy_
  global bstack1l1l111l11_opy_
  global bstack1ll1111ll_opy_
  global bstack1l111l11_opy_
  global CONFIG
  percy.shutdown()
  bstack11lllll1l_opy_ = os.environ.get(bstack1ll11l_opy_ (u"࠭ࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࡡࡘࡗࡊࡊࠧট"))
  if bstack11lllll1l_opy_ in [bstack1ll11l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ঠ"), bstack1ll11l_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧড")]:
    bstack1ll1ll111l_opy_()
  if bstack1lll1l1l_opy_:
    logger.warning(bstack1111l111l_opy_.format(str(bstack1lll1l1l_opy_)))
  else:
    try:
      bstack1lll1lll1_opy_ = bstack1ll1ll11ll_opy_(bstack1ll11l_opy_ (u"ࠩ࠱ࡦࡸࡺࡡࡤ࡭࠰ࡧࡴࡴࡦࡪࡩ࠱࡮ࡸࡵ࡮ࠨঢ"), logger)
      if bstack1lll1lll1_opy_.get(bstack1ll11l_opy_ (u"ࠪࡲࡺࡪࡧࡦࡡ࡯ࡳࡨࡧ࡬ࠨণ")) and bstack1lll1lll1_opy_.get(bstack1ll11l_opy_ (u"ࠫࡳࡻࡤࡨࡧࡢࡰࡴࡩࡡ࡭ࠩত")).get(bstack1ll11l_opy_ (u"ࠬ࡮࡯ࡴࡶࡱࡥࡲ࡫ࠧথ")):
        logger.warning(bstack1111l111l_opy_.format(str(bstack1lll1lll1_opy_[bstack1ll11l_opy_ (u"࠭࡮ࡶࡦࡪࡩࡤࡲ࡯ࡤࡣ࡯ࠫদ")][bstack1ll11l_opy_ (u"ࠧࡩࡱࡶࡸࡳࡧ࡭ࡦࠩধ")])))
    except Exception as e:
      logger.error(e)
  logger.info(bstack1lll1llll1_opy_)
  global bstack1111111ll_opy_
  if bstack1111111ll_opy_:
    bstack11l111ll_opy_()
  try:
    for driver in bstack1l11l1l111_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack1l11l11l1_opy_)
  if bstack1l111l11_opy_ == bstack1ll11l_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧন"):
    bstack1ll1111ll_opy_ = bstack1lll1111l1_opy_(bstack1ll11l_opy_ (u"ࠩࡵࡳࡧࡵࡴࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰࠪ঩"))
  if bstack1l111l11_opy_ == bstack1ll11l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪপ") and len(bstack1l1l111l11_opy_) == 0:
    bstack1l1l111l11_opy_ = bstack1lll1111l1_opy_(bstack1ll11l_opy_ (u"ࠫࡵࡽ࡟ࡱࡻࡷࡩࡸࡺ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷ࠲࡯ࡹ࡯࡯ࠩফ"))
    if len(bstack1l1l111l11_opy_) == 0:
      bstack1l1l111l11_opy_ = bstack1lll1111l1_opy_(bstack1ll11l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡤࡶࡰࡱࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠴ࡪࡴࡱࡱࠫব"))
  bstack1l1ll1111l_opy_ = bstack1ll11l_opy_ (u"࠭ࠧভ")
  if len(bstack1l1llll1ll_opy_) > 0:
    bstack1l1ll1111l_opy_ = bstack1l111lll_opy_(bstack1l1llll1ll_opy_)
  elif len(bstack1l1l111l11_opy_) > 0:
    bstack1l1ll1111l_opy_ = bstack1l111lll_opy_(bstack1l1l111l11_opy_)
  elif len(bstack1ll1111ll_opy_) > 0:
    bstack1l1ll1111l_opy_ = bstack1l111lll_opy_(bstack1ll1111ll_opy_)
  elif len(bstack1ll11l1l1_opy_) > 0:
    bstack1l1ll1111l_opy_ = bstack1l111lll_opy_(bstack1ll11l1l1_opy_)
  if bool(bstack1l1ll1111l_opy_):
    bstack111l11lll_opy_(bstack1l1ll1111l_opy_)
  else:
    bstack111l11lll_opy_()
  bstack1l1l1llll1_opy_(bstack1l1ll1l111_opy_, logger)
  bstack1llll1lll1_opy_.bstack1llll1ll11_opy_(CONFIG)
  if len(bstack1ll1111ll_opy_) > 0:
    sys.exit(len(bstack1ll1111ll_opy_))
def bstack1l1l11lll_opy_(self, *args):
  logger.error(bstack1111l11l_opy_)
  bstack1l1l111lll_opy_()
  sys.exit(1)
def bstack11l11l1l_opy_(err):
  logger.critical(bstack1lll1l1l1_opy_.format(str(err)))
  bstack111l11lll_opy_(bstack1lll1l1l1_opy_.format(str(err)), True)
  atexit.unregister(bstack1l1l111lll_opy_)
  bstack1ll1ll111l_opy_()
  sys.exit(1)
def bstack1ll1ll111_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack111l11lll_opy_(message, True)
  atexit.unregister(bstack1l1l111lll_opy_)
  bstack1ll1ll111l_opy_()
  sys.exit(1)
def bstack1l1lll1l1_opy_():
  global CONFIG
  global bstack11ll1l1l_opy_
  global bstack1l1ll1l1_opy_
  global bstack1ll1l11l1_opy_
  CONFIG = bstack1lll11ll1l_opy_()
  load_dotenv(CONFIG.get(bstack1ll11l_opy_ (u"ࠧࡦࡰࡹࡊ࡮ࡲࡥࠨম")))
  bstack1l1l11ll11_opy_()
  bstack1l11ll1l1_opy_()
  CONFIG = bstack11ll11111_opy_(CONFIG)
  update(CONFIG, bstack1l1ll1l1_opy_)
  update(CONFIG, bstack11ll1l1l_opy_)
  CONFIG = bstack1ll1l1111l_opy_(CONFIG)
  bstack1ll1l11l1_opy_ = bstack11ll1l11_opy_(CONFIG)
  bstack1l11l111l_opy_.bstack1l11ll11l_opy_(bstack1ll11l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩয"), bstack1ll1l11l1_opy_)
  if (bstack1ll11l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬর") in CONFIG and bstack1ll11l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭঱") in bstack11ll1l1l_opy_) or (
          bstack1ll11l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧল") in CONFIG and bstack1ll11l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ঳") not in bstack1l1ll1l1_opy_):
    if os.getenv(bstack1ll11l_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡃࡐࡏࡅࡍࡓࡋࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪ঴")):
      CONFIG[bstack1ll11l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ঵")] = os.getenv(bstack1ll11l_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡠࡅࡒࡑࡇࡏࡎࡆࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠬশ"))
    else:
      bstack1lll11ll1_opy_()
  elif (bstack1ll11l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬষ") not in CONFIG and bstack1ll11l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬস") in CONFIG) or (
          bstack1ll11l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧহ") in bstack1l1ll1l1_opy_ and bstack1ll11l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ঺") not in bstack11ll1l1l_opy_):
    del (CONFIG[bstack1ll11l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ঻")])
  if bstack11111lll1_opy_(CONFIG):
    bstack11l11l1l_opy_(bstack1ll11111_opy_)
  bstack1ll11ll1_opy_()
  bstack1l11l11l_opy_()
  if bstack111l11111_opy_:
    CONFIG[bstack1ll11l_opy_ (u"ࠧࡢࡲࡳ়ࠫ")] = bstack1l111l1ll_opy_(CONFIG)
    logger.info(bstack11llll1l1_opy_.format(CONFIG[bstack1ll11l_opy_ (u"ࠨࡣࡳࡴࠬঽ")]))
  if not bstack1ll1l11l1_opy_:
    CONFIG[bstack1ll11l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬা")] = [{}]
def bstack1ll1111ll1_opy_(config, bstack1lll1ll1_opy_):
  global CONFIG
  global bstack111l11111_opy_
  CONFIG = config
  bstack111l11111_opy_ = bstack1lll1ll1_opy_
def bstack1l11l11l_opy_():
  global CONFIG
  global bstack111l11111_opy_
  if bstack1ll11l_opy_ (u"ࠪࡥࡵࡶࠧি") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack1ll1ll111_opy_(e, bstack1l111l111_opy_)
    bstack111l11111_opy_ = True
    bstack1l11l111l_opy_.bstack1l11ll11l_opy_(bstack1ll11l_opy_ (u"ࠫࡦࡶࡰࡠࡣࡸࡸࡴࡳࡡࡵࡧࠪী"), True)
def bstack1l111l1ll_opy_(config):
  bstack1l1l111ll1_opy_ = bstack1ll11l_opy_ (u"ࠬ࠭ু")
  app = config[bstack1ll11l_opy_ (u"࠭ࡡࡱࡲࠪূ")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack1ll111ll1_opy_:
      if os.path.exists(app):
        bstack1l1l111ll1_opy_ = bstack11l1lll11_opy_(config, app)
      elif bstack1ll1ll1l1l_opy_(app):
        bstack1l1l111ll1_opy_ = app
      else:
        bstack11l11l1l_opy_(bstack11l1l111l_opy_.format(app))
    else:
      if bstack1ll1ll1l1l_opy_(app):
        bstack1l1l111ll1_opy_ = app
      elif os.path.exists(app):
        bstack1l1l111ll1_opy_ = bstack11l1lll11_opy_(app)
      else:
        bstack11l11l1l_opy_(bstack1l11ll11ll_opy_)
  else:
    if len(app) > 2:
      bstack11l11l1l_opy_(bstack1lllll1111_opy_)
    elif len(app) == 2:
      if bstack1ll11l_opy_ (u"ࠧࡱࡣࡷ࡬ࠬৃ") in app and bstack1ll11l_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡠ࡫ࡧࠫৄ") in app:
        if os.path.exists(app[bstack1ll11l_opy_ (u"ࠩࡳࡥࡹ࡮ࠧ৅")]):
          bstack1l1l111ll1_opy_ = bstack11l1lll11_opy_(config, app[bstack1ll11l_opy_ (u"ࠪࡴࡦࡺࡨࠨ৆")], app[bstack1ll11l_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡣ࡮ࡪࠧে")])
        else:
          bstack11l11l1l_opy_(bstack11l1l111l_opy_.format(app))
      else:
        bstack11l11l1l_opy_(bstack1lllll1111_opy_)
    else:
      for key in app:
        if key in bstack1lll1ll11_opy_:
          if key == bstack1ll11l_opy_ (u"ࠬࡶࡡࡵࡪࠪৈ"):
            if os.path.exists(app[key]):
              bstack1l1l111ll1_opy_ = bstack11l1lll11_opy_(config, app[key])
            else:
              bstack11l11l1l_opy_(bstack11l1l111l_opy_.format(app))
          else:
            bstack1l1l111ll1_opy_ = app[key]
        else:
          bstack11l11l1l_opy_(bstack1111lll1l_opy_)
  return bstack1l1l111ll1_opy_
def bstack1ll1ll1l1l_opy_(bstack1l1l111ll1_opy_):
  import re
  bstack11l1l1l11_opy_ = re.compile(bstack1ll11l_opy_ (u"ࡸࠢ࡟࡝ࡤ࠱ࡿࡇ࡛࠭࠲࠰࠽ࡡࡥ࠮࡝࠯ࡠ࠮ࠩࠨ৉"))
  bstack1l11l111_opy_ = re.compile(bstack1ll11l_opy_ (u"ࡲࠣࡠ࡞ࡥ࠲ࢀࡁ࠮࡜࠳࠱࠾ࡢ࡟࠯࡞࠰ࡡ࠯࠵࡛ࡢ࠯ࡽࡅ࠲ࡠ࠰࠮࠻࡟ࡣ࠳ࡢ࠭࡞ࠬࠧࠦ৊"))
  if bstack1ll11l_opy_ (u"ࠨࡤࡶ࠾࠴࠵ࠧো") in bstack1l1l111ll1_opy_ or re.fullmatch(bstack11l1l1l11_opy_, bstack1l1l111ll1_opy_) or re.fullmatch(bstack1l11l111_opy_, bstack1l1l111ll1_opy_):
    return True
  else:
    return False
def bstack11l1lll11_opy_(config, path, bstack1l1lll1lll_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack1ll11l_opy_ (u"ࠩࡵࡦࠬৌ")).read()).hexdigest()
  bstack1ll11llll_opy_ = bstack1llll11l1_opy_(md5_hash)
  bstack1l1l111ll1_opy_ = None
  if bstack1ll11llll_opy_:
    logger.info(bstack1l1l11111_opy_.format(bstack1ll11llll_opy_, md5_hash))
    return bstack1ll11llll_opy_
  bstack1ll1ll1l_opy_ = MultipartEncoder(
    fields={
      bstack1ll11l_opy_ (u"ࠪࡪ࡮ࡲࡥࠨ্"): (os.path.basename(path), open(os.path.abspath(path), bstack1ll11l_opy_ (u"ࠫࡷࡨࠧৎ")), bstack1ll11l_opy_ (u"ࠬࡺࡥࡹࡶ࠲ࡴࡱࡧࡩ࡯ࠩ৏")),
      bstack1ll11l_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡥࡩࡥࠩ৐"): bstack1l1lll1lll_opy_
    }
  )
  response = requests.post(bstack11lllllll_opy_, data=bstack1ll1ll1l_opy_,
                           headers={bstack1ll11l_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭৑"): bstack1ll1ll1l_opy_.content_type},
                           auth=(config[bstack1ll11l_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ৒")], config[bstack1ll11l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ৓")]))
  try:
    res = json.loads(response.text)
    bstack1l1l111ll1_opy_ = res[bstack1ll11l_opy_ (u"ࠪࡥࡵࡶ࡟ࡶࡴ࡯ࠫ৔")]
    logger.info(bstack111lll1ll_opy_.format(bstack1l1l111ll1_opy_))
    bstack11ll1ll1l_opy_(md5_hash, bstack1l1l111ll1_opy_)
  except ValueError as err:
    bstack11l11l1l_opy_(bstack1llll11l_opy_.format(str(err)))
  return bstack1l1l111ll1_opy_
def bstack1ll11ll1_opy_():
  global CONFIG
  global bstack1ll111l11l_opy_
  bstack1l111ll1l_opy_ = 0
  bstack1l1l1ll11_opy_ = 1
  if bstack1ll11l_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫ৕") in CONFIG:
    bstack1l1l1ll11_opy_ = CONFIG[bstack1ll11l_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ৖")]
  if bstack1ll11l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩৗ") in CONFIG:
    bstack1l111ll1l_opy_ = len(CONFIG[bstack1ll11l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ৘")])
  bstack1ll111l11l_opy_ = int(bstack1l1l1ll11_opy_) * int(bstack1l111ll1l_opy_)
def bstack1llll11l1_opy_(md5_hash):
  bstack11ll1lll1_opy_ = os.path.join(os.path.expanduser(bstack1ll11l_opy_ (u"ࠨࢀࠪ৙")), bstack1ll11l_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ৚"), bstack1ll11l_opy_ (u"ࠪࡥࡵࡶࡕࡱ࡮ࡲࡥࡩࡓࡄ࠶ࡊࡤࡷ࡭࠴ࡪࡴࡱࡱࠫ৛"))
  if os.path.exists(bstack11ll1lll1_opy_):
    bstack1l111ll11_opy_ = json.load(open(bstack11ll1lll1_opy_, bstack1ll11l_opy_ (u"ࠫࡷࡨࠧড়")))
    if md5_hash in bstack1l111ll11_opy_:
      bstack1ll1ll1ll1_opy_ = bstack1l111ll11_opy_[md5_hash]
      bstack1l1l1l1l_opy_ = datetime.datetime.now()
      bstack111lllll1_opy_ = datetime.datetime.strptime(bstack1ll1ll1ll1_opy_[bstack1ll11l_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨঢ়")], bstack1ll11l_opy_ (u"࠭ࠥࡥ࠱ࠨࡱ࠴࡙ࠫࠡࠧࡋ࠾ࠪࡓ࠺ࠦࡕࠪ৞"))
      if (bstack1l1l1l1l_opy_ - bstack111lllll1_opy_).days > 30:
        return None
      elif version.parse(str(__version__)) > version.parse(bstack1ll1ll1ll1_opy_[bstack1ll11l_opy_ (u"ࠧࡴࡦ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬয়")]):
        return None
      return bstack1ll1ll1ll1_opy_[bstack1ll11l_opy_ (u"ࠨ࡫ࡧࠫৠ")]
  else:
    return None
def bstack11ll1ll1l_opy_(md5_hash, bstack1l1l111ll1_opy_):
  bstack111ll1111_opy_ = os.path.join(os.path.expanduser(bstack1ll11l_opy_ (u"ࠩࢁࠫৡ")), bstack1ll11l_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪৢ"))
  if not os.path.exists(bstack111ll1111_opy_):
    os.makedirs(bstack111ll1111_opy_)
  bstack11ll1lll1_opy_ = os.path.join(os.path.expanduser(bstack1ll11l_opy_ (u"ࠫࢃ࠭ৣ")), bstack1ll11l_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ৤"), bstack1ll11l_opy_ (u"࠭ࡡࡱࡲࡘࡴࡱࡵࡡࡥࡏࡇ࠹ࡍࡧࡳࡩ࠰࡭ࡷࡴࡴࠧ৥"))
  bstack11111111_opy_ = {
    bstack1ll11l_opy_ (u"ࠧࡪࡦࠪ০"): bstack1l1l111ll1_opy_,
    bstack1ll11l_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ১"): datetime.datetime.strftime(datetime.datetime.now(), bstack1ll11l_opy_ (u"ࠩࠨࡨ࠴ࠫ࡭࠰ࠧ࡜ࠤࠪࡎ࠺ࠦࡏ࠽ࠩࡘ࠭২")),
    bstack1ll11l_opy_ (u"ࠪࡷࡩࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ৩"): str(__version__)
  }
  if os.path.exists(bstack11ll1lll1_opy_):
    bstack1l111ll11_opy_ = json.load(open(bstack11ll1lll1_opy_, bstack1ll11l_opy_ (u"ࠫࡷࡨࠧ৪")))
  else:
    bstack1l111ll11_opy_ = {}
  bstack1l111ll11_opy_[md5_hash] = bstack11111111_opy_
  with open(bstack11ll1lll1_opy_, bstack1ll11l_opy_ (u"ࠧࡽࠫࠣ৫")) as outfile:
    json.dump(bstack1l111ll11_opy_, outfile)
def bstack1l1llll1l1_opy_(self):
  return
def bstack11lllll11_opy_(self):
  return
def bstack1ll1lll1l_opy_(self):
  global bstack1l11l1l1l1_opy_
  bstack1l11l1l1l1_opy_(self)
def bstack1llll1111l_opy_():
  global bstack1ll11l1ll1_opy_
  bstack1ll11l1ll1_opy_ = True
def bstack111ll11l1_opy_(self):
  global bstack11ll11ll1_opy_
  global bstack1lll11111_opy_
  global bstack11l1111ll_opy_
  try:
    if bstack1ll11l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭৬") in bstack11ll11ll1_opy_ and self.session_id != None and bstack1l1l111l1l_opy_(threading.current_thread(), bstack1ll11l_opy_ (u"ࠧࡵࡧࡶࡸࡘࡺࡡࡵࡷࡶࠫ৭"), bstack1ll11l_opy_ (u"ࠨࠩ৮")) != bstack1ll11l_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ৯"):
      bstack111lll11_opy_ = bstack1ll11l_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪৰ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1ll11l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫৱ")
      if bstack111lll11_opy_ == bstack1ll11l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ৲"):
        bstack1l1l11l11l_opy_(logger)
      if self != None:
        bstack1111ll11_opy_(self, bstack111lll11_opy_, bstack1ll11l_opy_ (u"࠭ࠬࠡࠩ৳").join(threading.current_thread().bstackTestErrorMessages))
    threading.current_thread().testStatus = bstack1ll11l_opy_ (u"ࠧࠨ৴")
    if bstack1ll11l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ৵") in bstack11ll11ll1_opy_ and getattr(threading.current_thread(), bstack1ll11l_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ৶"), None):
      bstack1l1l1l1l11_opy_.bstack11ll1lll_opy_(self, bstack1lll1l1l11_opy_, logger, wait=True)
  except Exception as e:
    logger.debug(bstack1ll11l_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡ࡯ࡤࡶࡰ࡯࡮ࡨࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࠦ৷") + str(e))
  bstack11l1111ll_opy_(self)
  self.session_id = None
def bstack1ll1lllll_opy_(self, command_executor=bstack1ll11l_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳࠶࠸࠷࠯࠲࠱࠴࠳࠷࠺࠵࠶࠷࠸ࠧ৸"), *args, **kwargs):
  bstack1l1l1lll_opy_ = bstack1ll1l11ll_opy_(self, command_executor, *args, **kwargs)
  try:
    logger.debug(bstack1ll11l_opy_ (u"ࠬࡉ࡯࡮࡯ࡤࡲࡩࠦࡅࡹࡧࡦࡹࡹࡵࡲࠡࡹ࡫ࡩࡳࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢ࡬ࡷࠥ࡬ࡡ࡭ࡵࡨࠤ࠲ࠦࡻࡾࠩ৹").format(str(command_executor)))
    logger.debug(bstack1ll11l_opy_ (u"࠭ࡈࡶࡤ࡙ࠣࡗࡒࠠࡪࡵࠣ࠱ࠥࢁࡽࠨ৺").format(str(command_executor._url)))
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    if isinstance(command_executor, RemoteConnection) and bstack1ll11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪ৻") in command_executor._url:
      bstack1l11l111l_opy_.bstack1l11ll11l_opy_(bstack1ll11l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩৼ"), True)
  except:
    pass
  if (isinstance(command_executor, str) and bstack1ll11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬ৽") in command_executor):
    bstack1l11l111l_opy_.bstack1l11ll11l_opy_(bstack1ll11l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࠫ৾"), True)
  threading.current_thread().bstackSessionDriver = self
  bstack1l111lll1_opy_.bstack1ll111lll_opy_(self)
  return bstack1l1l1lll_opy_
def bstack1ll1l1ll1l_opy_(args):
  return bstack1ll11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠬ৿") in str(args)
def bstack1lll111l1_opy_(self, driver_command, *args, **kwargs):
  global bstack111111l1l_opy_
  global bstack11ll11l1l_opy_
  bstack1l11l1l1_opy_ = bstack1l1l111l1l_opy_(threading.current_thread(), bstack1ll11l_opy_ (u"ࠬ࡯ࡳࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩ਀"), None) and bstack1l1l111l1l_opy_(
          threading.current_thread(), bstack1ll11l_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬਁ"), None)
  bstack111l11l11_opy_ = getattr(self, bstack1ll11l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࡗ࡭ࡵࡵ࡭ࡦࡖࡧࡦࡴࠧਂ"), None) != None and getattr(self, bstack1ll11l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨਃ"), None) == True
  if not bstack11ll11l1l_opy_ and bstack1ll1l11l1_opy_ and bstack1ll11l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ਄") in CONFIG and CONFIG[bstack1ll11l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪਅ")] == True and bstack1111l1l1_opy_.bstack1llll1l11_opy_(driver_command) and (bstack111l11l11_opy_ or bstack1l11l1l1_opy_) and not bstack1ll1l1ll1l_opy_(args):
    try:
      bstack11ll11l1l_opy_ = True
      logger.debug(bstack1ll11l_opy_ (u"ࠫࡕ࡫ࡲࡧࡱࡵࡱ࡮ࡴࡧࠡࡵࡦࡥࡳࠦࡦࡰࡴࠣࡿࢂ࠭ਆ").format(driver_command))
      logger.debug(perform_scan(self, driver_command=driver_command))
    except Exception as err:
      logger.debug(bstack1ll11l_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡨࡶ࡫ࡵࡲ࡮ࠢࡶࡧࡦࡴࠠࡼࡿࠪਇ").format(str(err)))
    bstack11ll11l1l_opy_ = False
  response = bstack111111l1l_opy_(self, driver_command, *args, **kwargs)
  if bstack1ll11l_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬਈ") in str(bstack11ll11ll1_opy_).lower() and bstack1l111lll1_opy_.on():
    try:
      if driver_command == bstack1ll11l_opy_ (u"ࠧࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠫਉ"):
        bstack1l111lll1_opy_.bstack1l11llll_opy_({
            bstack1ll11l_opy_ (u"ࠨ࡫ࡰࡥ࡬࡫ࠧਊ"): response[bstack1ll11l_opy_ (u"ࠩࡹࡥࡱࡻࡥࠨ਋")],
            bstack1ll11l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ਌"): bstack1l111lll1_opy_.current_test_uuid() if bstack1l111lll1_opy_.current_test_uuid() else bstack1l111lll1_opy_.current_hook_uuid()
        })
    except:
      pass
  return response
def bstack11lll1lll_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
  global CONFIG
  global bstack1lll11111_opy_
  global bstack11l111l11_opy_
  global bstack1l11ll1l_opy_
  global bstack11l111111_opy_
  global bstack1lll1ll111_opy_
  global bstack11ll11ll1_opy_
  global bstack1ll1l11ll_opy_
  global bstack1l11l1l111_opy_
  global bstack111ll1ll1_opy_
  global bstack1lll1l1l11_opy_
  CONFIG[bstack1ll11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭਍")] = str(bstack11ll11ll1_opy_) + str(__version__)
  command_executor = bstack1ll1l111_opy_()
  logger.debug(bstack1l1l1l11ll_opy_.format(command_executor))
  proxy = bstack11l1l1ll1_opy_(CONFIG, proxy)
  bstack1lllll11ll_opy_ = 0 if bstack11l111l11_opy_ < 0 else bstack11l111l11_opy_
  try:
    if bstack11l111111_opy_ is True:
      bstack1lllll11ll_opy_ = int(multiprocessing.current_process().name)
    elif bstack1lll1ll111_opy_ is True:
      bstack1lllll11ll_opy_ = int(threading.current_thread().name)
  except:
    bstack1lllll11ll_opy_ = 0
  bstack1ll111l1l_opy_ = bstack1lll1111ll_opy_(CONFIG, bstack1lllll11ll_opy_)
  logger.debug(bstack111ll111l_opy_.format(str(bstack1ll111l1l_opy_)))
  if bstack1ll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ਎") in CONFIG and bstack1l11111l1_opy_(CONFIG[bstack1ll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪਏ")]):
    bstack1l111l11l_opy_(bstack1ll111l1l_opy_)
  if bstack1ll1lll1ll_opy_.bstack11llllll_opy_(CONFIG, bstack1lllll11ll_opy_) and bstack1ll1lll1ll_opy_.bstack1ll1l1l1l1_opy_(bstack1ll111l1l_opy_, options):
    threading.current_thread().a11yPlatform = True
    bstack1ll1lll1ll_opy_.set_capabilities(bstack1ll111l1l_opy_, CONFIG)
  if desired_capabilities:
    bstack11lllll1_opy_ = bstack11ll11111_opy_(desired_capabilities)
    bstack11lllll1_opy_[bstack1ll11l_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧਐ")] = bstack1l11lllll1_opy_(CONFIG)
    bstack11111l11l_opy_ = bstack1lll1111ll_opy_(bstack11lllll1_opy_)
    if bstack11111l11l_opy_:
      bstack1ll111l1l_opy_ = update(bstack11111l11l_opy_, bstack1ll111l1l_opy_)
    desired_capabilities = None
  if options:
    bstack11l11111_opy_(options, bstack1ll111l1l_opy_)
  if not options:
    options = bstack1l11ll1lll_opy_(bstack1ll111l1l_opy_)
  bstack1lll1l1l11_opy_ = CONFIG.get(bstack1ll11l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ਑"))[bstack1lllll11ll_opy_]
  if proxy and bstack1lll1l1ll_opy_() >= version.parse(bstack1ll11l_opy_ (u"ࠩ࠷࠲࠶࠶࠮࠱ࠩ਒")):
    options.proxy(proxy)
  if options and bstack1lll1l1ll_opy_() >= version.parse(bstack1ll11l_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩਓ")):
    desired_capabilities = None
  if (
          not options and not desired_capabilities
  ) or (
          bstack1lll1l1ll_opy_() < version.parse(bstack1ll11l_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪਔ")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack1ll111l1l_opy_)
  logger.info(bstack1l1l1lll11_opy_)
  if bstack1lll1l1ll_opy_() >= version.parse(bstack1ll11l_opy_ (u"ࠬ࠺࠮࠲࠲࠱࠴ࠬਕ")):
    bstack1ll1l11ll_opy_(self, command_executor=command_executor,
              options=options, keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1lll1l1ll_opy_() >= version.parse(bstack1ll11l_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬਖ")):
    bstack1ll1l11ll_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities, options=options,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1lll1l1ll_opy_() >= version.parse(bstack1ll11l_opy_ (u"ࠧ࠳࠰࠸࠷࠳࠶ࠧਗ")):
    bstack1ll1l11ll_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  else:
    bstack1ll1l11ll_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive)
  try:
    bstack1lll1111l_opy_ = bstack1ll11l_opy_ (u"ࠨࠩਘ")
    if bstack1lll1l1ll_opy_() >= version.parse(bstack1ll11l_opy_ (u"ࠩ࠷࠲࠵࠴࠰ࡣ࠳ࠪਙ")):
      bstack1lll1111l_opy_ = self.caps.get(bstack1ll11l_opy_ (u"ࠥࡳࡵࡺࡩ࡮ࡣ࡯ࡌࡺࡨࡕࡳ࡮ࠥਚ"))
    else:
      bstack1lll1111l_opy_ = self.capabilities.get(bstack1ll11l_opy_ (u"ࠦࡴࡶࡴࡪ࡯ࡤࡰࡍࡻࡢࡖࡴ࡯ࠦਛ"))
    if bstack1lll1111l_opy_:
      bstack1l1ll11l1l_opy_(bstack1lll1111l_opy_)
      if bstack1lll1l1ll_opy_() <= version.parse(bstack1ll11l_opy_ (u"ࠬ࠹࠮࠲࠵࠱࠴ࠬਜ")):
        self.command_executor._url = bstack1ll11l_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢਝ") + bstack11l1ll1l_opy_ + bstack1ll11l_opy_ (u"ࠢ࠻࠺࠳࠳ࡼࡪ࠯ࡩࡷࡥࠦਞ")
      else:
        self.command_executor._url = bstack1ll11l_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࠥਟ") + bstack1lll1111l_opy_ + bstack1ll11l_opy_ (u"ࠤ࠲ࡻࡩ࠵ࡨࡶࡤࠥਠ")
      logger.debug(bstack1lll111ll1_opy_.format(bstack1lll1111l_opy_))
    else:
      logger.debug(bstack1l111l1l1_opy_.format(bstack1ll11l_opy_ (u"ࠥࡓࡵࡺࡩ࡮ࡣ࡯ࠤࡍࡻࡢࠡࡰࡲࡸࠥ࡬࡯ࡶࡰࡧࠦਡ")))
  except Exception as e:
    logger.debug(bstack1l111l1l1_opy_.format(e))
  if bstack1ll11l_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪਢ") in bstack11ll11ll1_opy_:
    bstack1l11lll1l_opy_(bstack11l111l11_opy_, bstack111ll1ll1_opy_)
  bstack1lll11111_opy_ = self.session_id
  if bstack1ll11l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬਣ") in bstack11ll11ll1_opy_ or bstack1ll11l_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭ਤ") in bstack11ll11ll1_opy_ or bstack1ll11l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ਥ") in bstack11ll11ll1_opy_:
    threading.current_thread().bstackSessionId = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
    bstack1l111lll1_opy_.bstack1ll111lll_opy_(self)
  bstack1l11l1l111_opy_.append(self)
  if bstack1ll11l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫਦ") in CONFIG and bstack1ll11l_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧਧ") in CONFIG[bstack1ll11l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ਨ")][bstack1lllll11ll_opy_]:
    bstack1l11ll1l_opy_ = CONFIG[bstack1ll11l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ਩")][bstack1lllll11ll_opy_][bstack1ll11l_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪਪ")]
  logger.debug(bstack1l1ll111_opy_.format(bstack1lll11111_opy_))
try:
  try:
    import Browser
    from subprocess import Popen
    def bstack1l1111l1l_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      global bstack1l1ll111ll_opy_
      if(bstack1ll11l_opy_ (u"ࠨࡩ࡯ࡦࡨࡼ࠳ࡰࡳࠣਫ") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack1ll11l_opy_ (u"ࠧࡿࠩਬ")), bstack1ll11l_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨਭ"), bstack1ll11l_opy_ (u"ࠩ࠱ࡷࡪࡹࡳࡪࡱࡱ࡭ࡩࡹ࠮ࡵࡺࡷࠫਮ")), bstack1ll11l_opy_ (u"ࠪࡻࠬਯ")) as fp:
          fp.write(bstack1ll11l_opy_ (u"ࠦࠧਰ"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack1ll11l_opy_ (u"ࠧ࡯࡮ࡥࡧࡻࡣࡧࡹࡴࡢࡥ࡮࠲࡯ࡹࠢ਱")))):
          with open(args[1], bstack1ll11l_opy_ (u"࠭ࡲࠨਲ")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack1ll11l_opy_ (u"ࠧࡢࡵࡼࡲࡨࠦࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠡࡡࡱࡩࡼࡖࡡࡨࡧࠫࡧࡴࡴࡴࡦࡺࡷ࠰ࠥࡶࡡࡨࡧࠣࡁࠥࡼ࡯ࡪࡦࠣ࠴࠮࠭ਲ਼") in line), None)
            if index is not None:
                lines.insert(index+2, bstack1lll111l_opy_)
            lines.insert(1, bstack1ll1l11ll1_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack1ll11l_opy_ (u"ࠣ࡫ࡱࡨࡪࡾ࡟ࡣࡵࡷࡥࡨࡱ࠮࡫ࡵࠥ਴")), bstack1ll11l_opy_ (u"ࠩࡺࠫਵ")) as bstack1lllll11l_opy_:
              bstack1lllll11l_opy_.writelines(lines)
        CONFIG[bstack1ll11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬਸ਼")] = str(bstack11ll11ll1_opy_) + str(__version__)
        bstack1lllll11ll_opy_ = 0 if bstack11l111l11_opy_ < 0 else bstack11l111l11_opy_
        try:
          if bstack11l111111_opy_ is True:
            bstack1lllll11ll_opy_ = int(multiprocessing.current_process().name)
          elif bstack1lll1ll111_opy_ is True:
            bstack1lllll11ll_opy_ = int(threading.current_thread().name)
        except:
          bstack1lllll11ll_opy_ = 0
        CONFIG[bstack1ll11l_opy_ (u"ࠦࡺࡹࡥࡘ࠵ࡆࠦ਷")] = False
        CONFIG[bstack1ll11l_opy_ (u"ࠧ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦਸ")] = True
        bstack1ll111l1l_opy_ = bstack1lll1111ll_opy_(CONFIG, bstack1lllll11ll_opy_)
        logger.debug(bstack111ll111l_opy_.format(str(bstack1ll111l1l_opy_)))
        if CONFIG.get(bstack1ll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪਹ")):
          bstack1l111l11l_opy_(bstack1ll111l1l_opy_)
        if bstack1ll11l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ਺") in CONFIG and bstack1ll11l_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭਻") in CONFIG[bstack1ll11l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷ਼ࠬ")][bstack1lllll11ll_opy_]:
          bstack1l11ll1l_opy_ = CONFIG[bstack1ll11l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭਽")][bstack1lllll11ll_opy_][bstack1ll11l_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩਾ")]
        args.append(os.path.join(os.path.expanduser(bstack1ll11l_opy_ (u"ࠬࢄࠧਿ")), bstack1ll11l_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ੀ"), bstack1ll11l_opy_ (u"ࠧ࠯ࡵࡨࡷࡸ࡯࡯࡯࡫ࡧࡷ࠳ࡺࡸࡵࠩੁ")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack1ll111l1l_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack1ll11l_opy_ (u"ࠣ࡫ࡱࡨࡪࡾ࡟ࡣࡵࡷࡥࡨࡱ࠮࡫ࡵࠥੂ"))
      bstack1l1ll111ll_opy_ = True
      return bstack111111l11_opy_(self, args, bufsize=bufsize, executable=executable,
                    stdin=stdin, stdout=stdout, stderr=stderr,
                    preexec_fn=preexec_fn, close_fds=close_fds,
                    shell=shell, cwd=cwd, env=env, universal_newlines=universal_newlines,
                    startupinfo=startupinfo, creationflags=creationflags,
                    restore_signals=restore_signals, start_new_session=start_new_session,
                    pass_fds=pass_fds, user=user, group=group, extra_groups=extra_groups,
                    encoding=encoding, errors=errors, text=text, umask=umask, pipesize=pipesize)
  except Exception as e:
    pass
  import playwright._impl._api_structures
  import playwright._impl._helper
  def bstack1l1ll1ll_opy_(self,
        executablePath = None,
        channel = None,
        args = None,
        ignoreDefaultArgs = None,
        handleSIGINT = None,
        handleSIGTERM = None,
        handleSIGHUP = None,
        timeout = None,
        env = None,
        headless = None,
        devtools = None,
        proxy = None,
        downloadsPath = None,
        slowMo = None,
        tracesDir = None,
        chromiumSandbox = None,
        firefoxUserPrefs = None
        ):
    global CONFIG
    global bstack11l111l11_opy_
    global bstack1l11ll1l_opy_
    global bstack11l111111_opy_
    global bstack1lll1ll111_opy_
    global bstack11ll11ll1_opy_
    CONFIG[bstack1ll11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫ੃")] = str(bstack11ll11ll1_opy_) + str(__version__)
    bstack1lllll11ll_opy_ = 0 if bstack11l111l11_opy_ < 0 else bstack11l111l11_opy_
    try:
      if bstack11l111111_opy_ is True:
        bstack1lllll11ll_opy_ = int(multiprocessing.current_process().name)
      elif bstack1lll1ll111_opy_ is True:
        bstack1lllll11ll_opy_ = int(threading.current_thread().name)
    except:
      bstack1lllll11ll_opy_ = 0
    CONFIG[bstack1ll11l_opy_ (u"ࠥ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤ੄")] = True
    bstack1ll111l1l_opy_ = bstack1lll1111ll_opy_(CONFIG, bstack1lllll11ll_opy_)
    logger.debug(bstack111ll111l_opy_.format(str(bstack1ll111l1l_opy_)))
    if CONFIG.get(bstack1ll11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ੅")):
      bstack1l111l11l_opy_(bstack1ll111l1l_opy_)
    if bstack1ll11l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ੆") in CONFIG and bstack1ll11l_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫੇ") in CONFIG[bstack1ll11l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪੈ")][bstack1lllll11ll_opy_]:
      bstack1l11ll1l_opy_ = CONFIG[bstack1ll11l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ੉")][bstack1lllll11ll_opy_][bstack1ll11l_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ੊")]
    import urllib
    import json
    bstack1lll111ll_opy_ = bstack1ll11l_opy_ (u"ࠪࡻࡸࡹ࠺࠰࠱ࡦࡨࡵ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࡅࡣࡢࡲࡶࡁࠬੋ") + urllib.parse.quote(json.dumps(bstack1ll111l1l_opy_))
    browser = self.connect(bstack1lll111ll_opy_)
    return browser
except Exception as e:
    pass
def bstack1l11ll111_opy_():
    global bstack1l1ll111ll_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        BrowserType.launch = bstack1l1ll1ll_opy_
        bstack1l1ll111ll_opy_ = True
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack1l1111l1l_opy_
      bstack1l1ll111ll_opy_ = True
    except Exception as e:
      pass
def bstack11llll1l_opy_(context, bstack1l1llllll1_opy_):
  try:
    context.page.evaluate(bstack1ll11l_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧੌ"), bstack1ll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻੍ࠩ")+ json.dumps(bstack1l1llllll1_opy_) + bstack1ll11l_opy_ (u"ࠨࡽࡾࠤ੎"))
  except Exception as e:
    logger.debug(bstack1ll11l_opy_ (u"ࠢࡦࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠢࡾࢁࠧ੏"), e)
def bstack1lll11l11_opy_(context, message, level):
  try:
    context.page.evaluate(bstack1ll11l_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤ੐"), bstack1ll11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧੑ") + json.dumps(message) + bstack1ll11l_opy_ (u"ࠪ࠰ࠧࡲࡥࡷࡧ࡯ࠦ࠿࠭੒") + json.dumps(level) + bstack1ll11l_opy_ (u"ࠫࢂࢃࠧ੓"))
  except Exception as e:
    logger.debug(bstack1ll11l_opy_ (u"ࠧ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡣࡱࡲࡴࡺࡡࡵ࡫ࡲࡲࠥࢁࡽࠣ੔"), e)
def bstack1llll111l_opy_(self, url):
  global bstack1l11ll1111_opy_
  try:
    bstack1lll1ll1l1_opy_(url)
  except Exception as err:
    logger.debug(bstack11l1l1lll_opy_.format(str(err)))
  try:
    bstack1l11ll1111_opy_(self, url)
  except Exception as e:
    try:
      bstack11llllll1_opy_ = str(e)
      if any(err_msg in bstack11llllll1_opy_ for err_msg in bstack1lll1l1ll1_opy_):
        bstack1lll1ll1l1_opy_(url, True)
    except Exception as err:
      logger.debug(bstack11l1l1lll_opy_.format(str(err)))
    raise e
def bstack11111ll1_opy_(self):
  global bstack1llllll11_opy_
  bstack1llllll11_opy_ = self
  return
def bstack111lllll_opy_(self):
  global bstack1l1l1l11l_opy_
  bstack1l1l1l11l_opy_ = self
  return
def bstack11l1ll1ll_opy_(test_name, bstack1l1111ll_opy_):
  global CONFIG
  if CONFIG.get(bstack1ll11l_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬ੕"), False):
    bstack11llll111_opy_ = os.path.relpath(bstack1l1111ll_opy_, start=os.getcwd())
    suite_name, _ = os.path.splitext(bstack11llll111_opy_)
    bstack1l1l11l1ll_opy_ = suite_name + bstack1ll11l_opy_ (u"ࠢ࠮ࠤ੖") + test_name
    threading.current_thread().percySessionName = bstack1l1l11l1ll_opy_
def bstack1l1l1l11_opy_(self, test, *args, **kwargs):
  global bstack1l1l1ll1l_opy_
  test_name = None
  bstack1l1111ll_opy_ = None
  if test:
    test_name = str(test.name)
    bstack1l1111ll_opy_ = str(test.source)
  bstack11l1ll1ll_opy_(test_name, bstack1l1111ll_opy_)
  bstack1l1l1ll1l_opy_(self, test, *args, **kwargs)
def bstack11lll1l11_opy_(driver, bstack1l1l11l1ll_opy_):
  if not bstack11111l1ll_opy_ and bstack1l1l11l1ll_opy_:
      bstack111lll1l1_opy_ = {
          bstack1ll11l_opy_ (u"ࠨࡣࡦࡸ࡮ࡵ࡮ࠨ੗"): bstack1ll11l_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ੘"),
          bstack1ll11l_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ਖ਼"): {
              bstack1ll11l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩਗ਼"): bstack1l1l11l1ll_opy_
          }
      }
      bstack1l1111111_opy_ = bstack1ll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠪਜ਼").format(json.dumps(bstack111lll1l1_opy_))
      driver.execute_script(bstack1l1111111_opy_)
  if bstack1ll1l11111_opy_:
      bstack1l111l1l_opy_ = {
          bstack1ll11l_opy_ (u"࠭ࡡࡤࡶ࡬ࡳࡳ࠭ੜ"): bstack1ll11l_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩ੝"),
          bstack1ll11l_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫਫ਼"): {
              bstack1ll11l_opy_ (u"ࠩࡧࡥࡹࡧࠧ੟"): bstack1l1l11l1ll_opy_ + bstack1ll11l_opy_ (u"ࠪࠤࡵࡧࡳࡴࡧࡧࠥࠬ੠"),
              bstack1ll11l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ੡"): bstack1ll11l_opy_ (u"ࠬ࡯࡮ࡧࡱࠪ੢")
          }
      }
      if bstack1ll1l11111_opy_.status == bstack1ll11l_opy_ (u"࠭ࡐࡂࡕࡖࠫ੣"):
          bstack1l1l1l1l1l_opy_ = bstack1ll11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬ੤").format(json.dumps(bstack1l111l1l_opy_))
          driver.execute_script(bstack1l1l1l1l1l_opy_)
          bstack1111ll11_opy_(driver, bstack1ll11l_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ੥"))
      elif bstack1ll1l11111_opy_.status == bstack1ll11l_opy_ (u"ࠩࡉࡅࡎࡒࠧ੦"):
          reason = bstack1ll11l_opy_ (u"ࠥࠦ੧")
          bstack1lllll1ll_opy_ = bstack1l1l11l1ll_opy_ + bstack1ll11l_opy_ (u"ࠫࠥ࡬ࡡࡪ࡮ࡨࡨࠬ੨")
          if bstack1ll1l11111_opy_.message:
              reason = str(bstack1ll1l11111_opy_.message)
              bstack1lllll1ll_opy_ = bstack1lllll1ll_opy_ + bstack1ll11l_opy_ (u"ࠬࠦࡷࡪࡶ࡫ࠤࡪࡸࡲࡰࡴ࠽ࠤࠬ੩") + reason
          bstack1l111l1l_opy_[bstack1ll11l_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩ੪")] = {
              bstack1ll11l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭੫"): bstack1ll11l_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ੬"),
              bstack1ll11l_opy_ (u"ࠩࡧࡥࡹࡧࠧ੭"): bstack1lllll1ll_opy_
          }
          bstack1l1l1l1l1l_opy_ = bstack1ll11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠨ੮").format(json.dumps(bstack1l111l1l_opy_))
          driver.execute_script(bstack1l1l1l1l1l_opy_)
          bstack1111ll11_opy_(driver, bstack1ll11l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ੯"), reason)
          bstack111l1l11_opy_(reason, str(bstack1ll1l11111_opy_), str(bstack11l111l11_opy_), logger)
def bstack1ll1111l11_opy_(driver, test):
  if CONFIG.get(bstack1ll11l_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫੰ"), False) and CONFIG.get(bstack1ll11l_opy_ (u"࠭ࡰࡦࡴࡦࡽࡈࡧࡰࡵࡷࡵࡩࡒࡵࡤࡦࠩੱ"), bstack1ll11l_opy_ (u"ࠢࡢࡷࡷࡳࠧੲ")) == bstack1ll11l_opy_ (u"ࠣࡶࡨࡷࡹࡩࡡࡴࡧࠥੳ"):
      bstack1ll1l1ll1_opy_ = bstack1l1l111l1l_opy_(threading.current_thread(), bstack1ll11l_opy_ (u"ࠩࡳࡩࡷࡩࡹࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬੴ"), None)
      bstack1ll11lll11_opy_(driver, bstack1ll1l1ll1_opy_)
  if bstack1l1l111l1l_opy_(threading.current_thread(), bstack1ll11l_opy_ (u"ࠪ࡭ࡸࡇ࠱࠲ࡻࡗࡩࡸࡺࠧੵ"), None) and bstack1l1l111l1l_opy_(
          threading.current_thread(), bstack1ll11l_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ੶"), None):
      logger.info(bstack1ll11l_opy_ (u"ࠧࡇࡵࡵࡱࡰࡥࡹ࡫ࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡳࡳࠦࡨࡢࡵࠣࡩࡳࡪࡥࡥ࠰ࠣࡔࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡯ࡳࠡࡷࡱࡨࡪࡸࡷࡢࡻ࠱ࠤࠧ੷"))
      bstack1ll1lll1ll_opy_.bstack1l1lll1111_opy_(driver, class_name=test.parent.name, name=test.name, module_name=None,
                              path=test.source, bstack1l1l11ll1l_opy_=bstack1lll1l1l11_opy_)
def bstack1l1lllll_opy_(test, bstack1l1l11l1ll_opy_):
    try:
      data = {}
      if test:
        data[bstack1ll11l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ੸")] = bstack1l1l11l1ll_opy_
      if bstack1ll1l11111_opy_:
        if bstack1ll1l11111_opy_.status == bstack1ll11l_opy_ (u"ࠧࡑࡃࡖࡗࠬ੹"):
          data[bstack1ll11l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ੺")] = bstack1ll11l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ੻")
        elif bstack1ll1l11111_opy_.status == bstack1ll11l_opy_ (u"ࠪࡊࡆࡏࡌࠨ੼"):
          data[bstack1ll11l_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ੽")] = bstack1ll11l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ੾")
          if bstack1ll1l11111_opy_.message:
            data[bstack1ll11l_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭੿")] = str(bstack1ll1l11111_opy_.message)
      user = CONFIG[bstack1ll11l_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ઀")]
      key = CONFIG[bstack1ll11l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫઁ")]
      url = bstack1ll11l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡿࢂࡀࡻࡾࡂࡤࡴ࡮࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠳ࡸ࡫ࡳࡴ࡫ࡲࡲࡸ࠵ࡻࡾ࠰࡭ࡷࡴࡴࠧં").format(user, key, bstack1lll11111_opy_)
      headers = {
        bstack1ll11l_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩઃ"): bstack1ll11l_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧ઄"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers)
    except Exception as e:
      logger.error(bstack1l1lll111l_opy_.format(str(e)))
def bstack1l11lll11_opy_(test, bstack1l1l11l1ll_opy_):
  global CONFIG
  global bstack1l1l1l11l_opy_
  global bstack1llllll11_opy_
  global bstack1lll11111_opy_
  global bstack1ll1l11111_opy_
  global bstack1l11ll1l_opy_
  global bstack1l1llll1l_opy_
  global bstack11llll11l_opy_
  global bstack1l1ll1lll1_opy_
  global bstack1lllll111_opy_
  global bstack1l11l1l111_opy_
  global bstack1lll1l1l11_opy_
  try:
    if not bstack1lll11111_opy_:
      with open(os.path.join(os.path.expanduser(bstack1ll11l_opy_ (u"ࠬࢄࠧઅ")), bstack1ll11l_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭આ"), bstack1ll11l_opy_ (u"ࠧ࠯ࡵࡨࡷࡸ࡯࡯࡯࡫ࡧࡷ࠳ࡺࡸࡵࠩઇ"))) as f:
        bstack11111l1l1_opy_ = json.loads(bstack1ll11l_opy_ (u"ࠣࡽࠥઈ") + f.read().strip() + bstack1ll11l_opy_ (u"ࠩࠥࡼࠧࡀࠠࠣࡻࠥࠫઉ") + bstack1ll11l_opy_ (u"ࠥࢁࠧઊ"))
        bstack1lll11111_opy_ = bstack11111l1l1_opy_[str(threading.get_ident())]
  except:
    pass
  if bstack1l11l1l111_opy_:
    for driver in bstack1l11l1l111_opy_:
      if bstack1lll11111_opy_ == driver.session_id:
        if test:
          bstack1ll1111l11_opy_(driver, test)
        bstack11lll1l11_opy_(driver, bstack1l1l11l1ll_opy_)
  elif bstack1lll11111_opy_:
    bstack1l1lllll_opy_(test, bstack1l1l11l1ll_opy_)
  if bstack1l1l1l11l_opy_:
    bstack11llll11l_opy_(bstack1l1l1l11l_opy_)
  if bstack1llllll11_opy_:
    bstack1l1ll1lll1_opy_(bstack1llllll11_opy_)
  if bstack1ll11l1ll1_opy_:
    bstack1lllll111_opy_()
def bstack1lllllll11_opy_(self, test, *args, **kwargs):
  bstack1l1l11l1ll_opy_ = None
  if test:
    bstack1l1l11l1ll_opy_ = str(test.name)
  bstack1l11lll11_opy_(test, bstack1l1l11l1ll_opy_)
  bstack1l1llll1l_opy_(self, test, *args, **kwargs)
def bstack1llll111_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack1l1l1l1111_opy_
  global CONFIG
  global bstack1l11l1l111_opy_
  global bstack1lll11111_opy_
  bstack1ll1ll1lll_opy_ = None
  try:
    if bstack1l1l111l1l_opy_(threading.current_thread(), bstack1ll11l_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪઋ"), None):
      try:
        if not bstack1lll11111_opy_:
          with open(os.path.join(os.path.expanduser(bstack1ll11l_opy_ (u"ࠬࢄࠧઌ")), bstack1ll11l_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ઍ"), bstack1ll11l_opy_ (u"ࠧ࠯ࡵࡨࡷࡸ࡯࡯࡯࡫ࡧࡷ࠳ࡺࡸࡵࠩ઎"))) as f:
            bstack11111l1l1_opy_ = json.loads(bstack1ll11l_opy_ (u"ࠣࡽࠥએ") + f.read().strip() + bstack1ll11l_opy_ (u"ࠩࠥࡼࠧࡀࠠࠣࡻࠥࠫઐ") + bstack1ll11l_opy_ (u"ࠥࢁࠧઑ"))
            bstack1lll11111_opy_ = bstack11111l1l1_opy_[str(threading.get_ident())]
      except:
        pass
      if bstack1l11l1l111_opy_:
        for driver in bstack1l11l1l111_opy_:
          if bstack1lll11111_opy_ == driver.session_id:
            bstack1ll1ll1lll_opy_ = driver
    bstack1ll1l111ll_opy_ = bstack1ll1lll1ll_opy_.bstack11ll1l1l1_opy_(CONFIG, test.tags)
    if bstack1ll1ll1lll_opy_:
      threading.current_thread().isA11yTest = bstack1ll1lll1ll_opy_.bstack1llll1l1l1_opy_(bstack1ll1ll1lll_opy_, bstack1ll1l111ll_opy_)
    else:
      threading.current_thread().isA11yTest = bstack1ll1l111ll_opy_
  except:
    pass
  bstack1l1l1l1111_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack1ll1l11111_opy_
  bstack1ll1l11111_opy_ = self._test
def bstack1ll1l1l1_opy_():
  global bstack1l1l1llll_opy_
  try:
    if os.path.exists(bstack1l1l1llll_opy_):
      os.remove(bstack1l1l1llll_opy_)
  except Exception as e:
    logger.debug(bstack1ll11l_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡤࡦ࡮ࡨࡸ࡮ࡴࡧࠡࡴࡲࡦࡴࡺࠠࡳࡧࡳࡳࡷࡺࠠࡧ࡫࡯ࡩ࠿ࠦࠧ઒") + str(e))
def bstack1l11lllll_opy_():
  global bstack1l1l1llll_opy_
  bstack1lll1lll1_opy_ = {}
  try:
    if not os.path.isfile(bstack1l1l1llll_opy_):
      with open(bstack1l1l1llll_opy_, bstack1ll11l_opy_ (u"ࠬࡽࠧઓ")):
        pass
      with open(bstack1l1l1llll_opy_, bstack1ll11l_opy_ (u"ࠨࡷࠬࠤઔ")) as outfile:
        json.dump({}, outfile)
    if os.path.exists(bstack1l1l1llll_opy_):
      bstack1lll1lll1_opy_ = json.load(open(bstack1l1l1llll_opy_, bstack1ll11l_opy_ (u"ࠧࡳࡤࠪક")))
  except Exception as e:
    logger.debug(bstack1ll11l_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡶࡪࡧࡤࡪࡰࡪࠤࡷࡵࡢࡰࡶࠣࡶࡪࡶ࡯ࡳࡶࠣࡪ࡮ࡲࡥ࠻ࠢࠪખ") + str(e))
  finally:
    return bstack1lll1lll1_opy_
def bstack1l11lll1l_opy_(platform_index, item_index):
  global bstack1l1l1llll_opy_
  try:
    bstack1lll1lll1_opy_ = bstack1l11lllll_opy_()
    bstack1lll1lll1_opy_[item_index] = platform_index
    with open(bstack1l1l1llll_opy_, bstack1ll11l_opy_ (u"ࠤࡺ࠯ࠧગ")) as outfile:
      json.dump(bstack1lll1lll1_opy_, outfile)
  except Exception as e:
    logger.debug(bstack1ll11l_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡽࡲࡪࡶ࡬ࡲ࡬ࠦࡴࡰࠢࡵࡳࡧࡵࡴࠡࡴࡨࡴࡴࡸࡴࠡࡨ࡬ࡰࡪࡀࠠࠨઘ") + str(e))
def bstack1l1llll11_opy_(bstack1l1lll1ll_opy_):
  global CONFIG
  bstack1l1111l1_opy_ = bstack1ll11l_opy_ (u"ࠫࠬઙ")
  if not bstack1ll11l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨચ") in CONFIG:
    logger.info(bstack1ll11l_opy_ (u"࠭ࡎࡰࠢࡳࡰࡦࡺࡦࡰࡴࡰࡷࠥࡶࡡࡴࡵࡨࡨࠥࡻ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡩࡨࡲࡪࡸࡡࡵࡧࠣࡶࡪࡶ࡯ࡳࡶࠣࡪࡴࡸࠠࡓࡱࡥࡳࡹࠦࡲࡶࡰࠪછ"))
  try:
    platform = CONFIG[bstack1ll11l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪજ")][bstack1l1lll1ll_opy_]
    if bstack1ll11l_opy_ (u"ࠨࡱࡶࠫઝ") in platform:
      bstack1l1111l1_opy_ += str(platform[bstack1ll11l_opy_ (u"ࠩࡲࡷࠬઞ")]) + bstack1ll11l_opy_ (u"ࠪ࠰ࠥ࠭ટ")
    if bstack1ll11l_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠧઠ") in platform:
      bstack1l1111l1_opy_ += str(platform[bstack1ll11l_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨડ")]) + bstack1ll11l_opy_ (u"࠭ࠬࠡࠩઢ")
    if bstack1ll11l_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫણ") in platform:
      bstack1l1111l1_opy_ += str(platform[bstack1ll11l_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬત")]) + bstack1ll11l_opy_ (u"ࠩ࠯ࠤࠬથ")
    if bstack1ll11l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬદ") in platform:
      bstack1l1111l1_opy_ += str(platform[bstack1ll11l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ધ")]) + bstack1ll11l_opy_ (u"ࠬ࠲ࠠࠨન")
    if bstack1ll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫ઩") in platform:
      bstack1l1111l1_opy_ += str(platform[bstack1ll11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬપ")]) + bstack1ll11l_opy_ (u"ࠨ࠮ࠣࠫફ")
    if bstack1ll11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪબ") in platform:
      bstack1l1111l1_opy_ += str(platform[bstack1ll11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫભ")]) + bstack1ll11l_opy_ (u"ࠫ࠱ࠦࠧમ")
  except Exception as e:
    logger.debug(bstack1ll11l_opy_ (u"࡙ࠬ࡯࡮ࡧࠣࡩࡷࡸ࡯ࡳࠢ࡬ࡲࠥ࡭ࡥ࡯ࡧࡵࡥࡹ࡯࡮ࡨࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤࡸࡺࡲࡪࡰࡪࠤ࡫ࡵࡲࠡࡴࡨࡴࡴࡸࡴࠡࡩࡨࡲࡪࡸࡡࡵ࡫ࡲࡲࠬય") + str(e))
  finally:
    if bstack1l1111l1_opy_[len(bstack1l1111l1_opy_) - 2:] == bstack1ll11l_opy_ (u"࠭ࠬࠡࠩર"):
      bstack1l1111l1_opy_ = bstack1l1111l1_opy_[:-2]
    return bstack1l1111l1_opy_
def bstack1ll11l111_opy_(path, bstack1l1111l1_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack1111lllll_opy_ = ET.parse(path)
    bstack1llllllll1_opy_ = bstack1111lllll_opy_.getroot()
    bstack111l1l11l_opy_ = None
    for suite in bstack1llllllll1_opy_.iter(bstack1ll11l_opy_ (u"ࠧࡴࡷ࡬ࡸࡪ࠭઱")):
      if bstack1ll11l_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨલ") in suite.attrib:
        suite.attrib[bstack1ll11l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧળ")] += bstack1ll11l_opy_ (u"ࠪࠤࠬ઴") + bstack1l1111l1_opy_
        bstack111l1l11l_opy_ = suite
    bstack1l1l111ll_opy_ = None
    for robot in bstack1llllllll1_opy_.iter(bstack1ll11l_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪવ")):
      bstack1l1l111ll_opy_ = robot
    bstack1llll1ll1_opy_ = len(bstack1l1l111ll_opy_.findall(bstack1ll11l_opy_ (u"ࠬࡹࡵࡪࡶࡨࠫશ")))
    if bstack1llll1ll1_opy_ == 1:
      bstack1l1l111ll_opy_.remove(bstack1l1l111ll_opy_.findall(bstack1ll11l_opy_ (u"࠭ࡳࡶ࡫ࡷࡩࠬષ"))[0])
      bstack1111111l_opy_ = ET.Element(bstack1ll11l_opy_ (u"ࠧࡴࡷ࡬ࡸࡪ࠭સ"), attrib={bstack1ll11l_opy_ (u"ࠨࡰࡤࡱࡪ࠭હ"): bstack1ll11l_opy_ (u"ࠩࡖࡹ࡮ࡺࡥࡴࠩ઺"), bstack1ll11l_opy_ (u"ࠪ࡭ࡩ࠭઻"): bstack1ll11l_opy_ (u"ࠫࡸ࠶઼ࠧ")})
      bstack1l1l111ll_opy_.insert(1, bstack1111111l_opy_)
      bstack1ll11lll_opy_ = None
      for suite in bstack1l1l111ll_opy_.iter(bstack1ll11l_opy_ (u"ࠬࡹࡵࡪࡶࡨࠫઽ")):
        bstack1ll11lll_opy_ = suite
      bstack1ll11lll_opy_.append(bstack111l1l11l_opy_)
      bstack111111111_opy_ = None
      for status in bstack111l1l11l_opy_.iter(bstack1ll11l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ા")):
        bstack111111111_opy_ = status
      bstack1ll11lll_opy_.append(bstack111111111_opy_)
    bstack1111lllll_opy_.write(path)
  except Exception as e:
    logger.debug(bstack1ll11l_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡳࡥࡷࡹࡩ࡯ࡩࠣࡻ࡭࡯࡬ࡦࠢࡪࡩࡳ࡫ࡲࡢࡶ࡬ࡲ࡬ࠦࡲࡰࡤࡲࡸࠥࡸࡥࡱࡱࡵࡸࠬિ") + str(e))
def bstack11l11l11l_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack1ll111l11_opy_
  global CONFIG
  if bstack1ll11l_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࡱࡣࡷ࡬ࠧી") in options:
    del options[bstack1ll11l_opy_ (u"ࠤࡳࡽࡹ࡮࡯࡯ࡲࡤࡸ࡭ࠨુ")]
  bstack11lll1l1l_opy_ = bstack1l11lllll_opy_()
  for bstack1ll1l111l_opy_ in bstack11lll1l1l_opy_.keys():
    path = os.path.join(os.getcwd(), bstack1ll11l_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࡡࡵࡩࡸࡻ࡬ࡵࡵࠪૂ"), str(bstack1ll1l111l_opy_), bstack1ll11l_opy_ (u"ࠫࡴࡻࡴࡱࡷࡷ࠲ࡽࡳ࡬ࠨૃ"))
    bstack1ll11l111_opy_(path, bstack1l1llll11_opy_(bstack11lll1l1l_opy_[bstack1ll1l111l_opy_]))
  bstack1ll1l1l1_opy_()
  return bstack1ll111l11_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack1lllll111l_opy_(self, ff_profile_dir):
  global bstack1ll1lllll1_opy_
  if not ff_profile_dir:
    return None
  return bstack1ll1lllll1_opy_(self, ff_profile_dir)
def bstack1ll1l1l111_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack111l1l1l_opy_
  bstack1lll11l111_opy_ = []
  if bstack1ll11l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨૄ") in CONFIG:
    bstack1lll11l111_opy_ = CONFIG[bstack1ll11l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩૅ")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack1ll11l_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࠣ૆")],
      pabot_args[bstack1ll11l_opy_ (u"ࠣࡸࡨࡶࡧࡵࡳࡦࠤે")],
      argfile,
      pabot_args.get(bstack1ll11l_opy_ (u"ࠤ࡫࡭ࡻ࡫ࠢૈ")),
      pabot_args[bstack1ll11l_opy_ (u"ࠥࡴࡷࡵࡣࡦࡵࡶࡩࡸࠨૉ")],
      platform[0],
      bstack111l1l1l_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack1ll11l_opy_ (u"ࠦࡦࡸࡧࡶ࡯ࡨࡲࡹ࡬ࡩ࡭ࡧࡶࠦ૊")] or [(bstack1ll11l_opy_ (u"ࠧࠨો"), None)]
    for platform in enumerate(bstack1lll11l111_opy_)
  ]
def bstack11l1111l1_opy_(self, datasources, outs_dir, options,
                        execution_item, command, verbose, argfile,
                        hive=None, processes=0, platform_index=0, bstack11l1lll1l_opy_=bstack1ll11l_opy_ (u"࠭ࠧૌ")):
  global bstack1lll111lll_opy_
  self.platform_index = platform_index
  self.bstack1l1lll111_opy_ = bstack11l1lll1l_opy_
  bstack1lll111lll_opy_(self, datasources, outs_dir, options,
                      execution_item, command, verbose, argfile, hive, processes)
def bstack111l1111_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1ll1lll1l1_opy_
  global bstack111ll1lll_opy_
  if not bstack1ll11l_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦ્ࠩ") in item.options:
    item.options[bstack1ll11l_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪ૎")] = []
  for v in item.options[bstack1ll11l_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫ૏")]:
    if bstack1ll11l_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡓࡐࡆ࡚ࡆࡐࡔࡐࡍࡓࡊࡅ࡙ࠩૐ") in v:
      item.options[bstack1ll11l_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭૑")].remove(v)
    if bstack1ll11l_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡈࡒࡉࡂࡔࡊࡗࠬ૒") in v:
      item.options[bstack1ll11l_opy_ (u"࠭ࡶࡢࡴ࡬ࡥࡧࡲࡥࠨ૓")].remove(v)
  item.options[bstack1ll11l_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩ૔")].insert(0, bstack1ll11l_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡑࡎࡄࡘࡋࡕࡒࡎࡋࡑࡈࡊ࡞࠺ࡼࡿࠪ૕").format(item.platform_index))
  item.options[bstack1ll11l_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫ૖")].insert(0, bstack1ll11l_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡇࡉࡋࡒࡏࡄࡃࡏࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘ࠺ࡼࡿࠪ૗").format(item.bstack1l1lll111_opy_))
  if bstack111ll1lll_opy_:
    item.options[bstack1ll11l_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭૘")].insert(0, bstack1ll11l_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡈࡒࡉࡂࡔࡊࡗ࠿ࢁࡽࠨ૙").format(bstack111ll1lll_opy_))
  return bstack1ll1lll1l1_opy_(caller_id, datasources, is_last, item, outs_dir)
def bstack1ll1l11lll_opy_(command, item_index):
  if bstack1l11l111l_opy_.get_property(bstack1ll11l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧ૚")):
    os.environ[bstack1ll11l_opy_ (u"ࠧࡄࡗࡕࡖࡊࡔࡔࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡈࡆ࡚ࡁࠨ૛")] = json.dumps(CONFIG[bstack1ll11l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ૜")][item_index % bstack1111l11ll_opy_])
  global bstack111ll1lll_opy_
  if bstack111ll1lll_opy_:
    command[0] = command[0].replace(bstack1ll11l_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ૝"), bstack1ll11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠯ࡶࡨࡰࠦࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠠ࠮࠯ࡥࡷࡹࡧࡣ࡬ࡡ࡬ࡸࡪࡳ࡟ࡪࡰࡧࡩࡽࠦࠧ૞") + str(
      item_index) + bstack1ll11l_opy_ (u"ࠫࠥ࠭૟") + bstack111ll1lll_opy_, 1)
  else:
    command[0] = command[0].replace(bstack1ll11l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫૠ"),
                                    bstack1ll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠲ࡹࡤ࡬ࠢࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠣ࠱࠲ࡨࡳࡵࡣࡦ࡯ࡤ࡯ࡴࡦ࡯ࡢ࡭ࡳࡪࡥࡹࠢࠪૡ") + str(item_index), 1)
def bstack1l1l11llll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack1llll11111_opy_
  bstack1ll1l11lll_opy_(command, item_index)
  return bstack1llll11111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
def bstack1l1l11l11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack1llll11111_opy_
  bstack1ll1l11lll_opy_(command, item_index)
  return bstack1llll11111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
def bstack1l11lll111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack1llll11111_opy_
  bstack1ll1l11lll_opy_(command, item_index)
  return bstack1llll11111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
def bstack1111111l1_opy_(self, runner, quiet=False, capture=True):
  global bstack1lll111111_opy_
  bstack1l11ll1l1l_opy_ = bstack1lll111111_opy_(self, runner, quiet=False, capture=True)
  if self.exception:
    if not hasattr(runner, bstack1ll11l_opy_ (u"ࠧࡦࡺࡦࡩࡵࡺࡩࡰࡰࡢࡥࡷࡸࠧૢ")):
      runner.exception_arr = []
    if not hasattr(runner, bstack1ll11l_opy_ (u"ࠨࡧࡻࡧࡤࡺࡲࡢࡥࡨࡦࡦࡩ࡫ࡠࡣࡵࡶࠬૣ")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack1l11ll1l1l_opy_
def bstack11l111ll1_opy_(self, name, context, *args):
  os.environ[bstack1ll11l_opy_ (u"ࠩࡆ࡙ࡗࡘࡅࡏࡖࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡊࡁࡕࡃࠪ૤")] = json.dumps(CONFIG[bstack1ll11l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭૥")][int(threading.current_thread()._name) % bstack1111l11ll_opy_])
  global bstack1llll1l11l_opy_
  if name == bstack1ll11l_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣ࡫࡫ࡡࡵࡷࡵࡩࠬ૦"):
    bstack1llll1l11l_opy_(self, name, context, *args)
    try:
      if not bstack11111l1ll_opy_:
        bstack1ll1ll1lll_opy_ = threading.current_thread().bstackSessionDriver if bstack1l1llllll_opy_(bstack1ll11l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫ૧")) else context.browser
        bstack1l1llllll1_opy_ = str(self.feature.name)
        bstack11llll1l_opy_(context, bstack1l1llllll1_opy_)
        bstack1ll1ll1lll_opy_.execute_script(bstack1ll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠣࠫ૨") + json.dumps(bstack1l1llllll1_opy_) + bstack1ll11l_opy_ (u"ࠧࡾࡿࠪ૩"))
      self.driver_before_scenario = False
    except Exception as e:
      logger.debug(bstack1ll11l_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠠࡪࡰࠣࡦࡪ࡬࡯ࡳࡧࠣࡪࡪࡧࡴࡶࡴࡨ࠾ࠥࢁࡽࠨ૪").format(str(e)))
  elif name == bstack1ll11l_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫ૫"):
    bstack1llll1l11l_opy_(self, name, context, *args)
    try:
      if not hasattr(self, bstack1ll11l_opy_ (u"ࠪࡨࡷ࡯ࡶࡦࡴࡢࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬ૬")):
        self.driver_before_scenario = True
      if (not bstack11111l1ll_opy_):
        scenario_name = args[0].name
        feature_name = bstack1l1llllll1_opy_ = str(self.feature.name)
        bstack1l1llllll1_opy_ = feature_name + bstack1ll11l_opy_ (u"ࠫࠥ࠳ࠠࠨ૭") + scenario_name
        bstack1ll1ll1lll_opy_ = threading.current_thread().bstackSessionDriver if bstack1l1llllll_opy_(bstack1ll11l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫ૮")) else context.browser
        if self.driver_before_scenario:
          bstack11llll1l_opy_(context, bstack1l1llllll1_opy_)
          bstack1ll1ll1lll_opy_.execute_script(bstack1ll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠣࠫ૯") + json.dumps(bstack1l1llllll1_opy_) + bstack1ll11l_opy_ (u"ࠧࡾࡿࠪ૰"))
    except Exception as e:
      logger.debug(bstack1ll11l_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠠࡪࡰࠣࡦࡪ࡬࡯ࡳࡧࠣࡷࡨ࡫࡮ࡢࡴ࡬ࡳ࠿ࠦࡻࡾࠩ૱").format(str(e)))
  elif name == bstack1ll11l_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡵࡦࡩࡳࡧࡲࡪࡱࠪ૲"):
    try:
      bstack1ll111lll1_opy_ = args[0].status.name
      bstack1ll1ll1lll_opy_ = threading.current_thread().bstackSessionDriver if bstack1ll11l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩ૳") in threading.current_thread().__dict__.keys() else context.browser
      if str(bstack1ll111lll1_opy_).lower() == bstack1ll11l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ૴"):
        bstack1l1l11l1l_opy_ = bstack1ll11l_opy_ (u"ࠬ࠭૵")
        bstack1ll1ll1ll_opy_ = bstack1ll11l_opy_ (u"࠭ࠧ૶")
        bstack1l1111ll1_opy_ = bstack1ll11l_opy_ (u"ࠧࠨ૷")
        try:
          import traceback
          bstack1l1l11l1l_opy_ = self.exception.__class__.__name__
          bstack1ll1l1l1ll_opy_ = traceback.format_tb(self.exc_traceback)
          bstack1ll1ll1ll_opy_ = bstack1ll11l_opy_ (u"ࠨࠢࠪ૸").join(bstack1ll1l1l1ll_opy_)
          bstack1l1111ll1_opy_ = bstack1ll1l1l1ll_opy_[-1]
        except Exception as e:
          logger.debug(bstack1l11l1l1ll_opy_.format(str(e)))
        bstack1l1l11l1l_opy_ += bstack1l1111ll1_opy_
        bstack1lll11l11_opy_(context, json.dumps(str(args[0].name) + bstack1ll11l_opy_ (u"ࠤࠣ࠱ࠥࡌࡡࡪ࡮ࡨࡨࠦࡢ࡮ࠣૹ") + str(bstack1ll1ll1ll_opy_)),
                            bstack1ll11l_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤૺ"))
        if self.driver_before_scenario:
          bstack11l1ll11l_opy_(getattr(context, bstack1ll11l_opy_ (u"ࠫࡵࡧࡧࡦࠩૻ"), None), bstack1ll11l_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧૼ"), bstack1l1l11l1l_opy_)
          bstack1ll1ll1lll_opy_.execute_script(bstack1ll11l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫ૽") + json.dumps(str(args[0].name) + bstack1ll11l_opy_ (u"ࠢࠡ࠯ࠣࡊࡦ࡯࡬ࡦࡦࠤࡠࡳࠨ૾") + str(bstack1ll1ll1ll_opy_)) + bstack1ll11l_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡥࡳࡴࡲࡶࠧࢃࡽࠨ૿"))
        if self.driver_before_scenario:
          bstack1111ll11_opy_(bstack1ll1ll1lll_opy_, bstack1ll11l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ଀"), bstack1ll11l_opy_ (u"ࠥࡗࡨ࡫࡮ࡢࡴ࡬ࡳࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡽࡩࡵࡪ࠽ࠤࡡࡴࠢଁ") + str(bstack1l1l11l1l_opy_))
      else:
        bstack1lll11l11_opy_(context, bstack1ll11l_opy_ (u"ࠦࡕࡧࡳࡴࡧࡧࠥࠧଂ"), bstack1ll11l_opy_ (u"ࠧ࡯࡮ࡧࡱࠥଃ"))
        if self.driver_before_scenario:
          bstack11l1ll11l_opy_(getattr(context, bstack1ll11l_opy_ (u"࠭ࡰࡢࡩࡨࠫ଄"), None), bstack1ll11l_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢଅ"))
        bstack1ll1ll1lll_opy_.execute_script(bstack1ll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭ଆ") + json.dumps(str(args[0].name) + bstack1ll11l_opy_ (u"ࠤࠣ࠱ࠥࡖࡡࡴࡵࡨࡨࠦࠨଇ")) + bstack1ll11l_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣ࡫ࡱࡪࡴࠨࡽࡾࠩଈ"))
        if self.driver_before_scenario:
          bstack1111ll11_opy_(bstack1ll1ll1lll_opy_, bstack1ll11l_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦଉ"))
    except Exception as e:
      logger.debug(bstack1ll11l_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡ࡯ࡤࡶࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡪࡰࠣࡥ࡫ࡺࡥࡳࠢࡩࡩࡦࡺࡵࡳࡧ࠽ࠤࢀࢃࠧଊ").format(str(e)))
  elif name == bstack1ll11l_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤ࡬ࡥࡢࡶࡸࡶࡪ࠭ଋ"):
    try:
      bstack1ll1ll1lll_opy_ = threading.current_thread().bstackSessionDriver if bstack1l1llllll_opy_(bstack1ll11l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ଌ")) else context.browser
      if context.failed is True:
        bstack1l1l1111l_opy_ = []
        bstack1l1l1111l1_opy_ = []
        bstack11l111l1l_opy_ = []
        bstack1l1l1lll1l_opy_ = bstack1ll11l_opy_ (u"ࠨࠩ଍")
        try:
          import traceback
          for exc in self.exception_arr:
            bstack1l1l1111l_opy_.append(exc.__class__.__name__)
          for exc_tb in self.exc_traceback_arr:
            bstack1ll1l1l1ll_opy_ = traceback.format_tb(exc_tb)
            bstack111l111ll_opy_ = bstack1ll11l_opy_ (u"ࠩࠣࠫ଎").join(bstack1ll1l1l1ll_opy_)
            bstack1l1l1111l1_opy_.append(bstack111l111ll_opy_)
            bstack11l111l1l_opy_.append(bstack1ll1l1l1ll_opy_[-1])
        except Exception as e:
          logger.debug(bstack1l11l1l1ll_opy_.format(str(e)))
        bstack1l1l11l1l_opy_ = bstack1ll11l_opy_ (u"ࠪࠫଏ")
        for i in range(len(bstack1l1l1111l_opy_)):
          bstack1l1l11l1l_opy_ += bstack1l1l1111l_opy_[i] + bstack11l111l1l_opy_[i] + bstack1ll11l_opy_ (u"ࠫࡡࡴࠧଐ")
        bstack1l1l1lll1l_opy_ = bstack1ll11l_opy_ (u"ࠬࠦࠧ଑").join(bstack1l1l1111l1_opy_)
        if not self.driver_before_scenario:
          bstack1lll11l11_opy_(context, bstack1l1l1lll1l_opy_, bstack1ll11l_opy_ (u"ࠨࡥࡳࡴࡲࡶࠧ଒"))
          bstack11l1ll11l_opy_(getattr(context, bstack1ll11l_opy_ (u"ࠧࡱࡣࡪࡩࠬଓ"), None), bstack1ll11l_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣଔ"), bstack1l1l11l1l_opy_)
          bstack1ll1ll1lll_opy_.execute_script(bstack1ll11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧକ") + json.dumps(bstack1l1l1lll1l_opy_) + bstack1ll11l_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣࡧࡵࡶࡴࡸࠢࡾࡿࠪଖ"))
          bstack1111ll11_opy_(bstack1ll1ll1lll_opy_, bstack1ll11l_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦଗ"), bstack1ll11l_opy_ (u"࡙ࠧ࡯࡮ࡧࠣࡷࡨ࡫࡮ࡢࡴ࡬ࡳࡸࠦࡦࡢ࡫࡯ࡩࡩࡀࠠ࡝ࡰࠥଘ") + str(bstack1l1l11l1l_opy_))
          bstack11ll111ll_opy_ = bstack11l11ll11_opy_(bstack1l1l1lll1l_opy_, self.feature.name, logger)
          if (bstack11ll111ll_opy_ != None):
            bstack1ll11l1l1_opy_.append(bstack11ll111ll_opy_)
      else:
        if not self.driver_before_scenario:
          bstack1lll11l11_opy_(context, bstack1ll11l_opy_ (u"ࠨࡆࡦࡣࡷࡹࡷ࡫࠺ࠡࠤଙ") + str(self.feature.name) + bstack1ll11l_opy_ (u"ࠢࠡࡲࡤࡷࡸ࡫ࡤࠢࠤଚ"), bstack1ll11l_opy_ (u"ࠣ࡫ࡱࡪࡴࠨଛ"))
          bstack11l1ll11l_opy_(getattr(context, bstack1ll11l_opy_ (u"ࠩࡳࡥ࡬࡫ࠧଜ"), None), bstack1ll11l_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥଝ"))
          bstack1ll1ll1lll_opy_.execute_script(bstack1ll11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩଞ") + json.dumps(bstack1ll11l_opy_ (u"ࠧࡌࡥࡢࡶࡸࡶࡪࡀࠠࠣଟ") + str(self.feature.name) + bstack1ll11l_opy_ (u"ࠨࠠࡱࡣࡶࡷࡪࡪࠡࠣଠ")) + bstack1ll11l_opy_ (u"ࠧ࠭ࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡯࡮ࡧࡱࠥࢁࢂ࠭ଡ"))
          bstack1111ll11_opy_(bstack1ll1ll1lll_opy_, bstack1ll11l_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨଢ"))
          bstack11ll111ll_opy_ = bstack11l11ll11_opy_(bstack1l1l1lll1l_opy_, self.feature.name, logger)
          if (bstack11ll111ll_opy_ != None):
            bstack1ll11l1l1_opy_.append(bstack11ll111ll_opy_)
    except Exception as e:
      logger.debug(bstack1ll11l_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡳࡡࡳ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡵࡷࡶࠤ࡮ࡴࠠࡢࡨࡷࡩࡷࠦࡦࡦࡣࡷࡹࡷ࡫࠺ࠡࡽࢀࠫଣ").format(str(e)))
  else:
    bstack1llll1l11l_opy_(self, name, context, *args)
  if name in [bstack1ll11l_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡩࡩࡦࡺࡵࡳࡧࠪତ"), bstack1ll11l_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬଥ")]:
    bstack1llll1l11l_opy_(self, name, context, *args)
    if (name == bstack1ll11l_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭ଦ") and self.driver_before_scenario) or (
            name == bstack1ll11l_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤ࡬ࡥࡢࡶࡸࡶࡪ࠭ଧ") and not self.driver_before_scenario):
      try:
        bstack1ll1ll1lll_opy_ = threading.current_thread().bstackSessionDriver if bstack1l1llllll_opy_(bstack1ll11l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ନ")) else context.browser
        bstack1ll1ll1lll_opy_.quit()
      except Exception:
        pass
def bstack1ll111llll_opy_(config, startdir):
  return bstack1ll11l_opy_ (u"ࠣࡦࡵ࡭ࡻ࡫ࡲ࠻ࠢࡾ࠴ࢂࠨ଩").format(bstack1ll11l_opy_ (u"ࠤࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠣପ"))
notset = Notset()
def bstack11lll11ll_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack1llllll1l1_opy_
  if str(name).lower() == bstack1ll11l_opy_ (u"ࠪࡨࡷ࡯ࡶࡦࡴࠪଫ"):
    return bstack1ll11l_opy_ (u"ࠦࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠥବ")
  else:
    return bstack1llllll1l1_opy_(self, name, default, skip)
def bstack11l1l1111_opy_(item, when):
  global bstack1l1ll1111_opy_
  try:
    bstack1l1ll1111_opy_(item, when)
  except Exception as e:
    pass
def bstack1l11111ll_opy_():
  return
def bstack1ll11lllll_opy_(type, name, status, reason, bstack1ll1lll11l_opy_, bstack11l1llll_opy_):
  bstack111lll1l1_opy_ = {
    bstack1ll11l_opy_ (u"ࠬࡧࡣࡵ࡫ࡲࡲࠬଭ"): type,
    bstack1ll11l_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩମ"): {}
  }
  if type == bstack1ll11l_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩଯ"):
    bstack111lll1l1_opy_[bstack1ll11l_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫର")][bstack1ll11l_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ଱")] = bstack1ll1lll11l_opy_
    bstack111lll1l1_opy_[bstack1ll11l_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ଲ")][bstack1ll11l_opy_ (u"ࠫࡩࡧࡴࡢࠩଳ")] = json.dumps(str(bstack11l1llll_opy_))
  if type == bstack1ll11l_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭଴"):
    bstack111lll1l1_opy_[bstack1ll11l_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩଵ")][bstack1ll11l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬଶ")] = name
  if type == bstack1ll11l_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫଷ"):
    bstack111lll1l1_opy_[bstack1ll11l_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬସ")][bstack1ll11l_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪହ")] = status
    if status == bstack1ll11l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ଺"):
      bstack111lll1l1_opy_[bstack1ll11l_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ଻")][bstack1ll11l_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ଼࠭")] = json.dumps(str(reason))
  bstack1l1111111_opy_ = bstack1ll11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬଽ").format(json.dumps(bstack111lll1l1_opy_))
  return bstack1l1111111_opy_
def bstack111l1ll1l_opy_(driver_command, response):
    if driver_command == bstack1ll11l_opy_ (u"ࠨࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠬା"):
        bstack1l111lll1_opy_.bstack1l11llll_opy_({
            bstack1ll11l_opy_ (u"ࠩ࡬ࡱࡦ࡭ࡥࠨି"): response[bstack1ll11l_opy_ (u"ࠪࡺࡦࡲࡵࡦࠩୀ")],
            bstack1ll11l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫୁ"): bstack1l111lll1_opy_.current_test_uuid()
        })
def bstack11l11ll1l_opy_(item, call, rep):
  global bstack1111llll_opy_
  global bstack1l11l1l111_opy_
  global bstack11111l1ll_opy_
  name = bstack1ll11l_opy_ (u"ࠬ࠭ୂ")
  try:
    if rep.when == bstack1ll11l_opy_ (u"࠭ࡣࡢ࡮࡯ࠫୃ"):
      bstack1lll11111_opy_ = threading.current_thread().bstackSessionId
      try:
        if not bstack11111l1ll_opy_:
          name = str(rep.nodeid)
          bstack11111lll_opy_ = bstack1ll11lllll_opy_(bstack1ll11l_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨୄ"), name, bstack1ll11l_opy_ (u"ࠨࠩ୅"), bstack1ll11l_opy_ (u"ࠩࠪ୆"), bstack1ll11l_opy_ (u"ࠪࠫେ"), bstack1ll11l_opy_ (u"ࠫࠬୈ"))
          threading.current_thread().bstack1l11l1l11_opy_ = name
          for driver in bstack1l11l1l111_opy_:
            if bstack1lll11111_opy_ == driver.session_id:
              driver.execute_script(bstack11111lll_opy_)
      except Exception as e:
        logger.debug(bstack1ll11l_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠦࡦࡰࡴࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡴࡧࡶࡷ࡮ࡵ࡮࠻ࠢࡾࢁࠬ୉").format(str(e)))
      try:
        bstack1l1llll111_opy_(rep.outcome.lower())
        if rep.outcome.lower() != bstack1ll11l_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ୊"):
          status = bstack1ll11l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧୋ") if rep.outcome.lower() == bstack1ll11l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨୌ") else bstack1ll11l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥ୍ࠩ")
          reason = bstack1ll11l_opy_ (u"ࠪࠫ୎")
          if status == bstack1ll11l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ୏"):
            reason = rep.longrepr.reprcrash.message
            if (not threading.current_thread().bstackTestErrorMessages):
              threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(reason)
          level = bstack1ll11l_opy_ (u"ࠬ࡯࡮ࡧࡱࠪ୐") if status == bstack1ll11l_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭୑") else bstack1ll11l_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭୒")
          data = name + bstack1ll11l_opy_ (u"ࠨࠢࡳࡥࡸࡹࡥࡥࠣࠪ୓") if status == bstack1ll11l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ୔") else name + bstack1ll11l_opy_ (u"ࠪࠤ࡫ࡧࡩ࡭ࡧࡧࠥࠥ࠭୕") + reason
          bstack1ll1l1l11l_opy_ = bstack1ll11lllll_opy_(bstack1ll11l_opy_ (u"ࠫࡦࡴ࡮ࡰࡶࡤࡸࡪ࠭ୖ"), bstack1ll11l_opy_ (u"ࠬ࠭ୗ"), bstack1ll11l_opy_ (u"࠭ࠧ୘"), bstack1ll11l_opy_ (u"ࠧࠨ୙"), level, data)
          for driver in bstack1l11l1l111_opy_:
            if bstack1lll11111_opy_ == driver.session_id:
              driver.execute_script(bstack1ll1l1l11l_opy_)
      except Exception as e:
        logger.debug(bstack1ll11l_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡩ࡯࡯ࡶࡨࡼࡹࠦࡦࡰࡴࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡴࡧࡶࡷ࡮ࡵ࡮࠻ࠢࡾࢁࠬ୚").format(str(e)))
  except Exception as e:
    logger.debug(bstack1ll11l_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡴࡢࡶࡨࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹ࡫ࡳࡵࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࡿࢂ࠭୛").format(str(e)))
  bstack1111llll_opy_(item, call, rep)
def bstack1ll11lll11_opy_(driver, bstack1lll11llll_opy_):
  PercySDK.screenshot(driver, bstack1lll11llll_opy_)
def bstack1l11ll1ll_opy_(driver):
  if bstack1ll1111lll_opy_.bstack1lll1lll_opy_() is True or bstack1ll1111lll_opy_.capturing() is True:
    return
  bstack1ll1111lll_opy_.bstack11l1l1ll_opy_()
  while not bstack1ll1111lll_opy_.bstack1lll1lll_opy_():
    bstack111111ll_opy_ = bstack1ll1111lll_opy_.bstack1ll11l11ll_opy_()
    bstack1ll11lll11_opy_(driver, bstack111111ll_opy_)
  bstack1ll1111lll_opy_.bstack1ll11lll1_opy_()
def bstack1l1ll1l1l_opy_(sequence, driver_command, response = None, bstack1ll11l1l_opy_ = None, args = None):
    try:
      if sequence != bstack1ll11l_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࠪଡ଼"):
        return
      if not CONFIG.get(bstack1ll11l_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪଢ଼"), False):
        return
      bstack111111ll_opy_ = bstack1l1l111l1l_opy_(threading.current_thread(), bstack1ll11l_opy_ (u"ࠬࡶࡥࡳࡥࡼࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ୞"), None)
      for command in bstack1111ll1l1_opy_:
        if command == driver_command:
          for driver in bstack1l11l1l111_opy_:
            bstack1l11ll1ll_opy_(driver)
      bstack1ll11l111l_opy_ = CONFIG.get(bstack1ll11l_opy_ (u"࠭ࡰࡦࡴࡦࡽࡈࡧࡰࡵࡷࡵࡩࡒࡵࡤࡦࠩୟ"), bstack1ll11l_opy_ (u"ࠢࡢࡷࡷࡳࠧୠ"))
      if driver_command in bstack1lll11ll_opy_[bstack1ll11l111l_opy_]:
        bstack1ll1111lll_opy_.bstack1ll1ll1l11_opy_(bstack111111ll_opy_, driver_command)
    except Exception as e:
      pass
def bstack1l1llll1_opy_(framework_name):
  global bstack11ll11ll1_opy_
  global bstack1l1ll111ll_opy_
  global bstack1l1l1l1ll_opy_
  bstack11ll11ll1_opy_ = framework_name
  logger.info(bstack1l1ll11l1_opy_.format(bstack11ll11ll1_opy_.split(bstack1ll11l_opy_ (u"ࠨ࠯ࠪୡ"))[0]))
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    if bstack1ll1l11l1_opy_:
      Service.start = bstack1l1llll1l1_opy_
      Service.stop = bstack11lllll11_opy_
      webdriver.Remote.get = bstack1llll111l_opy_
      WebDriver.close = bstack1ll1lll1l_opy_
      WebDriver.quit = bstack111ll11l1_opy_
      webdriver.Remote.__init__ = bstack11lll1lll_opy_
      WebDriver.getAccessibilityResults = getAccessibilityResults
      WebDriver.get_accessibility_results = getAccessibilityResults
      WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
      WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
      WebDriver.performScan = perform_scan
      WebDriver.perform_scan = perform_scan
    if not bstack1ll1l11l1_opy_ and bstack1l111lll1_opy_.on():
      webdriver.Remote.__init__ = bstack1ll1lllll_opy_
    WebDriver.execute = bstack1lll111l1_opy_
    bstack1l1ll111ll_opy_ = True
  except Exception as e:
    pass
  try:
    if bstack1ll1l11l1_opy_:
      from QWeb.keywords import browser
      browser.close_browser = bstack1llll1111l_opy_
  except Exception as e:
    pass
  bstack1l11ll111_opy_()
  if not bstack1l1ll111ll_opy_:
    bstack1ll1ll111_opy_(bstack1ll11l_opy_ (u"ࠤࡓࡥࡨࡱࡡࡨࡧࡶࠤࡳࡵࡴࠡ࡫ࡱࡷࡹࡧ࡬࡭ࡧࡧࠦୢ"), bstack111lll1l_opy_)
  if bstack1l1l11l1_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      RemoteConnection._get_proxy_url = bstack1l111llll_opy_
    except Exception as e:
      logger.error(bstack11ll1111l_opy_.format(str(e)))
  if bstack1lll1ll11l_opy_():
    bstack1ll1ll11_opy_(CONFIG, logger)
  if (bstack1ll11l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩୣ") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        if CONFIG.get(bstack1ll11l_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪ୤"), False):
          bstack111111l1_opy_(bstack1l1ll1l1l_opy_)
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack1lllll111l_opy_
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCache.close = bstack111lllll_opy_
      except Exception as e:
        logger.warn(bstack1lllll1l1l_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import bstack1ll11l11l1_opy_
        bstack1ll11l11l1_opy_.close = bstack11111ll1_opy_
      except Exception as e:
        logger.debug(bstack1llll1llll_opy_ + str(e))
    except Exception as e:
      bstack1ll1ll111_opy_(e, bstack1lllll1l1l_opy_)
    Output.start_test = bstack1l1l1l11_opy_
    Output.end_test = bstack1lllllll11_opy_
    TestStatus.__init__ = bstack1llll111_opy_
    QueueItem.__init__ = bstack11l1111l1_opy_
    pabot._create_items = bstack1ll1l1l111_opy_
    try:
      from pabot import __version__ as bstack1lll1l111_opy_
      if version.parse(bstack1lll1l111_opy_) >= version.parse(bstack1ll11l_opy_ (u"ࠬ࠸࠮࠲࠷࠱࠴ࠬ୥")):
        pabot._run = bstack1l11lll111_opy_
      elif version.parse(bstack1lll1l111_opy_) >= version.parse(bstack1ll11l_opy_ (u"࠭࠲࠯࠳࠶࠲࠵࠭୦")):
        pabot._run = bstack1l1l11l11_opy_
      else:
        pabot._run = bstack1l1l11llll_opy_
    except Exception as e:
      pabot._run = bstack1l1l11llll_opy_
    pabot._create_command_for_execution = bstack111l1111_opy_
    pabot._report_results = bstack11l11l11l_opy_
  if bstack1ll11l_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧ୧") in str(framework_name).lower():
    if not bstack1ll1l11l1_opy_:
      return
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1ll1ll111_opy_(e, bstack111ll1l11_opy_)
    Runner.run_hook = bstack11l111ll1_opy_
    Step.run = bstack1111111l1_opy_
  if bstack1ll11l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ୨") in str(framework_name).lower():
    if not bstack1ll1l11l1_opy_:
      return
    try:
      if CONFIG.get(bstack1ll11l_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨ୩"), False):
          bstack111111l1_opy_(bstack1l1ll1l1l_opy_)
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      pytest_selenium.pytest_report_header = bstack1ll111llll_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack1l11111ll_opy_
      Config.getoption = bstack11lll11ll_opy_
    except Exception as e:
      pass
    try:
      from pytest_bdd import reporting
      reporting.runtest_makereport = bstack11l11ll1l_opy_
    except Exception as e:
      pass
def bstack1l1ll1ll11_opy_():
  global CONFIG
  if bstack1ll11l_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ୪") in CONFIG and int(CONFIG[bstack1ll11l_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫ୫")]) > 1:
    logger.warn(bstack11l11lll1_opy_)
def bstack1ll11l1l1l_opy_(arg, bstack11l11111l_opy_, bstack1ll111l1_opy_=None):
  global CONFIG
  global bstack11l1ll1l_opy_
  global bstack111l11111_opy_
  global bstack1ll1l11l1_opy_
  global bstack1l11l111l_opy_
  bstack11lllll1l_opy_ = bstack1ll11l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ୬")
  if bstack11l11111l_opy_ and isinstance(bstack11l11111l_opy_, str):
    bstack11l11111l_opy_ = eval(bstack11l11111l_opy_)
  CONFIG = bstack11l11111l_opy_[bstack1ll11l_opy_ (u"࠭ࡃࡐࡐࡉࡍࡌ࠭୭")]
  bstack11l1ll1l_opy_ = bstack11l11111l_opy_[bstack1ll11l_opy_ (u"ࠧࡉࡗࡅࡣ࡚ࡘࡌࠨ୮")]
  bstack111l11111_opy_ = bstack11l11111l_opy_[bstack1ll11l_opy_ (u"ࠨࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪ୯")]
  bstack1ll1l11l1_opy_ = bstack11l11111l_opy_[bstack1ll11l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠬ୰")]
  bstack1l11l111l_opy_.bstack1l11ll11l_opy_(bstack1ll11l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࠫୱ"), bstack1ll1l11l1_opy_)
  os.environ[bstack1ll11l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭୲")] = bstack11lllll1l_opy_
  os.environ[bstack1ll11l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡕࡎࡇࡋࡊࠫ୳")] = json.dumps(CONFIG)
  os.environ[bstack1ll11l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡎࡕࡃࡡࡘࡖࡑ࠭୴")] = bstack11l1ll1l_opy_
  os.environ[bstack1ll11l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨ୵")] = str(bstack111l11111_opy_)
  os.environ[bstack1ll11l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑ࡛ࡗࡉࡘ࡚࡟ࡑࡎࡘࡋࡎࡔࠧ୶")] = str(True)
  if bstack1llll1l111_opy_(arg, [bstack1ll11l_opy_ (u"ࠩ࠰ࡲࠬ୷"), bstack1ll11l_opy_ (u"ࠪ࠱࠲ࡴࡵ࡮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫ୸")]) != -1:
    os.environ[bstack1ll11l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔ࡞࡚ࡅࡔࡖࡢࡔࡆࡘࡁࡍࡎࡈࡐࠬ୹")] = str(True)
  if len(sys.argv) <= 1:
    logger.critical(bstack1lll11l1ll_opy_)
    return
  bstack1lll111l1l_opy_()
  global bstack1ll111l11l_opy_
  global bstack11l111l11_opy_
  global bstack111l1l1l_opy_
  global bstack111ll1lll_opy_
  global bstack1l1l111l11_opy_
  global bstack1l1l1l1ll_opy_
  global bstack11l111111_opy_
  arg.append(bstack1ll11l_opy_ (u"ࠧ࠳ࡗࠣ୺"))
  arg.append(bstack1ll11l_opy_ (u"ࠨࡩࡨࡰࡲࡶࡪࡀࡍࡰࡦࡸࡰࡪࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡪ࡯ࡳࡳࡷࡺࡥࡥ࠼ࡳࡽࡹ࡫ࡳࡵ࠰ࡓࡽࡹ࡫ࡳࡵ࡙ࡤࡶࡳ࡯࡮ࡨࠤ୻"))
  arg.append(bstack1ll11l_opy_ (u"ࠢ࠮࡙ࠥ୼"))
  arg.append(bstack1ll11l_opy_ (u"ࠣ࡫ࡪࡲࡴࡸࡥ࠻ࡖ࡫ࡩࠥ࡮࡯ࡰ࡭࡬ࡱࡵࡲࠢ୽"))
  global bstack1ll1l11ll_opy_
  global bstack11l1111ll_opy_
  global bstack111111l1l_opy_
  global bstack1l1l1l1111_opy_
  global bstack1ll1lllll1_opy_
  global bstack1lll111lll_opy_
  global bstack1ll1lll1l1_opy_
  global bstack1l11l1l1l1_opy_
  global bstack1l11ll1111_opy_
  global bstack1l1l1ll111_opy_
  global bstack1llllll1l1_opy_
  global bstack1l1ll1111_opy_
  global bstack1111llll_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1ll1l11ll_opy_ = webdriver.Remote.__init__
    bstack11l1111ll_opy_ = WebDriver.quit
    bstack1l11l1l1l1_opy_ = WebDriver.close
    bstack1l11ll1111_opy_ = WebDriver.get
    bstack111111l1l_opy_ = WebDriver.execute
  except Exception as e:
    pass
  if bstack1l1l1ll1ll_opy_(CONFIG) and bstack1llll1l1ll_opy_():
    if bstack1lll1l1ll_opy_() < version.parse(bstack1ll1l1lll_opy_):
      logger.error(bstack1l1lll11l_opy_.format(bstack1lll1l1ll_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack1l1l1ll111_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack11ll1111l_opy_.format(str(e)))
  try:
    from _pytest.config import Config
    bstack1llllll1l1_opy_ = Config.getoption
    from _pytest import runner
    bstack1l1ll1111_opy_ = runner._update_current_test_var
  except Exception as e:
    logger.warn(e, bstack111llll1l_opy_)
  try:
    from pytest_bdd import reporting
    bstack1111llll_opy_ = reporting.runtest_makereport
  except Exception as e:
    logger.debug(bstack1ll11l_opy_ (u"ࠩࡓࡰࡪࡧࡳࡦࠢ࡬ࡲࡸࡺࡡ࡭࡮ࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡱࠣࡶࡺࡴࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹ࡫ࡳࡵࡵࠪ୾"))
  bstack111l1l1l_opy_ = CONFIG.get(bstack1ll11l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ୿"), {}).get(bstack1ll11l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭஀"))
  bstack11l111111_opy_ = True
  bstack1l1llll1_opy_(bstack11l11lll_opy_)
  os.environ[bstack1ll11l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ࠭஁")] = CONFIG[bstack1ll11l_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨஂ")]
  os.environ[bstack1ll11l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪஃ")] = CONFIG[bstack1ll11l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫ஄")]
  os.environ[bstack1ll11l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠬஅ")] = bstack1ll1l11l1_opy_.__str__()
  from _pytest.config import main as bstack1lllll1l11_opy_
  bstack1111ll111_opy_ = []
  try:
    bstack1l1111l11_opy_ = bstack1lllll1l11_opy_(arg)
    if bstack1ll11l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺࠧஆ") in multiprocessing.current_process().__dict__.keys():
      for bstack1l1ll1l11_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1111ll111_opy_.append(bstack1l1ll1l11_opy_)
    try:
      bstack1ll11111ll_opy_ = (bstack1111ll111_opy_, int(bstack1l1111l11_opy_))
      bstack1ll111l1_opy_.append(bstack1ll11111ll_opy_)
    except:
      bstack1ll111l1_opy_.append((bstack1111ll111_opy_, bstack1l1111l11_opy_))
  except Exception as e:
    logger.error(traceback.format_exc())
    bstack1111ll111_opy_.append({bstack1ll11l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩஇ"): bstack1ll11l_opy_ (u"ࠬࡖࡲࡰࡥࡨࡷࡸࠦࠧஈ") + os.environ.get(bstack1ll11l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭உ")), bstack1ll11l_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ஊ"): traceback.format_exc(), bstack1ll11l_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧ஋"): int(os.environ.get(bstack1ll11l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩ஌")))})
    bstack1ll111l1_opy_.append((bstack1111ll111_opy_, 1))
def bstack1l1lllll1_opy_(arg):
  bstack1l1llll1_opy_(bstack1111l111_opy_)
  os.environ[bstack1ll11l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫ஍")] = str(bstack111l11111_opy_)
  from behave.__main__ import main as bstack1l1111lll_opy_
  bstack1l1111lll_opy_(arg)
def bstack111lll11l_opy_():
  logger.info(bstack1lll11l1l_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack1ll11l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪஎ"), help=bstack1ll11l_opy_ (u"ࠬࡍࡥ࡯ࡧࡵࡥࡹ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡣࡰࡰࡩ࡭࡬࠭ஏ"))
  parser.add_argument(bstack1ll11l_opy_ (u"࠭࠭ࡶࠩஐ"), bstack1ll11l_opy_ (u"ࠧ࠮࠯ࡸࡷࡪࡸ࡮ࡢ࡯ࡨࠫ஑"), help=bstack1ll11l_opy_ (u"ࠨ࡛ࡲࡹࡷࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡻࡳࡦࡴࡱࡥࡲ࡫ࠧஒ"))
  parser.add_argument(bstack1ll11l_opy_ (u"ࠩ࠰࡯ࠬஓ"), bstack1ll11l_opy_ (u"ࠪ࠱࠲ࡱࡥࡺࠩஔ"), help=bstack1ll11l_opy_ (u"ࠫ࡞ࡵࡵࡳࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡣࡦࡧࡪࡹࡳࠡ࡭ࡨࡽࠬக"))
  parser.add_argument(bstack1ll11l_opy_ (u"ࠬ࠳ࡦࠨ஖"), bstack1ll11l_opy_ (u"࠭࠭࠮ࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ஗"), help=bstack1ll11l_opy_ (u"࡚ࠧࡱࡸࡶࠥࡺࡥࡴࡶࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭஘"))
  bstack1ll111ll_opy_ = parser.parse_args()
  try:
    bstack1lll1l11l1_opy_ = bstack1ll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡨࡧࡱࡩࡷ࡯ࡣ࠯ࡻࡰࡰ࠳ࡹࡡ࡮ࡲ࡯ࡩࠬங")
    if bstack1ll111ll_opy_.framework and bstack1ll111ll_opy_.framework not in (bstack1ll11l_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩச"), bstack1ll11l_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠶ࠫ஛")):
      bstack1lll1l11l1_opy_ = bstack1ll11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠴ࡹ࡮࡮࠱ࡷࡦࡳࡰ࡭ࡧࠪஜ")
    bstack1l1l111111_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1lll1l11l1_opy_)
    bstack1l1l11l1l1_opy_ = open(bstack1l1l111111_opy_, bstack1ll11l_opy_ (u"ࠬࡸࠧ஝"))
    bstack11l11l1ll_opy_ = bstack1l1l11l1l1_opy_.read()
    bstack1l1l11l1l1_opy_.close()
    if bstack1ll111ll_opy_.username:
      bstack11l11l1ll_opy_ = bstack11l11l1ll_opy_.replace(bstack1ll11l_opy_ (u"࡙࠭ࡐࡗࡕࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ࠭ஞ"), bstack1ll111ll_opy_.username)
    if bstack1ll111ll_opy_.key:
      bstack11l11l1ll_opy_ = bstack11l11l1ll_opy_.replace(bstack1ll11l_opy_ (u"࡚ࠧࡑࡘࡖࡤࡇࡃࡄࡇࡖࡗࡤࡑࡅ࡚ࠩட"), bstack1ll111ll_opy_.key)
    if bstack1ll111ll_opy_.framework:
      bstack11l11l1ll_opy_ = bstack11l11l1ll_opy_.replace(bstack1ll11l_opy_ (u"ࠨ࡛ࡒ࡙ࡗࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩ஠"), bstack1ll111ll_opy_.framework)
    file_name = bstack1ll11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰࠬ஡")
    file_path = os.path.abspath(file_name)
    bstack1l1l1l1lll_opy_ = open(file_path, bstack1ll11l_opy_ (u"ࠪࡻࠬ஢"))
    bstack1l1l1l1lll_opy_.write(bstack11l11l1ll_opy_)
    bstack1l1l1l1lll_opy_.close()
    logger.info(bstack111l1l1ll_opy_)
    try:
      os.environ[bstack1ll11l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭ண")] = bstack1ll111ll_opy_.framework if bstack1ll111ll_opy_.framework != None else bstack1ll11l_opy_ (u"ࠧࠨத")
      config = yaml.safe_load(bstack11l11l1ll_opy_)
      config[bstack1ll11l_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭஥")] = bstack1ll11l_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠭ࡴࡧࡷࡹࡵ࠭஦")
      bstack1l11l1ll1_opy_(bstack11l11ll1_opy_, config)
    except Exception as e:
      logger.debug(bstack1llllll1ll_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack111111lll_opy_.format(str(e)))
def bstack1l11l1ll1_opy_(bstack1ll1ll1l1_opy_, config, bstack1l1l1l1l1_opy_={}):
  global bstack1ll1l11l1_opy_
  global bstack1l111l11_opy_
  if not config:
    return
  bstack1l11ll1l11_opy_ = bstack1l1l1lllll_opy_ if not bstack1ll1l11l1_opy_ else (
    bstack1111llll1_opy_ if bstack1ll11l_opy_ (u"ࠨࡣࡳࡴࠬ஧") in config else bstack1l11l1l1l_opy_)
  bstack1l11llllll_opy_ = False
  bstack1lllllll1_opy_ = False
  if bstack1ll1l11l1_opy_ is True:
      if bstack1ll11l_opy_ (u"ࠩࡤࡴࡵ࠭ந") in config:
          bstack1l11llllll_opy_ = True
      else:
          bstack1lllllll1_opy_ = True
  bstack1l11l1111_opy_ = {
      bstack1ll11l_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪன"): bstack1l111lll1_opy_.bstack1lll11l1l1_opy_(bstack1l111l11_opy_),
      bstack1ll11l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫப"): bstack1ll1lll1ll_opy_.bstack11l11llll_opy_(config),
      bstack1ll11l_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫ஫"): config.get(bstack1ll11l_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬ஬"), False),
      bstack1ll11l_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩ஭"): bstack1lllllll1_opy_,
      bstack1ll11l_opy_ (u"ࠨࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠧம"): bstack1l11llllll_opy_
  }
  data = {
    bstack1ll11l_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫய"): config[bstack1ll11l_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬர")],
    bstack1ll11l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧற"): config[bstack1ll11l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨல")],
    bstack1ll11l_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪள"): bstack1ll1ll1l1_opy_,
    bstack1ll11l_opy_ (u"ࠧࡥࡧࡷࡩࡨࡺࡥࡥࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫழ"): os.environ.get(bstack1ll11l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪவ"), bstack1l111l11_opy_),
    bstack1ll11l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫஶ"): bstack1l1l111l_opy_,
    bstack1ll11l_opy_ (u"ࠪࡳࡵࡺࡩ࡮ࡣ࡯ࡣ࡭ࡻࡢࡠࡷࡵࡰࠬஷ"): bstack11lll1l1_opy_(),
    bstack1ll11l_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠧஸ"): {
      bstack1ll11l_opy_ (u"ࠬࡲࡡ࡯ࡩࡸࡥ࡬࡫࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪஹ"): str(config[bstack1ll11l_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭஺")]) if bstack1ll11l_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧ஻") in config else bstack1ll11l_opy_ (u"ࠣࡷࡱ࡯ࡳࡵࡷ࡯ࠤ஼"),
      bstack1ll11l_opy_ (u"ࠩ࡯ࡥࡳ࡭ࡵࡢࡩࡨ࡚ࡪࡸࡳࡪࡱࡱࠫ஽"): sys.version,
      bstack1ll11l_opy_ (u"ࠪࡶࡪ࡬ࡥࡳࡴࡨࡶࠬா"): bstack1llllll11l_opy_(os.getenv(bstack1ll11l_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐࠨி"), bstack1ll11l_opy_ (u"ࠧࠨீ"))),
      bstack1ll11l_opy_ (u"࠭࡬ࡢࡰࡪࡹࡦ࡭ࡥࠨு"): bstack1ll11l_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧூ"),
      bstack1ll11l_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࠩ௃"): bstack1l11ll1l11_opy_,
      bstack1ll11l_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࡢࡱࡦࡶࠧ௄"): bstack1l11l1111_opy_,
      bstack1ll11l_opy_ (u"ࠪࡸࡪࡹࡴࡩࡷࡥࡣࡺࡻࡩࡥࠩ௅"): os.environ[bstack1ll11l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩெ")],
      bstack1ll11l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨே"): bstack11lll1ll1_opy_(os.environ.get(bstack1ll11l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨை"), bstack1l111l11_opy_)),
      bstack1ll11l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ௉"): config[bstack1ll11l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫொ")] if config[bstack1ll11l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬோ")] else bstack1ll11l_opy_ (u"ࠥࡹࡳࡱ࡮ࡰࡹࡱࠦௌ"),
      bstack1ll11l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ்࠭"): str(config[bstack1ll11l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ௎")]) if bstack1ll11l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ௏") in config else bstack1ll11l_opy_ (u"ࠢࡶࡰ࡮ࡲࡴࡽ࡮ࠣௐ"),
      bstack1ll11l_opy_ (u"ࠨࡱࡶࠫ௑"): sys.platform,
      bstack1ll11l_opy_ (u"ࠩ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠫ௒"): socket.gethostname()
    }
  }
  update(data[bstack1ll11l_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡳࡶࡴࡶࡥࡳࡶ࡬ࡩࡸ࠭௓")], bstack1l1l1l1l1_opy_)
  try:
    response = bstack11l1llll1_opy_(bstack1ll11l_opy_ (u"ࠫࡕࡕࡓࡕࠩ௔"), bstack111l1ll1_opy_(bstack1l1l1l11l1_opy_), data, {
      bstack1ll11l_opy_ (u"ࠬࡧࡵࡵࡪࠪ௕"): (config[bstack1ll11l_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ௖")], config[bstack1ll11l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪௗ")])
    })
    if response:
      logger.debug(bstack1llllll1l_opy_.format(bstack1ll1ll1l1_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack1ll1llllll_opy_.format(str(e)))
def bstack1llllll11l_opy_(framework):
  return bstack1ll11l_opy_ (u"ࠣࡽࢀ࠱ࡵࡿࡴࡩࡱࡱࡥ࡬࡫࡮ࡵ࠱ࡾࢁࠧ௘").format(str(framework), __version__) if framework else bstack1ll11l_opy_ (u"ࠤࡳࡽࡹ࡮࡯࡯ࡣࡪࡩࡳࡺ࠯ࡼࡿࠥ௙").format(
    __version__)
def bstack1lll111l1l_opy_():
  global CONFIG
  global bstack111ll1ll_opy_
  if bool(CONFIG):
    return
  try:
    bstack1l1lll1l1_opy_()
    logger.debug(bstack1ll11l11l_opy_.format(str(CONFIG)))
    bstack111ll1ll_opy_ = bstack1llll1lll1_opy_.bstack111ll1l1_opy_(CONFIG, bstack111ll1ll_opy_)
    bstack1llll1lll_opy_()
  except Exception as e:
    logger.error(bstack1ll11l_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࡸࡴ࠱ࠦࡥࡳࡴࡲࡶ࠿ࠦࠢ௚") + str(e))
    sys.exit(1)
  sys.excepthook = bstack1lll11l1_opy_
  atexit.register(bstack1l1l111lll_opy_)
  signal.signal(signal.SIGINT, bstack1l1l11lll_opy_)
  signal.signal(signal.SIGTERM, bstack1l1l11lll_opy_)
def bstack1lll11l1_opy_(exctype, value, traceback):
  global bstack1l11l1l111_opy_
  try:
    for driver in bstack1l11l1l111_opy_:
      bstack1111ll11_opy_(driver, bstack1ll11l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ௛"), bstack1ll11l_opy_ (u"࡙ࠧࡥࡴࡵ࡬ࡳࡳࠦࡦࡢ࡫࡯ࡩࡩࠦࡷࡪࡶ࡫࠾ࠥࡢ࡮ࠣ௜") + str(value))
  except Exception:
    pass
  bstack111l11lll_opy_(value, True)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack111l11lll_opy_(message=bstack1ll11l_opy_ (u"࠭ࠧ௝"), bstack1l1lllll1l_opy_ = False):
  global CONFIG
  bstack1111lll11_opy_ = bstack1ll11l_opy_ (u"ࠧࡨ࡮ࡲࡦࡦࡲࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠩ௞") if bstack1l1lllll1l_opy_ else bstack1ll11l_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ௟")
  try:
    if message:
      bstack1l1l1l1l1_opy_ = {
        bstack1111lll11_opy_ : str(message)
      }
      bstack1l11l1ll1_opy_(bstack1ll1l11l_opy_, CONFIG, bstack1l1l1l1l1_opy_)
    else:
      bstack1l11l1ll1_opy_(bstack1ll1l11l_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack1l11lll1_opy_.format(str(e)))
def bstack1ll111111l_opy_(bstack1lll1l11ll_opy_, size):
  bstack1ll11ll1l1_opy_ = []
  while len(bstack1lll1l11ll_opy_) > size:
    bstack11l1ll111_opy_ = bstack1lll1l11ll_opy_[:size]
    bstack1ll11ll1l1_opy_.append(bstack11l1ll111_opy_)
    bstack1lll1l11ll_opy_ = bstack1lll1l11ll_opy_[size:]
  bstack1ll11ll1l1_opy_.append(bstack1lll1l11ll_opy_)
  return bstack1ll11ll1l1_opy_
def bstack1l1lll1l11_opy_(args):
  if bstack1ll11l_opy_ (u"ࠩ࠰ࡱࠬ௠") in args and bstack1ll11l_opy_ (u"ࠪࡴࡩࡨࠧ௡") in args:
    return True
  return False
def run_on_browserstack(bstack1ll11ll1l_opy_=None, bstack1ll111l1_opy_=None, bstack1111l1l1l_opy_=False):
  global CONFIG
  global bstack11l1ll1l_opy_
  global bstack111l11111_opy_
  global bstack1l111l11_opy_
  bstack11lllll1l_opy_ = bstack1ll11l_opy_ (u"ࠫࠬ௢")
  bstack1l1l1llll1_opy_(bstack1l1ll1l111_opy_, logger)
  if bstack1ll11ll1l_opy_ and isinstance(bstack1ll11ll1l_opy_, str):
    bstack1ll11ll1l_opy_ = eval(bstack1ll11ll1l_opy_)
  if bstack1ll11ll1l_opy_:
    CONFIG = bstack1ll11ll1l_opy_[bstack1ll11l_opy_ (u"ࠬࡉࡏࡏࡈࡌࡋࠬ௣")]
    bstack11l1ll1l_opy_ = bstack1ll11ll1l_opy_[bstack1ll11l_opy_ (u"࠭ࡈࡖࡄࡢ࡙ࡗࡒࠧ௤")]
    bstack111l11111_opy_ = bstack1ll11ll1l_opy_[bstack1ll11l_opy_ (u"ࠧࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩ௥")]
    bstack1l11l111l_opy_.bstack1l11ll11l_opy_(bstack1ll11l_opy_ (u"ࠨࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪ௦"), bstack111l11111_opy_)
    bstack11lllll1l_opy_ = bstack1ll11l_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ௧")
  if not bstack1111l1l1l_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack1lll11l1ll_opy_)
      return
    if sys.argv[1] == bstack1ll11l_opy_ (u"ࠪ࠱࠲ࡼࡥࡳࡵ࡬ࡳࡳ࠭௨") or sys.argv[1] == bstack1ll11l_opy_ (u"ࠫ࠲ࡼࠧ௩"):
      logger.info(bstack1ll11l_opy_ (u"ࠬࡈࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡕࡿࡴࡩࡱࡱࠤࡘࡊࡋࠡࡸࡾࢁࠬ௪").format(__version__))
      return
    if sys.argv[1] == bstack1ll11l_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬ௫"):
      bstack111lll11l_opy_()
      return
  args = sys.argv
  bstack1lll111l1l_opy_()
  global bstack1ll111l11l_opy_
  global bstack1111l11ll_opy_
  global bstack11l111111_opy_
  global bstack1lll1ll111_opy_
  global bstack11l111l11_opy_
  global bstack111l1l1l_opy_
  global bstack111ll1lll_opy_
  global bstack1l1llll1ll_opy_
  global bstack1l1l111l11_opy_
  global bstack1l1l1l1ll_opy_
  global bstack1ll1llll1l_opy_
  bstack1111l11ll_opy_ = len(CONFIG.get(bstack1ll11l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ௬"), []))
  if not bstack11lllll1l_opy_:
    if args[1] == bstack1ll11l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ௭") or args[1] == bstack1ll11l_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠵ࠪ௮"):
      bstack11lllll1l_opy_ = bstack1ll11l_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ௯")
      args = args[2:]
    elif args[1] == bstack1ll11l_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ௰"):
      bstack11lllll1l_opy_ = bstack1ll11l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ௱")
      args = args[2:]
    elif args[1] == bstack1ll11l_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬ௲"):
      bstack11lllll1l_opy_ = bstack1ll11l_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭௳")
      args = args[2:]
    elif args[1] == bstack1ll11l_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩ௴"):
      bstack11lllll1l_opy_ = bstack1ll11l_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪ௵")
      args = args[2:]
    elif args[1] == bstack1ll11l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ௶"):
      bstack11lllll1l_opy_ = bstack1ll11l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ௷")
      args = args[2:]
    elif args[1] == bstack1ll11l_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ௸"):
      bstack11lllll1l_opy_ = bstack1ll11l_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭௹")
      args = args[2:]
    else:
      if not bstack1ll11l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ௺") in CONFIG or str(CONFIG[bstack1ll11l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ௻")]).lower() in [bstack1ll11l_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ௼"), bstack1ll11l_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠶ࠫ௽")]:
        bstack11lllll1l_opy_ = bstack1ll11l_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ௾")
        args = args[1:]
      elif str(CONFIG[bstack1ll11l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ௿")]).lower() == bstack1ll11l_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬఀ"):
        bstack11lllll1l_opy_ = bstack1ll11l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ఁ")
        args = args[1:]
      elif str(CONFIG[bstack1ll11l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫం")]).lower() == bstack1ll11l_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨః"):
        bstack11lllll1l_opy_ = bstack1ll11l_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩఄ")
        args = args[1:]
      elif str(CONFIG[bstack1ll11l_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧఅ")]).lower() == bstack1ll11l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬఆ"):
        bstack11lllll1l_opy_ = bstack1ll11l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ఇ")
        args = args[1:]
      elif str(CONFIG[bstack1ll11l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪఈ")]).lower() == bstack1ll11l_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨఉ"):
        bstack11lllll1l_opy_ = bstack1ll11l_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩఊ")
        args = args[1:]
      else:
        os.environ[bstack1ll11l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬఋ")] = bstack11lllll1l_opy_
        bstack11l11l1l_opy_(bstack1lllllll1l_opy_)
  os.environ[bstack1ll11l_opy_ (u"ࠫࡋࡘࡁࡎࡇ࡚ࡓࡗࡑ࡟ࡖࡕࡈࡈࠬఌ")] = bstack11lllll1l_opy_
  bstack1l111l11_opy_ = bstack11lllll1l_opy_
  global bstack111111l11_opy_
  if bstack1ll11ll1l_opy_:
    try:
      os.environ[bstack1ll11l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧ఍")] = bstack11lllll1l_opy_
      bstack1l11l1ll1_opy_(bstack1ll1ll11l1_opy_, CONFIG)
    except Exception as e:
      logger.debug(bstack1l11lll1_opy_.format(str(e)))
  global bstack1ll1l11ll_opy_
  global bstack11l1111ll_opy_
  global bstack1l1l1ll1l_opy_
  global bstack1l1llll1l_opy_
  global bstack1l1ll1lll1_opy_
  global bstack11llll11l_opy_
  global bstack1l1l1l1111_opy_
  global bstack1ll1lllll1_opy_
  global bstack1llll11111_opy_
  global bstack1lll111lll_opy_
  global bstack1ll1lll1l1_opy_
  global bstack1l11l1l1l1_opy_
  global bstack1llll1l11l_opy_
  global bstack1lll111111_opy_
  global bstack1l11ll1111_opy_
  global bstack1l1l1ll111_opy_
  global bstack1llllll1l1_opy_
  global bstack1l1ll1111_opy_
  global bstack1ll111l11_opy_
  global bstack1111llll_opy_
  global bstack111111l1l_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack1ll1l11ll_opy_ = webdriver.Remote.__init__
    bstack11l1111ll_opy_ = WebDriver.quit
    bstack1l11l1l1l1_opy_ = WebDriver.close
    bstack1l11ll1111_opy_ = WebDriver.get
    bstack111111l1l_opy_ = WebDriver.execute
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack111111l11_opy_ = Popen.__init__
  except Exception as e:
    pass
  try:
    global bstack1lllll111_opy_
    from QWeb.keywords import browser
    bstack1lllll111_opy_ = browser.close_browser
  except Exception as e:
    pass
  if bstack1l1l1ll1ll_opy_(CONFIG) and bstack1llll1l1ll_opy_():
    if bstack1lll1l1ll_opy_() < version.parse(bstack1ll1l1lll_opy_):
      logger.error(bstack1l1lll11l_opy_.format(bstack1lll1l1ll_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack1l1l1ll111_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack11ll1111l_opy_.format(str(e)))
  if not CONFIG.get(bstack1ll11l_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡁࡶࡶࡲࡇࡦࡶࡴࡶࡴࡨࡐࡴ࡭ࡳࠨఎ"), False) and not bstack1ll11ll1l_opy_:
    logger.info(bstack1l1ll11l11_opy_)
  if bstack11lllll1l_opy_ != bstack1ll11l_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧఏ") or (bstack11lllll1l_opy_ == bstack1ll11l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨఐ") and not bstack1ll11ll1l_opy_):
    bstack1llll111ll_opy_()
  if (bstack11lllll1l_opy_ in [bstack1ll11l_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨ఑"), bstack1ll11l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩఒ"), bstack1ll11l_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬఓ")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCreator._get_ff_profile = bstack1lllll111l_opy_
        bstack11llll11l_opy_ = WebDriverCache.close
      except Exception as e:
        logger.warn(bstack1lllll1l1l_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import bstack1ll11l11l1_opy_
        bstack1l1ll1lll1_opy_ = bstack1ll11l11l1_opy_.close
      except Exception as e:
        logger.debug(bstack1llll1llll_opy_ + str(e))
    except Exception as e:
      bstack1ll1ll111_opy_(e, bstack1lllll1l1l_opy_)
    if bstack11lllll1l_opy_ != bstack1ll11l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭ఔ"):
      bstack1ll1l1l1_opy_()
    bstack1l1l1ll1l_opy_ = Output.start_test
    bstack1l1llll1l_opy_ = Output.end_test
    bstack1l1l1l1111_opy_ = TestStatus.__init__
    bstack1llll11111_opy_ = pabot._run
    bstack1lll111lll_opy_ = QueueItem.__init__
    bstack1ll1lll1l1_opy_ = pabot._create_command_for_execution
    bstack1ll111l11_opy_ = pabot._report_results
  if bstack11lllll1l_opy_ == bstack1ll11l_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭క"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack1ll1ll111_opy_(e, bstack111ll1l11_opy_)
    bstack1llll1l11l_opy_ = Runner.run_hook
    bstack1lll111111_opy_ = Step.run
  if bstack11lllll1l_opy_ == bstack1ll11l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧఖ"):
    try:
      from _pytest.config import Config
      bstack1llllll1l1_opy_ = Config.getoption
      from _pytest import runner
      bstack1l1ll1111_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warn(e, bstack111llll1l_opy_)
    try:
      from pytest_bdd import reporting
      bstack1111llll_opy_ = reporting.runtest_makereport
    except Exception as e:
      logger.debug(bstack1ll11l_opy_ (u"ࠨࡒ࡯ࡩࡦࡹࡥࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡰࠢࡵࡹࡳࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡪࡹࡴࡴࠩగ"))
  try:
    framework_name = bstack1ll11l_opy_ (u"ࠩࡕࡳࡧࡵࡴࠨఘ") if bstack11lllll1l_opy_ in [bstack1ll11l_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩఙ"), bstack1ll11l_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪచ"), bstack1ll11l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭ఛ")] else bstack11ll11l11_opy_(bstack11lllll1l_opy_)
    bstack1l111lll1_opy_.launch(CONFIG, {
      bstack1ll11l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࠧజ"): bstack1ll11l_opy_ (u"ࠧࡼ࠲ࢀ࠱ࡨࡻࡣࡶ࡯ࡥࡩࡷ࠭ఝ").format(framework_name) if bstack11lllll1l_opy_ == bstack1ll11l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨఞ") and bstack1ll11l1ll_opy_() else framework_name,
      bstack1ll11l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ట"): bstack11lll1ll1_opy_(framework_name),
      bstack1ll11l_opy_ (u"ࠪࡷࡩࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨఠ"): __version__,
      bstack1ll11l_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡶࡵࡨࡨࠬడ"): bstack11lllll1l_opy_
    })
  except Exception as e:
    logger.debug(bstack111l1lll_opy_.format(bstack1ll11l_opy_ (u"ࠬࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬఢ"), str(e)))
  if bstack11lllll1l_opy_ in bstack1lll1l1l1l_opy_:
    try:
      framework_name = bstack1ll11l_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬణ") if bstack11lllll1l_opy_ in [bstack1ll11l_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭త"), bstack1ll11l_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧథ")] else bstack11lllll1l_opy_
      if bstack1ll1l11l1_opy_ and bstack1ll11l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩద") in CONFIG and CONFIG[bstack1ll11l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪధ")] == True:
        if bstack1ll11l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫన") in CONFIG:
          os.environ[bstack1ll11l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭఩")] = os.getenv(bstack1ll11l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧప"), json.dumps(CONFIG[bstack1ll11l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧఫ")]))
          CONFIG[bstack1ll11l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨబ")].pop(bstack1ll11l_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧభ"), None)
          CONFIG[bstack1ll11l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪమ")].pop(bstack1ll11l_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩయ"), None)
        bstack1l1ll11l_opy_, bstack11111l1l_opy_ = bstack1ll1lll1ll_opy_.bstack1ll11l11_opy_(CONFIG, bstack11lllll1l_opy_, bstack11lll1ll1_opy_(framework_name), str(bstack1lll1l1ll_opy_()))
        if not bstack1l1ll11l_opy_ is None:
          os.environ[bstack1ll11l_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪర")] = bstack1l1ll11l_opy_
          os.environ[bstack1ll11l_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡕࡇࡖࡘࡤࡘࡕࡏࡡࡌࡈࠬఱ")] = str(bstack11111l1l_opy_)
    except Exception as e:
      logger.debug(bstack111l1lll_opy_.format(bstack1ll11l_opy_ (u"ࠧࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧల"), str(e)))
  if bstack11lllll1l_opy_ == bstack1ll11l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨళ"):
    bstack11l111111_opy_ = True
    if bstack1ll11ll1l_opy_ and bstack1111l1l1l_opy_:
      bstack111l1l1l_opy_ = CONFIG.get(bstack1ll11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ఴ"), {}).get(bstack1ll11l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬవ"))
      bstack1l1llll1_opy_(bstack11l1l111_opy_)
    elif bstack1ll11ll1l_opy_:
      bstack111l1l1l_opy_ = CONFIG.get(bstack1ll11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨశ"), {}).get(bstack1ll11l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧష"))
      global bstack1l11l1l111_opy_
      try:
        if bstack1l1lll1l11_opy_(bstack1ll11ll1l_opy_[bstack1ll11l_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩస")]) and multiprocessing.current_process().name == bstack1ll11l_opy_ (u"ࠧ࠱ࠩహ"):
          bstack1ll11ll1l_opy_[bstack1ll11l_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ఺")].remove(bstack1ll11l_opy_ (u"ࠩ࠰ࡱࠬ఻"))
          bstack1ll11ll1l_opy_[bstack1ll11l_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ఼࠭")].remove(bstack1ll11l_opy_ (u"ࠫࡵࡪࡢࠨఽ"))
          bstack1ll11ll1l_opy_[bstack1ll11l_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨా")] = bstack1ll11ll1l_opy_[bstack1ll11l_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩి")][0]
          with open(bstack1ll11ll1l_opy_[bstack1ll11l_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪీ")], bstack1ll11l_opy_ (u"ࠨࡴࠪు")) as f:
            bstack111l111l1_opy_ = f.read()
          bstack1ll111l1l1_opy_ = bstack1ll11l_opy_ (u"ࠤࠥࠦ࡫ࡸ࡯࡮ࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡵࡧ࡯ࠥ࡯࡭ࡱࡱࡵࡸࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣ࡮ࡴࡩࡵ࡫ࡤࡰ࡮ࢀࡥ࠼ࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠ࡫ࡱ࡭ࡹ࡯ࡡ࡭࡫ࡽࡩ࠭ࢁࡽࠪ࠽ࠣࡪࡷࡵ࡭ࠡࡲࡧࡦࠥ࡯࡭ࡱࡱࡵࡸࠥࡖࡤࡣ࠽ࠣࡳ࡬ࡥࡤࡣࠢࡀࠤࡕࡪࡢ࠯ࡦࡲࡣࡧࡸࡥࡢ࡭࠾ࠎࡩ࡫ࡦࠡ࡯ࡲࡨࡤࡨࡲࡦࡣ࡮ࠬࡸ࡫࡬ࡧ࠮ࠣࡥࡷ࡭ࠬࠡࡶࡨࡱࡵࡵࡲࡢࡴࡼࠤࡂࠦ࠰ࠪ࠼ࠍࠤࠥࡺࡲࡺ࠼ࠍࠤࠥࠦࠠࡢࡴࡪࠤࡂࠦࡳࡵࡴࠫ࡭ࡳࡺࠨࡢࡴࡪ࠭࠰࠷࠰ࠪࠌࠣࠤࡪࡾࡣࡦࡲࡷࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡢࡵࠣࡩ࠿ࠐࠠࠡࠢࠣࡴࡦࡹࡳࠋࠢࠣࡳ࡬ࡥࡤࡣࠪࡶࡩࡱ࡬ࠬࡢࡴࡪ࠰ࡹ࡫࡭ࡱࡱࡵࡥࡷࡿࠩࠋࡒࡧࡦ࠳ࡪ࡯ࡠࡤࠣࡁࠥࡳ࡯ࡥࡡࡥࡶࡪࡧ࡫ࠋࡒࡧࡦ࠳ࡪ࡯ࡠࡤࡵࡩࡦࡱࠠ࠾ࠢࡰࡳࡩࡥࡢࡳࡧࡤ࡯ࠏࡖࡤࡣࠪࠬ࠲ࡸ࡫ࡴࡠࡶࡵࡥࡨ࡫ࠨࠪ࡞ࡱࠦࠧࠨూ").format(str(bstack1ll11ll1l_opy_))
          bstack1ll111ll1l_opy_ = bstack1ll111l1l1_opy_ + bstack111l111l1_opy_
          bstack111l111l_opy_ = bstack1ll11ll1l_opy_[bstack1ll11l_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ృ")] + bstack1ll11l_opy_ (u"ࠫࡤࡨࡳࡵࡣࡦ࡯ࡤࡺࡥ࡮ࡲ࠱ࡴࡾ࠭ౄ")
          with open(bstack111l111l_opy_, bstack1ll11l_opy_ (u"ࠬࡽࠧ౅")):
            pass
          with open(bstack111l111l_opy_, bstack1ll11l_opy_ (u"ࠨࡷࠬࠤె")) as f:
            f.write(bstack1ll111ll1l_opy_)
          import subprocess
          bstack1llll111l1_opy_ = subprocess.run([bstack1ll11l_opy_ (u"ࠢࡱࡻࡷ࡬ࡴࡴࠢే"), bstack111l111l_opy_])
          if os.path.exists(bstack111l111l_opy_):
            os.unlink(bstack111l111l_opy_)
          os._exit(bstack1llll111l1_opy_.returncode)
        else:
          if bstack1l1lll1l11_opy_(bstack1ll11ll1l_opy_[bstack1ll11l_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫై")]):
            bstack1ll11ll1l_opy_[bstack1ll11l_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ౉")].remove(bstack1ll11l_opy_ (u"ࠪ࠱ࡲ࠭ొ"))
            bstack1ll11ll1l_opy_[bstack1ll11l_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧో")].remove(bstack1ll11l_opy_ (u"ࠬࡶࡤࡣࠩౌ"))
            bstack1ll11ll1l_opy_[bstack1ll11l_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦ్ࠩ")] = bstack1ll11ll1l_opy_[bstack1ll11l_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ౎")][0]
          bstack1l1llll1_opy_(bstack11l1l111_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack1ll11ll1l_opy_[bstack1ll11l_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ౏")])))
          sys.argv = sys.argv[2:]
          mod_globals = globals()
          mod_globals[bstack1ll11l_opy_ (u"ࠩࡢࡣࡳࡧ࡭ࡦࡡࡢࠫ౐")] = bstack1ll11l_opy_ (u"ࠪࡣࡤࡳࡡࡪࡰࡢࡣࠬ౑")
          mod_globals[bstack1ll11l_opy_ (u"ࠫࡤࡥࡦࡪ࡮ࡨࡣࡤ࠭౒")] = os.path.abspath(bstack1ll11ll1l_opy_[bstack1ll11l_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ౓")])
          exec(open(bstack1ll11ll1l_opy_[bstack1ll11l_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩ౔")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack1ll11l_opy_ (u"ࠧࡄࡣࡸ࡫࡭ࡺࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰ࠽ࠤࢀࢃౕࠧ").format(str(e)))
          for driver in bstack1l11l1l111_opy_:
            bstack1ll111l1_opy_.append({
              bstack1ll11l_opy_ (u"ࠨࡰࡤࡱࡪౖ࠭"): bstack1ll11ll1l_opy_[bstack1ll11l_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ౗")],
              bstack1ll11l_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩౘ"): str(e),
              bstack1ll11l_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪౙ"): multiprocessing.current_process().name
            })
            bstack1111ll11_opy_(driver, bstack1ll11l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬౚ"), bstack1ll11l_opy_ (u"ࠨࡓࡦࡵࡶ࡭ࡴࡴࠠࡧࡣ࡬ࡰࡪࡪࠠࡸ࡫ࡷ࡬࠿ࠦ࡜࡯ࠤ౛") + str(e))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack1l11l1l111_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      percy.init(bstack111l11111_opy_, CONFIG, logger)
      bstack1111lll1_opy_()
      bstack1l1ll1ll11_opy_()
      bstack11l11111l_opy_ = {
        bstack1ll11l_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪ౜"): args[0],
        bstack1ll11l_opy_ (u"ࠨࡅࡒࡒࡋࡏࡇࠨౝ"): CONFIG,
        bstack1ll11l_opy_ (u"ࠩࡋ࡙ࡇࡥࡕࡓࡎࠪ౞"): bstack11l1ll1l_opy_,
        bstack1ll11l_opy_ (u"ࠪࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬ౟"): bstack111l11111_opy_
      }
      percy.bstack1lll11lll1_opy_()
      if bstack1ll11l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧౠ") in CONFIG:
        bstack11lll11l1_opy_ = []
        manager = multiprocessing.Manager()
        bstack11l1l11l1_opy_ = manager.list()
        if bstack1l1lll1l11_opy_(args):
          for index, platform in enumerate(CONFIG[bstack1ll11l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨౡ")]):
            if index == 0:
              bstack11l11111l_opy_[bstack1ll11l_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩౢ")] = args
            bstack11lll11l1_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack11l11111l_opy_, bstack11l1l11l1_opy_)))
        else:
          for index, platform in enumerate(CONFIG[bstack1ll11l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪౣ")]):
            bstack11lll11l1_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack11l11111l_opy_, bstack11l1l11l1_opy_)))
        for t in bstack11lll11l1_opy_:
          t.start()
        for t in bstack11lll11l1_opy_:
          t.join()
        bstack1l1llll1ll_opy_ = list(bstack11l1l11l1_opy_)
      else:
        if bstack1l1lll1l11_opy_(args):
          bstack11l11111l_opy_[bstack1ll11l_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ౤")] = args
          test = multiprocessing.Process(name=str(0),
                                         target=run_on_browserstack, args=(bstack11l11111l_opy_,))
          test.start()
          test.join()
        else:
          bstack1l1llll1_opy_(bstack11l1l111_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack1ll11l_opy_ (u"ࠩࡢࡣࡳࡧ࡭ࡦࡡࡢࠫ౥")] = bstack1ll11l_opy_ (u"ࠪࡣࡤࡳࡡࡪࡰࡢࡣࠬ౦")
          mod_globals[bstack1ll11l_opy_ (u"ࠫࡤࡥࡦࡪ࡮ࡨࡣࡤ࠭౧")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack11lllll1l_opy_ == bstack1ll11l_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫ౨") or bstack11lllll1l_opy_ == bstack1ll11l_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ౩"):
    percy.init(bstack111l11111_opy_, CONFIG, logger)
    percy.bstack1lll11lll1_opy_()
    try:
      from pabot import pabot
    except Exception as e:
      bstack1ll1ll111_opy_(e, bstack1lllll1l1l_opy_)
    bstack1111lll1_opy_()
    bstack1l1llll1_opy_(bstack1ll11l1111_opy_)
    if bstack1ll1l11l1_opy_ and bstack1ll11l_opy_ (u"ࠧ࠮࠯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬ౪") in args:
      i = args.index(bstack1ll11l_opy_ (u"ࠨ࠯࠰ࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭౫"))
      args.pop(i)
      args.pop(i)
    if bstack1ll1l11l1_opy_:
      args.insert(0, str(bstack1ll111l11l_opy_))
      args.insert(0, str(bstack1ll11l_opy_ (u"ࠩ࠰࠱ࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧ౬")))
    if bstack1l111lll1_opy_.on():
      try:
        from robot.run import USAGE
        from robot.utils import ArgumentParser
        from pabot.arguments import _parse_pabot_args
        bstack111lll111_opy_, pabot_args = _parse_pabot_args(args)
        opts, bstack11ll111l_opy_ = ArgumentParser(
            USAGE,
            auto_pythonpath=False,
            auto_argumentfile=True,
            env_options=bstack1ll11l_opy_ (u"ࠥࡖࡔࡈࡏࡕࡡࡒࡔ࡙ࡏࡏࡏࡕࠥ౭"),
        ).parse_args(bstack111lll111_opy_)
        bstack1ll1ll11l_opy_ = args.index(bstack111lll111_opy_[0]) if len(bstack111lll111_opy_) > 0 else len(args)
        args.insert(bstack1ll1ll11l_opy_, str(bstack1ll11l_opy_ (u"ࠫ࠲࠳࡬ࡪࡵࡷࡩࡳ࡫ࡲࠨ౮")))
        args.insert(bstack1ll1ll11l_opy_ + 1, str(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1ll11l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡸ࡯ࡣࡱࡷࡣࡱ࡯ࡳࡵࡧࡱࡩࡷ࠴ࡰࡺࠩ౯"))))
        if bstack1l11111l1_opy_(os.environ.get(bstack1ll11l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࠫ౰"))) and str(os.environ.get(bstack1ll11l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࡤ࡚ࡅࡔࡖࡖࠫ౱"), bstack1ll11l_opy_ (u"ࠨࡰࡸࡰࡱ࠭౲"))) != bstack1ll11l_opy_ (u"ࠩࡱࡹࡱࡲࠧ౳"):
          for bstack1lll1ll1ll_opy_ in bstack11ll111l_opy_:
            args.remove(bstack1lll1ll1ll_opy_)
          bstack1lll1l111l_opy_ = os.environ.get(bstack1ll11l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࡠࡖࡈࡗ࡙࡙ࠧ౴")).split(bstack1ll11l_opy_ (u"ࠫ࠱࠭౵"))
          for bstack1llll11l11_opy_ in bstack1lll1l111l_opy_:
            args.append(bstack1llll11l11_opy_)
      except Exception as e:
        logger.error(bstack1ll11l_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡥࡹࡺࡡࡤࡪ࡬ࡲ࡬ࠦ࡬ࡪࡵࡷࡩࡳ࡫ࡲࠡࡨࡲࡶࠥࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽ࠳ࠦࡅࡳࡴࡲࡶࠥ࠳ࠠࠣ౶").format(e))
    pabot.main(args)
  elif bstack11lllll1l_opy_ == bstack1ll11l_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧ౷"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack1ll1ll111_opy_(e, bstack1lllll1l1l_opy_)
    for a in args:
      if bstack1ll11l_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡐࡍࡃࡗࡊࡔࡘࡍࡊࡐࡇࡉ࡝࠭౸") in a:
        bstack11l111l11_opy_ = int(a.split(bstack1ll11l_opy_ (u"ࠨ࠼ࠪ౹"))[1])
      if bstack1ll11l_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡆࡈࡊࡑࡕࡃࡂࡎࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭౺") in a:
        bstack111l1l1l_opy_ = str(a.split(bstack1ll11l_opy_ (u"ࠪ࠾ࠬ౻"))[1])
      if bstack1ll11l_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡇࡑࡏࡁࡓࡉࡖࠫ౼") in a:
        bstack111ll1lll_opy_ = str(a.split(bstack1ll11l_opy_ (u"ࠬࡀࠧ౽"))[1])
    bstack1ll11ll1ll_opy_ = None
    if bstack1ll11l_opy_ (u"࠭࠭࠮ࡤࡶࡸࡦࡩ࡫ࡠ࡫ࡷࡩࡲࡥࡩ࡯ࡦࡨࡼࠬ౾") in args:
      i = args.index(bstack1ll11l_opy_ (u"ࠧ࠮࠯ࡥࡷࡹࡧࡣ࡬ࡡ࡬ࡸࡪࡳ࡟ࡪࡰࡧࡩࡽ࠭౿"))
      args.pop(i)
      bstack1ll11ll1ll_opy_ = args.pop(i)
    if bstack1ll11ll1ll_opy_ is not None:
      global bstack111ll1ll1_opy_
      bstack111ll1ll1_opy_ = bstack1ll11ll1ll_opy_
    bstack1l1llll1_opy_(bstack1ll11l1111_opy_)
    run_cli(args)
    if bstack1ll11l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸࠬಀ") in multiprocessing.current_process().__dict__.keys():
      for bstack1l1ll1l11_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1ll111l1_opy_.append(bstack1l1ll1l11_opy_)
  elif bstack11lllll1l_opy_ == bstack1ll11l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩಁ"):
    percy.init(bstack111l11111_opy_, CONFIG, logger)
    percy.bstack1lll11lll1_opy_()
    bstack1ll1lll111_opy_ = bstack1l1l1l1l11_opy_(args, logger, CONFIG, bstack1ll1l11l1_opy_)
    bstack1ll1lll111_opy_.bstack1l11lll11l_opy_()
    bstack1111lll1_opy_()
    bstack1lll1ll111_opy_ = True
    bstack1l1l1l1ll_opy_ = bstack1ll1lll111_opy_.bstack1l1ll1lll_opy_()
    bstack1ll1lll111_opy_.bstack11l11111l_opy_(bstack11111l1ll_opy_)
    bstack1l1ll11111_opy_ = bstack1ll1lll111_opy_.bstack1l1lllll11_opy_(bstack1ll11l1l1l_opy_, {
      bstack1ll11l_opy_ (u"ࠪࡌ࡚ࡈ࡟ࡖࡔࡏࠫಂ"): bstack11l1ll1l_opy_,
      bstack1ll11l_opy_ (u"ࠫࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭ಃ"): bstack111l11111_opy_,
      bstack1ll11l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨ಄"): bstack1ll1l11l1_opy_
    })
    try:
      bstack1111ll111_opy_, bstack11l1111l_opy_ = map(list, zip(*bstack1l1ll11111_opy_))
      bstack1l1l111l11_opy_ = bstack1111ll111_opy_[0]
      for status_code in bstack11l1111l_opy_:
        if status_code != 0:
          bstack1ll1llll1l_opy_ = status_code
          break
    except Exception as e:
      logger.debug(bstack1ll11l_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡥࡻ࡫ࠠࡦࡴࡵࡳࡷࡹࠠࡢࡰࡧࠤࡸࡺࡡࡵࡷࡶࠤࡨࡵࡤࡦ࠰ࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦ࠺ࠡࡽࢀࠦಅ").format(str(e)))
  elif bstack11lllll1l_opy_ == bstack1ll11l_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧಆ"):
    try:
      from behave.__main__ import main as bstack1l1111lll_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack1ll1ll111_opy_(e, bstack111ll1l11_opy_)
    bstack1111lll1_opy_()
    bstack1lll1ll111_opy_ = True
    bstack11ll1l111_opy_ = 1
    if bstack1ll11l_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨಇ") in CONFIG:
      bstack11ll1l111_opy_ = CONFIG[bstack1ll11l_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩಈ")]
    bstack1llll1l1l_opy_ = int(bstack11ll1l111_opy_) * int(len(CONFIG[bstack1ll11l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ಉ")]))
    config = Configuration(args)
    bstack111llll1_opy_ = config.paths
    if len(bstack111llll1_opy_) == 0:
      import glob
      pattern = bstack1ll11l_opy_ (u"ࠫ࠯࠰࠯ࠫ࠰ࡩࡩࡦࡺࡵࡳࡧࠪಊ")
      bstack11lll111l_opy_ = glob.glob(pattern, recursive=True)
      args.extend(bstack11lll111l_opy_)
      config = Configuration(args)
      bstack111llll1_opy_ = config.paths
    bstack1l1lllllll_opy_ = [os.path.normpath(item) for item in bstack111llll1_opy_]
    bstack1l11lll1ll_opy_ = [os.path.normpath(item) for item in args]
    bstack1ll1l1llll_opy_ = [item for item in bstack1l11lll1ll_opy_ if item not in bstack1l1lllllll_opy_]
    import platform as pf
    if pf.system().lower() == bstack1ll11l_opy_ (u"ࠬࡽࡩ࡯ࡦࡲࡻࡸ࠭ಋ"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack1l1lllllll_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1111ll1l_opy_)))
                    for bstack1111ll1l_opy_ in bstack1l1lllllll_opy_]
    bstack1l1lll11ll_opy_ = []
    for spec in bstack1l1lllllll_opy_:
      bstack11l1l1l1_opy_ = []
      bstack11l1l1l1_opy_ += bstack1ll1l1llll_opy_
      bstack11l1l1l1_opy_.append(spec)
      bstack1l1lll11ll_opy_.append(bstack11l1l1l1_opy_)
    execution_items = []
    for bstack11l1l1l1_opy_ in bstack1l1lll11ll_opy_:
      for index, _ in enumerate(CONFIG[bstack1ll11l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩಌ")]):
        item = {}
        item[bstack1ll11l_opy_ (u"ࠧࡢࡴࡪࠫ಍")] = bstack1ll11l_opy_ (u"ࠨࠢࠪಎ").join(bstack11l1l1l1_opy_)
        item[bstack1ll11l_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨಏ")] = index
        execution_items.append(item)
    bstack1l1ll11lll_opy_ = bstack1ll111111l_opy_(execution_items, bstack1llll1l1l_opy_)
    for execution_item in bstack1l1ll11lll_opy_:
      bstack11lll11l1_opy_ = []
      for item in execution_item:
        bstack11lll11l1_opy_.append(bstack11ll111l1_opy_(name=str(item[bstack1ll11l_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩಐ")]),
                                             target=bstack1l1lllll1_opy_,
                                             args=(item[bstack1ll11l_opy_ (u"ࠫࡦࡸࡧࠨ಑")],)))
      for t in bstack11lll11l1_opy_:
        t.start()
      for t in bstack11lll11l1_opy_:
        t.join()
  else:
    bstack11l11l1l_opy_(bstack1lllllll1l_opy_)
  if not bstack1ll11ll1l_opy_:
    bstack1ll1ll111l_opy_()
  bstack1llll1lll1_opy_.bstack1ll11111l_opy_()
def browserstack_initialize(bstack11ll1ll11_opy_=None):
  run_on_browserstack(bstack11ll1ll11_opy_, None, True)
def bstack1ll1ll111l_opy_():
  global CONFIG
  global bstack1l111l11_opy_
  global bstack1ll1llll1l_opy_
  bstack1l111lll1_opy_.stop()
  bstack1l111lll1_opy_.bstack11lll1111_opy_()
  if bstack1ll1lll1ll_opy_.bstack11l11llll_opy_(CONFIG):
    bstack1ll1lll1ll_opy_.bstack1ll11l1l11_opy_()
  [bstack111l1ll11_opy_, bstack1ll111l111_opy_] = get_build_link()
  if bstack111l1ll11_opy_ is not None and bstack11111llll_opy_() != -1:
    sessions = bstack1ll1l1l11_opy_(bstack111l1ll11_opy_)
    bstack1l1l11111l_opy_(sessions, bstack1ll111l111_opy_)
  if bstack1l111l11_opy_ == bstack1ll11l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬಒ") and bstack1ll1llll1l_opy_ != 0:
    sys.exit(bstack1ll1llll1l_opy_)
def bstack11ll11l11_opy_(bstack1lll1l11l_opy_):
  if bstack1lll1l11l_opy_:
    return bstack1lll1l11l_opy_.capitalize()
  else:
    return bstack1ll11l_opy_ (u"࠭ࠧಓ")
def bstack1l1ll11ll1_opy_(bstack1111ll11l_opy_):
  if bstack1ll11l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬಔ") in bstack1111ll11l_opy_ and bstack1111ll11l_opy_[bstack1ll11l_opy_ (u"ࠨࡰࡤࡱࡪ࠭ಕ")] != bstack1ll11l_opy_ (u"ࠩࠪಖ"):
    return bstack1111ll11l_opy_[bstack1ll11l_opy_ (u"ࠪࡲࡦࡳࡥࠨಗ")]
  else:
    bstack1l1l11l1ll_opy_ = bstack1ll11l_opy_ (u"ࠦࠧಘ")
    if bstack1ll11l_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬಙ") in bstack1111ll11l_opy_ and bstack1111ll11l_opy_[bstack1ll11l_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭ಚ")] != None:
      bstack1l1l11l1ll_opy_ += bstack1111ll11l_opy_[bstack1ll11l_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧಛ")] + bstack1ll11l_opy_ (u"ࠣ࠮ࠣࠦಜ")
      if bstack1111ll11l_opy_[bstack1ll11l_opy_ (u"ࠩࡲࡷࠬಝ")] == bstack1ll11l_opy_ (u"ࠥ࡭ࡴࡹࠢಞ"):
        bstack1l1l11l1ll_opy_ += bstack1ll11l_opy_ (u"ࠦ࡮ࡕࡓࠡࠤಟ")
      bstack1l1l11l1ll_opy_ += (bstack1111ll11l_opy_[bstack1ll11l_opy_ (u"ࠬࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠩಠ")] or bstack1ll11l_opy_ (u"࠭ࠧಡ"))
      return bstack1l1l11l1ll_opy_
    else:
      bstack1l1l11l1ll_opy_ += bstack11ll11l11_opy_(bstack1111ll11l_opy_[bstack1ll11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨಢ")]) + bstack1ll11l_opy_ (u"ࠣࠢࠥಣ") + (
              bstack1111ll11l_opy_[bstack1ll11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫತ")] or bstack1ll11l_opy_ (u"ࠪࠫಥ")) + bstack1ll11l_opy_ (u"ࠦ࠱ࠦࠢದ")
      if bstack1111ll11l_opy_[bstack1ll11l_opy_ (u"ࠬࡵࡳࠨಧ")] == bstack1ll11l_opy_ (u"ࠨࡗࡪࡰࡧࡳࡼࡹࠢನ"):
        bstack1l1l11l1ll_opy_ += bstack1ll11l_opy_ (u"ࠢࡘ࡫ࡱࠤࠧ಩")
      bstack1l1l11l1ll_opy_ += bstack1111ll11l_opy_[bstack1ll11l_opy_ (u"ࠨࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬಪ")] or bstack1ll11l_opy_ (u"ࠩࠪಫ")
      return bstack1l1l11l1ll_opy_
def bstack1lll11l11l_opy_(bstack1lll1llll_opy_):
  if bstack1lll1llll_opy_ == bstack1ll11l_opy_ (u"ࠥࡨࡴࡴࡥࠣಬ"):
    return bstack1ll11l_opy_ (u"ࠫࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࡧࡳࡧࡨࡲࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࡧࡳࡧࡨࡲࠧࡄࡃࡰ࡯ࡳࡰࡪࡺࡥࡥ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧಭ")
  elif bstack1lll1llll_opy_ == bstack1ll11l_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧಮ"):
    return bstack1ll11l_opy_ (u"࠭࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࡴࡨࡨࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࡲࡦࡦࠥࡂࡋࡧࡩ࡭ࡧࡧࡀ࠴࡬࡯࡯ࡶࡁࡀ࠴ࡺࡤ࠿ࠩಯ")
  elif bstack1lll1llll_opy_ == bstack1ll11l_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢರ"):
    return bstack1ll11l_opy_ (u"ࠨ࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽࡫ࡷ࡫ࡥ࡯࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥ࡫ࡷ࡫ࡥ࡯ࠤࡁࡔࡦࡹࡳࡦࡦ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨಱ")
  elif bstack1lll1llll_opy_ == bstack1ll11l_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣಲ"):
    return bstack1ll11l_opy_ (u"ࠪࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿ࡸࡥࡥ࠽ࠥࡂࡁ࡬࡯࡯ࡶࠣࡧࡴࡲ࡯ࡳ࠿ࠥࡶࡪࡪࠢ࠿ࡇࡵࡶࡴࡸ࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬಳ")
  elif bstack1lll1llll_opy_ == bstack1ll11l_opy_ (u"ࠦࡹ࡯࡭ࡦࡱࡸࡸࠧ಴"):
    return bstack1ll11l_opy_ (u"ࠬࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࠤࡧࡨࡥ࠸࠸࠶࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࠦࡩࡪࡧ࠳࠳࠸ࠥࡂ࡙࡯࡭ࡦࡱࡸࡸࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪವ")
  elif bstack1lll1llll_opy_ == bstack1ll11l_opy_ (u"ࠨࡲࡶࡰࡱ࡭ࡳ࡭ࠢಶ"):
    return bstack1ll11l_opy_ (u"ࠧ࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࡥࡰࡦࡩ࡫࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࡥࡰࡦࡩ࡫ࠣࡀࡕࡹࡳࡴࡩ࡯ࡩ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨಷ")
  else:
    return bstack1ll11l_opy_ (u"ࠨ࠾ࡷࡨࠥࡧ࡬ࡪࡩࡱࡁࠧࡩࡥ࡯ࡶࡨࡶࠧࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾ࡧࡲࡡࡤ࡭࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦࡧࡲࡡࡤ࡭ࠥࡂࠬಸ") + bstack11ll11l11_opy_(
      bstack1lll1llll_opy_) + bstack1ll11l_opy_ (u"ࠩ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨಹ")
def bstack1lll1111_opy_(session):
  return bstack1ll11l_opy_ (u"ࠪࡀࡹࡸࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡳࡱࡺࠦࡃࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠠࡴࡧࡶࡷ࡮ࡵ࡮࠮ࡰࡤࡱࡪࠨ࠾࠽ࡣࠣ࡬ࡷ࡫ࡦ࠾ࠤࡾࢁࠧࠦࡴࡢࡴࡪࡩࡹࡃࠢࡠࡤ࡯ࡥࡳࡱࠢ࠿ࡽࢀࡀ࠴ࡧ࠾࠽࠱ࡷࡨࡃࢁࡽࡼࡿ࠿ࡸࡩࠦࡡ࡭࡫ࡪࡲࡂࠨࡣࡦࡰࡷࡩࡷࠨࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࡄࡻࡾ࠾࠲ࡸࡩࡄ࠼ࡵࡦࠣࡥࡱ࡯ࡧ࡯࠿ࠥࡧࡪࡴࡴࡦࡴࠥࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࡁࡿࢂࡂ࠯ࡵࡦࡁࡀࡹࡪࠠࡢ࡮࡬࡫ࡳࡃࠢࡤࡧࡱࡸࡪࡸࠢࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨ࠾ࡼࡿ࠿࠳ࡹࡪ࠾࠽ࡶࡧࠤࡦࡲࡩࡨࡰࡀࠦࡨ࡫࡮ࡵࡧࡵࠦࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࡂࢀࢃ࠼࠰ࡶࡧࡂࡁ࠵ࡴࡳࡀࠪ಺").format(
    session[bstack1ll11l_opy_ (u"ࠫࡵࡻࡢ࡭࡫ࡦࡣࡺࡸ࡬ࠨ಻")], bstack1l1ll11ll1_opy_(session), bstack1lll11l11l_opy_(session[bstack1ll11l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡸࡺࡡࡵࡷࡶ಼ࠫ")]),
    bstack1lll11l11l_opy_(session[bstack1ll11l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ಽ")]),
    bstack11ll11l11_opy_(session[bstack1ll11l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨಾ")] or session[bstack1ll11l_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨಿ")] or bstack1ll11l_opy_ (u"ࠩࠪೀ")) + bstack1ll11l_opy_ (u"ࠥࠤࠧು") + (session[bstack1ll11l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ೂ")] or bstack1ll11l_opy_ (u"ࠬ࠭ೃ")),
    session[bstack1ll11l_opy_ (u"࠭࡯ࡴࠩೄ")] + bstack1ll11l_opy_ (u"ࠢࠡࠤ೅") + session[bstack1ll11l_opy_ (u"ࠨࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬೆ")], session[bstack1ll11l_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫೇ")] or bstack1ll11l_opy_ (u"ࠪࠫೈ"),
    session[bstack1ll11l_opy_ (u"ࠫࡨࡸࡥࡢࡶࡨࡨࡤࡧࡴࠨ೉")] if session[bstack1ll11l_opy_ (u"ࠬࡩࡲࡦࡣࡷࡩࡩࡥࡡࡵࠩೊ")] else bstack1ll11l_opy_ (u"࠭ࠧೋ"))
def bstack1l1l11111l_opy_(sessions, bstack1ll111l111_opy_):
  try:
    bstack1l1l1l1ll1_opy_ = bstack1ll11l_opy_ (u"ࠢࠣೌ")
    if not os.path.exists(bstack1ll1111l1l_opy_):
      os.mkdir(bstack1ll1111l1l_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1ll11l_opy_ (u"ࠨࡣࡶࡷࡪࡺࡳ࠰ࡴࡨࡴࡴࡸࡴ࠯ࡪࡷࡱࡱ್࠭")), bstack1ll11l_opy_ (u"ࠩࡵࠫ೎")) as f:
      bstack1l1l1l1ll1_opy_ = f.read()
    bstack1l1l1l1ll1_opy_ = bstack1l1l1l1ll1_opy_.replace(bstack1ll11l_opy_ (u"ࠪࡿࠪࡘࡅࡔࡗࡏࡘࡘࡥࡃࡐࡗࡑࡘࠪࢃࠧ೏"), str(len(sessions)))
    bstack1l1l1l1ll1_opy_ = bstack1l1l1l1ll1_opy_.replace(bstack1ll11l_opy_ (u"ࠫࢀࠫࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠧࢀࠫ೐"), bstack1ll111l111_opy_)
    bstack1l1l1l1ll1_opy_ = bstack1l1l1l1ll1_opy_.replace(bstack1ll11l_opy_ (u"ࠬࢁࠥࡃࡗࡌࡐࡉࡥࡎࡂࡏࡈࠩࢂ࠭೑"),
                                              sessions[0].get(bstack1ll11l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤࡴࡡ࡮ࡧࠪ೒")) if sessions[0] else bstack1ll11l_opy_ (u"ࠧࠨ೓"))
    with open(os.path.join(bstack1ll1111l1l_opy_, bstack1ll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠭ࡳࡧࡳࡳࡷࡺ࠮ࡩࡶࡰࡰࠬ೔")), bstack1ll11l_opy_ (u"ࠩࡺࠫೕ")) as stream:
      stream.write(bstack1l1l1l1ll1_opy_.split(bstack1ll11l_opy_ (u"ࠪࡿ࡙ࠪࡅࡔࡕࡌࡓࡓ࡙࡟ࡅࡃࡗࡅࠪࢃࠧೖ"))[0])
      for session in sessions:
        stream.write(bstack1lll1111_opy_(session))
      stream.write(bstack1l1l1l1ll1_opy_.split(bstack1ll11l_opy_ (u"ࠫࢀࠫࡓࡆࡕࡖࡍࡔࡔࡓࡠࡆࡄࡘࡆࠫࡽࠨ೗"))[1])
    logger.info(bstack1ll11l_opy_ (u"ࠬࡍࡥ࡯ࡧࡵࡥࡹ࡫ࡤࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡣࡷ࡬ࡰࡩࠦࡡࡳࡶ࡬ࡪࡦࡩࡴࡴࠢࡤࡸࠥࢁࡽࠨ೘").format(bstack1ll1111l1l_opy_));
  except Exception as e:
    logger.debug(bstack1l1l1lll1_opy_.format(str(e)))
def bstack1ll1l1l11_opy_(bstack111l1ll11_opy_):
  global CONFIG
  try:
    host = bstack1ll11l_opy_ (u"࠭ࡡࡱ࡫࠰ࡧࡱࡵࡵࡥࠩ೙") if bstack1ll11l_opy_ (u"ࠧࡢࡲࡳࠫ೚") in CONFIG else bstack1ll11l_opy_ (u"ࠨࡣࡳ࡭ࠬ೛")
    user = CONFIG[bstack1ll11l_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ೜")]
    key = CONFIG[bstack1ll11l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ೝ")]
    bstack1llll1l1_opy_ = bstack1ll11l_opy_ (u"ࠫࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧࠪೞ") if bstack1ll11l_opy_ (u"ࠬࡧࡰࡱࠩ೟") in CONFIG else bstack1ll11l_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨೠ")
    url = bstack1ll11l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡽࢀ࠾ࢀࢃࡀࡼࡿ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡻࡾ࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁ࠴ࡹࡥࡴࡵ࡬ࡳࡳࡹ࠮࡫ࡵࡲࡲࠬೡ").format(user, key, host, bstack1llll1l1_opy_,
                                                                                bstack111l1ll11_opy_)
    headers = {
      bstack1ll11l_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡷࡽࡵ࡫ࠧೢ"): bstack1ll11l_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬೣ"),
    }
    proxies = bstack1lllll11l1_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies)
    if response.json():
      return list(map(lambda session: session[bstack1ll11l_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨ೤")], response.json()))
  except Exception as e:
    logger.debug(bstack11l11l11_opy_.format(str(e)))
def get_build_link():
  global CONFIG
  global bstack1l1l111l_opy_
  try:
    if bstack1ll11l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ೥") in CONFIG:
      host = bstack1ll11l_opy_ (u"ࠬࡧࡰࡪ࠯ࡦࡰࡴࡻࡤࠨ೦") if bstack1ll11l_opy_ (u"࠭ࡡࡱࡲࠪ೧") in CONFIG else bstack1ll11l_opy_ (u"ࠧࡢࡲ࡬ࠫ೨")
      user = CONFIG[bstack1ll11l_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ೩")]
      key = CONFIG[bstack1ll11l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ೪")]
      bstack1llll1l1_opy_ = bstack1ll11l_opy_ (u"ࠪࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦࠩ೫") if bstack1ll11l_opy_ (u"ࠫࡦࡶࡰࠨ೬") in CONFIG else bstack1ll11l_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ೭")
      url = bstack1ll11l_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡼࡿ࠽ࡿࢂࡆࡻࡾ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࢁࡽ࠰ࡤࡸ࡭ࡱࡪࡳ࠯࡬ࡶࡳࡳ࠭೮").format(user, key, host, bstack1llll1l1_opy_)
      headers = {
        bstack1ll11l_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡶࡼࡴࡪ࠭೯"): bstack1ll11l_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫ೰"),
      }
      if bstack1ll11l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫೱ") in CONFIG:
        params = {bstack1ll11l_opy_ (u"ࠪࡲࡦࡳࡥࠨೲ"): CONFIG[bstack1ll11l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧೳ")], bstack1ll11l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ೴"): CONFIG[bstack1ll11l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ೵")]}
      else:
        params = {bstack1ll11l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ೶"): CONFIG[bstack1ll11l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ೷")]}
      proxies = bstack1lllll11l1_opy_(CONFIG, url)
      response = requests.get(url, params=params, headers=headers, proxies=proxies)
      if response.json():
        bstack1lll1l1111_opy_ = response.json()[0][bstack1ll11l_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡢࡶ࡫࡯ࡨࠬ೸")]
        if bstack1lll1l1111_opy_:
          bstack1ll111l111_opy_ = bstack1lll1l1111_opy_[bstack1ll11l_opy_ (u"ࠪࡴࡺࡨ࡬ࡪࡥࡢࡹࡷࡲࠧ೹")].split(bstack1ll11l_opy_ (u"ࠫࡵࡻࡢ࡭࡫ࡦ࠱ࡧࡻࡩ࡭ࡦࠪ೺"))[0] + bstack1ll11l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡷ࠴࠭೻") + bstack1lll1l1111_opy_[
            bstack1ll11l_opy_ (u"࠭ࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩ೼")]
          logger.info(bstack1l11llll11_opy_.format(bstack1ll111l111_opy_))
          bstack1l1l111l_opy_ = bstack1lll1l1111_opy_[bstack1ll11l_opy_ (u"ࠧࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪ೽")]
          bstack1ll1ll1111_opy_ = CONFIG[bstack1ll11l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ೾")]
          if bstack1ll11l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ೿") in CONFIG:
            bstack1ll1ll1111_opy_ += bstack1ll11l_opy_ (u"ࠪࠤࠬഀ") + CONFIG[bstack1ll11l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ഁ")]
          if bstack1ll1ll1111_opy_ != bstack1lll1l1111_opy_[bstack1ll11l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪം")]:
            logger.debug(bstack1l11l1llll_opy_.format(bstack1lll1l1111_opy_[bstack1ll11l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫഃ")], bstack1ll1ll1111_opy_))
          return [bstack1lll1l1111_opy_[bstack1ll11l_opy_ (u"ࠧࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪഄ")], bstack1ll111l111_opy_]
    else:
      logger.warn(bstack1l1l11lll1_opy_)
  except Exception as e:
    logger.debug(bstack111l11ll1_opy_.format(str(e)))
  return [None, None]
def bstack1lll1ll1l1_opy_(url, bstack1ll11llll1_opy_=False):
  global CONFIG
  global bstack1lll1l1l_opy_
  if not bstack1lll1l1l_opy_:
    hostname = bstack1llll1ll_opy_(url)
    is_private = bstack1lll1ll1l_opy_(hostname)
    if (bstack1ll11l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬഅ") in CONFIG and not bstack1l11111l1_opy_(CONFIG[bstack1ll11l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ആ")])) and (is_private or bstack1ll11llll1_opy_):
      bstack1lll1l1l_opy_ = hostname
def bstack1llll1ll_opy_(url):
  return urlparse(url).hostname
def bstack1lll1ll1l_opy_(hostname):
  for bstack1l111111_opy_ in bstack1l111111l_opy_:
    regex = re.compile(bstack1l111111_opy_)
    if regex.match(hostname):
      return True
  return False
def bstack1l1llllll_opy_(key_name):
  return True if key_name in threading.current_thread().__dict__.keys() else False
def getAccessibilityResults(driver):
  global CONFIG
  global bstack11l111l11_opy_
  bstack111l11ll_opy_ = not (bstack1l1l111l1l_opy_(threading.current_thread(), bstack1ll11l_opy_ (u"ࠪ࡭ࡸࡇ࠱࠲ࡻࡗࡩࡸࡺࠧഇ"), None) and bstack1l1l111l1l_opy_(
          threading.current_thread(), bstack1ll11l_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪഈ"), None))
  bstack1lll111l11_opy_ = getattr(driver, bstack1ll11l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡆ࠷࠱ࡺࡕ࡫ࡳࡺࡲࡤࡔࡥࡤࡲࠬഉ"), None) != True
  if not bstack1ll1lll1ll_opy_.bstack11llllll_opy_(CONFIG, bstack11l111l11_opy_) or (bstack1lll111l11_opy_ and bstack111l11ll_opy_):
    logger.warning(bstack1ll11l_opy_ (u"ࠨࡎࡰࡶࠣࡥࡳࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡷࡪࡹࡳࡪࡱࡱ࠰ࠥࡩࡡ࡯ࡰࡲࡸࠥࡸࡥࡵࡴ࡬ࡩࡻ࡫ࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡳࡧࡶࡹࡱࡺࡳ࠯ࠤഊ"))
    return {}
  try:
    logger.debug(bstack1ll11l_opy_ (u"ࠧࡑࡧࡵࡪࡴࡸ࡭ࡪࡰࡪࠤࡸࡩࡡ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡶࡪࡹࡵ࡭ࡶࡶࠫഋ"))
    logger.debug(perform_scan(driver))
    results = driver.execute_async_script(bstack1111l1l1_opy_.bstack1l1ll11ll_opy_)
    return results
  except Exception:
    logger.error(bstack1ll11l_opy_ (u"ࠣࡐࡲࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠥࡽࡥࡳࡧࠣࡪࡴࡻ࡮ࡥ࠰ࠥഌ"))
    return {}
def getAccessibilityResultsSummary(driver):
  global CONFIG
  global bstack11l111l11_opy_
  bstack111l11ll_opy_ = not (bstack1l1l111l1l_opy_(threading.current_thread(), bstack1ll11l_opy_ (u"ࠩ࡬ࡷࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭഍"), None) and bstack1l1l111l1l_opy_(
          threading.current_thread(), bstack1ll11l_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩഎ"), None))
  bstack1lll111l11_opy_ = getattr(driver, bstack1ll11l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡅ࠶࠷ࡹࡔࡪࡲࡹࡱࡪࡓࡤࡣࡱࠫഏ"), None) != True
  if not bstack1ll1lll1ll_opy_.bstack11llllll_opy_(CONFIG, bstack11l111l11_opy_) or (bstack1lll111l11_opy_ and bstack111l11ll_opy_):
    logger.warning(bstack1ll11l_opy_ (u"ࠧࡔ࡯ࡵࠢࡤࡲࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡶࡩࡸࡹࡩࡰࡰ࠯ࠤࡨࡧ࡮࡯ࡱࡷࠤࡷ࡫ࡴࡳ࡫ࡨࡺࡪࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡲࡦࡵࡸࡰࡹࡹࠠࡴࡷࡰࡱࡦࡸࡹ࠯ࠤഐ"))
    return {}
  try:
    logger.debug(bstack1ll11l_opy_ (u"࠭ࡐࡦࡴࡩࡳࡷࡳࡩ࡯ࡩࠣࡷࡨࡧ࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡵࡩࡸࡻ࡬ࡵࡵࠣࡷࡺࡳ࡭ࡢࡴࡼࠫ഑"))
    logger.debug(perform_scan(driver))
    bstack1l1l11l111_opy_ = driver.execute_async_script(bstack1111l1l1_opy_.bstack1ll11ll11l_opy_)
    return bstack1l1l11l111_opy_
  except Exception:
    logger.error(bstack1ll11l_opy_ (u"ࠢࡏࡱࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡺࡳ࡭ࡢࡴࡼࠤࡼࡧࡳࠡࡨࡲࡹࡳࡪ࠮ࠣഒ"))
    return {}
def perform_scan(driver, *args, **kwargs):
  global CONFIG
  global bstack11l111l11_opy_
  bstack111l11ll_opy_ = not (bstack1l1l111l1l_opy_(threading.current_thread(), bstack1ll11l_opy_ (u"ࠨ࡫ࡶࡅ࠶࠷ࡹࡕࡧࡶࡸࠬഓ"), None) and bstack1l1l111l1l_opy_(
          threading.current_thread(), bstack1ll11l_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨഔ"), None))
  bstack1lll111l11_opy_ = getattr(driver, bstack1ll11l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡄ࠵࠶ࡿࡓࡩࡱࡸࡰࡩ࡙ࡣࡢࡰࠪക"), None) != True
  if not bstack1ll1lll1ll_opy_.bstack11llllll_opy_(CONFIG, bstack11l111l11_opy_) or (bstack1lll111l11_opy_ and bstack111l11ll_opy_):
    logger.warning(bstack1ll11l_opy_ (u"ࠦࡓࡵࡴࠡࡣࡱࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡵࡨࡷࡸ࡯࡯࡯࠮ࠣࡧࡦࡴ࡮ࡰࡶࠣࡶࡺࡴࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡴࡥࡤࡲ࠳ࠨഖ"))
    return {}
  try:
    bstack11111111l_opy_ = driver.execute_async_script(bstack1111l1l1_opy_.perform_scan, {bstack1ll11l_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࠬഗ"): kwargs.get(bstack1ll11l_opy_ (u"࠭ࡤࡳ࡫ࡹࡩࡷࡥࡣࡰ࡯ࡰࡥࡳࡪࠧഘ"), None) or bstack1ll11l_opy_ (u"ࠧࠨങ")})
    return bstack11111111l_opy_
  except Exception:
    logger.error(bstack1ll11l_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡷࡻ࡮ࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡵࡦࡥࡳ࠴ࠢച"))
    return {}