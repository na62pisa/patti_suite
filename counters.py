#!/usr/bin/python
import os;
import time;
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RED = '\033[31m'



import sys
sys.stdout.write("\x1b]2;PATTI COUNTERS\x07")
sys.stdout.write("\x1b[8;43;150t")
arg1 = sys.argv[1]
narg = len(sys.argv)
if narg!='2':
	if arg1=='0' or arg1=="PP0" or arg1=="pp0":
		baddr=0x4000000
	if arg1=='1' or arg1=="PP1" or arg1=="pp1":
		baddr=0x5000000
	if arg1=='2' or arg1=="PP2" or arg1=="pp2":
		baddr=0x6000000
	if arg1=='3' or arg1=="PP3" or arg1=="pp3":
		baddr=0x7000000
else:
	print "Number of PP is required!"
	sys.exit()

pid=os.getpid()
filen=".tmp_cnt_"+str(pid)	

import signal
def signal_handler(signal, frame):
        os.system("rm "+filen)
        print('PATTI RULES!')
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


address=0x100000+baddr
eobadd=0x100208+baddr
oldeob=0
spill=0x10020C+baddr
trig_addr=0x100200+baddr
gen_addr=0x2088+baddr

nburst=-1
while(1):
        time.sleep(2)
        eob=os.popen("lbread "+hex(eobadd)+" 1|awk '{print $2}'").read()
        gen=os.popen("lbread "+hex(gen_addr)+" 1|awk '{print $2}'").read()
        gstartp=gen[6]
        gstartt=gen[7]
        if eob!=oldeob: 
	        nburst=nburst+1
		os.system("lbread "+hex(address)+" 128 |awk '{print $2 FS $3 FS $4 FS $5}' > .tmp_cnt_"+str(pid))
		time.sleep(1)
		dataf = open(filen,"r")
		x = []	
		for line in dataf.readlines():
			y = [value for value in line.split()]
			x.append(y)
		dataf.close()
		a=0
		v0=[]
		v1=[]
		v2=[]
		v3=[]
		spill_time=os.popen("lbread "+hex(spill)+" 1|awk '{print $2}'").read()
                print spill_time[0:8],"ciao"
		if spill_time[0:8]=='ffffffff':
                        print "CIAO"
			spill_time=str(0)
		while a < 32:
        		i0 = a 
        		i1 = a + 32
        		i2 = a + 64
        		i3 = a + 96   
        		a0 = x[int(i0/4)][i0%4]
        		a1 = x[int(i1/4)][i1%4]
        		a2 = x[int(i2/4)][i2%4]
        		a3 = x[int(i3/4)][i3%4]
        		v0.append(a0)
        		v1.append(a1)
        		v2.append(a2)
        		v3.append(a3)
			a = a + 1
                print " "
                print bcolors.BOLD+"Burst: "+str(nburst)+bcolors.ENDC
        	print '%30s %30s %30s %30s' % ("TDC0","TDC1","TDC2","TDC3")
                print "----------------------------------------------------------------------------------------------------------------------------------------"
		a=0
		while a < 32:
                        n0=int(v0[a],16)
                        n1=int(v1[a],16)
                        n2=int(v2[a],16)
                        n3=int(v3[a],16)
                        if int(spill_time,16)!=0:
	                        r0=round((n0/(int(spill_time,16)*25*0.000000001))*0.001,2)
	                        r1=round((n1/(int(spill_time,16)*25*0.000000001))*0.001,2)
	                        r2=round((n2/(int(spill_time,16)*25*0.000000001))*0.001,2)
	                        r3=round((n3/(int(spill_time,16)*25*0.000000001))*0.001,2)
			else:
				r0=0
				r1=0
				r2=0
				r3=0
                        rate0=bcolors.OKBLUE+" ("+str(r0)+" kHz)"+bcolors.ENDC
                        rate1=bcolors.OKBLUE+" ("+str(r1)+" kHz)"+bcolors.ENDC
                        rate2=bcolors.OKBLUE+" ("+str(r2)+" kHz)"+bcolors.ENDC
                        rate3=bcolors.OKBLUE+" ("+str(r3)+" kHz)"+bcolors.ENDC

			s0='%15s %15s' % (str(int(v0[a],16)), rate0)
			s1='%15s %15s' % (str(int(v1[a],16)), rate1)
			s2='%15s %15s' % (str(int(v2[a],16)), rate2)
			s3='%15s %15s' % (str(int(v3[a],16)), rate3)
			print 'ch(%2d) %40s %40s %40s %40s' % (a, s0, s1, s2, s3)                           
			a = a + 1
                print bcolors.RED+"----------------------------------------------------------------------------------------------------------------------------------------"+bcolors.ENDC
                v0 = [int(x,16) for x in v0]
                v1 = [int(x,16) for x in v1]
                v2 = [int(x,16) for x in v2]
                v3 = [int(x,16) for x in v3]

                tot0=sum(v0)
                tot1=sum(v1)
                tot2=sum(v2)
                tot3=sum(v3)
                if int(spill_time,16)!=0:
	                r0=round((tot0/(int(spill_time,16)*25*0.000000001))*0.001,2)
	                r1=round((tot1/(int(spill_time,16)*25*0.000000001))*0.001,2)
	                r2=round((tot2/(int(spill_time,16)*25*0.000000001))*0.001,2)
	                r3=round((tot3/(int(spill_time,16)*25*0.000000001))*0.001,2)
		else:
			r0=0
			r1=0
			r2=0
			r3=0
                rate0=bcolors.OKBLUE+" ("+str(r0)+" kHz)"+bcolors.ENDC
                rate1=bcolors.OKBLUE+" ("+str(r1)+" kHz)"+bcolors.ENDC
                rate2=bcolors.OKBLUE+" ("+str(r2)+" kHz)"+bcolors.ENDC
                rate3=bcolors.OKBLUE+" ("+str(r3)+" kHz)"+bcolors.ENDC
		s0='%15s %15s' % (bcolors.RED+str(tot0), str(rate0))
		s1='%15s %15s' % (bcolors.RED+str(tot1), str(rate1))
		s2='%15s %15s' % (bcolors.RED+str(tot2), str(rate2))
		s3='%15s %15s' % (bcolors.RED+str(tot3), str(rate3))
                print 'SUMMARY:        %40s      %40s      %40s      %40s' % (s0,s1,s2,s3)
                trigx=os.popen("lbread "+hex(trig_addr)+" 1|awk '{print $2}'").read()
                trig=bcolors.RED+str(int(trigx,16))+bcolors.ENDC
                sstime=bcolors.RED+str(int(spill_time,16)*25*0.000000001)+bcolors.ENDC
                
                print 'TRIGGERS: %20s    SPILL LENGTH: %20s s' % (trig,sstime)
                if gstartp=="1":
                	pon = bcolors.OKGREEN+"ON"+bcolors.ENDC
		else:
                	pon = bcolors.RED+"OFF"+bcolors.ENDC
                if gstartt=="1":
                	ton = bcolors.OKGREEN+"ON"+bcolors.ENDC
		else:
                	ton = bcolors.RED+"OFF"+bcolors.ENDC
		print "PATTI PULSER: "+pon+"  PATTI TRIGGER: "+ton
                print bcolors.RED+"----------------------------------------------------------------------------------------------------------------------------------------"+bcolors.ENDC
		print " "                
 		oldeob=eob
