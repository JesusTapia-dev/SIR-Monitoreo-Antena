"""
The GRAPHICS_MISC.py module gathers classes and/or functions useful for generation of plots.

MODULES CALLED:
NUMPY, OS

MODIFICATION HISTORY:
Created by Ing. Freddy Galindo (frederickgalindo@gmail.com). ROJ, 13 August 2009.
"""

import os
import numpy
import sys


class ColorTable:
    def __init__(self,table=1,filepath=None):
        self.table = table
        #set to path for data folder, file: col_koki.dat
        if filepath==None:
            filepath= './apps/abs/utils/data/'
        self.filepath = filepath

    def readTable(self):
        if self.table>0:
            if self.table==1:
                
                f = open(os.path.join(self.filepath, './col_koki.dat') ,'rb')
                

                #f = open('./col_koki.dat','rb')

                # Reading SkyNoise Power (lineal scale)
                blue = numpy.fromfile(f,numpy.dtype([('var','b')]),256)
                blue = numpy.int32(blue['var'])
                val = numpy.where(blue<0)
                if val[0].size:blue[val] = blue[val] + numpy.int32(256)

                green = numpy.fromfile(f,numpy.dtype([('var','b')]),256)
                green = numpy.int32(green['var'])
                val = numpy.where(green<0)
                if val[0].size:green[val] = green[val] + numpy.int32(256)

                red = numpy.fromfile(f,numpy.dtype([('var','b')]),256)
                red = numpy.int32(red['var'])
                val = numpy.where(red<0)
                if val[0].size:red[val] = red[val] + numpy.int32(256)
                
                f.close()

                colortable = numpy.array([red/255.,green/255.,blue/255.])

                return colortable
