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
from urllib.parse import urlparse
from bstack_utils.messages import bstack111l11l1ll_opy_
def bstack11111111ll_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack1llllllllll_opy_(bstack1lllllllll1_opy_, bstack11111111l1_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack1lllllllll1_opy_):
        with open(bstack1lllllllll1_opy_) as f:
            pac = PACFile(f.read())
    elif bstack11111111ll_opy_(bstack1lllllllll1_opy_):
        pac = get_pac(url=bstack1lllllllll1_opy_)
    else:
        raise Exception(bstack1ll11l_opy_ (u"ࠪࡔࡦࡩࠠࡧ࡫࡯ࡩࠥࡪ࡯ࡦࡵࠣࡲࡴࡺࠠࡦࡺ࡬ࡷࡹࡀࠠࡼࡿࠪᐜ").format(bstack1lllllllll1_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack1ll11l_opy_ (u"ࠦ࠽࠴࠸࠯࠺࠱࠼ࠧᐝ"), 80))
        bstack1llllllll1l_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack1llllllll1l_opy_ = bstack1ll11l_opy_ (u"ࠬ࠶࠮࠱࠰࠳࠲࠵࠭ᐞ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack11111111l1_opy_, bstack1llllllll1l_opy_)
    return proxy_url
def bstack1l1l1ll1ll_opy_(config):
    return bstack1ll11l_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩᐟ") in config or bstack1ll11l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫᐠ") in config
def bstack1l1ll1l1l1_opy_(config):
    if not bstack1l1l1ll1ll_opy_(config):
        return
    if config.get(bstack1ll11l_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫᐡ")):
        return config.get(bstack1ll11l_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬᐢ"))
    if config.get(bstack1ll11l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧᐣ")):
        return config.get(bstack1ll11l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨᐤ"))
def bstack1lllll11l1_opy_(config, bstack11111111l1_opy_):
    proxy = bstack1l1ll1l1l1_opy_(config)
    proxies = {}
    if config.get(bstack1ll11l_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨᐥ")) or config.get(bstack1ll11l_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪᐦ")):
        if proxy.endswith(bstack1ll11l_opy_ (u"ࠧ࠯ࡲࡤࡧࠬᐧ")):
            proxies = bstack1lll1l1lll_opy_(proxy, bstack11111111l1_opy_)
        else:
            proxies = {
                bstack1ll11l_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧᐨ"): proxy
            }
    return proxies
def bstack1lll1l1lll_opy_(bstack1lllllllll1_opy_, bstack11111111l1_opy_):
    proxies = {}
    global bstack111111111l_opy_
    if bstack1ll11l_opy_ (u"ࠩࡓࡅࡈࡥࡐࡓࡑ࡛࡝ࠬᐩ") in globals():
        return bstack111111111l_opy_
    try:
        proxy = bstack1llllllllll_opy_(bstack1lllllllll1_opy_, bstack11111111l1_opy_)
        if bstack1ll11l_opy_ (u"ࠥࡈࡎࡘࡅࡄࡖࠥᐪ") in proxy:
            proxies = {}
        elif bstack1ll11l_opy_ (u"ࠦࡍ࡚ࡔࡑࠤᐫ") in proxy or bstack1ll11l_opy_ (u"ࠧࡎࡔࡕࡒࡖࠦᐬ") in proxy or bstack1ll11l_opy_ (u"ࠨࡓࡐࡅࡎࡗࠧᐭ") in proxy:
            bstack1111111111_opy_ = proxy.split(bstack1ll11l_opy_ (u"ࠢࠡࠤᐮ"))
            if bstack1ll11l_opy_ (u"ࠣ࠼࠲࠳ࠧᐯ") in bstack1ll11l_opy_ (u"ࠤࠥᐰ").join(bstack1111111111_opy_[1:]):
                proxies = {
                    bstack1ll11l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩᐱ"): bstack1ll11l_opy_ (u"ࠦࠧᐲ").join(bstack1111111111_opy_[1:])
                }
            else:
                proxies = {
                    bstack1ll11l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫᐳ"): str(bstack1111111111_opy_[0]).lower() + bstack1ll11l_opy_ (u"ࠨ࠺࠰࠱ࠥᐴ") + bstack1ll11l_opy_ (u"ࠢࠣᐵ").join(bstack1111111111_opy_[1:])
                }
        elif bstack1ll11l_opy_ (u"ࠣࡒࡕࡓ࡝࡟ࠢᐶ") in proxy:
            bstack1111111111_opy_ = proxy.split(bstack1ll11l_opy_ (u"ࠤࠣࠦᐷ"))
            if bstack1ll11l_opy_ (u"ࠥ࠾࠴࠵ࠢᐸ") in bstack1ll11l_opy_ (u"ࠦࠧᐹ").join(bstack1111111111_opy_[1:]):
                proxies = {
                    bstack1ll11l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࠫᐺ"): bstack1ll11l_opy_ (u"ࠨࠢᐻ").join(bstack1111111111_opy_[1:])
                }
            else:
                proxies = {
                    bstack1ll11l_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭ᐼ"): bstack1ll11l_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤᐽ") + bstack1ll11l_opy_ (u"ࠤࠥᐾ").join(bstack1111111111_opy_[1:])
                }
        else:
            proxies = {
                bstack1ll11l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩᐿ"): proxy
            }
    except Exception as e:
        print(bstack1ll11l_opy_ (u"ࠦࡸࡵ࡭ࡦࠢࡨࡶࡷࡵࡲࠣᑀ"), bstack111l11l1ll_opy_.format(bstack1lllllllll1_opy_, str(e)))
    bstack111111111l_opy_ = proxies
    return proxies