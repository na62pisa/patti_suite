#!/usr/bin/python
import sys;
import os;
import time;
import random;
import imp;
try:
    imp.find_module('matplotlib')
    found_math = True
except ImportError:
    found_math = False

if found_math==True:    
    import matplotlib.pyplot as plt;
    print ("Visual review available!")

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
print bcolors.OKBLUE+"WELCOME TO MEM FILE WIZARD"+bcolors.ENDC
print bcolors.RED+"-----------------------------------------------"+bcolors.ENDC
channel=[[0 for x in range(4096)] for x in range(33)]
proto=[[0 for x in range(4096)] for x in range(10)] 
nproto=[0 for x in range(10)]
list_channel=[]

def q_main(question, default="review"):
        valid = {"proto":0, "fill":1, "review":2, "reset":3, "dump":4, "exit":5,
        "P":0, "F":1, "R":2, "S":3, "D":4, "E":5,
        "p":0, "f":1, "r":2, "s":3, "d":4, "e":5}
        if default is None:
		prompt="[no default]"
	else:
		prompt="["+default+"]"
	while True:
                print bcolors.BOLD,
		print(question+prompt)
                print bcolors.ENDC,
		choice = raw_input().lower()
		if choice in valid:
			return valid[choice]
		elif choice == '':
			print default
			return valid[default]
		else:
			print bcolors.RED+'Please respond a valid option'+bcolors.ENDC        


def q_fill(question, default="0"):
        valid = {"proto":0, "full":1, "partial":2, "free":3, "random":4,
        "p":0, "f":1, "a":2, "e":3, "r":4,
        "P":0, "F":1, "A":2, "E":3, "R":4}

        if default is None:
		prompt="[no default]"
	else:
		prompt="["+default+"]"
	while True:
                print bcolors.BOLD,
		print(question+prompt)
                print bcolors.ENDC,
		choice = raw_input().lower()
		if choice in valid:
			return valid[choice]
		elif choice == '':
			print valid[default]
			return valid[default]
		else:
			print bcolors.RED+'Please respond a valid option'+bcolors.ENDC        


def set_proto(ProtoIndex):
    print("How many slot do you want to fill?")
    nslot=input()
    if (nslot<4096):
        nproto[ProtoIndex]=nslot
        for i in range(0,nslot):
            nn=99
            while (not(nn==0 or nn==1)):
                print "Set Element n."+str(i)+": "
                nn= input()
                proto[ProtoIndex][i]=nn
    else:
        print "Too many slots required for proto"
        return 0


def inspect():
    rowslot=[0 for x in range(4096)]
    for j in range(4096):
        ii=0
        for i in range(len(channel)):
            rowslot=channel[i]
            if ii==0:
                print "Slot "+str(j)+": "+str(rowslot[j]),
            elif ii==32:
               print " "
            else:
                print " "+str(rowslot[j]),
            ii=ii+1
    return 0


def inspect_sl(nsl):
    rowslot=[0 for x in range(4096)]
    j=nsl
    ii=0
    for i in range(len(channel)):
        rowslot=channel[i]
        if ii==0:
            print "Slot "+str(j)+": "+str(rowslot[j]),
        elif ii==32:
            print " "
        else:
            print " "+str(rowslot[j]),
        ii=ii+1
    return 0

def inspect_ch(nch):
    print "Channel: "+str(nch)
    print channel[nch]
        
def vis_inspect():
    fig = plt.figure()
    for i in range(33):
        rowslot=channel[i]
        plt.subplot(33,1,i+1)
        plt.plot(rowslot)
    plt.show()

        
def vispart_inspect(listch,start,end):
    fig = plt.figure()
    nch=len(listch)
    ii=0
    for ch in listch:
        rowslot=channel[ch]
        plt.subplot(nch,1,ii+1)
        plt.plot(rowslot)
        plt.axis([start,end,-0.1,1.1])
        ii=ii+1
    plt.show()


def q_review(question, default="all"):
        valid = {"slot":0, "channel":1, "all":2}
        if default is None:
		prompt="[no default]"
	else:
		prompt="["+default+"]"
	while True:
                print bcolors.BOLD,
		print(question+prompt)
                print bcolors.ENDC,
		choice = raw_input().lower()
		if choice in valid:
			return valid[choice]
		elif choice == '':
			print valid[default]
			return valid[default]
		else:
			print bcolors.RED+'Please respond a valid option'+bcolors.ENDC        


def q_reset(question, default="all"):
        valid = {"area":1, "all":0}
        if default is None:
		prompt="[no default]"
	else:
		prompt="["+default+"]"
	while True:
                print bcolors.BOLD,
		print(question+prompt)
                print bcolors.ENDC,
		choice = raw_input().lower()
		if choice in valid:
			return valid[choice]
		elif choice == '':
			print valid[default]
			return valid[default]
		else:
			print bcolors.RED+'Please respond a valid option'+bcolors.ENDC        


def q_visual(question, default="global"):
        valid = {"global":1, "partial":0,
                 "g":1, "p":0,
                 "G":1, "P":0}
        if default is None:
		prompt="[no default]"
	else:
		prompt="["+default+"]"
	while True:
                print bcolors.BOLD,
		print(question+prompt)
                print bcolors.ENDC,
		choice = raw_input().lower()
		if choice in valid:
			return valid[choice]
		elif choice == '':
			print valid[default]
			return valid[default]
		else:
			print bcolors.RED+'Please respond a valid option'+bcolors.ENDC        


def q_yesno(question, default="yes"):
        valid = {"yes":0, "no":1}
        if default is None:
		prompt="[no default]"
	else:
		prompt="["+default+"]"
	while True:
                print bcolors.BOLD,
		print(question+prompt)
                print bcolors.ENDC,
		choice = raw_input().lower()
		if choice in valid:
			return valid[choice]
		elif choice == '':
			print valid[default]
			return valid[default]
		else:
			print bcolors.RED+'Please respond yes or no'+bcolors.ENDC        

def wregister(addr,cont):
#        line = 'lbwrite '+str(hex(addr))+' '+str(hex(cont))+'\n'
        line = 'lbwrite '+str(hex(addr))+' '+str("0x%x"%cont)+'\n'
        return line

def dumpfile(NameOfFile, NameOfFileTrigger, pp, tdc):
    ok_flag=1
    f = open(NameOfFile,'w')
    g = open(NameOfFileTrigger,'w')
    rowslot=[0 for x in range(4096)]
    pp_op = {0: 0x0,
             1: 0x4,
             2: 0x8,
             3: 0xC}
    ntdc=pp_op[tdc]    
    jj=0
    for j in range(4096):
        ii=0
        word=0
        word_trigger=0
        for i in range(len(channel)):
            rowslot=channel[i]
            word=word|((rowslot[j]&1)<<ii)
            if ii==32:
                word_trigger=((rowslot[j]&1))
            ii=ii+1

#        addr=((pp&0xF)<<24)+((2&0xF)<<20)+((ntdc&0xF)<<12)+((jj&0xFFF))
        addr=((pp&0xF)<<24)+((2&0xF)<<20)+((jj+(ntdc*0x1000)&0xFFFF))
        cont=word
        f.write(wregister(addr,cont))
        addrt=((pp&0xF)<<24)+((2&0xFF)<<16)+((jj+(ntdc*0x1000)&0xFFFF))
        contt=word_trigger
        g.write(wregister(addrt,contt))
        jj=jj+4
        ok_flag=0
    f.close()
    g.close()
    return ok_flag


def q_pptdc(question, default="0"):
        valid = {"0":0, "1":1, "2":2, "3":3}
        if default is None:
		prompt="[no default]"
	else:
		prompt="["+default+"]"
	while True:
                print bcolors.BOLD,
		print(question+prompt)
                print bcolors.ENDC,
		choice = raw_input().lower()
		if choice in valid:
			return valid[choice]
		elif choice == '':
			print valid[default]
			return valid[default]
		else:
			print bcolors.RED+'Please respond a valid PP number'+bcolors.ENDC        


def q_output_file(question, default="patti_mem.dat"):
        if default is None:
		prompt="[no default]"
	else:
		prompt="["+default+"]"
	while True:
                print bcolors.BOLD,
                print(question+prompt)
                print bcolors.ENDC,
		choice = raw_input().lower()
                if choice=='':
                        return default
                else:
                        return choice



# --- main
while (True):
    choice=q_main("Action?(Proto - Fill - Review - reSet - Dump - Exit)")
    if (choice==0):
        for i in range(10):
            print "Proto n."+str(i)+": "+str(nproto[i])
        print "Which proto do you want to set?"
        nn=input()
        set_proto(nn)
        print "Proto n."+str(nn)+": "
        print proto[nn][0:nproto[nn]]
    elif (choice==1):
        print "Please insert the list of channels to fill (99 for all the channels, 33 for trigger)"
        s = raw_input()
        list_channel = []
        if (s=="99"):
            list_channel=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]
        else:
            list_channel = map(int, s.split())

    #    print list_channel
        choice_fill=q_fill("Which fill style do you prefere? (Proto - Full - pArtial - frEe - Random)")
        if(choice_fill==0):
            print "Available Protos:"
            for i in range(10):
                print "Proto n."+str(i)+": "+str(nproto[i])
            protoi=input("Which prototype do you want to use?")
            protomax=nproto[protoi]
            start_slot=input("Start slot:")
            end_slot=input("End slot:")
            for ch in list_channel:
                ii=-1
                for i in range(start_slot, end_slot):
                    ii=ii+1
                    if ii>protomax:              
                        ii=0
                        channel[ch][i]=proto[protoi][ii]
                    else:
                        channel[ch][i]=proto[protoi][ii]
        elif(choice_fill==1):
            zeros_full=input("how many zeros?")
            ones_full=input("followed by how many ones?")
            for ch in list_channel:
                ii=-1
                for i in range(4096):

                    for j in range(zeros_full):
                        if ii<4095:
                            ii=ii+1
                            channel[ch][ii]=0
                    for k in range(ones_full):
                        if ii<4095:
                            ii=ii+1
                            channel[ch][ii]=1
        elif(choice_fill==2):
            start_slot=input("Start slot:")
            end_slot=input("End slot:")
            zeros_full=input("how many zeros?")
            ones_full=input("followed by how many ones?")
            for ch in list_channel:
                ii=start_slot-1
                for i in range(start_slot, end_slot):
                    for j in range(zeros_full):
                        if ii<4095:
                            ii=ii+1
                            channel[ch][ii]=0
                    for k in range(ones_full):
                        if ii<4095:
                            ii=ii+1
                            channel[ch][ii]=1
        elif(choice_fill==3):
            start_slot=input("Start slot:")
            end_slot=input("End slot:")
            for ch in list_channel:
                for i in range(start_slot, end_slot):
                    print "Input value for ch "+str(ch)+" slot "+str(i)
                    nn=input()
                    channel[ch][i]=nn
        elif(choice_fill==4):
            random.seed()
            start_slot=input("Start slot:")
            end_slot=input("End slot:")
            rand_freq=input("Rand frequency (higher number means smaller probability):")
            random.seed()
            print list_channel
            for ch in list_channel:
                for i in range(start_slot, end_slot):
                    if rand_freq>1:
                        rr=random.randint(0,rand_freq)
                        if rr>rand_freq-1:
                            nn=random.getrandbits(1)
                            channel[ch][i]=nn
                        else:
                            nn=0
                            channel[ch][i]=nn
                    else:
                        nn=random.getrandbits(1)
                        channel[ch][i]=nn
    elif(choice==2):
        choice_review=q_review("Review per slot, channel, all?")
        if choice_review==0:
            nsl=input("N slot to review")
            inspect_sl(nsl)
        elif choice_review==1:
            nch=input("N channel to review")
            inspect_ch(nch)
        elif choice_review==2:
            inspect()
            if(found_math==True):
                qvis=q_yesno("Do you want to have the visual review?")
                if qvis==0:
                    qvisc=q_visual("Do you want to have Global or Partial view?")
                    if (qvisc==1):
                        vis_inspect()
                    elif (qvisc==0):
                        print "Please insert the list of channels to view (99 for all the channels, 33 for trigger)"
                        sss = raw_input()
                        list_channel_view = []
                        if (sss=="99"):
                            list_channel_view=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]
                        else:
                            list_channel_view = map(int, sss.split())
                            print "Please insert the starting tslot to view"
                            view_start= input()
                            print "Please insert the ending tslot to view"
                            view_end= input()
                        vispart_inspect(list_channel_view,view_start,view_end)

    elif(choice==3):
        choice_reset=q_reset("Do you want to reset all or area?")
        if (choice_reset==0):
            channel=[[0 for x in range(4096)] for x in range(33)]
        elif (choice_reset==1):
            print "Please insert the list of channels to reset (99 for all the channels, 33 for trigger)"
            ss = raw_input()
            list_channel_reset = []
            if (ss=="99"):
                list_channel_reset=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]
            else:
                list_channel_reset = map(int, ss.split())

            print "Please insert the starting tslot to reset"
            reset_start= input()
            print "Please insert the ending tslot to reset"
            reset_end= input()
            for ch in list_channel_reset:
                for i in range(reset_start, reset_end):
                    channel[ch][i]=0

    elif(choice==4):
        qdump=q_yesno("Do you want to dump the memory files?")
        if qdump==0:
            NameOfFile=q_output_file("Name of the output file (pattern)?")
            NameOfFileTrigger=q_output_file("Name of the output file (trigger)?", "patti_trg.dat")
            pp_ans = q_pptdc("Which PP do you want to configure?")
            pp_op = {0: 4,
                     1: 5,
                     2: 6,
                     3: 7}
            pp=pp_op[pp_ans]
            cont=True
            while(cont):
                tdc_ans = q_pptdc("Which TDC do you want to configure?")
                tdc=tdc_ans
                NameOfFilex,exten=os.path.splitext(NameOfFile)
                NameOfFileTriggerx,extenx=os.path.splitext(NameOfFileTrigger)
                NameOfFilex=NameOfFilex+"_tdc"+str(tdc)+exten
                NameOfFileTriggerx=NameOfFileTriggerx+"_tdc"+str(tdc)+extenx
                rdump=dumpfile(NameOfFilex,NameOfFileTriggerx,pp,tdc)
                q_tdccont=q_yesno("Do you want to dump additional file for different tdc")
                if rdump==0:
                    print "Files dumped!"
                    print "Wizard exit normally! Well Done!"
#                    sys.exit()
                else:
                    print "Problem in writing files"
                if q_tdccont == 0:
                    cont=True
                else:
                    cont=False
            sys.exit()
    elif(choice==5):
        print "Exit without dump :( "
        sys.exit()
    #print channel[4][:] #canale 4: lista con tutte le slot
    #print channel[1:4][5]
#    inspect()
    #vis_inspect()
