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
from urllib.parse import urlparse
from bstack_utils.messages import bstack111l11l111_opy_
def bstack1lllllll11l_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack1llllllll1l_opy_(bstack1llllllll11_opy_, bstack1llllllllll_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack1llllllll11_opy_):
        with open(bstack1llllllll11_opy_) as f:
            pac = PACFile(f.read())
    elif bstack1lllllll11l_opy_(bstack1llllllll11_opy_):
        pac = get_pac(url=bstack1llllllll11_opy_)
    else:
        raise Exception(bstack1llll1l_opy_ (u"ࠪࡔࡦࡩࠠࡧ࡫࡯ࡩࠥࡪ࡯ࡦࡵࠣࡲࡴࡺࠠࡦࡺ࡬ࡷࡹࡀࠠࡼࡿࠪᐜ").format(bstack1llllllll11_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack1llll1l_opy_ (u"ࠦ࠽࠴࠸࠯࠺࠱࠼ࠧᐝ"), 80))
        bstack1lllllllll1_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack1lllllllll1_opy_ = bstack1llll1l_opy_ (u"ࠬ࠶࠮࠱࠰࠳࠲࠵࠭ᐞ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack1llllllllll_opy_, bstack1lllllllll1_opy_)
    return proxy_url
def bstack1ll1lll1l1_opy_(config):
    return bstack1llll1l_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩᐟ") in config or bstack1llll1l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫᐠ") in config
def bstack1ll1l11lll_opy_(config):
    if not bstack1ll1lll1l1_opy_(config):
        return
    if config.get(bstack1llll1l_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫᐡ")):
        return config.get(bstack1llll1l_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬᐢ"))
    if config.get(bstack1llll1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧᐣ")):
        return config.get(bstack1llll1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨᐤ"))
def bstack1ll11ll11l_opy_(config, bstack1llllllllll_opy_):
    proxy = bstack1ll1l11lll_opy_(config)
    proxies = {}
    if config.get(bstack1llll1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨᐥ")) or config.get(bstack1llll1l_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪᐦ")):
        if proxy.endswith(bstack1llll1l_opy_ (u"ࠧ࠯ࡲࡤࡧࠬᐧ")):
            proxies = bstack1lll1l11l_opy_(proxy, bstack1llllllllll_opy_)
        else:
            proxies = {
                bstack1llll1l_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧᐨ"): proxy
            }
    return proxies
def bstack1lll1l11l_opy_(bstack1llllllll11_opy_, bstack1llllllllll_opy_):
    proxies = {}
    global bstack1lllllll1l1_opy_
    if bstack1llll1l_opy_ (u"ࠩࡓࡅࡈࡥࡐࡓࡑ࡛࡝ࠬᐩ") in globals():
        return bstack1lllllll1l1_opy_
    try:
        proxy = bstack1llllllll1l_opy_(bstack1llllllll11_opy_, bstack1llllllllll_opy_)
        if bstack1llll1l_opy_ (u"ࠥࡈࡎࡘࡅࡄࡖࠥᐪ") in proxy:
            proxies = {}
        elif bstack1llll1l_opy_ (u"ࠦࡍ࡚ࡔࡑࠤᐫ") in proxy or bstack1llll1l_opy_ (u"ࠧࡎࡔࡕࡒࡖࠦᐬ") in proxy or bstack1llll1l_opy_ (u"ࠨࡓࡐࡅࡎࡗࠧᐭ") in proxy:
            bstack1lllllll1ll_opy_ = proxy.split(bstack1llll1l_opy_ (u"ࠢࠡࠤᐮ"))
            if bstack1llll1l_opy_ (u"ࠣ࠼࠲࠳ࠧᐯ") in bstack1llll1l_opy_ (u"ࠤࠥᐰ").join(bstack1lllllll1ll_opy_[1:]):
                proxies = {
                    bstack1llll1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩᐱ"): bstack1llll1l_opy_ (u"ࠦࠧᐲ").join(bstack1lllllll1ll_opy_[1:])
                }
            else:
                proxies = {
                    bstack1llll1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫᐳ"): str(bstack1lllllll1ll_opy_[0]).lower() + bstack1llll1l_opy_ (u"ࠨ࠺࠰࠱ࠥᐴ") + bstack1llll1l_opy_ (u"ࠢࠣᐵ").join(bstack1lllllll1ll_opy_[1:])
                }
        elif bstack1llll1l_opy_ (u"ࠣࡒࡕࡓ࡝࡟ࠢᐶ") in proxy:
            bstack1lllllll1ll_opy_ = proxy.split(bstack1llll1l_opy_ (u"ࠤࠣࠦᐷ"))
            if bstack1llll1l_opy_ (u"ࠥ࠾࠴࠵ࠢᐸ") in bstack1llll1l_opy_ (u"ࠦࠧᐹ").join(bstack1lllllll1ll_opy_[1:]):
                proxies = {
                    bstack1llll1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫᐺ"): bstack1llll1l_opy_ (u"ࠨࠢᐻ").join(bstack1lllllll1ll_opy_[1:])
                }
            else:
                proxies = {
                    bstack1llll1l_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭ᐼ"): bstack1llll1l_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤᐽ") + bstack1llll1l_opy_ (u"ࠤࠥᐾ").join(bstack1lllllll1ll_opy_[1:])
                }
        else:
            proxies = {
                bstack1llll1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩᐿ"): proxy
            }
    except Exception as e:
        print(bstack1llll1l_opy_ (u"ࠦࡸࡵ࡭ࡦࠢࡨࡶࡷࡵࡲࠣᑀ"), bstack111l11l111_opy_.format(bstack1llllllll11_opy_, str(e)))
    bstack1lllllll1l1_opy_ = proxies
    return proxies