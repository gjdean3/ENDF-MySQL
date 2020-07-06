# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 16:45:42 2020

@author: Design
"""
import supFns as sf

class d451:
    def __init__(self,za,awr,lrp,lfi,nlib,nmod):
        self.za   = sf.s2i(za)
        self.awr  = sf.s2f(awr)
        self.lrp  = int(lrp)
        self.lfi  = int(lfi)
        self.nlib = int(nlib)
        self.nmod = int(nmod)
        self.idVal = -1
        
    def readLine2(self,elis,sta,lis,liso,_,nfor):
        self.elis = sf.s2i(elis)
        self.sta  = sf.s2i(sta)
        self.lis  = int(lis)
        self.liso = int(liso)
        self.nfor = int(nfor)
        
    def readLine3(self,awi,emax,lrel,_,nsub,nver):
        self.awi  = sf.s2i(awi)
        self.emax = sf.s2i(emax)
        self.lrel = int(lrel)
        self.nsub = int(nsub)
        self.nver = int(nver)
        
    def readLine4(self,temp,_,ldrv,__,nwd,nxc):
        self.temp = sf.s2i(temp)
        self.ldrv = int(ldrv)
        self.nwd  = int(nwd)
        self.nxc  = int(nxc)
        
    def readLine5(self,zsaym,alab,edate):
        self.zsaym = zsaym
        self.alab  = alab
        self.edate = edate
        
    def readLine6(self,ref,ddate,endate):
        self.ref    = ref
        self.ddate  = ddate
        self.endate = endate
        
    def readNote(self,hsub):
        self.hsub  = hsub
        self.abund = -1
        
    def returnData(self):
        return (self.za,self.awr,self.lrp,self.lfi,self.nlib,self.nmod,
                self.elis,self.sta,self.lis,self.liso,self.nfor,self.awi,
                self.emax,self.lrel,self.nsub,self.nver,self.temp,self.ldrv,
                self.nwd,self.nxc,self.zsaym,self.alab,self.edate,self.ref,
                self.ddate,self.endate,self.hsub,self.abund)
    





























