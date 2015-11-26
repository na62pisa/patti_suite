#!/usr/bin/python
# ------------------------------------------
# VERSION 1.5
# - (1.4) added temporary patch for bug in fw when the latency is not set (to be removed)
# - (1.5) added selection of external pulser in back selection register
# GL software
# ------------------------------
import os;
import time;
import sys;
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

os.system('clear')

import signal
def signal_handler(signal, frame):
        print('Exit without any dumped file :(')
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

#GLOBAL VARIABLE
trgyes=0
patchyes=0
reset_register=0
reset_addr=0
start_register=0
start_addr=0
conf_register=0
conf_addr=0
period_register =0
period_addr =0
selection_register = 0
selection_addr = 0
selection_register_back = 0
selection_addr_back = 0
window_register = 0
window_addr = 0
mask_register = 0
mask_addr = 0
pulse_register = 0
pulse_addr= 0
trigger_register = 0
trigger_addr = 0 
triggerp_register = 0
triggerp_addr = 0 
latency_register = 0
latency_addr = 0
chtrg_register_0 = 0
chtrg_register_1 = 0
chtrg_register_2 = 0
chtrg_register_3 = 0
chtrg_addr= 0
tdc_cht=0
mfile0=""
mfile1=""
mfile2=""
mfile3=""
trg_file=""
smode_global=99
tdc_global=0
trgmode_global=0
icont=0
configured_tdc=[0,0,0,0]
memyesg=0
memyesg2=0
trgfileyg=0

#SUM
sum_pp=""
sum_tdc=""
sum_pulser=""
sum_width=""
sum_cont=""
sum_nmem=""
sum_ext=""
sum_trgmsg=""
sum_specialt=""
sum_rndperiod=""
sum_ttc=""
sum_burstpulser=""
print bcolors.RED+"-----------------------------------------------"
print bcolors.OKBLUE+"WELCOME TO PATTI WIZARD"+bcolors.ENDC
print bcolors.RED+"-----------------------------------------------"+bcolors.ENDC


def q_pp(question, default="0"):
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
                        sum_pp = choice
			return valid[choice]
		elif choice == '':
                        sum_pp = default
			print valid[default]
			return valid[default]
		else:
			print bcolors.RED+'Please respond a valid PP number'+bcolors.ENDC        


def q_tdc(question, default="0xF"):
        if default is None:
		prompt="[no default]"
	else:
		prompt="["+default+"]"
	while True:
                print bcolors.BOLD,
		print(question+prompt)
                print bcolors.ENDC,
		sdelay = raw_input().lower()
		if sdelay == '':
                        sum_tdc=str(default)
			print int(default,0)
			return int(default,0)
		elif int(sdelay,0)<0x10:
                        sum_tdc=str(sdelay)
			return int(sdelay,0) 	
		else:
			print bcolors.RED+'Please put a valid TDC number'+bcolors.ENDC



def q_special_cfg(question, default="no"):
	valid = {"no":0, "yes":1}
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
			print bcolors.RED+'Please respond with yes or no'+bcolors.ENDC



def q_pulser_cfg(question, default="periodic"):
	valid = {"nothing": 0, "periodic":1, "random":2, "shoot":3, 
	"externalpulse":4, "external+periodic1":5, 
	"external+periodic2":6, "external pulse trigger":7}
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
                        sum_pulser=choice
			return valid[choice]
		elif choice == '':
                        sum_pulser=default
			print valid[default]
			return valid[default]
		else:
			print bcolors.RED+'Please respond with nothing, periodic,' \
			      ' random, shoot, externalpulse, ' \
 			      ' external+periodic1,'\
 			      ' external+periodic2 or external+pulse+trigger'+bcolors.ENDC

def q_width_cfg(question, default="clock"):
	valid = {"clock":0, "pulse":1}
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
                        sum_width=choice
			return valid[choice]
		elif choice == '':
                        sum_width=default
			print valid[default]
			return valid[default]
		else:
			print bcolors.RED+'Please respond with clock or pulse'+bcolors.ENDC

def q_cont_cfg(question, default="continue"):
	valid = {"continue":0, "npulse":1}
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
                        sum_cont=choice
			return valid[choice]
		elif choice == '':
                        sum_cont=default
			print valid[default]
			return valid[default]
		else:
			print bcolors.RED+'Please respond with continue or npulse'+bcolors.ENDC



def q_nmem_cfg(question, default="0x1"):
        if default is None:
		prompt="[no default]"
	else:
		prompt="["+default+"]"
	while True:
                print bcolors.BOLD,
                print(question+prompt)
                print bcolors.ENDC,
		speriod = raw_input().lower()
		if speriod == '':
                        sum_nmem=str(default)
			return int(default,0)
		elif int(speriod,0)<=0xFFFF:
                        sum_nmem=str(speriod)
			return int(speriod,0) 	
		else:
			print bcolors.RED+'Please put a number less than 0xFFFFFFFF'+bcolors.ENDC


	
def q_extpulse_cfg(question,default="external"):
	valid = {"external":1, "choke":0}
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
                        sum_ext=choice
			return valid[choice]
		elif choice == '':
                        sum_ext=default
			print valid[default]
			return valid[default]
		else:
			print bcolors.RED+'Please respond with external or choke'+bcolors.ENDC



def q_wpulser(question, default="0xF"):
        if default is None:
		prompt="[no default]"
	else:
		prompt="["+default+"]"
	while True:
                print bcolors.BOLD,
		print(question+prompt)
                print bcolors.ENDC,
		sdelay = raw_input().lower()
		if sdelay == '':
                        sum_tdc=str(default)
			print int(default,0)
			return int(default,0)
		elif int(sdelay,0)<0x10:
                        sum_tdc=str(sdelay)
			return int(sdelay,0) 	
		else:
			print bcolors.RED+'Please put which TDCs should be pulsered by external'+bcolors.ENDC

def q_trgmsg_cfg(question, default="0x01"):
        if default is None:
		prompt="[no default]"
	else:
		prompt="["+default+"]"
	while True:
                print bcolors.BOLD,
                print(question+prompt)
                print bcolors.ENDC,
		trgmsg = raw_input().lower()
                if trgmsg=='':
                        sum_trgmsg=default
			print int(default,0)
                        return int(default,0)
		elif int(trgmsg,0)<=0x3f:
                        sum_trgmsg=trgmsg
			return int(trgmsg,0) 	
		else:
			print bcolors.RED+'Please put a valid msg number'+bcolors.ENDC

def q_specialt_cfg(question, default="direct"):
	valid = {"normal":0, "direct":1, "random0":2, "random1":3}
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
                        sum_specialt=choice
			return valid[choice]
		elif choice == '':
                        sum_specialt=default
			print valid[default]
			return valid[default]
		else:
			print bcolors.RED+'Please respond with normal, direct, random0 or random1'+bcolors.ENDC
	

def q_rndperiod_cfg(question, default="custom"):
	valid = {"160":0, "custom":1}
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
                        sum_rndperiod=choice
			return valid[choice]
		elif choice == '':
                        sum_rndperiod=default
			print valid[default]
			return valid[default]
		else:
			print bcolors.RED+'Please respond with 160 or custom'+bcolors.ENDC


def q_burstpulser_cfg(question, default="no"):
	valid = {"no":0, "yes":1}
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
                        sum_burstpulser=choice
			return valid[choice]
		elif choice == '':
                        sum_burstpulser=default
			print valid[default]
			return valid[default]
		else:
			print bcolors.RED+'Please respond with yes or no'+bcolors.ENDC


def q_ttctrigger_cfg(question, default="no"):
	valid = {"no":0, "yes":1}
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
                        sum_ttc=choice
			return valid[choice]
		elif choice == '':
                        sum_ttc=default
			print valid[default]
			return valid[default]
		else:
			print bcolors.RED+'Please respond with yes or no'+bcolors.ENDC


def q_ttcwindow_cfg(question, default="0xF"):
        if default is None:
		prompt="[no default]"
	else:
		prompt="["+default+"]"
	while True:
                print bcolors.BOLD,
                print(question+prompt)
                print bcolors.ENDC,
		speriod = raw_input().lower()
		if speriod == '':
                        sum_ttcw=default
			return int(default,0)
		elif int(speriod,0)<=0xFFFFFFFF:
                        sum_ttcw=speriod
			return int(speriod,0) 	
		else:
			print bcolors.RED+'Please put a window width less than 0xFFFFFFFF'+bcolors.ENDC


def q_enadelay_cfg(question, default="yes"):
	valid = {"no":0, "yes":1}
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
			print bcolors.RED+'Please respond with yes or no'+bcolors.ENDC

def q_sdelay_cfg(question, default="0xE"):
        if default is None:
		prompt="[no default]"
	else:
		prompt="["+default+"]"
	while True:
                print bcolors.BOLD,
                print(question+prompt)
                print bcolors.ENDC,
		sdelay = raw_input().lower()
		if sdelay == '':
			print int(default,0)
			return int(default,0)
		if int(sdelay,0)<0xF:
			return int(sdelay,0) 	
		else:
			print bcolors.RED+'Please put a time less than 0xE'+bcolors.ENDC

def q_period_per(question, default="0x100"):
        if default is None:
		prompt="[no default]"
	else:
		prompt="["+default+"]"
	while True:
                print bcolors.BOLD,
                print(question+prompt)
                print bcolors.ENDC,
		speriod = raw_input().lower()
		if speriod == '':
			print int(default,0)
			return int(default,0)
		elif int(speriod,0)<0xFFFFFFFF:
			return int(speriod,0) 	
		else:
			print bcolors.RED+'Please put a time less than 0xFFFFFFFF'+bcolors.ENDC


def q_npulse_pul(question, default="0x10"):
        if default is None:
		prompt="[no default]"
	else:
		prompt="["+default+"]"
	while True:
                print bcolors.BOLD,
                print(question+prompt)
                print bcolors.ENDC,
		snum = raw_input().lower()
		if snum == '':
			print int(default,0)
			return int(default,0)
		elif int(snum,0)<0xFFFFFE:
			return int(snum,0) 	
		else:
			print bcolors.REDC+'Please put a number lower than 0xff'+bcolors.ENDC

def q_nmem_pul(question, default="0x1"):
        if default is None:
		prompt="[no default]"
	else:
		prompt="["+default+"]"
	while True:
                print bcolors.BOLD,
                print(question+prompt)
                print bcolors.ENDC,
		snum = raw_input().lower()
		if snum == '':
			print int(default,0)
			return int(default,0)
		elif int(snum,0)<0xFF:
			return int(snum,0) 	
		else:
			print bcolors.REDC+'Please put a number lower than 0xff'+bcolors.ENDC

def q_mask_msk(question, default="0xFFFFFFFF"):
        if default is None:
		prompt="[no default]"
	else:
		prompt="["+default+"]"
	while True:
                print bcolors.BOLD,
                print(question+prompt)
                print bcolors.ENDC,
		snum = raw_input().lower()
		if snum == '':
			print hex(int(default,0))
			return int(default,0)
		elif int(snum,0)<=0xFFFFFFFF:
			return int(snum,0) 	
		else:
			print bcolors.RED+'Please put a number lower than 0xffffffff'+bcolors.ENDC

def q_selection_sel(question, default="0xF"):
        if default is None:
		prompt="[no default]"
	else:
		prompt="["+default+"]"
	while True:
                print bcolors.BOLD,
                print(question+prompt)
                print bcolors.ENDC,
		snum = raw_input().lower()
		if snum == '':
			print int(default,0)
			return int(default,0)
		elif int(snum,0)<0x10:
			return int(snum,0) 	
		else:
			print bcolors.RED+'Please put a number lower than 0xF'+bcolors.ENDC

def q_trigger_opt(question, default="no"):
	valid = {"no":0, "yes":1}
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
			print bcolors.RED+'Please respond with yes or no'+bcolors.ENDC

def q_trigger_mode(question, default="uncorrelated"):		
        valid = {"correlated": 0, "uncorrelated": 1}
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
			print bcolors.RED+'Please respond with correlated or uncorrelated'+bcolors.ENDC

def q_trigger_conf(question, default="nothing"):		
	valid = {"nothing": 0, "downscaled":1, "memory":2, "random":3, 
	"periodic":4, "fast random":5, 
	"fast periodic":6}
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
			print bcolors.RED+'Please respond with yes or no'+bcolors.ENDC

def q_trigger_uncorr(question, default="nothing"):		
	valid = {"nothing": 0, "random":3, "periodic":4, "fast random":5, 
	         "fast periodic":6}
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
			print bcolors.RED+'Please respond with yes or no'+bcolors+ENDC


def q_trigger_corr(question, default="nothing"):		
	valid = {"nothing": 0, "downscaled":1, "memory":2}
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
			print bcolors.RED+'Please respond with yes or no'+bcolors.ENDC


def q_trigger_per(question, default="0x100"):
        if default is None:
		prompt="[no default]"
	else:
		prompt="["+default+"]"
	while True:
                print bcolors.BOLD,
                print(question+prompt)
                print bcolors.ENDC,
		speriod = raw_input().lower()
		if speriod == '':
			return int(default,0)
		elif int(speriod,0)<0xFFFFFFFF:
			return int(speriod,0) 	
		else:
			print bcolors.RED+'Please put a time less than 0xFFFFFFFF'+bcolors.ENDC


def q_trigger_dw(question, default="0x1"):
        if default is None:
		prompt="[no default]"
	else:
		prompt="["+default+"]"
	while True:
                print bcolors.BOLD,
                print(question+prompt)
                print bcolors.ENDC,
		speriod = raw_input().lower()
		if speriod == '':
			return int(default,0)
		elif int(speriod,0)<0x100:
			return int(speriod,0) 	
		else:
			print bcolors.RED+'Please put a downscaling less than 0xFF'+bcolors.ENDC

def q_trigger_msg(question, default="0x01"):
        if default is None:
		prompt="[no default]"
	else:
		prompt="["+default+"]"
	while True:
                print bcolors.BOLD,
                print(question+prompt)
                print bcolors.ENDC,
		speriod = raw_input().lower()
		if speriod == '':
			return int(default,0)
		if int(speriod,0)<0x30:
			return int(speriod,0) 	
		else:
			print bcolors.RED+'Please put a time less than 0x2F'+bcolors.ENDC

def q_latency_q(question, default="no"):
	valid = {"no":0, "yes":1}
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
			print bcolors.RED+'Please respond with yes or no'+bcolors.ENDC


def q_trigger_lat(question, default="0x0"):
        if default is None:
		prompt="[no default]"
	else:
		prompt="["+default+"]"
	while True:
                print bcolors.BOLD,
                print(question+prompt)
                print bcolors.ENDC,
		speriod = raw_input().lower()
		if speriod == '':
			return int(default,0)
		if int(speriod,0)<0x10000:
			return int(speriod,0) 	
		else:
			print bcolors.RED+'Please put a latency less than 0xFFFF'+bcolors.ENDC


def q_trigger_ch(question, default="0xFFFFFFFF"):
        if default is None:
		prompt="[no default]"
	else:
		prompt="["+default+"]"
	while True:
                print bcolors.BOLD,
                print(question+prompt)
                print bcolors.ENDC,
		speriod = raw_input().lower()
		if speriod == '':
			return int(default,0)
		elif int(speriod,0)<=0xFFFFFFFF:
			return int(speriod,0) 	
		else:
			print bcolors.RED+'Please put word less than 0xFFFFFFFF'+bcolors.ENDC


def q_slpatti_q(question, default="no"):
	valid = {"no":0, "yes":1}
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
			print bcolors.RED+'Please respond with yes or no'+bcolors.ENDC


def q_slpatti_pp(question, default="0"):
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
			print bcolors.RED+'Please respond with a valid PP number'+bcolors.ENDC



def q_shoot_msg(question, default="0x2F"):
        if default is None:
		prompt="[no default]"
	else:
		prompt="["+default+"]"
	while True:
                print bcolors.BOLD,
                print(question+prompt)
                print bcolors.ENDC,
		speriod = input()
		if speriod == '':
			return int(default,0)
		elif int(speriod,0)<0x30:
			return int(speriod,0) 	
		else:
			print bcolors.RED+'Please put a valid shooting message (6 bits)'+bcolors.ENDC


def q_yesno(question, default="no"):
	valid = {"no":0, "yes":1}
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
			print bcolors.RED+'Please respond with yes or no'+bcolors.ENDC


def q_mem_file0(question, default="patti_memf_tdc0.spy"):
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

def q_mem_file1(question, default="patti_memf_tdc1.spy"):
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

def q_mem_file2(question, default="patti_memf_tdc2.spy"):
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


def q_mem_file3(question, default="patti_memf_tdc3.spy"):
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

def q_output_file(question, default="patti_script.spy"):
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

def wregister(addr,cont):
        line = 'lbwrite '+str(hex(addr))+' '+str(hex(cont))+'\n'
        return line

def wfilename(name):
        line = '@'+name+'\n'
        return line

def wfilename_com(name):
        line = '#@'+name+'\n'
        return line


def wfilenamesh(name):
        line = './'+name+'\n'
        return line

def wfilenamesh_com(name):
        line = '#./'+name+'\n'
        return line

def print_file(NameOfFile):
        f = open(NameOfFile,'w')
        f.write ('#-----------------------------------\n')
        f.write ('# THIS FILE IS GENERATED WITH THE PATTI WIZARD #\n')
        f.write ('# feel free to modify if you know what you are doing.\n')
        f.write ('# Have fun!\n')
        f.write ('#-----------------------------------\n')
        f.write ('\n')
        f.write ("#Preliminary reset\n")
        f.write (wregister(reset_addr,reset_register))
        f.write ("#------> PULSER CONFIGURATION SECTION <----------\n")
        f.write ("#Selection register (forward call)\n")
        f.write (wregister(selection_addr,selection_register))
        f.write ("#Configuration register\n")
        f.write (wregister(conf_addr,conf_register))
        f.write ("#Period register\n")
        f.write (wregister(period_addr,period_register))
        f.write ("#Mask register\n")
        f.write (wregister(mask_addr,mask_register))
        f.write ("#Pulse register\n")
        f.write (wregister(pulse_addr,pulse_register))
        f.write ("#TTC window register\n")
        f.write (wregister(window_addr,window_register))
        f.write ("#Selection register (backward call)\n")
        f.write (wregister(selection_addr_back,selection_register_back))
        if (smode_global==0):
                memyes=q_yesno("Do you want to activate the pattern memory load inside the script?")
                if(memyes==1):
                        f.write ("#------> LOAD PATTERN MEMORY <----------\n")
                        if(tdc_global&1!=0):
                                f.write(wfilename(mfile0))
                        if(tdc_global&2!=0):
                                f.write(wfilename(mfile1))
                        if(tdc_global&4!=0):
                                f.write(wfilename(mfile2))
                        if(tdc_global&8!=0):
                                f.write(wfilename(mfile3))
                elif(memyes==0):
                        f.write ("#------> LOAD PATTERN MEMORY <----------\n")
                        f.write ("#attention! The loading could be commented\n")
                        if(tdc_global&1!=0):
                                f.write(wfilename_com(mfile0))
                        if(tdc_global&2!=0):
                                f.write(wfilename_com(mfile1))
                        if(tdc_global&4!=0):
                                f.write(wfilename_com(mfile2))
                        if(tdc_global&8!=0):
                                f.write(wfilename_com(mfile3))
        if(icont!=0):
#                        with open(tmpfile,'r') as openfileobject:
                print "icont "+str(icont)
                for i in range(icont):
                        tmpfile="_tmp"+str(i)
                        openfileobject=open(tmpfile,'r')
                        for line in openfileobject:
                                f.write(line)
                        os.remove(tmpfile)
                        openfileobject.close()
        if trgyes==1:
                f.write ("#------> TRIGGER CONFIGURATION SECTION <----------\n")
                f.write ("#Trigger conf register\n")
                f.write (wregister(trigger_addr,trigger_register))
                f.write ("#Trigger period conf register\n")
                f.write (wregister(triggerp_addr,triggerp_register))
                f.write ("#Latency conf register\n")
                f.write (wregister(latency_addr,latency_register))
                f.write ("#CHtrigger Selection register (forward call)\n")
                f.write (wregister(selection_addr,0x1))
                f.write ("#chtrigger register for TDC0\n")
                f.write (wregister(chtrg_addr,chtrg_register_0))
                f.write ("#CHtrigger Selection register (backward call)\n")
                f.write (wregister(selection_addr,0x1))
                f.write ("#CHtrigger Selection register (forward call)\n")
                f.write (wregister(selection_addr,0x2))
                f.write ("#chtrigger register for TDC1\n")
                f.write (wregister(chtrg_addr,chtrg_register_1))
                f.write ("#CHtrigger Selection register (backward call)\n")
                f.write (wregister(selection_addr,0x2))
                f.write ("#CHtrigger Selection register (forward call)\n")
                f.write (wregister(selection_addr,0x4))
                f.write ("#chtrigger register for TDC2\n")
                f.write (wregister(chtrg_addr,chtrg_register_2))
                f.write ("#CHtrigger Selection register (backward call)\n")
                f.write (wregister(selection_addr,0x4))
                f.write ("#CHtrigger Selection register (forward call)\n")
                f.write (wregister(selection_addr,0x8))
                f.write ("#chtrigger register for TDC3\n")
                f.write (wregister(chtrg_addr,chtrg_register_3))
                f.write ("#CHtrigger Selection register (backward call)\n")
                f.write (wregister(selection_addr,0x8))
                if(trgmode_global==2):
                        trgfiley=q_yesno("Do you want to activate the trigger memory load inside the script?")
                        trgfileyg=trgfiley
                        if(trgfiley==1):
                                f.write ("#------> LOAD TRIGGER MEMORY <----------\n")
                                f.write(wfilename(trg_file))
                        elif(trgfiley==0):
                                f.write ("#------> LOAD TRIGGER MEMORY <----------\n")
                                f.write ("#attention! The loading could be commented\n")
                                f.write(wfilename_com(trg_file))

        else:
                f.write ("#------> NO TRIGGER CONFIGURATION SECTION PRESENT<----------\n")
                f.write ("\n")  
        if patchyes==0:
                f.write ("#------> TEMPORARY PATCH (in case of no latency set) <------\n")
                f.write (wregister(patch_addr, patch_register))
        f.write ("#------> START <----------\n")
        f.write ("wait 1000\n")
        f.write (wregister(start_addr,start_register))
        f.close()


def print_file_sh(NameOfFile):
        f = open(NameOfFile,'w')
        f.write (wregister(reset_addr,reset_register))
        f.write (wregister(selection_addr,selection_register))
        f.write (wregister(conf_addr,conf_register))
        f.write (wregister(period_addr,period_register))
        f.write (wregister(mask_addr,mask_register))
        f.write (wregister(pulse_addr,pulse_register))
        f.write (wregister(window_addr,window_register))
        f.write (wregister(selection_addr_back,selection_register_back))
        if (smode_global==0):
                if(memyesg2==1):
                        if(tdc_global&1!=0):
                                f.write(wfilenamesh(mfile0))
                        if(tdc_global&2!=0):
                                f.write(wfilenamesh(mfile1))
                        if(tdc_global&4!=0):
                                f.write(wfilenamesh(mfile2))
                        if(tdc_global&8!=0):
                                f.write(wfilenamesh(mfile3))
                elif(memyesg2==0):
                        if(tdc_global&1!=0):
                                f.write(wfilenamesh_com(mfile0))
                        if(tdc_global&2!=0):
                                f.write(wfilenamesh_com(mfile1))
                        if(tdc_global&4!=0):
                                f.write(wfilenamesh_com(mfile2))
                        if(tdc_global&8!=0):
                                f.write(wfilenamesh_com(mfile3))
        if(icont!=0):
                for i in range(icont):
                        tmpfilesh="_tmpsh"+str(i)
                        openfileobject=open(tmpfilesh,'r')
#                        with open(tmpfilesh,'r') as openfileobject:
                        for line in openfileobject:
                                f.write(line)
                        os.remove(tmpfilesh)
                        openfileobject.close()
        if trgyes==1:
                f.write (wregister(trigger_addr,trigger_register))
                f.write (wregister(triggerp_addr,triggerp_register))
                f.write (wregister(latency_addr,latency_register))
                f.write (wregister(selection_addr,0x1))
                f.write (wregister(chtrg_addr,chtrg_register_0))
                f.write (wregister(selection_addr,0x1))
                f.write (wregister(selection_addr,0x2))
                f.write (wregister(chtrg_addr,chtrg_register_1))
                f.write (wregister(selection_addr,0x2))
                f.write (wregister(selection_addr,0x4))
                f.write (wregister(chtrg_addr,chtrg_register_2))
                f.write (wregister(selection_addr,0x4))
                f.write (wregister(selection_addr,0x8))
                f.write (wregister(chtrg_addr,chtrg_register_3))
                f.write (wregister(selection_addr,0x8))
                if(trgmode_global==2):
                        if(trgfileyg==1):
                                f.write(wfilenamesh(trg_file))
                        elif(trgfileyg==0):
                                f.write(wfilenamesh_com(trg_file))
        if patchyes==0:
                f.write (wregister(patch_addr, patch_register))
        f.write (wregister(start_addr,start_register))
        f.close()

def print_file_tmp(NameOfFile):
        g = open(NameOfFile,'w')
        g.write ("#------> PULSER CONFIGURATION SECTION (additional)<----------\n")
        g.write ("#Selection register (forward call)\n")
        g.write (wregister(selection_addr,selection_register))
        g.write ("#Configuration register\n")
        g.write (wregister(conf_addr,conf_register))
        g.write ("#Period register\n")
        g.write (wregister(period_addr,period_register))
        g.write ("#Mask register\n")
        g.write (wregister(mask_addr,mask_register))
        g.write ("#Pulse register\n")
        g.write (wregister(pulse_addr,pulse_register))
        g.write ("#TTC window register\n")
        g.write (wregister(window_addr,window_register))
        g.write ("#Selection register (backward call)\n")
        g.write (wregister(selection_addr_back,selection_register_back))
        if (smode_global==0):
                memyes=q_yesno("Do you want to activate the pattern memory load inside the script (for the TDCs already configured)?")
                memyesg=memyes
                if(memyes==1):
                        g.write ("#------> LOAD PATTERN MEMORY (additional)<----------\n")
                        if(tdc_global&1!=0):
                                g.write(wfilename(mfile0))
                        if(tdc_global&2!=0):
                                g.write(wfilename(mfile1))
                        if(tdc_global&4!=0):
                                g.write(wfilename(mfile2))
                        if(tdc_global&8!=0):
                                g.write(wfilename(mfile3))
                elif(memyes==0):
                        g.write ("#------> LOAD PATTERN MEMORY (additional) <----------\n")
                        g.write ("#attention! The loading could be commented\n")
                        if(tdc_global&1!=0):
                                g.write(wfilename_com(mfile0))
                        if(tdc_global&2!=0):
                                g.write(wfilename_com(mfile1))
                        if(tdc_global&4!=0):
                                g.write(wfilename_com(mfile2))
                        if(tdc_global&8!=0):
                                g.write(wfilename_com(mfile3))
        g.close()


def print_file_tmp_sh(NameOfFile):
        g = open(NameOfFile,'w')
        g.write (wregister(selection_addr,selection_register))
        g.write (wregister(conf_addr,conf_register))
        g.write (wregister(period_addr,period_register))
        g.write (wregister(mask_addr,mask_register))
        g.write (wregister(pulse_addr,pulse_register))
        g.write (wregister(window_addr,window_register))
        g.write (wregister(selection_addr_back,selection_register_back))
        if (smode_global==0):
                if(memyesg==1):
                        if(tdc_global&1!=0):
                                g.write(wfilenamesh(mfile0))
                        if(tdc_global&2!=0):
                                g.write(wfilenamesh(mfile1))
                        if(tdc_global&4!=0):
                                g.write(wfilenamesh(mfile2))
                        if(tdc_global&8!=0):
                                g.write(wfilenamesh(mfile3))
                elif(memyesg==0):
                        if(tdc_global&1!=0):
                                g.write(wfilenamesh_com(mfile0))
                        if(tdc_global&2!=0):
                                g.write(wfilenamesh_com(mfile1))
                        if(tdc_global&4!=0):
                                g.write(wfilenamesh_com(mfile2))
                        if(tdc_global&8!=0):
                                g.write(wfilenamesh_com(mfile3))
        g.close()


def update_tdc(tdc):
        if (tdc&1!=0):
                configured_tdc[0]=1
        if (tdc&2!=0):
                configured_tdc[1]=1
        if (tdc&4!=0):
                configured_tdc[2]=1
        if (tdc&8!=0):
                configured_tdc[3]=1

def summary_pulser(tdc):
        line="# You configured the TDC(s) "+str(tdc)+" in the following way"
        summary_txt.append(line)
        line=""

#--------- START QUESTIONS------
#da fare:
#   - grafica (cancella schermo, etc.)
#   - in tutte le funzioni fare in modo che si possoa anche selezionare l'inizilae delle opzioni
# in maiuscolo o minuscolo e che nel testo dell adomanda compino le opzioni
#   - risolvere problema dello spazio
#   - summary nei commenti dello script (sarebbe figo se ci fosse un riassunto in poche parole di quello
#      che fa lo script) fare in ogni funzione di scelta una variabile text_qualcosa globale
# in modo che una funzione summary costruisca il testo

#PP choice
pp_ans = q_pp("Which PP do you want to configure?")
pp_op = {0: 4,
         1: 5,
         2: 6,
         3: 7}
pp=pp_op[pp_ans]


pulser_extdc=0
tdc_rem=0xF
cont_tdc=True
while(cont_tdc):
        #TDC choice
        tdc_ans = q_tdc("Which TDC(s) do you want to configure?",str(tdc_rem))
        tdc_rem=0
        tdc=tdc_ans
        update_tdc(tdc)

        # Configuration register
        conf_register = 0x00000000

        pulsermode_ans = q_pulser_cfg("Select pulser mode")
        pulsermode_opt = {0: 0x0,
                          1: 0x1,
                          2: 0x2,
                          3: 0x3,
                          4: 0x4,
                          5: 0x5,
                          6: 0x6,
                          7: 0x7}
        cfg_pulsermode=pulsermode_opt[pulsermode_ans]

        if cfg_pulsermode==4 or cfg_pulsermode==5 or cfg_pulsermode==6:
		pulser_extdc=tdc


        per_period=0;
        if cfg_pulsermode == 1 or cfg_pulsermode == 2 or cfg_pulsermode == 5 or cfg_pulsermode == 6:
                per_period = q_period_per("Which is the period you want?")

        extpulse=q_extpulse_cfg("Do you want to use the lvds connector for external or choke?")


        width_ans = q_width_cfg("Select source of pulser width")
        width_opt = {0: 0,
                     1: 1}
        cfg_width=width_opt[width_ans] 

        special_ans = q_special_cfg("Do you want to use the pulser in special mode?")

        cfg_smode=0
        smode_ans=0
        mfile=""
        if special_ans == 1:
                smode_ans = q_specialt_cfg("Select which special mode you want (normal, direct, random0, random1)")
        else:
                smode_ans = 0
        smode_opt = {0: 0x0,
                     1: 0x1,
                     2: 0x2,
                     3: 0x3}
        cfg_smode=smode_opt[smode_ans]
        smode_global=smode_ans

        if smode_ans==0:
                tdc_global=tdc
                if tdc&1!=0:
                        mfile0=q_mem_file0("Which is the name of the file for memory load for TDC 0?")
                if tdc&2!=0:
                        mfile1=q_mem_file1("Which is the name of the file for memory load for TDC 1?")
                if tdc&4!=0:
                        mfile2=q_mem_file2("Which is the name of the file for memory load for TDC 2?")
                if tdc&8!=0:
                        mfile3=q_mem_file3("Which is the name of the file for memory load for TDC 3?")




        cfg_rndper=0
        if cfg_smode==0x2 or cfg_smode==0x3:
                rndper_ans=q_rndperiod_cfg("Which is the base clock for random generation? (160 or custom)")
                rndper_opt = {0: 0x0,
                              1: 0x1}
                cfg_rndper=rndper_opt[rndper_ans]


        cont_ans = q_cont_cfg("Do you want continous or n pulses?")
        cfg_cont = cont_ans
        npulse=0
        nmem=0
        if cont_ans==1:
                npulse=q_npulse_pul("How many pulses you want?")
                npulse=npulse-1
        if cont_ans==1 and smode_ans==0:
                nmem=q_nmem_pul("How many times you want to read the memory?")


        burstp_ans=q_burstpulser_cfg("Do you want to have the 160MHz burst pulses?")
        burstp_opt = {0: 0x0,
                      1: 0x1}
        cfg_burstpulser = burstp_opt[burstp_ans]

        ttctrigger_ans=q_ttctrigger_cfg("Do you want to use the TTC trigger?")
        ttctrigger_opt = {0: 0x0,
                          1: 0x1}
        cfg_ttctrigger = ttctrigger_opt[burstp_ans]

        ttcwindow=0
        shootmsg=0
        if ttctrigger_ans==1:
                ttcwindow=q_ttcwindow_cfg("TTC trigger window width?")
                shootmsg=q_shoot_msg("Which is the TTC trigger msg to pilot the pulser?")

        enadelay_ans=q_enadelay_cfg("Do you want to have a delay between first pulse and SOB?")
        enadelay_opt = {0: 0x0,
                        1: 0x1}
        cfg_enadelay=enadelay_opt[enadelay_ans]

        cfg_wdelay=0x1
        if cfg_enadelay==1:
                wdelay_ans=q_sdelay_cfg("delay value? ")
                cfg_wdelay=wdelay_ans

        mask=q_mask_msk("Which are the channels enabled for pulses?")

        #---- Counter doesn't work for python < 2.7
#        from collections import Counter
#        ctdc=Counter(configured_tdc)
#        tot_tdc=ctdc[1]
        tot_tdc=0
        for ii in configured_tdc:
                if ii==1:
                        tot_tdc=tot_tdc+1
        print ""
        print bcolors.OKBLUE+"You configured "+str(tot_tdc)+" TDC(s)"+bcolors.ENDC
        if(tot_tdc!=4):
                print bcolors.FAIL+"The following TDCs are not configured"
                for idx,val in enumerate(configured_tdc):
                        if (val==0):
                                print idx
                                tdc_rem=tdc_rem|2**idx
                print bcolors.ENDC
                rem=q_yesno("Do you want to configure the remaining TDC(s)?")
                if (rem==1):
                        cont_tdc=True
                        temp_file="_tmp"+str(icont)
                        temp_file_sh="_tmpsh"+str(icont)
                        icont=icont+1
                        trg_msg_corr_xxx=q_trgmsg_cfg("Which is the correlated trigger message (for the TDCs already configured)?")
                        selection_register = tdc
                        selection_addr = ((pp&0xF)<<24)+0x206C
                        selection_register_back = tdc+(pulser_extdc<<4)
                        selection_addr_back = ((pp&0xF)<<24)+0x206C
                        conf_register=(cfg_pulsermode & 0x7)+((cfg_cont&0x1)<<4)+((extpulse&0x1)<<5)+(0x0<<6)+((cfg_width&0x1)<<7)+\
                                      +((trg_msg_corr_xxx&0x3f)<<8)+((cfg_smode&0x3)<<16)+((cfg_rndper&0x1)<<18)+((cfg_burstpulser&0x1)<<20)+\
                                      +((cfg_ttctrigger&0x1)<<21)+((cfg_wdelay&0xF)<<24)+((cfg_enadelay&0x1)<<28)+(0x7<<29)             
                        conf_addr=((pp&0xF)<<24)+0x205C
                        period_register = per_period
                        period_addr = ((pp&0xF)<<24)+0x2060
                        mask_register = mask
                        mask_addr = ((pp&0xF)<<24)+0x2068
                        pulse_register = ((npulse&0xfffff)<<9) + ((nmem&0x1ff))
                        pulse_addr= ((pp&0xF)<<24)+0x2064
                        window_register = ttcwindow
                        window_addr = ((pp&0xF)<<24)+0x2090
                        print_file_tmp(temp_file)
                        print_file_tmp_sh(temp_file_sh)
                else:
                        cont_tdc=False
        else:
                cont_tdc=False


#trigger
triggeropt=q_trigger_opt("Do you want to configure the trigger section?")
trg_mode=0
trg_dw=0
trg_msg_corr=0 #conf register bits 13..8
trg_msg_uncorr= 0 #trigger register bits 25..20
trg_period=0
trg_tdc=0
ch_sel_0=0
ch_sel_1=0
ch_sel_2=0
ch_sel_3=0
trg_lat=0
trg_lat_opt=0
trgyes=triggeropt
if triggeropt==1:
        triggermode=q_trigger_mode("Do you want to have correlated or uncorrelated trigger?")
        if triggermode==1: 
                trg_mode=q_trigger_uncorr("Which uncorrelated trigger mode you want?")
                trg_msg_uncorr=q_trgmsg_cfg("Which is the trigger message?")
                trg_period=q_trigger_per("Which is the trigger period?")
        else: #corr
                trg_mode=q_trigger_corr("Which correlated trigger mode you want?")
                trg_tdc=q_tdc("Which TDC will be used as trigger pulses source?")
                tdc_cht=trg_tdc
                if trg_tdc&1!=0:
                        ch_sel_0 = q_trigger_ch("Which channels will be used as trigger generator for TDC 0?")
                if trg_tdc&2!=0:
                        ch_sel_1 = q_trigger_ch("Which channels will be used as trigger generator for TDC 1?")
                if trg_tdc&4!=0:
                        ch_sel_2 = q_trigger_ch("Which channels will be used as trigger generator for TDC 2?")
                if trg_tdc&8!=0:
                        ch_sel_3 = q_trigger_ch("Which channels will be used as trigger generator for TDC 3?")

                trgmode_global=trg_mode
                if trg_mode==1:
                        trg_dw=q_trigger_dw("Which is the downscaling factor?")
                elif trg_mode==2:        
                        trg_file=q_tmem_file("Which is the name of the tmem file to load?")
                trg_msg_corr=q_trgmsg_cfg("Which is the trigger message?")
        trg_lat_opt = q_latency_q("Do you want to set a trigger latency?")
        if trg_lat_opt==1:
            trg_lat=q_trigger_lat("Set the trigger latency with respect to the pulses")
            patchyes=1
#build configuration register word
conf_register=(cfg_pulsermode & 0x7)+((cfg_cont&0x1)<<4)+((extpulse&0x1)<<5)+(0x0<<6)+((cfg_width&0x1)<<7)+\
              +((trg_msg_corr&0x3f)<<8)+((cfg_smode&0x3)<<16)+((cfg_rndper&0x1)<<18)+((cfg_burstpulser&0x1)<<20)+\
              +((cfg_ttctrigger&0x1)<<21)+((cfg_wdelay&0xF)<<24)+((cfg_enadelay&0x1)<<28)+(0x7<<29)             
conf_addr=((pp&0xF)<<24)+0x205C

#build period register word
period_register = per_period
period_addr = ((pp&0xF)<<24)+0x2060

#build selection register word
selection_register = tdc
selection_addr = ((pp&0xF)<<24)+0x206C


#build selection register word
selection_register_back = tdc+(pulser_extdc<<4)
selection_addr_back = ((pp&0xF)<<24)+0x206C

#build windw register
window_register = ttcwindow
window_addr = ((pp&0xF)<<24)+0x2090

#build mask register
mask_register = mask
mask_addr = ((pp&0xF)<<24)+0x2068

#build pulse register 
pulse_register = ((npulse&0xfffff)<<9) + ((nmem&0x1ff))
pulse_addr= ((pp&0xF)<<24)+0x2064

#build trigger register
trigger_register = ((trg_msg_uncorr&0x3F)<<20)+(1<<18)+((trg_dw&0xFF)<<8)+((trg_mode&0xF)<<4)+(trg_tdc&0xF)
trigger_addr = ((pp&0xF)<<24)+0x207C

#build trigger period register
triggerp_register = trg_period
triggerp_addr = ((pp&0xf)<<24)+0x2080

#build latency register
latency_register = ((trg_lat_opt&0x1)<<31)+(trg_lat&0xFFFF)
latency_addr = ((pp&0xf)<<24)+0x2084

#build ch trigger registers
chtrg_register_0 = ch_sel_0
chtrg_register_1 = ch_sel_1
chtrg_register_2 = ch_sel_2
chtrg_register_3 = ch_sel_3
chtrg_addr=((pp&0xF)<<24)+0x208C

#print "SELECTION REGISTER: ", hex(selection_register), hex(selection_addr)
#print "CONFIGURATION REGISTER: ", hex(conf_register), hex(conf_addr)
#print "PERIOD REGISTER: ", hex(period_register),hex(period_addr)
#print "PULSE REGISTER: ",hex (pulse_register), hex(pulse_addr)


#summary
#print "mode ",cfg_pulsermode
#print "period ", per_period
#print "width ", cfg_width
#print "special mode ",cfg_smode
#print "rndper ", cfg_rndper
#print "burstpulser ", cfg_burstpulser
#print "ttc trigger", cfg_ttctrigger
#print "ena delay ",cfg_enadelay
#print "delay ", cfg_wdelay



#-------------
start_register=0x00000011
start_addr=((pp&0xF)<<24)+0x2088
patch_register=0x00000f92
patch_addr=((pp&0xF)<<24)+0x2084
reset_register=0x9000000F
reset_addr=((pp&0xF)<<24)+0x2070
NameOfFile=q_output_file("Name of the tdspy script file to generate?")
NameOfFileSh,fileext=os.path.splitext(NameOfFile)
NameOfFileSh=NameOfFileSh+".sh"
print NameOfFile
print NameOfFileSh
print_file(NameOfFile)
print_file_sh(NameOfFileSh)

print bcolors.OKGREEN+"SCRIPT FILE DUMPED!!!"+bcolors.ENDC

