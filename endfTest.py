import os

from db_utils import create_connection,create_database
import supFns as sf
import data451
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 17:32:00 2020

@author: Design
"""
filePath = "C:\\Users\\Design\\Documents\\Python Scripts\\ENDF-B-VIII.0_decay"
#fileName = "dec-027_Co_060.endf"

if os.path.isfile('log.temp'):
    os.remove('log.temp')
if os.path.isfile("database451.sql"):
    os.remove("database451.sql")

logFile = open('log.temp','w')
con = create_connection("localhost","root","Password")
cur = con.cursor()
create_database(cur,"database451")
cur.execute("USE database451")
table451 = """
CREATE TABLE table451 (
id integer NOT NULL AUTO_INCREMENT PRIMARY KEY,
ZA integer NOT NULL, AWR real NOT NULL, LRP integer NOT NULL,
LFI integer NOT NULL, NLIB integer NOT NULL, NMOD integer NOT NULL,
ELIS integer NOT NULL, STA integer NOT NULL, LIS integer NOT NULL,
LISO integer NOT NULL, NFOR integer NOT NULL,
AWI integer NOT NULL, EMAX integer NOT NULL, LREL integer NOT NULL,
NSUB integer NOT NULL, NVER integer NOT NULL,
TEMP integer NOT NULL, LDRV integer NOT NULL, NWD integer NOT NULL,
NXC integer NOT NULL,
ZSAYM text NOT NULL, ALAB text NOT NULL, EDATE text NOT NULL,
REF text NOT NULL, DDATE text NOT NULL, ENDATE text NOT NULL,
HSUB text NOT NULL, ABUND real NOT NULL) """
cur.execute(table451)
entry451 = """
INSERT INTO table451 (ZA,AWR,LRP,LFI,NLIB,NMOD,ELIS,STA,LIS,LISO,NFOR,AWI,
EMAX,LREL,NSUB,NVER,TEMP,LDRV,NWD,NXC,ZSAYM,ALAB,EDATE,REF,DDATE,ENDATE,HSUB,ABUND) 
VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
"""
    
files = os.listdir(filePath)
for fileName in sorted(files):
    if ".endf" not in fileName: continue

    dFile = open(os.path.join(filePath,fileName),'r')
                 
    nLine = dFile.readline()
    header = nLine[:50]
    idVal = int(nLine[66:70])
    nLine = dFile.readline()
    lineData = nLine[:66].split()
    nData = data451.d451(*lineData)
    nData.idVal = idVal
        
    nLine = dFile.readline()
    lineData = nLine[:66].split()
    nData.readLine2(*lineData)
    
    nLine = dFile.readline()
    lineData = nLine[:66].split()
    nData.readLine3(*lineData)
        
    nLine = dFile.readline()
    lineData = nLine[:66].split()
    nData.readLine4(*lineData)
    
    nLine = dFile.readline()
    nData.readLine5(nLine[:10],nLine[10:22].strip(),nLine[22:].strip())
    nLine = dFile.readline()
    nData.readLine6(nLine[:22],nLine[22:55].strip(),nLine[55:].strip())
    nLine = dFile.readline()
    nData.readNote(nLine)
    for _ in range(nData.nwd-5):
        nLine = dFile.readline()
        nData.hsub += nLine
    nLine = dFile.readline()
    nData.hsub += nLine
    if nData.sta == 0 and 'Abundance' not in nLine:
        logFile.write("Error in "+fileName+". No abundance listed.\n")
        continue
    if nData.sta == 0:
        nData.abund = float(nLine[10:16].replace('%',''))
    nLine = dFile.readline()
    nData.hsub += nLine
    
    cur.execute(entry451, nData.returnData())
    con.commit()
    
    
    #################################################################
    """
    Section looks for values that are discrepant from the norm.  
    Things like metastable isotopes, fission, etc.
    """
    #################################################################
    if nData.sta == 0:continue
    if nData.lrp != -1: # line 2, -1-->no file 2 for resonances
        logFile.write("Error in "+fileName+" at line 2. LRP.\n")
        continue
    if nData.lfi != 0: # line 2, 0-->no fission
        logFile.write("Error in "+fileName+" at line 2. LFI.\n")
        continue
    if nData.nlib != 0: # line 2, 0-->ENDF
        logFile.write("Error in "+fileName+" at line 2. NLIB.\n")
        continue
    if nData.nmod != 0:
        logFile.write("Error in "+fileName+". New formatting.\n")
        continue
    if nData.elis != 0 or nData.lis != 0:
        logFile.write("Error in "+fileName+" at line 3. LIS.\n")
        continue
    if nData.nfor != 6:
        logFile.write("Error in "+fileName+" at line 3. NFOR.\n")
        continue
    if nData.awi != 0:
        logFile.write("Error in "+fileName+" at line 4. AWI.\n")
        continue
    if nData.emax != 0.0:
        logFile.write("Error in "+fileName+" at line 4. EMAX.\n")
        continue
    if nData.lrel != 0:
        logFile.write("Error in "+fileName+" at line 4. LREL.\n")
        continue
    if nData.nsub != 4:
        logFile.write("Error in "+fileName+" at line 4. NSUB.\n")
        continue
    if nData.nver != 8:
        logFile.write("Error in "+fileName+" at line 4. NVER.\n")
        continue
    if nData.temp != 0:
        logFile.write("Error in "+fileName+" at line 5. TEMP.\n")
        continue
    if nData.ldrv != 0:
        logFile.write("Error in "+fileName+" at line 5. LDRV.\n")
        continue
    if nData.nxc != 2:
        logFile.write("Error in "+fileName+" at line 5. NXC.\n")
        continue
    
    nLine = dFile.readline()
    lineData = nLine.split()
    if int(lineData[0]) != 1 or int(lineData[1]) != 451:
        logFile.write("Error in "+fileName+" at line 1 after description.\n")
        continue
    
    nLine = dFile.readline()
    lineData = nLine.split()
    if int(lineData[0]) != 8 or int(lineData[1]) != 457:
        logFile.write("Error in "+fileName+" at line 2 after description.\n")
        continue
    #################################################################
    
    nLine = dFile.readline()
    nLine = dFile.readline()
    nLine = dFile.readline()
    lineData = nLine.split()
    if int(lineData[4]) != 0:
        logFile.write("Error in "+fileName+" at line 5 after description.\n")
        continue
    
    nLine = dFile.readline()
    lineData = nLine.split()
    t12 = sf.s2f(lineData[0])
    t12u = sf.s2f(lineData[1])
    if int(lineData[4]) != 6:
        logFile.write("Error in "+fileName+" at line 6 after description.\n")
        continue
    
    nLine = dFile.readline()
    nLine = dFile.readline()
    lineData = nLine.split()  
    if int(lineData[5]) != 1:
        logFile.write("Error in "+fileName+".  Multiple decay modes.\n")
        continue
        
    nLine = dFile.readline()
    lineData = nLine.split()
    decayType = sf.s2f(lineData[0])
    if decayType == 1:
        if sf.s2f(lineData[1]) != 0:
            logFile.write("Error in "+fileName+" at line 9 after description.  Daughter not ground.\n")
            continue
        if sf.s2f(lineData[4]) != 1:
            logFile.write("Error in "+fileName+" at line 9 after description.\n")
            continue
    else:
        logFile.write("Error in "+fileName+" at line 9 after description. Decay type not beta-.\n")
        continue
        
    nLine = dFile.readline()
    lineData = nLine.split()
    if len(lineData) < 5:
        logFile.write("Error in "+fileName+". No emissions.\n")
        continue
    nEmis = int(lineData[5])
    radType = int(sf.s2f(lineData[1]))
    if radType == 0:
        if int(lineData[2]) != 0:
            logFile.write("Error in "+fileName+" at line 10 after description. Continuous spectra.\n")
            continue
        if int(lineData[3]) != 0:
            logFile.write("Error in "+fileName+" at line 10 after description. Covariance data.\n")
            continue
        
        nLine = dFile.readline()
        lineData = nLine.split()
        if sf.s2f(lineData[0]) != 1.0:
            logFile.write("Error in "+fileName+" at line 11 after description.\n")
            continue
        
        holdDict = dict()
        for _ in range(nEmis):
            nLine = dFile.readline()
            lineData = nLine.split()
            energy = sf.s2f(lineData[0])
            eUncert = sf.s2f(lineData[1])
            nData = int(lineData[4])
            nLine = dFile.readline()
            lineData = nLine.split()
            if sf.s2f(lineData[1]) != 0 or sf.s2f(lineData[4]) != 0.0:
                logFile.write("Error in "+fileName+" at energy "+str(energy)+".\n")
                break
            holdDict[energy] = [eUncert,sf.s2f(lineData[2]),sf.s2f(lineData[3])]
            if nData != 6:
                nLine = dFile.readline()
        
        dFile.close()
        
    else:
        logFile.write("Error in "+fileName+".  No gamma emissions. Other types possible.\n")
        continue
    
logFile.close()
cur.close()
con.close()























