""" 
The module MISC_ROUTINES gathers  classes and  functions which  are useful for daily processing. As an
example we have conversion factor or universal constants.

MODULES CALLED:
NUMPY, SYS

MODIFICATION HISTORY:
Created by Ing. Freddy Galindo (frederickgalindo@gmail.com). ROJ, 21 October 2009.
"""

import numpy
import sys

class CoFactors(object):
    """
    CoFactor class used to call pre-defined conversion factor (e.g. degree to radian).  The cu-
    The current available factor are:
       
    d2r = degree to radian.
    s2r = seconds to radian?, degree to arcsecond.?
    h2r = hour to radian. 
    h2d = hour to degree
    """
    
    d2r = numpy.pi/180.
    s2r = numpy.pi/(180.*3600.)
    h2r = numpy.pi/12.
    h2d = 15.
    
class Redirect(object):
    def __init__(self,stdout=None):
        self.stdout = stdout
    
    def write(self,message):
        self.stdout.insertPlainText(message)

class WidgetPrint(object):
    """
    WidgetPrint class allows to define the standard output.  
    """
    def __init__(self,textid=None):
        self.__stdout = sys.stdout
        self.textid = textid
        self.wPrint()
        
    def wPrint(self):
        if self.textid == None: sys.stdout = self.__stdout
        if self.textid != None: sys.stdout = Redirect(self.textid)
        print ("")
    
class Vector(object):
    """
    direction = 0 Polar to rectangular; direction=1 rectangular to polar
    """
    def __init__(self,vect=numpy.array([]),direction=0):
        nsize = numpy.size(vect)
        if nsize <= 3:
            vect = vect.reshape(1,nsize)
        
        self.vect = vect
        self.dirc = direction
        
        
    
    def Polar2Rect(self):
        if self.dirc == 0:
            jvect = self.vect*numpy.pi/180.
            mmx = numpy.cos(jvect[:,1])*numpy.sin(jvect[:,0])
            mmy = numpy.cos(jvect[:,1])*numpy.cos(jvect[:,0])
            mmz = numpy.sin(jvect[:,1])
            mm = numpy.array([mmx,mmy,mmz]).transpose()
        
        elif self.dirc == 1:
            mm = [numpy.arctan2(self.vect[:,0],self.vect[:,1]),numpy.arcsin(self.vect[:,2])]
            mm = numpy.array(mm)*180./numpy.pi
        
        return mm
        
if __name__ == "__main__":
    
    a=CoFactors()
    a=Redirect()
    a=WidgetPrint()
    a=WidgetPrint()
    a=Vector()
