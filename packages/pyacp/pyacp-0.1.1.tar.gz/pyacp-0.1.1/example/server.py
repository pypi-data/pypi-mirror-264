import ctypes
import sys
sys.path.append('./proto')
sys.path.append('.')
import pyacp
import acp_idl
import acp_idl_base.enumdef
import time
@pyacp.ffi.callback("void(const char *req, uint64_t req_len, char *resp, uint64_t *resp_len)")
def server_callback(req, req_len, resp, resp_len):    
    #request parse
    requset = acp_idl.Request()
    requset.parse(pyacp.ffi.string(req))
    print("Request ",requset.read_req.length)
    
    #response serialization
    response = acp_idl.Response()
    response.read_resp.result = acp_idl_base.enumdef.Errors.ACP_ERR_OK
    response.read_resp.data = b'application'
    stream = response.SerializeToString()
    response_len = len(stream)
    pyacp.ffi.memmove(resp, stream, response_len)
    resp_len[0] = response_len
    
    
def main():
    print("server")
    handle = pyacp.server_init(200,"PLCCTRL",server_callback)
    pyacp.server_run(handle)
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()