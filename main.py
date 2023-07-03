from scapy.all import *
from datetime import datetime
from multiprocessing import *
import functools
import sqlite3


startTime = datetime.now()

dst_ip = "123.14.32.31"
dst_port = 1024
range01 = range(34690,34700)
range02 = range(34700,34710)
range03 = range(34710,34720)
range04 = range(34720,34730)



def syn_send(param_dst_ip,param_dst_port):
    syn_package = IP(dst=param_dst_ip, id=RandShort(), ttl=99) / TCP(sport=RandShort(), dport=[param_dst_port],seq=RandShort(), ack=RandShort(),window=RandShort(), flags="S")
    ans = sr1(syn_package, verbose=0, timeout=2)
    try:
        pktflags = ans.getlayer(TCP).flags
        if pktflags == None:
            pass
        else:
            if pktflags == "SA":
                print("Port Open:", param_dst_port,param_dst_ip)
                conn = sqlite3.connect('maldb.db', timeout=15)
                now = datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M")
                conn.execute("INSERT INTO open_port (time,dst_ip_addr,dst_port) VALUES (?, ?, ?)", (dt_string, param_dst_ip, param_dst_port))
                conn.commit()
                conn.close()

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
