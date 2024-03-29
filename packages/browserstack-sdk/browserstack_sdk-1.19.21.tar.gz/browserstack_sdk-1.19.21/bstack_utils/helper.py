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
import datetime
import json
import os
import platform
import re
import subprocess
import traceback
import tempfile
import multiprocessing
import threading
from urllib.parse import urlparse
import git
import requests
from packaging import version
from bstack_utils.config import Config
from bstack_utils.constants import bstack11l1l111ll_opy_, bstack1l1l1l11ll_opy_, bstack1l1ll1ll1_opy_, bstack1l1l1lll11_opy_
from bstack_utils.messages import bstack1l1ll11l11_opy_, bstack11ll11lll_opy_
from bstack_utils.proxy import bstack1ll11ll11l_opy_, bstack1ll1l11lll_opy_
bstack1l1lll1ll1_opy_ = Config.bstack11ll1ll1_opy_()
def bstack11l1ll1ll1_opy_(config):
    return config[bstack1llll1l_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭ᆄ")]
def bstack11ll11111l_opy_(config):
    return config[bstack1llll1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨᆅ")]
def bstack1llll1ll_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack111ll1l1l1_opy_(obj):
    values = []
    bstack111lllllll_opy_ = re.compile(bstack1llll1l_opy_ (u"ࡸࠢ࡟ࡅࡘࡗ࡙ࡕࡍࡠࡖࡄࡋࡤࡢࡤࠬࠦࠥᆆ"), re.I)
    for key in obj.keys():
        if bstack111lllllll_opy_.match(key):
            values.append(obj[key])
    return values
def bstack11l11l1l1l_opy_(config):
    tags = []
    tags.extend(bstack111ll1l1l1_opy_(os.environ))
    tags.extend(bstack111ll1l1l1_opy_(config))
    return tags
def bstack11l11l11ll_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack11l11ll1ll_opy_(bstack11l111111l_opy_):
    if not bstack11l111111l_opy_:
        return bstack1llll1l_opy_ (u"ࠧࠨᆇ")
    return bstack1llll1l_opy_ (u"ࠣࡽࢀࠤ࠭ࢁࡽࠪࠤᆈ").format(bstack11l111111l_opy_.name, bstack11l111111l_opy_.email)
def bstack11ll1l1111_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack11l11lll1l_opy_ = repo.common_dir
        info = {
            bstack1llll1l_opy_ (u"ࠤࡶ࡬ࡦࠨᆉ"): repo.head.commit.hexsha,
            bstack1llll1l_opy_ (u"ࠥࡷ࡭ࡵࡲࡵࡡࡶ࡬ࡦࠨᆊ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack1llll1l_opy_ (u"ࠦࡧࡸࡡ࡯ࡥ࡫ࠦᆋ"): repo.active_branch.name,
            bstack1llll1l_opy_ (u"ࠧࡺࡡࡨࠤᆌ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack1llll1l_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡺࡥࡳࠤᆍ"): bstack11l11ll1ll_opy_(repo.head.commit.committer),
            bstack1llll1l_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺࡴࡦࡴࡢࡨࡦࡺࡥࠣᆎ"): repo.head.commit.committed_datetime.isoformat(),
            bstack1llll1l_opy_ (u"ࠣࡣࡸࡸ࡭ࡵࡲࠣᆏ"): bstack11l11ll1ll_opy_(repo.head.commit.author),
            bstack1llll1l_opy_ (u"ࠤࡤࡹࡹ࡮࡯ࡳࡡࡧࡥࡹ࡫ࠢᆐ"): repo.head.commit.authored_datetime.isoformat(),
            bstack1llll1l_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡢࡱࡪࡹࡳࡢࡩࡨࠦᆑ"): repo.head.commit.message,
            bstack1llll1l_opy_ (u"ࠦࡷࡵ࡯ࡵࠤᆒ"): repo.git.rev_parse(bstack1llll1l_opy_ (u"ࠧ࠳࠭ࡴࡪࡲࡻ࠲ࡺ࡯ࡱ࡮ࡨࡺࡪࡲࠢᆓ")),
            bstack1llll1l_opy_ (u"ࠨࡣࡰ࡯ࡰࡳࡳࡥࡧࡪࡶࡢࡨ࡮ࡸࠢᆔ"): bstack11l11lll1l_opy_,
            bstack1llll1l_opy_ (u"ࠢࡸࡱࡵ࡯ࡹࡸࡥࡦࡡࡪ࡭ࡹࡥࡤࡪࡴࠥᆕ"): subprocess.check_output([bstack1llll1l_opy_ (u"ࠣࡩ࡬ࡸࠧᆖ"), bstack1llll1l_opy_ (u"ࠤࡵࡩࡻ࠳ࡰࡢࡴࡶࡩࠧᆗ"), bstack1llll1l_opy_ (u"ࠥ࠱࠲࡭ࡩࡵ࠯ࡦࡳࡲࡳ࡯࡯࠯ࡧ࡭ࡷࠨᆘ")]).strip().decode(
                bstack1llll1l_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪᆙ")),
            bstack1llll1l_opy_ (u"ࠧࡲࡡࡴࡶࡢࡸࡦ࡭ࠢᆚ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack1llll1l_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡹ࡟ࡴ࡫ࡱࡧࡪࡥ࡬ࡢࡵࡷࡣࡹࡧࡧࠣᆛ"): repo.git.rev_list(
                bstack1llll1l_opy_ (u"ࠢࡼࡿ࠱࠲ࢀࢃࠢᆜ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack111lll111l_opy_ = []
        for remote in remotes:
            bstack111lllll11_opy_ = {
                bstack1llll1l_opy_ (u"ࠣࡰࡤࡱࡪࠨᆝ"): remote.name,
                bstack1llll1l_opy_ (u"ࠤࡸࡶࡱࠨᆞ"): remote.url,
            }
            bstack111lll111l_opy_.append(bstack111lllll11_opy_)
        return {
            bstack1llll1l_opy_ (u"ࠥࡲࡦࡳࡥࠣᆟ"): bstack1llll1l_opy_ (u"ࠦ࡬࡯ࡴࠣᆠ"),
            **info,
            bstack1llll1l_opy_ (u"ࠧࡸࡥ࡮ࡱࡷࡩࡸࠨᆡ"): bstack111lll111l_opy_
        }
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack1llll1l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡯ࡱࡷ࡯ࡥࡹ࡯࡮ࡨࠢࡊ࡭ࡹࠦ࡭ࡦࡶࡤࡨࡦࡺࡡࠡࡹ࡬ࡸ࡭ࠦࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠤᆢ").format(err))
        return {}
def bstack1lll11111_opy_():
    env = os.environ
    if (bstack1llll1l_opy_ (u"ࠢࡋࡇࡑࡏࡎࡔࡓࡠࡗࡕࡐࠧᆣ") in env and len(env[bstack1llll1l_opy_ (u"ࠣࡌࡈࡒࡐࡏࡎࡔࡡࡘࡖࡑࠨᆤ")]) > 0) or (
            bstack1llll1l_opy_ (u"ࠤࡍࡉࡓࡑࡉࡏࡕࡢࡌࡔࡓࡅࠣᆥ") in env and len(env[bstack1llll1l_opy_ (u"ࠥࡎࡊࡔࡋࡊࡐࡖࡣࡍࡕࡍࡆࠤᆦ")]) > 0):
        return {
            bstack1llll1l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᆧ"): bstack1llll1l_opy_ (u"ࠧࡐࡥ࡯࡭࡬ࡲࡸࠨᆨ"),
            bstack1llll1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᆩ"): env.get(bstack1llll1l_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥᆪ")),
            bstack1llll1l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᆫ"): env.get(bstack1llll1l_opy_ (u"ࠤࡍࡓࡇࡥࡎࡂࡏࡈࠦᆬ")),
            bstack1llll1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᆭ"): env.get(bstack1llll1l_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥᆮ"))
        }
    if env.get(bstack1llll1l_opy_ (u"ࠧࡉࡉࠣᆯ")) == bstack1llll1l_opy_ (u"ࠨࡴࡳࡷࡨࠦᆰ") and bstack111ll1l11_opy_(env.get(bstack1llll1l_opy_ (u"ࠢࡄࡋࡕࡇࡑࡋࡃࡊࠤᆱ"))):
        return {
            bstack1llll1l_opy_ (u"ࠣࡰࡤࡱࡪࠨᆲ"): bstack1llll1l_opy_ (u"ࠤࡆ࡭ࡷࡩ࡬ࡦࡅࡌࠦᆳ"),
            bstack1llll1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᆴ"): env.get(bstack1llll1l_opy_ (u"ࠦࡈࡏࡒࡄࡎࡈࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢᆵ")),
            bstack1llll1l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᆶ"): env.get(bstack1llll1l_opy_ (u"ࠨࡃࡊࡔࡆࡐࡊࡥࡊࡐࡄࠥᆷ")),
            bstack1llll1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᆸ"): env.get(bstack1llll1l_opy_ (u"ࠣࡅࡌࡖࡈࡒࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࠦᆹ"))
        }
    if env.get(bstack1llll1l_opy_ (u"ࠤࡆࡍࠧᆺ")) == bstack1llll1l_opy_ (u"ࠥࡸࡷࡻࡥࠣᆻ") and bstack111ll1l11_opy_(env.get(bstack1llll1l_opy_ (u"࡙ࠦࡘࡁࡗࡋࡖࠦᆼ"))):
        return {
            bstack1llll1l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᆽ"): bstack1llll1l_opy_ (u"ࠨࡔࡳࡣࡹ࡭ࡸࠦࡃࡊࠤᆾ"),
            bstack1llll1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᆿ"): env.get(bstack1llll1l_opy_ (u"ࠣࡖࡕࡅ࡛ࡏࡓࡠࡄࡘࡍࡑࡊ࡟ࡘࡇࡅࡣ࡚ࡘࡌࠣᇀ")),
            bstack1llll1l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᇁ"): env.get(bstack1llll1l_opy_ (u"ࠥࡘࡗࡇࡖࡊࡕࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧᇂ")),
            bstack1llll1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᇃ"): env.get(bstack1llll1l_opy_ (u"࡚ࠧࡒࡂࡘࡌࡗࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦᇄ"))
        }
    if env.get(bstack1llll1l_opy_ (u"ࠨࡃࡊࠤᇅ")) == bstack1llll1l_opy_ (u"ࠢࡵࡴࡸࡩࠧᇆ") and env.get(bstack1llll1l_opy_ (u"ࠣࡅࡌࡣࡓࡇࡍࡆࠤᇇ")) == bstack1llll1l_opy_ (u"ࠤࡦࡳࡩ࡫ࡳࡩ࡫ࡳࠦᇈ"):
        return {
            bstack1llll1l_opy_ (u"ࠥࡲࡦࡳࡥࠣᇉ"): bstack1llll1l_opy_ (u"ࠦࡈࡵࡤࡦࡵ࡫࡭ࡵࠨᇊ"),
            bstack1llll1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᇋ"): None,
            bstack1llll1l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᇌ"): None,
            bstack1llll1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᇍ"): None
        }
    if env.get(bstack1llll1l_opy_ (u"ࠣࡄࡌࡘࡇ࡛ࡃࡌࡇࡗࡣࡇࡘࡁࡏࡅࡋࠦᇎ")) and env.get(bstack1llll1l_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡉࡏࡎࡏࡌࡘࠧᇏ")):
        return {
            bstack1llll1l_opy_ (u"ࠥࡲࡦࡳࡥࠣᇐ"): bstack1llll1l_opy_ (u"ࠦࡇ࡯ࡴࡣࡷࡦ࡯ࡪࡺࠢᇑ"),
            bstack1llll1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᇒ"): env.get(bstack1llll1l_opy_ (u"ࠨࡂࡊࡖࡅ࡙ࡈࡑࡅࡕࡡࡊࡍ࡙ࡥࡈࡕࡖࡓࡣࡔࡘࡉࡈࡋࡑࠦᇓ")),
            bstack1llll1l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᇔ"): None,
            bstack1llll1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᇕ"): env.get(bstack1llll1l_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦᇖ"))
        }
    if env.get(bstack1llll1l_opy_ (u"ࠥࡇࡎࠨᇗ")) == bstack1llll1l_opy_ (u"ࠦࡹࡸࡵࡦࠤᇘ") and bstack111ll1l11_opy_(env.get(bstack1llll1l_opy_ (u"ࠧࡊࡒࡐࡐࡈࠦᇙ"))):
        return {
            bstack1llll1l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᇚ"): bstack1llll1l_opy_ (u"ࠢࡅࡴࡲࡲࡪࠨᇛ"),
            bstack1llll1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᇜ"): env.get(bstack1llll1l_opy_ (u"ࠤࡇࡖࡔࡔࡅࡠࡄࡘࡍࡑࡊ࡟ࡍࡋࡑࡏࠧᇝ")),
            bstack1llll1l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᇞ"): None,
            bstack1llll1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᇟ"): env.get(bstack1llll1l_opy_ (u"ࠧࡊࡒࡐࡐࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥᇠ"))
        }
    if env.get(bstack1llll1l_opy_ (u"ࠨࡃࡊࠤᇡ")) == bstack1llll1l_opy_ (u"ࠢࡵࡴࡸࡩࠧᇢ") and bstack111ll1l11_opy_(env.get(bstack1llll1l_opy_ (u"ࠣࡕࡈࡑࡆࡖࡈࡐࡔࡈࠦᇣ"))):
        return {
            bstack1llll1l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᇤ"): bstack1llll1l_opy_ (u"ࠥࡗࡪࡳࡡࡱࡪࡲࡶࡪࠨᇥ"),
            bstack1llll1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᇦ"): env.get(bstack1llll1l_opy_ (u"࡙ࠧࡅࡎࡃࡓࡌࡔࡘࡅࡠࡑࡕࡋࡆࡔࡉ࡛ࡃࡗࡍࡔࡔ࡟ࡖࡔࡏࠦᇧ")),
            bstack1llll1l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᇨ"): env.get(bstack1llll1l_opy_ (u"ࠢࡔࡇࡐࡅࡕࡎࡏࡓࡇࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧᇩ")),
            bstack1llll1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᇪ"): env.get(bstack1llll1l_opy_ (u"ࠤࡖࡉࡒࡇࡐࡉࡑࡕࡉࡤࡐࡏࡃࡡࡌࡈࠧᇫ"))
        }
    if env.get(bstack1llll1l_opy_ (u"ࠥࡇࡎࠨᇬ")) == bstack1llll1l_opy_ (u"ࠦࡹࡸࡵࡦࠤᇭ") and bstack111ll1l11_opy_(env.get(bstack1llll1l_opy_ (u"ࠧࡍࡉࡕࡎࡄࡆࡤࡉࡉࠣᇮ"))):
        return {
            bstack1llll1l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᇯ"): bstack1llll1l_opy_ (u"ࠢࡈ࡫ࡷࡐࡦࡨࠢᇰ"),
            bstack1llll1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᇱ"): env.get(bstack1llll1l_opy_ (u"ࠤࡆࡍࡤࡐࡏࡃࡡࡘࡖࡑࠨᇲ")),
            bstack1llll1l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᇳ"): env.get(bstack1llll1l_opy_ (u"ࠦࡈࡏ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤᇴ")),
            bstack1llll1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᇵ"): env.get(bstack1llll1l_opy_ (u"ࠨࡃࡊࡡࡍࡓࡇࡥࡉࡅࠤᇶ"))
        }
    if env.get(bstack1llll1l_opy_ (u"ࠢࡄࡋࠥᇷ")) == bstack1llll1l_opy_ (u"ࠣࡶࡵࡹࡪࠨᇸ") and bstack111ll1l11_opy_(env.get(bstack1llll1l_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࠧᇹ"))):
        return {
            bstack1llll1l_opy_ (u"ࠥࡲࡦࡳࡥࠣᇺ"): bstack1llll1l_opy_ (u"ࠦࡇࡻࡩ࡭ࡦ࡮࡭ࡹ࡫ࠢᇻ"),
            bstack1llll1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᇼ"): env.get(bstack1llll1l_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧᇽ")),
            bstack1llll1l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᇾ"): env.get(bstack1llll1l_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࡣࡑࡇࡂࡆࡎࠥᇿ")) or env.get(bstack1llll1l_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡏࡃࡐࡉࠧሀ")),
            bstack1llll1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤሁ"): env.get(bstack1llll1l_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡎࡍ࡙ࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨሂ"))
        }
    if bstack111ll1l11_opy_(env.get(bstack1llll1l_opy_ (u"࡚ࠧࡆࡠࡄࡘࡍࡑࡊࠢሃ"))):
        return {
            bstack1llll1l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦሄ"): bstack1llll1l_opy_ (u"ࠢࡗ࡫ࡶࡹࡦࡲࠠࡔࡶࡸࡨ࡮ࡵࠠࡕࡧࡤࡱ࡙ࠥࡥࡳࡸ࡬ࡧࡪࡹࠢህ"),
            bstack1llll1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦሆ"): bstack1llll1l_opy_ (u"ࠤࡾࢁࢀࢃࠢሇ").format(env.get(bstack1llll1l_opy_ (u"ࠪࡗ࡞࡙ࡔࡆࡏࡢࡘࡊࡇࡍࡇࡑࡘࡒࡉࡇࡔࡊࡑࡑࡗࡊࡘࡖࡆࡔࡘࡖࡎ࠭ለ")), env.get(bstack1llll1l_opy_ (u"ࠫࡘ࡟ࡓࡕࡇࡐࡣ࡙ࡋࡁࡎࡒࡕࡓࡏࡋࡃࡕࡋࡇࠫሉ"))),
            bstack1llll1l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢሊ"): env.get(bstack1llll1l_opy_ (u"ࠨࡓ࡚ࡕࡗࡉࡒࡥࡄࡆࡈࡌࡒࡎ࡚ࡉࡐࡐࡌࡈࠧላ")),
            bstack1llll1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨሌ"): env.get(bstack1llll1l_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡏࡄࠣል"))
        }
    if bstack111ll1l11_opy_(env.get(bstack1llll1l_opy_ (u"ࠤࡄࡔࡕ࡜ࡅ࡚ࡑࡕࠦሎ"))):
        return {
            bstack1llll1l_opy_ (u"ࠥࡲࡦࡳࡥࠣሏ"): bstack1llll1l_opy_ (u"ࠦࡆࡶࡰࡷࡧࡼࡳࡷࠨሐ"),
            bstack1llll1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣሑ"): bstack1llll1l_opy_ (u"ࠨࡻࡾ࠱ࡳࡶࡴࡰࡥࡤࡶ࠲ࡿࢂ࠵ࡻࡾ࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁࠧሒ").format(env.get(bstack1llll1l_opy_ (u"ࠧࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡘࡖࡑ࠭ሓ")), env.get(bstack1llll1l_opy_ (u"ࠨࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡅࡈࡉࡏࡖࡐࡗࡣࡓࡇࡍࡆࠩሔ")), env.get(bstack1llll1l_opy_ (u"ࠩࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡕࡘࡏࡋࡇࡆࡘࡤ࡙ࡌࡖࡉࠪሕ")), env.get(bstack1llll1l_opy_ (u"ࠪࡅࡕࡖࡖࡆ࡛ࡒࡖࡤࡈࡕࡊࡎࡇࡣࡎࡊࠧሖ"))),
            bstack1llll1l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨሗ"): env.get(bstack1llll1l_opy_ (u"ࠧࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤመ")),
            bstack1llll1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧሙ"): env.get(bstack1llll1l_opy_ (u"ࠢࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣሚ"))
        }
    if env.get(bstack1llll1l_opy_ (u"ࠣࡃ࡝࡙ࡗࡋ࡟ࡉࡖࡗࡔࡤ࡛ࡓࡆࡔࡢࡅࡌࡋࡎࡕࠤማ")) and env.get(bstack1llll1l_opy_ (u"ࠤࡗࡊࡤࡈࡕࡊࡎࡇࠦሜ")):
        return {
            bstack1llll1l_opy_ (u"ࠥࡲࡦࡳࡥࠣም"): bstack1llll1l_opy_ (u"ࠦࡆࢀࡵࡳࡧࠣࡇࡎࠨሞ"),
            bstack1llll1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣሟ"): bstack1llll1l_opy_ (u"ࠨࡻࡾࡽࢀ࠳ࡤࡨࡵࡪ࡮ࡧ࠳ࡷ࡫ࡳࡶ࡮ࡷࡷࡄࡨࡵࡪ࡮ࡧࡍࡩࡃࡻࡾࠤሠ").format(env.get(bstack1llll1l_opy_ (u"ࠧࡔ࡛ࡖࡘࡊࡓ࡟ࡕࡇࡄࡑࡋࡕࡕࡏࡆࡄࡘࡎࡕࡎࡔࡇࡕ࡚ࡊࡘࡕࡓࡋࠪሡ")), env.get(bstack1llll1l_opy_ (u"ࠨࡕ࡜ࡗ࡙ࡋࡍࡠࡖࡈࡅࡒࡖࡒࡐࡌࡈࡇ࡙࠭ሢ")), env.get(bstack1llll1l_opy_ (u"ࠩࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊࡉࡅࠩሣ"))),
            bstack1llll1l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧሤ"): env.get(bstack1llll1l_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡋࡇࠦሥ")),
            bstack1llll1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦሦ"): env.get(bstack1llll1l_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡍࡉࠨሧ"))
        }
    if any([env.get(bstack1llll1l_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧረ")), env.get(bstack1llll1l_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡗࡋࡓࡐࡎ࡙ࡉࡉࡥࡓࡐࡗࡕࡇࡊࡥࡖࡆࡔࡖࡍࡔࡔࠢሩ")), env.get(bstack1llll1l_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤ࡙ࡏࡖࡔࡆࡉࡤ࡜ࡅࡓࡕࡌࡓࡓࠨሪ"))]):
        return {
            bstack1llll1l_opy_ (u"ࠥࡲࡦࡳࡥࠣራ"): bstack1llll1l_opy_ (u"ࠦࡆ࡝ࡓࠡࡅࡲࡨࡪࡈࡵࡪ࡮ࡧࠦሬ"),
            bstack1llll1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣር"): env.get(bstack1llll1l_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡓ࡙ࡇࡒࡉࡄࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧሮ")),
            bstack1llll1l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤሯ"): env.get(bstack1llll1l_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࠨሰ")),
            bstack1llll1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣሱ"): env.get(bstack1llll1l_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠣሲ"))
        }
    if env.get(bstack1llll1l_opy_ (u"ࠦࡧࡧ࡭ࡣࡱࡲࡣࡧࡻࡩ࡭ࡦࡑࡹࡲࡨࡥࡳࠤሳ")):
        return {
            bstack1llll1l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥሴ"): bstack1llll1l_opy_ (u"ࠨࡂࡢ࡯ࡥࡳࡴࠨስ"),
            bstack1llll1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥሶ"): env.get(bstack1llll1l_opy_ (u"ࠣࡤࡤࡱࡧࡵ࡯ࡠࡤࡸ࡭ࡱࡪࡒࡦࡵࡸࡰࡹࡹࡕࡳ࡮ࠥሷ")),
            bstack1llll1l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦሸ"): env.get(bstack1llll1l_opy_ (u"ࠥࡦࡦࡳࡢࡰࡱࡢࡷ࡭ࡵࡲࡵࡌࡲࡦࡓࡧ࡭ࡦࠤሹ")),
            bstack1llll1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥሺ"): env.get(bstack1llll1l_opy_ (u"ࠧࡨࡡ࡮ࡤࡲࡳࡤࡨࡵࡪ࡮ࡧࡒࡺࡳࡢࡦࡴࠥሻ"))
        }
    if env.get(bstack1llll1l_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘࠢሼ")) or env.get(bstack1llll1l_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࡠࡏࡄࡍࡓࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡕࡗࡅࡗ࡚ࡅࡅࠤሽ")):
        return {
            bstack1llll1l_opy_ (u"ࠣࡰࡤࡱࡪࠨሾ"): bstack1llll1l_opy_ (u"ࠤ࡚ࡩࡷࡩ࡫ࡦࡴࠥሿ"),
            bstack1llll1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨቀ"): env.get(bstack1llll1l_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣቁ")),
            bstack1llll1l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢቂ"): bstack1llll1l_opy_ (u"ࠨࡍࡢ࡫ࡱࠤࡕ࡯ࡰࡦ࡮࡬ࡲࡪࠨቃ") if env.get(bstack1llll1l_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࡠࡏࡄࡍࡓࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡕࡗࡅࡗ࡚ࡅࡅࠤቄ")) else None,
            bstack1llll1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢቅ"): env.get(bstack1llll1l_opy_ (u"ࠤ࡚ࡉࡗࡉࡋࡆࡔࡢࡋࡎ࡚࡟ࡄࡑࡐࡑࡎ࡚ࠢቆ"))
        }
    if any([env.get(bstack1llll1l_opy_ (u"ࠥࡋࡈࡖ࡟ࡑࡔࡒࡎࡊࡉࡔࠣቇ")), env.get(bstack1llll1l_opy_ (u"ࠦࡌࡉࡌࡐࡗࡇࡣࡕࡘࡏࡋࡇࡆࡘࠧቈ")), env.get(bstack1llll1l_opy_ (u"ࠧࡍࡏࡐࡉࡏࡉࡤࡉࡌࡐࡗࡇࡣࡕࡘࡏࡋࡇࡆࡘࠧ቉"))]):
        return {
            bstack1llll1l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦቊ"): bstack1llll1l_opy_ (u"ࠢࡈࡱࡲ࡫ࡱ࡫ࠠࡄ࡮ࡲࡹࡩࠨቋ"),
            bstack1llll1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦቌ"): None,
            bstack1llll1l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦቍ"): env.get(bstack1llll1l_opy_ (u"ࠥࡔࡗࡕࡊࡆࡅࡗࡣࡎࡊࠢ቎")),
            bstack1llll1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ቏"): env.get(bstack1llll1l_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡎࡊࠢቐ"))
        }
    if env.get(bstack1llll1l_opy_ (u"ࠨࡓࡉࡋࡓࡔࡆࡈࡌࡆࠤቑ")):
        return {
            bstack1llll1l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧቒ"): bstack1llll1l_opy_ (u"ࠣࡕ࡫࡭ࡵࡶࡡࡣ࡮ࡨࠦቓ"),
            bstack1llll1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧቔ"): env.get(bstack1llll1l_opy_ (u"ࠥࡗࡍࡏࡐࡑࡃࡅࡐࡊࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤቕ")),
            bstack1llll1l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨቖ"): bstack1llll1l_opy_ (u"ࠧࡐ࡯ࡣࠢࠦࡿࢂࠨ቗").format(env.get(bstack1llll1l_opy_ (u"࠭ࡓࡉࡋࡓࡔࡆࡈࡌࡆࡡࡍࡓࡇࡥࡉࡅࠩቘ"))) if env.get(bstack1llll1l_opy_ (u"ࠢࡔࡊࡌࡔࡕࡇࡂࡍࡇࡢࡎࡔࡈ࡟ࡊࡆࠥ቙")) else None,
            bstack1llll1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢቚ"): env.get(bstack1llll1l_opy_ (u"ࠤࡖࡌࡎࡖࡐࡂࡄࡏࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦቛ"))
        }
    if bstack111ll1l11_opy_(env.get(bstack1llll1l_opy_ (u"ࠥࡒࡊ࡚ࡌࡊࡈ࡜ࠦቜ"))):
        return {
            bstack1llll1l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤቝ"): bstack1llll1l_opy_ (u"ࠧࡔࡥࡵ࡮࡬ࡪࡾࠨ቞"),
            bstack1llll1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ቟"): env.get(bstack1llll1l_opy_ (u"ࠢࡅࡇࡓࡐࡔ࡟࡟ࡖࡔࡏࠦበ")),
            bstack1llll1l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥቡ"): env.get(bstack1llll1l_opy_ (u"ࠤࡖࡍ࡙ࡋ࡟ࡏࡃࡐࡉࠧቢ")),
            bstack1llll1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤባ"): env.get(bstack1llll1l_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡍࡉࠨቤ"))
        }
    if bstack111ll1l11_opy_(env.get(bstack1llll1l_opy_ (u"ࠧࡍࡉࡕࡊࡘࡆࡤࡇࡃࡕࡋࡒࡒࡘࠨብ"))):
        return {
            bstack1llll1l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦቦ"): bstack1llll1l_opy_ (u"ࠢࡈ࡫ࡷࡌࡺࡨࠠࡂࡥࡷ࡭ࡴࡴࡳࠣቧ"),
            bstack1llll1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦቨ"): bstack1llll1l_opy_ (u"ࠤࡾࢁ࠴ࢁࡽ࠰ࡣࡦࡸ࡮ࡵ࡮ࡴ࠱ࡵࡹࡳࡹ࠯ࡼࡿࠥቩ").format(env.get(bstack1llll1l_opy_ (u"ࠪࡋࡎ࡚ࡈࡖࡄࡢࡗࡊࡘࡖࡆࡔࡢ࡙ࡗࡒࠧቪ")), env.get(bstack1llll1l_opy_ (u"ࠫࡌࡏࡔࡉࡗࡅࡣࡗࡋࡐࡐࡕࡌࡘࡔࡘ࡙ࠨቫ")), env.get(bstack1llll1l_opy_ (u"ࠬࡍࡉࡕࡊࡘࡆࡤࡘࡕࡏࡡࡌࡈࠬቬ"))),
            bstack1llll1l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣቭ"): env.get(bstack1llll1l_opy_ (u"ࠢࡈࡋࡗࡌ࡚ࡈ࡟ࡘࡑࡕࡏࡋࡒࡏࡘࠤቮ")),
            bstack1llll1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢቯ"): env.get(bstack1llll1l_opy_ (u"ࠤࡊࡍ࡙ࡎࡕࡃࡡࡕ࡙ࡓࡥࡉࡅࠤተ"))
        }
    if env.get(bstack1llll1l_opy_ (u"ࠥࡇࡎࠨቱ")) == bstack1llll1l_opy_ (u"ࠦࡹࡸࡵࡦࠤቲ") and env.get(bstack1llll1l_opy_ (u"ࠧ࡜ࡅࡓࡅࡈࡐࠧታ")) == bstack1llll1l_opy_ (u"ࠨ࠱ࠣቴ"):
        return {
            bstack1llll1l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧት"): bstack1llll1l_opy_ (u"ࠣࡘࡨࡶࡨ࡫࡬ࠣቶ"),
            bstack1llll1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧቷ"): bstack1llll1l_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࡿࢂࠨቸ").format(env.get(bstack1llll1l_opy_ (u"࡛ࠫࡋࡒࡄࡇࡏࡣ࡚ࡘࡌࠨቹ"))),
            bstack1llll1l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢቺ"): None,
            bstack1llll1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧቻ"): None,
        }
    if env.get(bstack1llll1l_opy_ (u"ࠢࡕࡇࡄࡑࡈࡏࡔ࡚ࡡ࡙ࡉࡗ࡙ࡉࡐࡐࠥቼ")):
        return {
            bstack1llll1l_opy_ (u"ࠣࡰࡤࡱࡪࠨች"): bstack1llll1l_opy_ (u"ࠤࡗࡩࡦࡳࡣࡪࡶࡼࠦቾ"),
            bstack1llll1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨቿ"): None,
            bstack1llll1l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨኀ"): env.get(bstack1llll1l_opy_ (u"࡚ࠧࡅࡂࡏࡆࡍ࡙࡟࡟ࡑࡔࡒࡎࡊࡉࡔࡠࡐࡄࡑࡊࠨኁ")),
            bstack1llll1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧኂ"): env.get(bstack1llll1l_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨኃ"))
        }
    if any([env.get(bstack1llll1l_opy_ (u"ࠣࡅࡒࡒࡈࡕࡕࡓࡕࡈࠦኄ")), env.get(bstack1llll1l_opy_ (u"ࠤࡆࡓࡓࡉࡏࡖࡔࡖࡉࡤ࡛ࡒࡍࠤኅ")), env.get(bstack1llll1l_opy_ (u"ࠥࡇࡔࡔࡃࡐࡗࡕࡗࡊࡥࡕࡔࡇࡕࡒࡆࡓࡅࠣኆ")), env.get(bstack1llll1l_opy_ (u"ࠦࡈࡕࡎࡄࡑࡘࡖࡘࡋ࡟ࡕࡇࡄࡑࠧኇ"))]):
        return {
            bstack1llll1l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥኈ"): bstack1llll1l_opy_ (u"ࠨࡃࡰࡰࡦࡳࡺࡸࡳࡦࠤ኉"),
            bstack1llll1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥኊ"): None,
            bstack1llll1l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥኋ"): env.get(bstack1llll1l_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥኌ")) or None,
            bstack1llll1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤኍ"): env.get(bstack1llll1l_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡍࡉࠨ኎"), 0)
        }
    if env.get(bstack1llll1l_opy_ (u"ࠧࡍࡏࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥ኏")):
        return {
            bstack1llll1l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦነ"): bstack1llll1l_opy_ (u"ࠢࡈࡱࡆࡈࠧኑ"),
            bstack1llll1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦኒ"): None,
            bstack1llll1l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦና"): env.get(bstack1llll1l_opy_ (u"ࠥࡋࡔࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣኔ")),
            bstack1llll1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥን"): env.get(bstack1llll1l_opy_ (u"ࠧࡍࡏࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡇࡔ࡛ࡎࡕࡇࡕࠦኖ"))
        }
    if env.get(bstack1llll1l_opy_ (u"ࠨࡃࡇࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦኗ")):
        return {
            bstack1llll1l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧኘ"): bstack1llll1l_opy_ (u"ࠣࡅࡲࡨࡪࡌࡲࡦࡵ࡫ࠦኙ"),
            bstack1llll1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧኚ"): env.get(bstack1llll1l_opy_ (u"ࠥࡇࡋࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤኛ")),
            bstack1llll1l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨኜ"): env.get(bstack1llll1l_opy_ (u"ࠧࡉࡆࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡒࡆࡓࡅࠣኝ")),
            bstack1llll1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧኞ"): env.get(bstack1llll1l_opy_ (u"ࠢࡄࡈࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧኟ"))
        }
    return {bstack1llll1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢአ"): None}
def get_host_info():
    return {
        bstack1llll1l_opy_ (u"ࠤ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠦኡ"): platform.node(),
        bstack1llll1l_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࠧኢ"): platform.system(),
        bstack1llll1l_opy_ (u"ࠦࡹࡿࡰࡦࠤኣ"): platform.machine(),
        bstack1llll1l_opy_ (u"ࠧࡼࡥࡳࡵ࡬ࡳࡳࠨኤ"): platform.version(),
        bstack1llll1l_opy_ (u"ࠨࡡࡳࡥ࡫ࠦእ"): platform.architecture()[0]
    }
def bstack1l11l1llll_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack11l1111l11_opy_():
    if bstack1l1lll1ll1_opy_.get_property(bstack1llll1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨኦ")):
        return bstack1llll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧኧ")
    return bstack1llll1l_opy_ (u"ࠩࡸࡲࡰࡴ࡯ࡸࡰࡢ࡫ࡷ࡯ࡤࠨከ")
def bstack111ll1l1ll_opy_(driver):
    info = {
        bstack1llll1l_opy_ (u"ࠪࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩኩ"): driver.capabilities,
        bstack1llll1l_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡯ࡤࠨኪ"): driver.session_id,
        bstack1llll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭ካ"): driver.capabilities.get(bstack1llll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫኬ"), None),
        bstack1llll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩክ"): driver.capabilities.get(bstack1llll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩኮ"), None),
        bstack1llll1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࠫኯ"): driver.capabilities.get(bstack1llll1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠩኰ"), None),
    }
    if bstack11l1111l11_opy_() == bstack1llll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪ኱"):
        info[bstack1llll1l_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹ࠭ኲ")] = bstack1llll1l_opy_ (u"࠭ࡡࡱࡲ࠰ࡥࡺࡺ࡯࡮ࡣࡷࡩࠬኳ") if bstack1ll1lll11l_opy_() else bstack1llll1l_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩኴ")
    return info
def bstack1ll1lll11l_opy_():
    if bstack1l1lll1ll1_opy_.get_property(bstack1llll1l_opy_ (u"ࠨࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠧኵ")):
        return True
    if bstack111ll1l11_opy_(os.environ.get(bstack1llll1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪ኶"), None)):
        return True
    return False
def bstack1ll1l11l_opy_(bstack11l111lll1_opy_, url, data, config):
    headers = config.get(bstack1llll1l_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫ኷"), None)
    proxies = bstack1ll11ll11l_opy_(config, url)
    auth = config.get(bstack1llll1l_opy_ (u"ࠫࡦࡻࡴࡩࠩኸ"), None)
    response = requests.request(
            bstack11l111lll1_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack111l111ll_opy_(bstack111lll1ll_opy_, size):
    bstack1lll111l_opy_ = []
    while len(bstack111lll1ll_opy_) > size:
        bstack1llllllll_opy_ = bstack111lll1ll_opy_[:size]
        bstack1lll111l_opy_.append(bstack1llllllll_opy_)
        bstack111lll1ll_opy_ = bstack111lll1ll_opy_[size:]
    bstack1lll111l_opy_.append(bstack111lll1ll_opy_)
    return bstack1lll111l_opy_
def bstack111ll1lll1_opy_(message, bstack111lll1lll_opy_=False):
    os.write(1, bytes(message, bstack1llll1l_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫኹ")))
    os.write(1, bytes(bstack1llll1l_opy_ (u"࠭࡜࡯ࠩኺ"), bstack1llll1l_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭ኻ")))
    if bstack111lll1lll_opy_:
        with open(bstack1llll1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠮ࡱ࠴࠵ࡾ࠳ࠧኼ") + os.environ[bstack1llll1l_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡎࡁࡔࡊࡈࡈࡤࡏࡄࠨኽ")] + bstack1llll1l_opy_ (u"ࠪ࠲ࡱࡵࡧࠨኾ"), bstack1llll1l_opy_ (u"ࠫࡦ࠭኿")) as f:
            f.write(message + bstack1llll1l_opy_ (u"ࠬࡢ࡮ࠨዀ"))
def bstack11l1111111_opy_():
    return os.environ[bstack1llll1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡕࡕࡑࡐࡅ࡙ࡏࡏࡏࠩ዁")].lower() == bstack1llll1l_opy_ (u"ࠧࡵࡴࡸࡩࠬዂ")
def bstack1l1ll1l1_opy_(bstack11l11l1111_opy_):
    return bstack1llll1l_opy_ (u"ࠨࡽࢀ࠳ࢀࢃࠧዃ").format(bstack11l1l111ll_opy_, bstack11l11l1111_opy_)
def bstack1l1l1llll_opy_():
    return datetime.datetime.utcnow().isoformat() + bstack1llll1l_opy_ (u"ࠩ࡝ࠫዄ")
def bstack11l11llll1_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack1llll1l_opy_ (u"ࠪ࡞ࠬዅ"))) - datetime.datetime.fromisoformat(start.rstrip(bstack1llll1l_opy_ (u"ࠫ࡟࠭዆")))).total_seconds() * 1000
def bstack111lll11ll_opy_(timestamp):
    return datetime.datetime.utcfromtimestamp(timestamp).isoformat() + bstack1llll1l_opy_ (u"ࠬࡠࠧ዇")
def bstack11l111llll_opy_(bstack111llll1ll_opy_):
    date_format = bstack1llll1l_opy_ (u"࡚࠭ࠥࠧࡰࠩࡩࠦࠥࡉ࠼ࠨࡑ࠿ࠫࡓ࠯ࠧࡩࠫወ")
    bstack111lll1l1l_opy_ = datetime.datetime.strptime(bstack111llll1ll_opy_, date_format)
    return bstack111lll1l1l_opy_.isoformat() + bstack1llll1l_opy_ (u"࡛ࠧࠩዉ")
def bstack11l11ll11l_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack1llll1l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨዊ")
    else:
        return bstack1llll1l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩዋ")
def bstack111ll1l11_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack1llll1l_opy_ (u"ࠪࡸࡷࡻࡥࠨዌ")
def bstack111llll11l_opy_(val):
    return val.__str__().lower() == bstack1llll1l_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪው")
def bstack1l111l1111_opy_(bstack11l1111l1l_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack11l1111l1l_opy_ as e:
                print(bstack1llll1l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦࡻࡾࠢ࠰ࡂࠥࢁࡽ࠻ࠢࡾࢁࠧዎ").format(func.__name__, bstack11l1111l1l_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack11l111l111_opy_(bstack11l11l1ll1_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack11l11l1ll1_opy_(cls, *args, **kwargs)
            except bstack11l1111l1l_opy_ as e:
                print(bstack1llll1l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࡼࡿࠣ࠱ࡃࠦࡻࡾ࠼ࠣࡿࢂࠨዏ").format(bstack11l11l1ll1_opy_.__name__, bstack11l1111l1l_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack11l111l111_opy_
    else:
        return decorator
def bstack1lll11ll11_opy_(bstack11ll1lllll_opy_):
    if bstack1llll1l_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫዐ") in bstack11ll1lllll_opy_ and bstack111llll11l_opy_(bstack11ll1lllll_opy_[bstack1llll1l_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬዑ")]):
        return False
    if bstack1llll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫዒ") in bstack11ll1lllll_opy_ and bstack111llll11l_opy_(bstack11ll1lllll_opy_[bstack1llll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬዓ")]):
        return False
    return True
def bstack1ll1l11l1_opy_():
    try:
        from pytest_bdd import reporting
        return True
    except Exception as e:
        return False
def bstack111l11lll_opy_(hub_url):
    if bstack111l11l1_opy_() <= version.parse(bstack1llll1l_opy_ (u"ࠫ࠸࠴࠱࠴࠰࠳ࠫዔ")):
        if hub_url != bstack1llll1l_opy_ (u"ࠬ࠭ዕ"):
            return bstack1llll1l_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢዖ") + hub_url + bstack1llll1l_opy_ (u"ࠢ࠻࠺࠳࠳ࡼࡪ࠯ࡩࡷࡥࠦ዗")
        return bstack1l1ll1ll1_opy_
    if hub_url != bstack1llll1l_opy_ (u"ࠨࠩዘ"):
        return bstack1llll1l_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲ࠦዙ") + hub_url + bstack1llll1l_opy_ (u"ࠥ࠳ࡼࡪ࠯ࡩࡷࡥࠦዚ")
    return bstack1l1l1lll11_opy_
def bstack11l11ll1l1_opy_():
    return isinstance(os.getenv(bstack1llll1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔ࡞࡚ࡅࡔࡖࡢࡔࡑ࡛ࡇࡊࡐࠪዛ")), str)
def bstack11l11ll11_opy_(url):
    return urlparse(url).hostname
def bstack11lll1ll_opy_(hostname):
    for bstack1l1llll1ll_opy_ in bstack1l1l1l11ll_opy_:
        regex = re.compile(bstack1l1llll1ll_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack111lll1ll1_opy_(bstack111ll1llll_opy_, file_name, logger):
    bstack1l1ll1l11l_opy_ = os.path.join(os.path.expanduser(bstack1llll1l_opy_ (u"ࠬࢄࠧዜ")), bstack111ll1llll_opy_)
    try:
        if not os.path.exists(bstack1l1ll1l11l_opy_):
            os.makedirs(bstack1l1ll1l11l_opy_)
        file_path = os.path.join(os.path.expanduser(bstack1llll1l_opy_ (u"࠭ࡾࠨዝ")), bstack111ll1llll_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack1llll1l_opy_ (u"ࠧࡸࠩዞ")):
                pass
            with open(file_path, bstack1llll1l_opy_ (u"ࠣࡹ࠮ࠦዟ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack1l1ll11l11_opy_.format(str(e)))
def bstack11l11ll111_opy_(file_name, key, value, logger):
    file_path = bstack111lll1ll1_opy_(bstack1llll1l_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩዠ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1lll1111l1_opy_ = json.load(open(file_path, bstack1llll1l_opy_ (u"ࠪࡶࡧ࠭ዡ")))
        else:
            bstack1lll1111l1_opy_ = {}
        bstack1lll1111l1_opy_[key] = value
        with open(file_path, bstack1llll1l_opy_ (u"ࠦࡼ࠱ࠢዢ")) as outfile:
            json.dump(bstack1lll1111l1_opy_, outfile)
def bstack111ll11ll_opy_(file_name, logger):
    file_path = bstack111lll1ll1_opy_(bstack1llll1l_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬዣ"), file_name, logger)
    bstack1lll1111l1_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack1llll1l_opy_ (u"࠭ࡲࠨዤ")) as bstack1l1ll11l1l_opy_:
            bstack1lll1111l1_opy_ = json.load(bstack1l1ll11l1l_opy_)
    return bstack1lll1111l1_opy_
def bstack11l11ll1_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack1llll1l_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡧࡩࡱ࡫ࡴࡪࡰࡪࠤ࡫࡯࡬ࡦ࠼ࠣࠫዥ") + file_path + bstack1llll1l_opy_ (u"ࠨࠢࠪዦ") + str(e))
def bstack111l11l1_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack1llll1l_opy_ (u"ࠤ࠿ࡒࡔ࡚ࡓࡆࡖࡁࠦዧ")
def bstack1ll111ll11_opy_(config):
    if bstack1llll1l_opy_ (u"ࠪ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩየ") in config:
        del (config[bstack1llll1l_opy_ (u"ࠫ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪዩ")])
        return False
    if bstack111l11l1_opy_() < version.parse(bstack1llll1l_opy_ (u"ࠬ࠹࠮࠵࠰࠳ࠫዪ")):
        return False
    if bstack111l11l1_opy_() >= version.parse(bstack1llll1l_opy_ (u"࠭࠴࠯࠳࠱࠹ࠬያ")):
        return True
    if bstack1llll1l_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧዬ") in config and config[bstack1llll1l_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨይ")] is False:
        return False
    else:
        return True
def bstack1l1111111_opy_(args_list, bstack111lll1111_opy_):
    index = -1
    for value in bstack111lll1111_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack11lll11ll1_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack11lll11ll1_opy_ = bstack11lll11ll1_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack1llll1l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩዮ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack1llll1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪዯ"), exception=exception)
    def bstack11ll1l11l1_opy_(self):
        if self.result != bstack1llll1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫደ"):
            return None
        if bstack1llll1l_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࠣዱ") in self.exception_type:
            return bstack1llll1l_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢዲ")
        return bstack1llll1l_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣዳ")
    def bstack11l111l1l1_opy_(self):
        if self.result != bstack1llll1l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨዴ"):
            return None
        if self.bstack11lll11ll1_opy_:
            return self.bstack11lll11ll1_opy_
        return bstack111lllll1l_opy_(self.exception)
def bstack111lllll1l_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack11l11l111l_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack1lll11l111_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack111ll111_opy_(config, logger):
    try:
        import playwright
        bstack11l111ll11_opy_ = playwright.__file__
        bstack111llllll1_opy_ = os.path.split(bstack11l111ll11_opy_)
        bstack11l11lll11_opy_ = bstack111llllll1_opy_[0] + bstack1llll1l_opy_ (u"ࠩ࠲ࡨࡷ࡯ࡶࡦࡴ࠲ࡴࡦࡩ࡫ࡢࡩࡨ࠳ࡱ࡯ࡢ࠰ࡥ࡯࡭࠴ࡩ࡬ࡪ࠰࡭ࡷࠬድ")
        os.environ[bstack1llll1l_opy_ (u"ࠪࡋࡑࡕࡂࡂࡎࡢࡅࡌࡋࡎࡕࡡࡋࡘ࡙ࡖ࡟ࡑࡔࡒ࡜࡞࠭ዶ")] = bstack1ll1l11lll_opy_(config)
        with open(bstack11l11lll11_opy_, bstack1llll1l_opy_ (u"ࠫࡷ࠭ዷ")) as f:
            bstack1llll1l11l_opy_ = f.read()
            bstack111ll1ll1l_opy_ = bstack1llll1l_opy_ (u"ࠬ࡭࡬ࡰࡤࡤࡰ࠲ࡧࡧࡦࡰࡷࠫዸ")
            bstack11l1111ll1_opy_ = bstack1llll1l11l_opy_.find(bstack111ll1ll1l_opy_)
            if bstack11l1111ll1_opy_ == -1:
              process = subprocess.Popen(bstack1llll1l_opy_ (u"ࠨ࡮ࡱ࡯ࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤ࡬ࡲ࡯ࡣࡣ࡯࠱ࡦ࡭ࡥ࡯ࡶࠥዹ"), shell=True, cwd=bstack111llllll1_opy_[0])
              process.wait()
              bstack11l111ll1l_opy_ = bstack1llll1l_opy_ (u"ࠧࠣࡷࡶࡩࠥࡹࡴࡳ࡫ࡦࡸࠧࡁࠧዺ")
              bstack11l11111ll_opy_ = bstack1llll1l_opy_ (u"ࠣࠤࠥࠤࡡࠨࡵࡴࡧࠣࡷࡹࡸࡩࡤࡶ࡟ࠦࡀࠦࡣࡰࡰࡶࡸࠥࢁࠠࡣࡱࡲࡸࡸࡺࡲࡢࡲࠣࢁࠥࡃࠠࡳࡧࡴࡹ࡮ࡸࡥࠩࠩࡪࡰࡴࡨࡡ࡭࠯ࡤ࡫ࡪࡴࡴࠨࠫ࠾ࠤ࡮࡬ࠠࠩࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡨࡲࡻ࠴ࡇࡍࡑࡅࡅࡑࡥࡁࡈࡇࡑࡘࡤࡎࡔࡕࡒࡢࡔࡗࡕࡘ࡚ࠫࠣࡦࡴࡵࡴࡴࡶࡵࡥࡵ࠮ࠩ࠼ࠢࠥࠦࠧዻ")
              bstack111llll111_opy_ = bstack1llll1l11l_opy_.replace(bstack11l111ll1l_opy_, bstack11l11111ll_opy_)
              with open(bstack11l11lll11_opy_, bstack1llll1l_opy_ (u"ࠩࡺࠫዼ")) as f:
                f.write(bstack111llll111_opy_)
    except Exception as e:
        logger.error(bstack11ll11lll_opy_.format(str(e)))
def bstack11llll11_opy_():
  try:
    bstack11l11l1lll_opy_ = os.path.join(tempfile.gettempdir(), bstack1llll1l_opy_ (u"ࠪࡳࡵࡺࡩ࡮ࡣ࡯ࡣ࡭ࡻࡢࡠࡷࡵࡰ࠳ࡰࡳࡰࡰࠪዽ"))
    bstack11l111l1ll_opy_ = []
    if os.path.exists(bstack11l11l1lll_opy_):
      with open(bstack11l11l1lll_opy_) as f:
        bstack11l111l1ll_opy_ = json.load(f)
      os.remove(bstack11l11l1lll_opy_)
    return bstack11l111l1ll_opy_
  except:
    pass
  return []
def bstack111l111l_opy_(bstack1lll1l11_opy_):
  try:
    bstack11l111l1ll_opy_ = []
    bstack11l11l1lll_opy_ = os.path.join(tempfile.gettempdir(), bstack1llll1l_opy_ (u"ࠫࡴࡶࡴࡪ࡯ࡤࡰࡤ࡮ࡵࡣࡡࡸࡶࡱ࠴ࡪࡴࡱࡱࠫዾ"))
    if os.path.exists(bstack11l11l1lll_opy_):
      with open(bstack11l11l1lll_opy_) as f:
        bstack11l111l1ll_opy_ = json.load(f)
    bstack11l111l1ll_opy_.append(bstack1lll1l11_opy_)
    with open(bstack11l11l1lll_opy_, bstack1llll1l_opy_ (u"ࠬࡽࠧዿ")) as f:
        json.dump(bstack11l111l1ll_opy_, f)
  except:
    pass
def bstack1l1l111ll_opy_(logger, bstack111ll1ll11_opy_ = False):
  try:
    test_name = os.environ.get(bstack1llll1l_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙ࡥࡔࡆࡕࡗࡣࡓࡇࡍࡆࠩጀ"), bstack1llll1l_opy_ (u"ࠧࠨጁ"))
    if test_name == bstack1llll1l_opy_ (u"ࠨࠩጂ"):
        test_name = threading.current_thread().__dict__.get(bstack1llll1l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡄࡧࡨࡤࡺࡥࡴࡶࡢࡲࡦࡳࡥࠨጃ"), bstack1llll1l_opy_ (u"ࠪࠫጄ"))
    bstack11l1111lll_opy_ = bstack1llll1l_opy_ (u"ࠫ࠱ࠦࠧጅ").join(threading.current_thread().bstackTestErrorMessages)
    if bstack111ll1ll11_opy_:
        bstack1l1l11l11_opy_ = os.environ.get(bstack1llll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬጆ"), bstack1llll1l_opy_ (u"࠭࠰ࠨጇ"))
        bstack1l1llll111_opy_ = {bstack1llll1l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬገ"): test_name, bstack1llll1l_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧጉ"): bstack11l1111lll_opy_, bstack1llll1l_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨጊ"): bstack1l1l11l11_opy_}
        bstack11l11l1l11_opy_ = []
        bstack111lll1l11_opy_ = os.path.join(tempfile.gettempdir(), bstack1llll1l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡴࡵࡶ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷ࠲࡯ࡹ࡯࡯ࠩጋ"))
        if os.path.exists(bstack111lll1l11_opy_):
            with open(bstack111lll1l11_opy_) as f:
                bstack11l11l1l11_opy_ = json.load(f)
        bstack11l11l1l11_opy_.append(bstack1l1llll111_opy_)
        with open(bstack111lll1l11_opy_, bstack1llll1l_opy_ (u"ࠫࡼ࠭ጌ")) as f:
            json.dump(bstack11l11l1l11_opy_, f)
    else:
        bstack1l1llll111_opy_ = {bstack1llll1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪግ"): test_name, bstack1llll1l_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬጎ"): bstack11l1111lll_opy_, bstack1llll1l_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ጏ"): str(multiprocessing.current_process().name)}
        if bstack1llll1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸࠬጐ") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack1l1llll111_opy_)
  except Exception as e:
      logger.warn(bstack1llll1l_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡴࡰࡴࡨࠤࡵࡿࡴࡦࡵࡷࠤ࡫ࡻ࡮࡯ࡧ࡯ࠤࡩࡧࡴࡢ࠼ࠣࡿࢂࠨ጑").format(e))
def bstack1111111l1_opy_(error_message, test_name, index, logger):
  try:
    bstack11l11l11l1_opy_ = []
    bstack1l1llll111_opy_ = {bstack1llll1l_opy_ (u"ࠪࡲࡦࡳࡥࠨጒ"): test_name, bstack1llll1l_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪጓ"): error_message, bstack1llll1l_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫጔ"): index}
    bstack111lll11l1_opy_ = os.path.join(tempfile.gettempdir(), bstack1llll1l_opy_ (u"࠭ࡲࡰࡤࡲࡸࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧጕ"))
    if os.path.exists(bstack111lll11l1_opy_):
        with open(bstack111lll11l1_opy_) as f:
            bstack11l11l11l1_opy_ = json.load(f)
    bstack11l11l11l1_opy_.append(bstack1l1llll111_opy_)
    with open(bstack111lll11l1_opy_, bstack1llll1l_opy_ (u"ࠧࡸࠩ጖")) as f:
        json.dump(bstack11l11l11l1_opy_, f)
  except Exception as e:
    logger.warn(bstack1llll1l_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡸࡺ࡯ࡳࡧࠣࡶࡴࡨ࡯ࡵࠢࡩࡹࡳࡴࡥ࡭ࠢࡧࡥࡹࡧ࠺ࠡࡽࢀࠦ጗").format(e))
def bstack1lll1111ll_opy_(bstack1l1ll1llll_opy_, name, logger):
  try:
    bstack1l1llll111_opy_ = {bstack1llll1l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧጘ"): name, bstack1llll1l_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩጙ"): bstack1l1ll1llll_opy_, bstack1llll1l_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪጚ"): str(threading.current_thread()._name)}
    return bstack1l1llll111_opy_
  except Exception as e:
    logger.warn(bstack1llll1l_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡳࡷ࡫ࠠࡣࡧ࡫ࡥࡻ࡫ࠠࡧࡷࡱࡲࡪࡲࠠࡥࡣࡷࡥ࠿ࠦࡻࡾࠤጛ").format(e))
  return
def bstack11l111l11l_opy_():
    return platform.system() == bstack1llll1l_opy_ (u"࠭ࡗࡪࡰࡧࡳࡼࡹࠧጜ")
def bstack1l1lll111_opy_(bstack11l11111l1_opy_, config, logger):
    bstack111llll1l1_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack11l11111l1_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack1llll1l_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡪ࡮ࡲࡴࡦࡴࠣࡧࡴࡴࡦࡪࡩࠣ࡯ࡪࡿࡳࠡࡤࡼࠤࡷ࡫ࡧࡦࡺࠣࡱࡦࡺࡣࡩ࠼ࠣࡿࢂࠨጝ").format(e))
    return bstack111llll1l1_opy_