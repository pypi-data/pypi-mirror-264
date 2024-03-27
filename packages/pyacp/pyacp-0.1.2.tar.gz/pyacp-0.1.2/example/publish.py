import ctypes
import sys
import time
sys.path.append('./proto')
sys.path.append('.')
import acp_pb2
import acp_enumdef_pb2
import pyacp
def main():
    print("publisher")
    handle = pyacp.publisher_init(0,"c_pub_test")
    print(handle) 
    req = acp_pb2.Request()
    req.ReadReq.IdGroup = acp_enumdef_pb2.PLC_APPBACKUP
    req.ReadReq.Offset = 0
    req.ReadReq.Length = 1111
    while pyacp.publisher_hassubscribers(handle) != True:
        print("has no subscribers")
        time.sleep(1)
    i = 0
    while(True):
        i+=1
        pyacp.publisher_publish(handle, req)
        time.sleep(1)
        if (i == 5):
            pyacp.publisher_destroy(handle)
            break
    
if __name__ == "__main__":
    main()