from wiliot_deployment_tools.ag.ut_defines import *
from wiliot_deployment_tools.ag.wlt_types_ag import *
def eval_pkt(str):
    try:
        return eval(str)
    except:
        return None

class WltPkt():
    supported_pkt_types = WLT_PKT_TYPES

    def __init__(self, raw='', hdr=None, generic=None, pkt=None):
        self.hdr = Hdr() if hdr is None else hdr
        self.generic = generic
        self.pkt = pkt
        if raw:
            self.set(raw)

    def __eq__(self, other):
        if isinstance(other, WltPkt):
            return (
                self.hdr == other.hdr and
                self.generic == other.generic and
                self.pkt == other.pkt
            )
        return False

    def dump(self):
        if self.pkt:
            return self.hdr.dump() + self.pkt.dump()
        return self.hdr.dump() + self.generic.dump()

    def set(self, string):
        if not string.startswith("1E16"):
            string = "1E16" + string

        self.hdr.set(string[0:14])
        if self.hdr.group_id == GROUP_ID_BRG2GW or self.hdr.group_id == GROUP_ID_GW2BRG:
            # GROUP_ID_BRG2GW & GROUP_ID_GW2BRG
            self.generic = eval_pkt(f'GenericV{API_VERSION_LATEST}()')
            self.generic.set(string[14:62])

            # MEL modules
            if self.generic.module_type:
                if self.generic.module_type == MODULE_CUSTOM:
                    self.pkt = eval_pkt(f'ModuleCustomLis2Dw12V{self.generic.api_version}()')
                else:
                    self.pkt = eval_pkt(f'{MODULES_DICT[self.generic.module_type]}{self.generic.api_version}()')
            elif self.generic.module_type == MODULE_GLOBAL:
                # Action pkts
                if self.generic.msg_type == BRG_MGMT_MSG_TYPE_ACTION:
                    pkt = eval_pkt(f'ActionGenericV{self.generic.api_version}("{string[14:62]}")')
                    if self.generic.api_version >= API_VERSION_V8:
                        pkt = eval_pkt(f'{ACTIONS_DICT[pkt.action_id]}{self.generic.api_version}()')
                    self.pkt = pkt
                # OLD global config (GW2BRG & BRG2GW)
                elif self.hdr.group_id == GROUP_ID_GW2BRG and self.generic.msg_type == BRG_MGMT_MSG_TYPE_CFG_SET:
                    self.pkt = eval_pkt(f'Gw2BrgCfgV{API_VERSION_LATEST}()') # no api_version field in Gw2BrgCfg pkts - default parse as latest
                elif self.hdr.group_id == GROUP_ID_BRG2GW:
                    if self.generic.msg_type == BRG_MGMT_MSG_TYPE_CFG_SET or self.generic.msg_type == BRG_MGMT_MSG_TYPE_CFG_INFO:
                        self.pkt = eval_pkt(f'Brg2GwCfgV{self.generic.api_version}()')
                # Brg2GwHb pkts
                    elif self.generic.msg_type == BRG_MGMT_MSG_TYPE_HB:
                        self.pkt = eval_pkt(f'Brg2GwHbV{self.generic.api_version}()')
        # SideInfo pkts
        elif self.hdr.group_id == GROUP_ID_SIDE_INFO_SENSOR:
            self.pkt = SideInfoSensor()
        elif self.hdr.group_id == GROUP_ID_SIDE_INFO:
            self.pkt = SideInfo()

        if self.pkt:
            self.pkt.set(string[14:62])

hex_str2int = lambda x: int(x,16)