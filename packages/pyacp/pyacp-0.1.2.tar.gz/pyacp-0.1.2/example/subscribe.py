import ctypes
import sys
sys.path.append('./proto')
sys.path.append('.')
import acp_pb2
import acp_enumdef_pb2
import pyacp
import time
@pyacp.ffi.callback("void(const char *msg, uint64_t msg_len)")
def sub_callback(msg, msg_len):
    #request parse
    requset = acp_pb2.Request()
    requset.ParseFromString(pyacp.ffi.string(msg))
    print("Request ",requset.ReadReq.Length)
    
def main():
    print("Starting11")
    handle = pyacp.subscriber_init(0,"c_pub_test",sub_callback)
    print(handle)
    if acp_enumdef_pb2.ACP_ERR_OK != pyacp.subscriber_listen(handle):
        print("Error subscription")
        return
    i = 0
    while True:
        i+=1
        time.sleep(0.5)
        # if i == 5:
        #     pyacp.subscriber_stop_listen(handle)
        #     break
    pyacp.subscriber_destroy(handle)
    
    
if __name__ == "__main__":
    main()