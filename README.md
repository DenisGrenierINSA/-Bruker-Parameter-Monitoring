This python script regularly print a list of Bruker paravision parameters and their value to help find bugs during Bruker method developpment.
It is a companion tool to gdb/eclipse because Bruker parameters values are not seen by gdb and can not be checked without using the shell command "pvcmd".

This script <b>MUST</b> be launched from a paravision terminal (i.e. Paravision Main window -> Programs -> Terminal)

Example: check every 2 seconds the value of PVM_EchoTime PVM_RepetitionTime and ExcPulse1.Flipangle

./ParsMon.py --refresh 2 --parameters PVM_EchoTime PVM_RepetitionTime ExcPulse1.Flipangle


