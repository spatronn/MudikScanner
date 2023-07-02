import multiprocessing

from scapy.all import *
from datetime import datetime
from multiprocessing import *
import functools

startTime = datetime.now()

dst_ip = "92.205.182.247"
dst_port = 1024
range01 = range(1024,16127)
range02 = range(16127,32254)
range03 = range(32254,48381)
range04 = range(48381,65536)

def syn_send(param_dst_ip,param_dst_port):
    syn_package = IP(dst=param_dst_ip, id=RandShort(), ttl=99) / TCP(sport=RandShort(), dport=[param_dst_port],seq=RandShort(), ack=RandShort(),window=RandShort(), flags="S")
    ans = sr1(syn_package, verbose=0, timeout=0.1)
    try:
        pktflags = ans.getlayer(TCP).flags
        if pktflags == None:
            pass
        else:
            print(pktflags)
            if pktflags == "SA":
                print("Port Open:", param_dst_port)
            else:
                pass
    except:
        pass
        #print("Timeout or closed port!!",param_dst_port)

def smap(f):
    return f()

def scan_01():
    for i in range01:
        syn_send(dst_ip,i)

def scan_02():
    for i in range02:
        syn_send(dst_ip,i)

def scan_03():
    for i in range03:
        syn_send(dst_ip,i)

def scan_04():
    for i in range04:
        syn_send(dst_ip,i)

def main():
    f_scan01 = functools.partial(scan_01)
    f_scan02 = functools.partial(scan_02)
    f_scan03 = functools.partial(scan_03)
    f_scan04 = functools.partial(scan_04)

    with Pool() as pool:
        res = pool.map(smap, [f_scan01,f_scan02,f_scan03,f_scan04])
if __name__ == '__main__':
    main()
    print("Elapsed Time : ", datetime.now() - startTime)
