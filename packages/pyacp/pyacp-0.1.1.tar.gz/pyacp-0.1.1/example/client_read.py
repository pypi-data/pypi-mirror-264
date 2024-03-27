import ctypes
from datetime import date
import acp_idl
import acp_idl_base.enumdef
from acp_idl_base.plchandler import VarInfo
from acp_idl_base.plchandler import VarList
from google.protobuf.message import Message
import pyacp
def main():
    print("clients")
    handle = pyacp.client_init(200,"PLCCTRL")
    print(handle)
    timeout_ms = 200
    max_retry = 3
    req = acp_idl.Request()
    req.read_req.id_group = acp_idl_base.enumdef.Idgroups.PLC_READSYMBOL
    ###########################Single varible#############################################
    data = VarList()
    varinfo = VarInfo()
    varinfo.psz_name = "Application.GVL.OP21"
    data.varinfo = varinfo
    req.read_req.data = data.SerializeToString()
    ################If you want to get all,remove this code block(line 18-22)##############################################################################
    resp_data = VarList()
    response = acp_idl.Response()
    pyacp.client_call(handle, req, response, timeout_ms, max_retry)
    resp_data.parse(response.read_resp.data)
    for it in resp_data.varinfo:
        print(it)
if __name__ == "__main__":
    main()