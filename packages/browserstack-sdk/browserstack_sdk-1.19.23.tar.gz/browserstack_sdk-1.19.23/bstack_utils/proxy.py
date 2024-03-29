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
from urllib.parse import urlparse
from bstack_utils.messages import bstack111l11l1l1_opy_
def bstack1111111111_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack1llllllll1l_opy_(bstack1llllllllll_opy_, bstack11111111ll_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack1llllllllll_opy_):
        with open(bstack1llllllllll_opy_) as f:
            pac = PACFile(f.read())
    elif bstack1111111111_opy_(bstack1llllllllll_opy_):
        pac = get_pac(url=bstack1llllllllll_opy_)
    else:
        raise Exception(bstack1l_opy_ (u"ࠪࡔࡦࡩࠠࡧ࡫࡯ࡩࠥࡪ࡯ࡦࡵࠣࡲࡴࡺࠠࡦࡺ࡬ࡷࡹࡀࠠࡼࡿࠪᐜ").format(bstack1llllllllll_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack1l_opy_ (u"ࠦ࠽࠴࠸࠯࠺࠱࠼ࠧᐝ"), 80))
        bstack11111111l1_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack11111111l1_opy_ = bstack1l_opy_ (u"ࠬ࠶࠮࠱࠰࠳࠲࠵࠭ᐞ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack11111111ll_opy_, bstack11111111l1_opy_)
    return proxy_url
def bstack1l11l1111_opy_(config):
    return bstack1l_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩᐟ") in config or bstack1l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫᐠ") in config
def bstack1l1ll1lll1_opy_(config):
    if not bstack1l11l1111_opy_(config):
        return
    if config.get(bstack1l_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫᐡ")):
        return config.get(bstack1l_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬᐢ"))
    if config.get(bstack1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧᐣ")):
        return config.get(bstack1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨᐤ"))
def bstack1lllll1l1l_opy_(config, bstack11111111ll_opy_):
    proxy = bstack1l1ll1lll1_opy_(config)
    proxies = {}
    if config.get(bstack1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨᐥ")) or config.get(bstack1l_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪᐦ")):
        if proxy.endswith(bstack1l_opy_ (u"ࠧ࠯ࡲࡤࡧࠬᐧ")):
            proxies = bstack1l11ll1l1_opy_(proxy, bstack11111111ll_opy_)
        else:
            proxies = {
                bstack1l_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧᐨ"): proxy
            }
    return proxies
def bstack1l11ll1l1_opy_(bstack1llllllllll_opy_, bstack11111111ll_opy_):
    proxies = {}
    global bstack111111111l_opy_
    if bstack1l_opy_ (u"ࠩࡓࡅࡈࡥࡐࡓࡑ࡛࡝ࠬᐩ") in globals():
        return bstack111111111l_opy_
    try:
        proxy = bstack1llllllll1l_opy_(bstack1llllllllll_opy_, bstack11111111ll_opy_)
        if bstack1l_opy_ (u"ࠥࡈࡎࡘࡅࡄࡖࠥᐪ") in proxy:
            proxies = {}
        elif bstack1l_opy_ (u"ࠦࡍ࡚ࡔࡑࠤᐫ") in proxy or bstack1l_opy_ (u"ࠧࡎࡔࡕࡒࡖࠦᐬ") in proxy or bstack1l_opy_ (u"ࠨࡓࡐࡅࡎࡗࠧᐭ") in proxy:
            bstack1lllllllll1_opy_ = proxy.split(bstack1l_opy_ (u"ࠢࠡࠤᐮ"))
            if bstack1l_opy_ (u"ࠣ࠼࠲࠳ࠧᐯ") in bstack1l_opy_ (u"ࠤࠥᐰ").join(bstack1lllllllll1_opy_[1:]):
                proxies = {
                    bstack1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩᐱ"): bstack1l_opy_ (u"ࠦࠧᐲ").join(bstack1lllllllll1_opy_[1:])
                }
            else:
                proxies = {
                    bstack1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫᐳ"): str(bstack1lllllllll1_opy_[0]).lower() + bstack1l_opy_ (u"ࠨ࠺࠰࠱ࠥᐴ") + bstack1l_opy_ (u"ࠢࠣᐵ").join(bstack1lllllllll1_opy_[1:])
                }
        elif bstack1l_opy_ (u"ࠣࡒࡕࡓ࡝࡟ࠢᐶ") in proxy:
            bstack1lllllllll1_opy_ = proxy.split(bstack1l_opy_ (u"ࠤࠣࠦᐷ"))
            if bstack1l_opy_ (u"ࠥ࠾࠴࠵ࠢᐸ") in bstack1l_opy_ (u"ࠦࠧᐹ").join(bstack1lllllllll1_opy_[1:]):
                proxies = {
                    bstack1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫᐺ"): bstack1l_opy_ (u"ࠨࠢᐻ").join(bstack1lllllllll1_opy_[1:])
                }
            else:
                proxies = {
                    bstack1l_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭ᐼ"): bstack1l_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤᐽ") + bstack1l_opy_ (u"ࠤࠥᐾ").join(bstack1lllllllll1_opy_[1:])
                }
        else:
            proxies = {
                bstack1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩᐿ"): proxy
            }
    except Exception as e:
        print(bstack1l_opy_ (u"ࠦࡸࡵ࡭ࡦࠢࡨࡶࡷࡵࡲࠣᑀ"), bstack111l11l1l1_opy_.format(bstack1llllllllll_opy_, str(e)))
    bstack111111111l_opy_ = proxies
    return proxies