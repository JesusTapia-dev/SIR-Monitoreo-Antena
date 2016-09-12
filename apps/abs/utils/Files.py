'''
Created on Jun 19, 2013

@author: Jose Antonio Sal y Rosas Celi
@contact: jose.salyrosas@jro.igp.gob.pe
'''

from datetime import datetime

class Files(object):

    def setFilename(self):
        return datetime.today().strftime("%Y%m%d%H%M%S%f")

    def save(self, filename, contentFile):
        f = open(filename, 'a+')
        f.write(contentFile)
        f.close()
