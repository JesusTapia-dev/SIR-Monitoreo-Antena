'''
Created on May 8, 2013

@author: Jose Antonio Sal y Rosas Celi
@contact: jose.salyrosas@jro.igp.gob.pe
'''

import os
from Files import Files

class OverJRO(Files):

    __scriptName = "OverJRO.py"

    def __init__(self):
        pass

    def setParameters(self, path, exp_name, phase_tx, gain_tx, gain_rx, ues_tx, just_rx):
        self.path = path
        self.exp_name = exp_name
        self.phase_tx = phase_tx
        self.gain_tx = gain_tx
        self.gain_rx = gain_rx
        self.ues_tx = ues_tx
        self.just_rx = just_rx

    def saveFile(self, contentFile):
        filename = self.setFilename()
        finalpath = os.path.join(self.path, self.setFileExtension(filename))
        print "HAHAH"
        finalpath = "apps/abs/static/data/"+finalpath
        self.save(finalpath, contentFile)
        return finalpath

    def setTextContent(self):
        title = "title ='%s'" % self.exp_name
        ues_tx = "ues_tx = %s" % self.ues_tx
        phase_tx = "phase_tx = %s" % (self.convertValue(self.phase_tx))
        gain_tx = "gain_tx = %s" % (self.convertValue(self.gain_tx))
        gain_rx = "gain_rx = %s" % (self.convertValue(self.gain_rx))
        just_rx = "just_rx = %d" % self.just_rx
        content = " %s\r\n\n %s\r\n\n %s\r\n %s\r\n %s\r\n %s\r\n" % (title, ues_tx, phase_tx, gain_tx, gain_rx, just_rx)
        return content

    def setFileExtension(self, filename):
        txtFile = filename + ".txt"

        return txtFile

    def convertValue(self, strAntenna):
        value = ""
        strAntenna = strAntenna.replace("],[","]+[")
        lsAntenna = strAntenna.split("+")
        for i,element in enumerate(lsAntenna):
            if i == 0:
                value += "%s,$\n" % element
            elif i == 7:
                value += "            %s\n" % element
            else:
                value += "            %s,$\n" % element

        return value


if __name__ == '__main__':
    path = "/home/fquino/workspace/radarsys/webapp/apps/abs/static/data"
    exp_name = "MST-ISR 2009 (NS-Up)"
    phase_tx = "[[0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5]," \
               "[1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0]," \
               "[0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5]," \
               "[0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5]," \
               "[1.0,1.0,1.0,1.0,1.5,1.5,1.5,1.5]," \
               "[0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5]," \
               "[1.0,1.0,1.0,1.0,1.0,1.0,1.0,1.0]," \
               "[0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5]]"
    gain_tx = "[[1,1,1,1,1,1,1,1]," \
              "[1,1,1,1,1,1,1,1]," \
              "[1,1,1,1,1,1,1,1]," \
              "[1,1,1,1,1,1,1,1]," \
              "[1,1,1,1,1,1,1,1]," \
              "[1,1,1,1,1,1,1,1]," \
              "[1,1,1,1,1,1,1,1]," \
              "[1,1,1,1,1,1,1,1]]"
    gain_rx = "[[1,1,1,1,0,0,0,0]," \
              "[1,1,1,1,0,0,0,0]," \
              "[1,1,1,1,0,0,0,0]," \
              "[1,1,1,1,0,0,0,0]," \
              "[0,0,0,0,1,1,1,1]," \
              "[0,0,0,0,1,1,1,1]," \
              "[0,0,0,0,1,1,1,1]," \
              "[0,0,0,0,1,1,1,1]]"
    ues_tx = "[0.533333,0.00000,1.06667,0.00000]"
    just_rx = 0
    data = OverJRO()
    data.setParameters(path, exp_name, phase_tx, gain_tx, gain_rx, ues_tx, just_rx)
    contentFile = data.setTextContent()
    data.saveFile(contentFile)
