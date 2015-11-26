#!/usr/bin/python
# new version with production of files for
# testbench
import sys;
import os;
import time;
import random;
import imp;

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

print bcolors.RED+"-----------------------------------------------"
print bcolors.OKBLUE+"WELCOME TO BENCHFILE GENERATOR"+bcolors.ENDC
print bcolors.RED+"-----------------------------------------------"+bcolors.ENDC

def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def input_pp(question,default=0):
    prompt="["+str(default)+"]"
    while True:
        print bcolors.BOLD+question+prompt+bcolors.ENDC
        pp_input=raw_input().lower()
        if pp_input=="":
            return default
        else:
            if is_number(pp_input):
                return pp_input
            else:
                print bcolors.RED+"Not valid number!"+bcolors.ENDC

def input_repeat(question,default=0):          
    prompt="["+str(default)+"]"
    while True:
        print bcolors.BOLD+question+prompt+bcolors.ENDC
        rr_input=raw_input().lower()
        if rr_input=="":
            return default
        else:
            if is_number(rr_input):
                return rr_input
            else:
                print bcolors.RED+"Not valid number!"+bcolors.ENDC

active_tdc=[0 for x in range(4)]
ntot_active_tdc=0
def input_period(question,default=5):
    prompt="["+str(default)+"]"
    while True:
        print bcolors.BOLD+question+bcolors.ENDC
        period=raw_input().lower()
        if is_number(period):
            return period
        else:
            print "Not valid number!"
            return

def input_file(question,ii,default=""):
    while True:
        global ntot_active_tdc
        print bcolors.BOLD,
        prompt = bcolors.RED+str(ii)+bcolors.ENDC
        print(question+prompt)
        print bcolors.ENDC,
        filename=raw_input().lower()
        if filename=='':
            print bcolors.RED+"no file for TDC "+str(ii)+bcolors.ENDC
            active_tdc[ii]=0
            return default
        else:
            if os.path.isfile(filename):
                ntot_active_tdc=ntot_active_tdc+1
                active_tdc[ii]=1
                return filename
            else:
                print bcolors.RED+"File doesn't exist!!!"+bcolors.ENDC

def conv_rawcont(rawcont):
    print rawcont+" "+str(int(rawcont,0))
    
def read_file(filename):
    irawcont_list=[0 for x in range(4096)]
    if (os.path.isfile(filename)):
        f=open(filename,"r")
        num_lines = sum(1 for line in f)
#        print num_lines
        f.seek(0)
        line_chk = f.readlines()
        word_chk=line_chk[0].split()
#        print word_chk[0]
        f.seek(0)
        if word_chk[0]=="lbwrite" and num_lines==4096:
            ii=0
            for line in f:
                wordl = line.split()
                rawcont=wordl[2]
                irawcont=int(rawcont,0)
                irawcont_list[ii]=irawcont
                ii=ii+1
            return irawcont_list        
        else :
            print "Problem!"
            return


def conv_channel(cont):
    ch=[0 for x in range(32)]
    for j in range(32):
        ch[j]=(cont&(1<<j))>>j 
    return ch

#---main

pp=int(input_pp("Enter the number of PP: "))
repeat=int(input_repeat("Enter number of reading file repeation: "))
repeat_list=[repeat for x in range(4)]
filename_out0="output_pp"
filename_out=filename_out0+str(pp)+".txt"
outfile=open(filename_out,"w")

#iin=0
filelist=[0 for x in range(4)]
for i in range(4):
    filen=input_file("Files to read (enter if no file):",i)

    if (filen!=""):
        filelist[i]=filen
       # iin=iin+1
        print bcolors.OKGREEN+"OK!"+bcolors.ENDC
period_list=[0 for x in range(4)]
ih=0
for i in range(4):
    if active_tdc[i]==1:
        a=0
        while(a==0):
            quest="Period for TDC "+str(i)
            period=input_period(quest)
            if period!="":
                period_list[i]=int(period)
                a=1
            else:
                period_list[i]=0
                print bcolors.RED+"Repeat!"+bcolors.ENDC
                a=0

irawcont_list=[[0 for x in range(4096)] for x in range(4)]
print bcolors.OKBLUE+"I'm reading the files:"+bcolors.ENDC
print active_tdc
print filelist
for i in range(4):
    if active_tdc[i]==1:
        print i,filelist[i]
        print "File "+filelist[i]
        irawcont_list[i]=read_file(filelist[i])
#        print irawcont_list[ih]

empty=0
ts_start=0xA0000000
freq=75
n_to_read=[0 for x in range(4)]
empty_list=[0 for x in range(4)]
for i in range(4):
    if active_tdc[i]==1:
        empty_list[i]=0
    else:
        empty_list[i]=1

while(empty!=4):
    space=" "
    aword=ts_start
    atime=1
    outfile.write("%x"%aword)
    outfile.write(space)
    outfile.write(str(atime))
    outfile.write("\n")
    htime=1
    btot=0
    for i in range(4):
        intcont=irawcont_list[i]
        ntdc=(i+pp*4)<<24
        if active_tdc[i]==1:
            nread=int(6400/(freq*period_list[i]))
            nstart=n_to_read[i]
            nend=nstart+nread
            if nend>4095:
                nend=4095
                n_to_read[i]=0
                repeat_list[i]=repeat_list[i]-1
            else:
                n_to_read[i]=nend
            if repeat_list[i]>-1:    
                t0=0
                for ww in range(nstart,nend):
                    lead0=0x40000000+(ts_start-0xA0000000)*4096
                    trai0=0x50000000+(ts_start-0xA0000000)*4096
                    channel_on=conv_channel(intcont[ww])
                    btmp=0
                    for jj in range(len(channel_on)):
                        if channel_on[jj]==1:
                            deltat=random.randint(0,4)
                            time=(t0+deltat)&0xFFFF
                            if time > 0xFFFF:
                                    time=0xFFF
                            lead=lead0+ntdc+(jj<<19)+time
                            trai=trai0+ntdc+(jj<<19)+time
#                            print nstart,nend,ntdc,hex(lead),hex(time),hex(t0),jj
                            outfile.write("%x"%lead)
                            outfile.write(space)
                            outfile.write(str(htime))
                            outfile.write("\n")
                            outfile.write("%x"%trai)
                            outfile.write(space)
                            outfile.write(str(htime))
                            outfile.write("\n")
                            btmp=btmp+2
                    btot=btot+btmp
                    t0=freq*(period_list[i])*10+t0

            else:
                empty_list[i]=1
                empty=empty_list[0]+empty_list[1]+empty_list[2]+empty_list[3]

    bword=0xB0000000+btot

    btime=0
    if (btot < 1024):
        btime=1024-btot
    else:
        btime=1
    outfile.write("%x"%bword)
    outfile.write(space)
    outfile.write(str(btime))
    outfile.write("\n")
    ts_start=ts_start+0x10



        

