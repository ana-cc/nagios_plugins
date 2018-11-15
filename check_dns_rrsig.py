import subprocess
import argparse
import sys
from datetime import datetime

def check_expiry(domain,c,w,server):
    OK, WARNING, CRITICAL, UNKNOWN = range(4)
    t = None
    dig_args = ['dig', domain, '+dnssec', '+short', 'SOA']
    if server:
        dig_args.append('@'+server)

    p = subprocess.Popen(dig_args, stdout=subprocess.PIPE)
    res = p.communicate()[0]
    res = (res.decode("utf-8")).split('\n')
    for line in res: 
        if line.startswith('SOA'):
            t = line.split(' ')[4]
    if t == None:
        print('Zone does not exist or is not DNSSEC enabled')
        return UNKNOWN
    else:
        d = datetime.strptime(t,'%Y%m%d%H%M%S')
        present = datetime.now()
        delta = d - present
     
        print('Signature expires in %s days' % str(delta.days))

        if delta.days < c:
            return CRITICAL
        if delta.days < w:
            return WARNING
        else: return OK 
   

parser = argparse.ArgumentParser(description='Checks the RRSIG expiry date on the SOA record of a DNSSEC enabled domain')

parser.add_argument('-c', type=int, help='Number of days left until expiry for which the plugin returns CRITICAL', default=10)
parser.add_argument('-w', type=int, help='Number of days left until expiry for which the plugin returns WARNING', default=28)
parser.add_argument('-s', type=str, help='Server to check against')
parser.add_argument('domain', type=str, help='Domain to check')

args = parser.parse_args()

sys.exit(check_expiry(args.domain, args.c, args.w, args.s))
