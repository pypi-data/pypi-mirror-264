
from celerys.app import BaseCeleryApp
from e4ting  import log

@BaseCeleryApp()
def test():
    print("test")
    return True

@BaseCeleryApp()
def flush_iptables():
    print("test")
    return True

@BaseCeleryApp()
def botnet_ws_keepalive():
    # from modules.botnet.utilbot import BotUtil
    # return BotUtil.all_keepalive()
    from e4ting.cluster.control     import NodeControl
    client = NodeControl(None)
    client.publish("e4ting.keepalive")
    return True

@BaseCeleryApp()
def refresh_online():
    # 刷新在线信息
    from common.mongo import DB
    from e4ting.cache import OnlineCache
    for uuid in DB.clients.keys():
        if OnlineCache(uuid).exists():
            DB.clients[uuid] = dict(online=True)
        else:
            DB.clients[uuid] = dict(online=False)
    return True

@BaseCeleryApp()
def send_note():
    from modules.botnet.utilbot import BotUtil
    return BotUtil.all_keepalive()

@BaseCeleryApp()
def send_syslog(address, data):
    from modules.webhook.robot import send_syslog
    return send_syslog(address, data)

@BaseCeleryApp()
def dispath_task(uuid="", role=""):
    from modules.botnet.device import Device
    return Device(uid=uuid).send_task(role=role)

@BaseCeleryApp()
def push_frp(uuid):
    from e4ting.api import FRP
    frp = FRP(uuid)
    return frp.push()

@BaseCeleryApp()
def get_user_detail(token, code):
    from e4ting.api import CasDoor
    from e4ting.cache import TokenCache

    data = CasDoor().get_user(token)
    log.info(data)
    TokenCache(token).set(**data)
    TokenCache(code).set(**data)
    return True

