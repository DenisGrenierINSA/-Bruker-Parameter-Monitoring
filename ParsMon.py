#!/usr/bin/env python
import argparse
import subprocess, multiprocessing, sys, os,tty,select,re,time

def get_psid():
  ShellCommand = pvcmdPath+"pvcmd -a ParxServer -r ListPs"
  Resultat = subprocess.check_output(ShellCommand, shell=True)
  regexp='PSID: +(\d+)'
  regtask = re.compile(regexp,re.MULTILINE)
  return  regtask.findall(Resultat)[0]

def getPVpar(i_psid, s_Name, parDict):
    ShellCommand = pvcmdPath+"pvcmd -a ParxServer -r ParamGetValue -psid "+str(i_psid)+" -param "+s_Name
    try:
        Resultat = subprocess.check_output(ShellCommand, shell=True)
        if (Resultat == parDict[s_Name][0]):
	  parDict[s_Name]=[Resultat,'']
	else:
	  parDict[s_Name]=[Resultat,'   < ----- changed']
    except subprocess.CalledProcessError as Err:
	print('##########################################################')
        print("error, the parameter "+s_Name+" does not exist in PV space")
	print('##########################################################')
        sys.exit(0)
        
def printPVpar(parDict):
    os.system('clear')
    print("Copyright Denis Grenier Creatis Lab. UMR CNRS 5220\npress ctrl+c to quit")
    for key in parDict:
        print(key + " = " + parDict[key][0] + parDict[key][1])

pvcmdPath = os.environ['XWINNMRHOME']+'/prog/bin/'
parser = argparse.ArgumentParser(description='Show values of a set of Paravision parameters (ctrl+c to quit)\nCopyright Denis Grenier Creatis Lab. UMR CNRS 5220')
parser.add_argument('--parameters', nargs="+", type=str,
		    help='give a space separated list of parameters to monitor')
parser.add_argument('--refresh',type=float,
                    help='refresh period (s) (default to 3s)')
parser.add_argument('--pvbinpath',type=str,
                    help='pvcmd path (default to '+pvcmdPath)

args = parser.parse_args()

par_Dict = dict()

if args.parameters == None:
  sys.exit(0)

for param in args.parameters:
  par_Dict[param]=['','']

if args.pvbinpath != None:
  pvcmdPath = args.pvbinpath
  
psid = get_psid()

try :
  while(True):
    for param in par_Dict:
      getPVpar(psid, param, par_Dict)
    printPVpar(par_Dict)
    if args.refresh==None :
      time.sleep(3.0)
    else:
      time.sleep(args.refresh)
except KeyboardInterrupt:
    sys.exit(0)
