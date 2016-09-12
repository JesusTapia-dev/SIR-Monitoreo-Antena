'''
The module JroAntSetup contains the pre-defined parameters for beam modelling of the Jicamarca ante-
nna. Any new configuration must be added in this module (if the user decides  that) using a specific
ID (pattern value) or it would be read from a file using pattern=None.

MODULES CALLED:
OS, NUMPY
    
MODIFICATION HISTORY:
Created by Ing. Freddy Galindo (frederickgalindo@gmail.com). ROJ Sep 20, 2009.
'''

import os
import numpy

def ReturnSetup(path=None,filename=None,pattern=0):
    """
        ReturnSetup is a pre-defined list of  Jicamarca antenna configurations which returns a dic-
    tionary giving the configuration  parameters (e.g. transmitted phases). To  choose one, the
    user must define the input "pattern" (See valid values below). 
    
    Parameters:
    -----------
    
    pattern = A integer (>=0) to specify the setup to choose. The default value is zero. If the
      antenna configuration is user-defined pattern must be None.
    
    path = Set this input a string to specifiy  the folder path where the user-defined configu-
      ration file is placed. If this value is not defined ReturnSetup will return None.
      
    file = Set this input a string to specifiy the name of the user-defined  configuration file
      (*.txt). if this value is not defined ReturnSEtup will return None.
    
    Examples:
    ---------
    
    Choosing a pre-defined antenna configuration
    setup = ReturnSetup(pattern=1)
    
    Reading a user-defined antenna configuration
    setup = ReturnSetup(path="/users/users/Progs/Patterns/",file="ExpSep232009.txt")
    """
    
    
    if pattern == 0:
        title = "for module (rx)"
        
        ues = numpy.array([1.,2.,2.,1.])
        phase = numpy.zeros([8,8])
        phase[0:4,:] = 4
        phase[4:8,:] = 5
        
        gaintx = numpy.zeros([8,8])
        gaintx[0,0] = 1

        gainrx = numpy.zeros([8,8])
        gainrx[0,0] = 1

        justrx = 1
    
    elif pattern==1: 
        # Configuration 1/16 on-axis (rx)
        title = " for 1/16 on-axis (rx)"    
        
        ues = numpy.array([1.,2.,2.,1.])
        phase = numpy.zeros([8,8])
        phase[0:4,:] = 4
        phase[4:8,:] = 5
        
        gaintx = numpy.zeros([8,8])
        gaintx[0:2,0:2] = 1
        
        gainrx = numpy.zeros([8,8])
        gainrx[0:2,0:2] = 1
        
        justrx = 1
    
    elif pattern == 2:
        # Configuration for On-Axis
        title = " for 1/4 on-axis (rx)"    
        
        ues = numpy.array([1.,2.,2.,1.])
        phase = numpy.zeros([8,8])
        phase[0:4,:] = 4
        phase[4:8,:] = 5

        gaintx = numpy.zeros([8,8])
        gaintx[0:4,0:4] = 1
        
        gainrx = numpy.zeros([8,8])
        gainrx[0:4,0:4] = 1
        
        justrx = 1
    
    elif pattern == 3:
        # Configuration for On-Axis
        title = " for all on-axis (rx)"    
        
        ues = numpy.array([1.,2.,2.,1.])
        phase = numpy.zeros([8,8])
        phase[0:4,:] = 4
        phase[4:8,:] = 5
        
        gaintx = numpy.zeros([8,8])
        gaintx[:,:] = 1
        
        gainrx = numpy.zeros([8,8])
        gainrx[:,:] = 1
        
        justrx = 0

    elif pattern == 4:
        # Configuration for oblique ISR On-Axis
        title = " for Oblique ISR On-axis"    
        
        ues = numpy.array([1.,2.,2.,1.])
        phase = numpy.zeros([8,8])
        phase[0:4,:] = 4
        phase[4:8,:] = 5
        
        gaintx = numpy.zeros([8,8])
        gaintx[:,:] = 1
        
        gainrx = numpy.zeros([8,8])
        gainrx[:,:] = 1
        
        justrx = 0

    elif pattern == 5:
        # Configuration for oblique ISR "4.5"
        title = " for Oblique ISR '4.5'"    
        
        ues = numpy.array([1.,2.,2.,1.])
        phase = numpy.array([[4,4,5,5,2,2,3,3],
                          [4,5,5,2,2,3,3,4],
                          [5,5,2,2,3,3,4,4],
                          [5,2,2,3,3,4,4,5],
                          [3,3,4,4,5,5,2,2],
                          [3,4,4,5,5,2,2,3],
                          [4,4,5,5,2,2,3,3],
                          [4,5,5,2,2,3,3,4]],dtype=float)
        
        gaintx = numpy.zeros([8,8])
        gaintx[:,:] = 1
        
        gainrx = numpy.zeros([8,8])
        gainrx[:,:] = 1
        
        justrx = 0

    elif pattern == 6:
        # Configuration for oblique ISR "6.0S"
        title = " for Oblique ISR '6.0S'"    

        ues = numpy.array([1.,2.,2.,1.])
        phase = numpy.array([[4,5,2,3,4,5,2,3],
                          [5,2,3,4,5,2,3,4],
                          [2,3,4,5,2,3,4,5],
                          [3,4,5,2,3,4,5,2],
                          [5,2,3,4,5,2,3,4],
                          [2,3,4,5,2,3,4,5],
                          [3,4,5,2,3,4,5,2],
                          [4,5,2,3,4,5,2,3]],dtype=float)
        
        gaintx = numpy.zeros([8,8])
        gaintx[:,:] = 1
        
        gainrx = numpy.zeros([8,8])
        gainrx[:,:] = 1
        
        justrx = 0

    elif pattern == 7:
        # Configuration for oblique ISR "3.0N"
        title = " for Oblique ISR '3.0N'"    
        
        ues = numpy.array([1.,2.,2.,1.])
        phase = numpy.array([[4,3,2,5,4,3,2,5],
                          [3,2,5,4,3,2,5,4],
                          [2,5,4,3,2,5,4,3],
                          [5,4,3,2,5,4,3,2],
                          [5,4,3,2,5,4,3,2],
                          [4,3,2,5,4,3,2,5],
                          [3,2,5,4,3,2,5,4],
                          [2,5,4,3,2,5,4,3]],dtype=float)
        
        gaintx = numpy.zeros([8,8])
        gaintx[:,:] = 1
        
        gainrx = numpy.zeros([8,8])
        gainrx[:,:] = 1
        
        justrx = 0
    
    elif pattern == 8:
        # Configuration for North Fritts"
        title = " for North (Fritts)"    

        ues = numpy.array([2.513, 1.0, 3.0, 0.413])
        phase = numpy.array([[4.29, 3.55, 2.82, 2.08, 4.20, 3.47, 2.73, 2.00],
                          [2.94, 2.20, 5.44, 4.70, 4.32, 3.59, 2.85, 2.12],
                          [5.56, 4.82, 4.09, 3.35, 4.44, 3.71, 2.97, 2.24],
                          [4.20, 3.47, 2.73, 2.00, 4.56, 3.82, 3.09, 2.35],
                          [4.20, 3.47, 2.73, 2.00, 4.56, 3.82, 3.09, 2.35],
                          [4.32, 3.59, 2.85, 2.12, 2.94, 2.20, 5.44, 4.70],
                          [4.44, 3.71, 2.97, 2.24, 5.56, 4.82, 4.09, 3.35],
                          [4.56, 3.82, 3.09, 2.35, 4.20, 3.47, 2.73, 2.00]],dtype=float)
        
        gaintx = numpy.zeros([8,8])
        gaintx[0:4,0:4] = 1
        gaintx[4:8,4:8] = 1
        
        gainrx = numpy.zeros([8,8])
        gainrx[0:4,0:4] = 1
        gainrx[4:8,4:8] = 1
        
        justrx = 0

    elif pattern == 9:
        # Configuration for West Fritts"
        title = " for West (Fritts)"    

        ues = numpy.array([2.513, 1.0, 3.0, 0.413])
        phase = numpy.array([[4.29, 3.55, 2.82, 2.08, 4.20, 3.47, 2.73, 2.00],
                          [2.94, 2.20, 5.44, 4.70, 4.32, 3.59, 2.85, 2.12],
                          [5.56, 4.82, 4.09, 3.35, 4.44, 3.71, 2.97, 2.24],
                          [4.20, 3.47, 2.73, 2.00, 4.56, 3.82, 3.09, 2.35],
                          [4.20, 3.47, 2.73, 2.00, 4.56, 3.82, 3.09, 2.35],
                          [4.32, 3.59, 2.85, 2.12, 2.94, 2.20, 5.44, 4.70],
                          [4.44, 3.71, 2.97, 2.24, 5.56, 4.82, 4.09, 3.35],
                          [4.56, 3.82, 3.09, 2.35, 4.20, 3.47, 2.73, 2.00]],dtype=float)
        
        gaintx = numpy.zeros([8,8])
        gaintx[4:8,0:4] = 1
        gaintx[4:8,0:4] = 1

        gainrx = numpy.zeros([8,8])
        gainrx[4:8,0:4] = 1
        gainrx[4:8,0:4] = 1

        justrx = 0

    elif pattern == 10:
        # Configuration for South Fritts"
        title = " for South (Fritts)"    

        ues = numpy.array([0.413, 2.0, 1.0, 1.513])
        phase = numpy.array([[2.0 , 2.73, 3.47, 4.2 , 2.08, 2.82, 3.55, 4.29],
                          [2.12, 2.85, 3.59, 4.32, 4.7 , 5.44, 2.20, 2.94],
                          [2.24, 2.97, 3.71, 4.44, 3.35, 4.09, 4.82, 5.56],
                          [2.35, 3.09, 3.82, 4.56, 2.0 , 2.73, 3.47, 4.20],
                          [2.08, 2.82, 3.55, 4.29, 2.0 , 2.73, 3.47, 4.20],
                          [4.70, 5.44, 2.20, 2.94, 2.12, 2.85, 3.59, 4.32],
                          [3.35, 4.09, 4.82, 5.56, 2.24, 2.97, 3.71, 4.44],
                          [2.00, 2.73, 3.47, 4.20, 2.35, 3.09, 3.82, 4.56]],dtype=float)

        gaintx = numpy.zeros([8,8])
        gaintx[0:4,0:4] = 1
        gaintx[4:8,4:8] = 1

        gainrx = numpy.zeros([8,8])
        gainrx[0:4,0:4] = 1
        gainrx[4:8,4:8] = 1

        justrx = 0

    elif pattern == 11:
        # Configuration for East Fritts"
        title = " for East (Fritts)"    

        ues = numpy.array([0.413, 2.0, 1.0, 1.513])
        phase = numpy.array([[2.0 , 2.73, 3.47, 4.2 , 2.08, 2.82, 3.55, 4.29],
                          [2.12, 2.85, 3.59, 4.32, 4.7 , 5.44, 2.20, 2.94],
                          [2.24, 2.97, 3.71, 4.44, 3.35, 4.09, 4.82, 5.56],
                          [2.35, 3.09, 3.82, 4.56, 2.0 , 2.73, 3.47, 4.20],
                          [2.08, 2.82, 3.55, 4.29, 2.0 , 2.73, 3.47, 4.20],
                          [4.70, 5.44, 2.20, 2.94, 2.12, 2.85, 3.59, 4.32],
                          [3.35, 4.09, 4.82, 5.56, 2.24, 2.97, 3.71, 4.44],
                          [2.00, 2.73, 3.47, 4.20, 2.35, 3.09, 3.82, 4.56]],dtype=float)
        
        gaintx = numpy.zeros([8,8])
        gaintx[4:8,0:4] = 1
        gaintx[4:8,0:4] = 1

        gainrx = numpy.zeros([8,8])
        gainrx[4:8,0:4] = 1
        gainrx[4:8,0:4] = 1

        justrx = 0

    elif pattern == 12:
        # Configuration for DEWD position (2009)
        title = " for DEWD position (2009) East Beam"    
        
        ues = numpy.array([0.,0.,0.75,0.75])
        phase = numpy.array([[2,3,3,3,3,4,4,4],
                          [5,2,2,2,2,3,3,3],
                          [3,4,4,4,4,5,5,5],
                          [2,3,3,3,3,4,4,4], 
                          [4,5,5,5,5,2,2,2],
                           [3,4,4,4,4,5,5,5],
                            [5,2,2,2,2,3,3,3],
                           [4,5,5,5,5,2,2,2]],dtype=float)
        
        gaintx = numpy.zeros([8,8])
        gaintx[:,:] = 1
        
        gainrx = numpy.zeros([8,8])
        gainrx[:,0:4] = 1
        
        justrx = 0
    
    elif pattern == 13:
        # Configuration for DEWD position (2009)
        title = " for DEWD position (2009) West Beam"    
        
        ues = numpy.array([1.0,0.5,1.5,2.0])
        phase = numpy.array([[5,4,2,5,3,2,4,3],
                          [2,5,3,2,4,3,5,4],
                          [2,5,3,2,4,3,5,4],
                          [3,2,4,3,5,4,2,5],
                          [3,2,4,3,5,4,2,5],
                          [4,3,5,4,2,5,3,2],  
                          [4,3,5,4,2,5,3,2],
                          [5,4,2,5,3,2,4,3]],dtype=float)

        gaintx = numpy.zeros([8,8])
        gaintx[:,:] = 1
        
        gainrx = numpy.zeros([8,8])
        gainrx[4:8,:] = 1
        
        justrx = 0

    elif pattern == 14:
        # Configuration for DVD position (2009)
        title = " for DVD position (2009)"    
        
        ues = numpy.array([1.0,2.0,2.0,1.25])
        phase = numpy.array([[2,2,5,5,4,4,3,3],
                          [2,5,5,4,4,3,3,2],
                          [5,5,4,4,3,3,2,2],
                             [5,4,4,3,3,2,2,5],
                             [5,5,4,4,3,3,2,2],
                          [5,4,4,3,3,2,2,5],  
                          [4,4,3,3,2,2,5,5],
                          [4,3,3,2,2,5,5,4]],dtype=float)

        gaintx = numpy.zeros([8,8])
        gaintx[:,:] = 1
        
        gainrx = numpy.zeros([8,8])
        gainrx[0:4,0:4] = 1

        justrx = 0

    elif pattern == 15:
        # Configuration for Julia CP2
        title = " for Julia CP2 Ew"    
        
        ues = numpy.array([0.0,1.0,1.0,0.0])
        phase = numpy.array([[2,2,5,4,3,3,2,5],
                          [2,5,4,4,3,2,5,5],
                          [5,4,3,3,2,5,4,4],
                          [4,4,3,2,5,5,4,3],
                          [4,4,3,2,5,5,4,3],
                          [4,3,2,2,5,4,3,3],
                          [3,2,5,5,4,3,2,2],
                          [2,2,5,4,3,3,2,5]],dtype=float)

        gaintx = numpy.zeros([8,8])
        gaintx[0:4,4:8] = 1
        gaintx[4:8,0:4] = 1

        gainrx = numpy.zeros([8,8])
        gainrx[0,0] = 1

        justrx = 0
    
    elif pattern == 16:
        # Configuration for Julia CP2
        title = " for Julia CP2 NS"    
        
        ues = numpy.array([1.0,2.0,2.0,1.0])
        phase = numpy.array([[4,4,3,2,5,5,4,3],
                          [4,3,2,2,5,4,3,3],
                          [3,2,5,5,4,3,2,2],
                          [2,2,5,4,3,3,2,5],
                          [2,2,5,4,3,3,2,5],
                          [2,5,4,4,3,2,5,5],
                          [5,4,3,3,2,5,4,4],
                          [4,4,3,2,5,5,4,3]],dtype=float)
        
        gaintx = numpy.zeros([8,8])
        gaintx[0:4,0:4] = 1
        gaintx[4:8,4:8] = 1
        
        gainrx = numpy.zeros([8,8])
        gainrx[0:4,0:4] = 1

        justrx = 0

    elif pattern == 17:
        # Configuration for Julia CP3
        title = " for Julia CP3 NS"    
        
        ues = numpy.array([1.0,1.0,1.0,1.0])
        phase = numpy.array([[4,4,3,2,5,5,4,3],
                          [4,3,2,2,5,4,3,3],
                          [3,2,5,5,4,3,2,2],
                          [2,2,5,4,3,3,2,5],
                          [2,2,5,4,3,3,2,5],
                          [2,5,4,4,3,2,5,5],
                          [5,4,3,3,2,5,4,4],
                          [4,4,3,2,5,5,4,3]],dtype=float)
        
        gaintx = numpy.zeros([8,8])
        gaintx[0:4,0:4] = 1
        gaintx[4:8,4:8] = 1
        
        gainrx = numpy.zeros([8,8])
        gainrx[0:4,0:4] = 1

        justrx = 0

    elif pattern == 18:
        # Configuration for Julia V
        title = " for Julia V"    
        
        ues = (2/3.)*numpy.array([1.5,3.0+0.75,3.0,1.5-0.75])
        phase = numpy.array([[4,4,3,3,2,2,5,5],
                          [4,3,3,2,2,5,5,4],
                          [3,3,2,2,5,5,4,4],
                          [3,2,2,5,5,4,4,3],
                            [3,3,2,2,5,5,4,4],
                             [3,2,2,5,5,4,4,3],
                          [2,2,5,5,4,4,3,3],
                          [2,5,5,4,4,3,3,2]],dtype=float)

        gaintx = numpy.zeros([8,8])
        gaintx[0:4,0:4] = 1
        gaintx[4:8,4:8] = 1
        
        gainrx = numpy.zeros([8,8])
        gainrx[0:4,0:4] = 1

        justrx = 0

    elif pattern == 19:
        # Configuration for Julia V
        title = " for Julia EW 2006-2007 (W)"    
        
        ues = numpy.array([1.0+0.66,2.0+0.66,2.0,1.0])
        phase = numpy.array([[4,3,2,5,4,3,2,5],
                          [4,3,2,5,4,3,2,5],
                          [4,3,2,5,4,3,2,5],
                          [4,3,2,5,4,3,2,5],
                          [5,4,3,2,5,4,3,2],
                          [5,4,3,2,5,4,3,2],
                            [5,4,3,2,5,4,3,2],
                          [5,4,3,2,5,4,3,2]],dtype=float)

        gaintx = numpy.zeros([8,8])
        gaintx[:,:] = 1
        
        gainrx = numpy.zeros([8,8])
        gainrx[:,:] = 1

        justrx = 0

    elif pattern == 20:
        # Configuration for Julia V
        title = " for Julia EW 2006-2007 (E)"    
        
        ues = numpy.array([1.0,1.0,1.0,1.0])
        phase = numpy.array([[4,4,4,4,5,5,5,5],
                          [3,3,3,3,4,4,4,4],
                          [5,5,5,5,2,2,2,2],
                          [4,4,4,4,5,5,5,5],
                          [2,2,2,2,3,3,3,3],
                          [5,5,5,5,2,2,2,2],
                          [3,3,3,3,4,4,4,4],
                          [2,2,2,2,3,3,3,3]],dtype=float)

        gaintx = numpy.zeros([8,8])
        gaintx[:,:] = 1

        gainrx = numpy.zeros([8,8])
        gainrx[0:4,0:4] = 1
        gainrx[4:8,4:8] = 1

        justrx = 0
    
    elif pattern == 21:
        # Configuration for EW Imaging 1996
        title = " for EW Imaging 1996"    
        
        ues = numpy.array([1.0,2.0,2.0,1.0])
        phase = numpy.array([[4,4,3,2,5,5,4,3],
                          [4,3,2,2,5,4,3,3],
                             [3,2,5,5,4,3,2,2],
                          [2,2,5,4,3,3,2,5],
                          [2,2,5,4,3,3,2,5],
                          [2,5,4,4,3,2,5,5],
                          [5,4,3,3,2,5,4,4],
                          [4,4,3,2,5,5,4,3]],dtype=float)

        gaintx = numpy.zeros([8,8])
        gaintx[0:4,0:4] = 1
        gaintx[4:8,4:8] = 1
        
        gainrx = numpy.zeros([8,8])
        gainrx[0,0] = 1

        justrx = 0

    elif pattern == 22:
        # Configuration for EW Imaging 2003
        title = " for EW Imaging 2003"    

        ues = numpy.array([1.0,1.0,1.0,1.0])
        phase = numpy.array([[4,4,3,2,0,0,0,0],
                          [2,3,2,2,0,0,0,0],
                             [5,0,2,5,0,0,0,0],
                          [2,4,3,4,0,0,0,0],
                          [0,0,0,0,3,3,2,5],
                          [0,0,0,0,2,2,5,5],
                          [0,0,0,0,4,3,5,4],
                          [0,0,0,0,5,3,2,3]],dtype=float)

        gaintx = numpy.zeros([8,8])
        gaintx[0:4,0:4] = 1
        gaintx[4:8,4:8] = 1
        
        gainrx = numpy.zeros([8,8])
        gainrx[0,0] = 1

        justrx = 0

    elif pattern == 23:
        # Configuration for EW Imaging 2003
        title = " for EW Imaging 2006-2008"    
        
        ues = numpy.array([1.0,1.0,1.0,2.0])
        phase = numpy.array([[4,4,3,2,0,0,0,0],
                          [2,3,2,2,0,0,0,0],
                             [5,0,2,5,0,0,0,0],
                          [2,4,3,4,0,0,0,0],
                          [0,0,0,0,3,3,2,5],
                          [0,0,0,0,2,2,5,5],
                          [0,0,0,0,4,3,5,4],
                          [0,0,0,0,5,3,2,3]],dtype=float)

        gaintx = numpy.zeros([8,8])
        gaintx[0:4,0:4] = 1
        gaintx[4:8,4:8] = 1
        
        gainrx = numpy.zeros([8,8])
        gainrx[0,0] = 1

        justrx = 0

    elif pattern == 50:
        # Configuration for vertical drift 1996
        title = " for Vertical drift 1996"    
        
        ues = (2/3.)*numpy.array([0.,1.5,1.5,0.])
        phase = numpy.array([[4,4,3,2,5,5,4,3],
                          [4,3,2,2,5,4,3,3],
                          [3,2,5,5,4,3,2,2],
                          [2,2,5,4,3,3,2,5],
                          [2,2,5,4,3,3,2,5],
                          [2,5,4,4,3,2,5,5],
                          [5,4,3,3,2,5,4,4],
                          [4,4,3,2,5,5,4,3]],dtype=float)

        gaintx = numpy.zeros([8,8])
        gaintx[:,:] = 1
        
        gainrx = numpy.zeros([8,8])
        gainrx[:,:] = 1

        justrx = 0
    
    elif pattern == 51:
        # Configuration for vertical drift 1996
        title = " for East-West Drifts 1996 (W beam)"    
        
        ues = numpy.array([0.0,1.0,2.0,1.0])
        phase = numpy.array([[4,3,5,4,2,5,3,2],
                          [4,3,5,4,2,5,3,2],
                          [4,3,5,4,2,5,3,2],
                          [4,3,5,4,2,5,3,2],
                          [5,4,2,5,3,2,4,3],
                          [5,4,2,5,3,2,4,3],
                          [5,4,2,5,3,2,4,3],
                          [5,4,2,5,3,2,4,3]],dtype=float)

        gaintx = numpy.zeros([8,8])
        gaintx[:,:] = 1
        
        gainrx = numpy.zeros([8,8])
        gainrx[4:8,:] = 1

        justrx = 0

    elif pattern == 52:
        # Configuration for vertical drift 1996
        title = " for East-West Drifts 1996 (E Beam)"    
        
        ues = numpy.array([1.0,1.0,0.0,0.0])
        phase = numpy.array([[4,4,4,4,5,5,5,5],
                          [3,3,3,3,4,4,4,4],
                          [5,5,5,5,2,2,2,2],
                          [4,4,4,4,5,5,5,5],
                          [2,2,2,2,3,3,3,3],
                          [5,5,5,5,2,2,2,2],
                          [3,3,3,3,4,4,4,4],
                          [2,2,2,2,3,3,3,3]],dtype=float)

        gaintx = numpy.zeros([8,8])
        gaintx[:,:] = 1
        
        gainrx = numpy.zeros([8,8])
        gainrx[:,0:4] = 1

        justrx = 0

    elif pattern == 53:
        # Configuration for vertical drift 1996
        title = " for DVD position 3 (2006-2008)"    
        
        ues = numpy.array([1.,2,2,1])
        phase = numpy.array([[4,4,3,3,2,2,5,5],
                          [4,3,3,2,2,5,5,4],
                          [3,3,2,2,5,5,4,4],
                          [3,2,2,5,5,4,4,3],
                          [3,3,2,2,5,5,4,4],
                          [3,2,2,5,5,4,4,3],
                          [2,2,5,5,4,4,3,3],
                          [2,5,5,4,4,3,3,2]],dtype=float)

        gaintx = numpy.zeros([8,8])
        gaintx[:,:] = 1
        
        gainrx = numpy.zeros([8,8])
        gainrx[0:4,4:8] = 1

        justrx = 0

    elif pattern == 54:
        # Configuration for vertical drift 1996
        title = " for DEWD (Mar 2005)"    
        
        ues = numpy.array([0.,1.,1/3.,1])
        phase = numpy.array([[4,3,2,5,3,3,3,3],
                          [4,3,2,5,2,2,2,2],
                          [4,3,2,4,5,5,5,5],
                          [4,3,2,4,4,4,3,3],
                          [5,4,3,2,2,2,2,2],
                          [5,4,3,2,5,5,5,5],
                          [5,4,3,5,4,4,4,4],
                          [5,4,3,5,3,3,2,2]],dtype=float)

        gaintx = numpy.zeros([8,8])
        gaintx[:,:] = 1
        
        gainrx = numpy.zeros([8,8])
        gainrx[:,0:4] = 1

        justrx = 0
    
    elif pattern == 55:
        # Configuration for vertical drift 1996
        title = " for DEWD (Mar 2005)"    
        
        ues = numpy.array([0.,1.,1/3.,1])
        phase = numpy.array([[4,3,2,5,3,3,3,3],
                          [4,3,2,5,2,2,2,2],
                          [4,3,2,4,5,5,5,5],
                          [4,3,2,4,4,4,3,3],
                          [5,4,3,2,2,2,2,2],
                          [5,4,3,2,5,5,5,5],
                          [5,4,3,5,4,4,4,4],
                          [5,4,3,5,3,3,2,2]],dtype=float)

        gaintx = numpy.zeros([8,8])
        gaintx[:,:] = 1
        
        gainrx = numpy.zeros([8,8])
        gainrx[0:4:,4:8] = 1

        justrx = 0

    elif pattern ==56:
        # Configuration using antenna compression
        title = " for antenna compression AA*"
        
        ues = numpy.array([0.0,0.0,0.0,0.0])
        phase = numpy.array([[4,4,4,2,4,4,2,4],
                          [4,4,4,2,4,4,2,4],
                          [2,2,2,4,2,2,4,2],
                          [4,4,4,2,4,4,2,4],
                          [2,2,2,4,2,2,4,2],
                          [2,2,2,4,2,2,4,2],
                          [4,4,4,2,4,4,2,4],
                          [2,2,2,4,2,2,4,2]],dtype=float)

        gaintx = numpy.zeros([8,8])
        gaintx[:,:] = 1
        
        gainrx = numpy.zeros([8,8])
        gainrx[0:4,0:4] = 1

        justrx = 0

    elif pattern ==57:
        # Configuration using antenna compression
        title = " for antenna compression AB*"
        
        ues = numpy.array([0.0,0.0,0.0,0.0])
        phase = numpy.array([[4,4,2,4,2,2,4,2],
                          [4,4,2,4,2,2,4,2],
                          [2,2,4,2,4,4,2,4],
                          [4,4,2,4,2,2,4,2],
                          [2,2,4,2,4,4,2,4],
                          [2,2,4,2,4,4,2,4],
                          [4,4,2,4,2,2,4,2],
                          [2,2,4,2,4,4,2,4]],dtype=float)

        gaintx = numpy.zeros([8,8])
        gaintx[:,:] = 1
        
        gainrx = numpy.zeros([8,8])
        gainrx[0:4,0:4] = 1

        justrx = 0

    elif pattern ==58:
        # Configuration using in Oblique ISR 4.5
        title = " for Oblique ISR 4.5"
        
        ues = numpy.array([1.0,2.0,2.0,1.0])
        phase = numpy.array([[4,4,5,5,2,2,3,3],
                          [4,5,5,2,2,3,3,4],
                          [5,5,2,2,3,3,4,4],
                          [5,2,2,3,3,4,4,5],
                          [3,3,4,4,5,5,2,2],
                          [3,4,4,5,5,2,2,3],
                          [4,4,5,5,2,2,3,3],
                          [4,5,5,2,2,3,3,4]],dtype=float)

        gaintx = numpy.zeros([8,8])
        gaintx[:,:] = 1
        
        gainrx = numpy.zeros([8,8])
        gainrx[:,:] = 1

        justrx = 1
    
    elif pattern == 60:
        title=" for Differential phase 2000"
        ues = (2/3.)*numpy.array([0.,1.5-0.5,1.5,0.+0.5])
        
        phase = numpy.array([[4,4,3,2,5,5,4,3],
                          [4,3,2,2,5,4,3,3],
                          [3,2,5,5,4,3,2,2],
                          [2,2,5,4,3,3,2,5],
                          [2,2,5,4,3,3,2,5],
                          [2,5,4,4,3,2,5,5],
                          [5,4,3,3,2,5,4,4],
                          [4,4,3,2,5,5,4,3]],dtype=float)
        
        gaintx = numpy.zeros([8,8])
        gaintx[:,:] = 1
        
        gainrx = numpy.zeros([8,8])
        gainrx[0:4,0:4] = 1
        
        justrx = 0
    
    elif pattern == 61:
        #for East-West 2003 W
        title=" for East-West 2003"
        
        ues = numpy.array([1.+0.66,2.+0.66,2.,1.]) 
        
        phase = numpy.array([[4,3,2,5,4,3,2,5],
                            [4,3,2,5,4,3,2,5],
                            [4,3,2,5,4,3,2,5],
                            [4,3,2,5,4,3,2,5],
                            [5,4,3,2,5,4,3,2],
                            [5,4,3,2,5,4,3,2],
                            [5,4,3,2,5,4,3,2],
                            [5,4,3,2,5,4,3,2]],dtype=float)
        
        gaintx = numpy.zeros([8,8])
        gaintx[:,:] = 1
        
        gainrx = numpy.zeros([8,8])
        gainrx[4:8,:] = 1
        
        justrx = 0
    
    elif pattern == 62:
        #for East-West 2003 E
        title=" for East-West 2003"
        
        ues = numpy.array([1.,1.,0.+1.0,0.+1.0])
        
        phase = numpy.array([[4,4,4,4,5,5,5,5],
                             [3,3,3,3,4,4,4,4],
                             [5,5,5,5,2,2,2,2],
                             [4,4,4,4,5,5,5,5],
                             [2,2,2,2,3,3,3,3],
                             [5,5,5,5,2,2,2,2],
                             [3,3,3,3,4,4,4,4],
                             [2,2,2,2,3,3,3,3]],dtype=float)

        gaintx = numpy.zeros([8,8])
        gaintx[:,:] = 1
        
        gainrx = numpy.zeros([8,8])
        gainrx[:,0:4] = 1
        
        justrx = 0
    
    elif pattern == 63:
        
        title=" for Differential phase 2004 High Alt."
        
        ues = (2/3.)*numpy.array([0.,1.5-1.0,1.5,0.+1.0])
        
        phase = numpy.array([[4,4,3,2,5,5,4,3],
                             [4,3,2,2,5,4,3,3],
                             [3,2,5,5,4,3,2,2],
                             [2,2,5,4,3,3,2,5],
                             [2,2,5,4,3,3,2,5],
                             [2,5,4,4,3,2,5,5],
                             [5,4,3,3,2,5,4,4],
                             [4,4,3,2,5,5,4,3]],dtype=float)

        gaintx = numpy.zeros([8,8])
        gaintx[:,:] = 1
        
        gainrx = numpy.zeros([8,8])
        gainrx[:,:] = 1
        
        justrx = 0
    
    elif pattern == 64:
        
        title=" for Differential Phase Perp to B 2005-2006"
        
        ues = (2/3.)*numpy.array([1.5,3.0+0.75,3.0,1.5-0.75])
        
        phase = numpy.array([[4,4,3,3,2,2,5,5],
                             [4,3,3,2,2,5,5,4],
                             [3,3,2,2,5,5,4,4],
                             [3,2,2,5,5,4,4,3],
                             [3,3,2,2,5,5,4,4],
                             [3,2,2,5,5,4,4,3],
                             [2,2,5,5,4,4,3,3],
                             [2,5,5,4,4,3,3,2]],dtype=float)

        gaintx = numpy.zeros([8,8])
        gaintx[:,:] = 1
        
        gainrx = numpy.zeros([8,8])
        gainrx[0:4,4:8] = 1
        
        justrx = 0
    
    elif pattern == 65:
        #for JULIA EW 2003 W
        title=" for JULIA EW 2003"
        
        ues = numpy.array([1+0.66,2+0.66,2.,1.])
        
        phase = numpy.array([[4,3,2,5,4,3,2,5],
                             [4,3,2,5,4,3,2,5],
                             [4,3,2,5,4,3,2,5],
                             [4,3,2,5,4,3,2,5],
                             [5,4,3,2,5,4,3,2],
                             [5,4,3,2,5,4,3,2],
                             [5,4,3,2,5,4,3,2],
                             [5,4,3,2,5,4,3,2]],dtype=float)

        gaintx = numpy.zeros([8,8])
        gaintx[:,:] = 1
        
        gainrx = numpy.zeros([8,8])
        gainrx[4:8,:] = 1
        
        justrx = 0
    
    elif pattern == 66:
        #for JULIA EW 2003 E
        title=" for JULIA EW 2003"
        
        ues = numpy.array([1.,1.,0.,0.])
        
        phase = numpy.array([[4,4,4,4,5,5,5,5],
                             [3,3,3,3,4,4,4,4],
                             [5,5,5,5,2,2,2,2],
                             [4,4,4,4,5,5,5,5],
                             [2,2,2,2,3,3,3,3],
                             [5,5,5,5,2,2,2,2],
                             [3,3,3,3,4,4,4,4],
                             [2,2,2,2,3,3,3,3]],dtype=float)

        gaintx = numpy.zeros([8,8])
        gaintx[:,:] = 1
        
        gainrx = numpy.zeros([8,8])
        gainrx[:,0:4] = 1
        
        justrx = 0
    
    elif pattern == 67:
        
        title=" for Vertical (Yellow Cables)"
        
        ues = numpy.array([0.25, 0.25, 0.25, 0.25])
        
        phase = numpy.array([[3.41, 3.41, 3.41, 3.41, 3.41, 3.41, 3.41, 3.41],
                             [2.78, 2.78, 2.78, 2.78, 2.78, 2.78, 2.78, 2.78],
                             [2.15, 2.15, 2.15, 2.15, 2.15, 2.15, 2.15, 2.15],
                             [5.52, 5.52, 5.52, 5.52, 5.52, 5.52, 5.52, 5.52],
                             [4.89, 4.89, 4.89, 4.89, 4.89, 4.89, 4.89, 4.89],
                             [4.26, 4.26, 4.26, 4.26, 4.26, 4.26, 4.26, 4.26],
                             [3.63, 3.63, 3.63, 3.63, 3.63, 3.63, 3.63, 3.63],
                             [3.00, 3.00, 3.00, 3.00, 3.00, 3.00, 3.00, 3.00]],dtype=float)

        gaintx = numpy.zeros([8,8])
        gaintx[:,:] = 1
        
        gainrx = numpy.zeros([8,8])
        gainrx[:,:] = 1
        
        justrx = 0
    
    elif pattern == 100:
        
        title=" for High Altitude Drift"
        
        ues = numpy.array([ 2.0,0.8,1.0,2.2])
        
        phase = numpy.array([[5,5,4,4, 4,4,3,3],
                [5,4,4,4, 4,3,3,3],
                [4,4,4,4, 3,3,3,3],
                [4,4,4,3, 3,3,3,2],
                [3,3,2,2, 2,2,5,5],
                [3,2,2,2, 2,5,5,5],
                [2,2,2,2, 5,5,5,5],
                [2,2,2,5, 5,5,5,4]],dtype=float)
        
        gaintx = numpy.zeros([8,8])
        gaintx[:,:] = 1
        
        gainrx = numpy.zeros([8,8])
        gainrx[:,:] = 1
        
        justrx = 0
        
    
    elif pattern==None:
        
        inputs = numpy.array(["title","ues_tx","phase_tx","gain_tx","gain_rx","just_rx"])

        # Reading user-defined configuration.
        if path==None:path = os.getcwd() + os.sep + "patterns" + os.sep
        if filename==None:filename = "jropattern.txt"
        
        ff = open(os.path.join(path,filename),'r')
        
        while  1:
            # Checking EOF.
            init = ff.tell()
            if not ff.readline():break
            else:ff.seek(init)

            line = ff.readline().lstrip()
            if line.__len__()!=0:
                if line[0]!='#':                    
                    keys = line.split("=")
                    key = keys[0].lstrip().rstrip().lower()
                    vv = numpy.where(inputs==key)
                    if vv[0][0]==0:
                        title = keys[1].lstrip().rstrip()
                    elif vv[0][0]==1:
                        ues = (keys[1].lstrip().rstrip())
                        ues = numpy.float32(ues[1:-1].split(","))
                    elif vv[0][0]==2:
                        phase = numpy.zeros([8,8])
                        tx = (keys[1].lstrip().rstrip())
                        tx = numpy.float32(tx[2:-3].split(","))
                        phase[0,:] = tx
                        for ii in numpy.arange(7):
                            tx = ff.readline().lstrip().rstrip()
                            tx = numpy.float32(tx[1:-3+(ii==6)].split(","))
                            phase[ii+1,:] = tx
                    elif vv[0][0]==3:
                        gaintx = numpy.zeros([8,8])
                        gg = (keys[1].lstrip().rstrip())
                        gg = numpy.float32(gg[2:-3].split(","))
                        gaintx[0,:] = gg
                        for ii in numpy.arange(7):
                            gg = ff.readline().lstrip().rstrip()
                            gg = numpy.float32(gg[1:-3+(ii==6)].split(","))
                            gaintx[ii+1,:] = gg
                    elif vv[0][0]==4:
                        gainrx = numpy.zeros([8,8])
                        gg = (keys[1].lstrip().rstrip())
                        gg = numpy.float32(gg[2:-3].split(","))
                        gainrx[0,:] = gg
                        for ii in numpy.arange(7):
                            gg = ff.readline().lstrip().rstrip()
                            gg = numpy.float32(gg[1:-3+(ii==6)].split(","))
                            gainrx[ii+1,:] = gg
                    elif vv[0][0]==5:
                        justrx = numpy.float(keys[1].lstrip().rstrip())
        
        ff.close()
    
    
    
    setup = {"ues":ues, "phase":phase, "gaintx":gaintx, "gainrx":gainrx, "justrx":justrx, \
     "title":title}
    
    return setup
    
    
        
    