import ctypes
from datetime import date
import acp_idl
import acp_idl_base.enumdef
from acp_idl_base.plchandler import VarInfo
from acp_idl_base.plchandler import VarList
import pyacp
def main():
    print("clients")
    handle = pyacp.client_init(200,"PLCCTRL")
    print(handle)
    timeout_ms = 200
    max_retry = 3
    req = acp_idl.Request()
    req.write_req.id_group = acp_idl_base.enumdef.Idgroups.PLC_WRITESYMBOL
    data = VarList()
    varinfo = VarInfo()
    unsigned_char_array_0 = bytes([1])
    varinfo.psz_name = "Application.GVL.OP21.test01"
    varinfo.psz_type = "BOOL"
    varinfo.ul_type_id = 0
    varinfo.us_ref_id = 0
    varinfo.ul_offset = 0
    varinfo.ul_size = 1
    varinfo.value = unsigned_char_array_0
    data.varinfo = varinfo
    req.write_req.data = data.SerializeToString()
    response = acp_idl.Response()
    pyacp.client_call(handle, req, response, timeout_ms, max_retry)
    
    # print("response ",response.read_resp.data.decode("utf-8"))
if __name__ == "__main__":
    main()