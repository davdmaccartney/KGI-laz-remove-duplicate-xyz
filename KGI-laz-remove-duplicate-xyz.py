import os
import numpy as np
from laspy.file import File
import easygui
from imutils import paths
import fnmatch
import sys
from timeit import default_timer as timer



def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def update_progress(progress):
    barLength = 30 # Modify this to change the length of the progress bar
    
    block = int(round(barLength*progress))
    text = "\rPercent: [{0}] {1}% ".format( "#"*block + "-"*(barLength-block), int(progress*100))
    sys.stdout.write(text)
    sys.stdout.flush()



dirname1 = easygui.diropenbox(msg=None, title="Please select the target directory", default=None )
total_con=len(fnmatch.filter(os.listdir(dirname1), '*.laz'))
D1 = str(total_con)
msg = str(total_con) +" files do you want to continue?"
title = "Please Confirm"
if easygui.ynbox(msg, title, ('Yes', 'No')): # show a Continue/Cancel dialog
    pass # user chose Continue else: # user chose Cancel
else:
    exit(0)


   
file_Dir1 = os.path.basename(dirname1)
dirout = os.path.join(dirname1,"no_duplicates")
if not os.path.exists(dirout):
    os.mkdir(dirout)
ci=0
cls()
eR=0
file = open(dirout+'\\'+"Stat.txt","w")


for filename in os.listdir(dirname1):
     if filename.endswith(".laz"):
        ci  += 1
        
        inFile = File(dirname1+'\\'+filename, mode='r')
 
        num_avant = len(inFile.points)
        coords = np.vstack((inFile.x, inFile.y, inFile.z)).transpose()
        unique, index = np.unique(coords, axis=0, return_index=True)
        points_kept = inFile.points[index]
        num_apres = len(points_kept)


      
        
        if (num_avant != num_apres):
            num_dupli = num_avant - num_apres
            nom= os.path.splitext(filename)[0]
         
            outFile1 = File(dirout+'\\'+nom+'.laz', mode = "w", header = inFile.header)
            outFile1.points = points_kept
            outFile1.close()

        
            file.write(filename+' '+str(num_dupli)+' duplicated (xyz) : sur '+str(num_avant)+' points\n')

        inFile.close()

        update_progress(ci/int(D1))

 
if eR>0:
   print('Process finnihed :'+str(eR)+' errors read Comp-result.txt in the source folder')
else:
   print('Process finnihed with no errors')
   

exit(0)