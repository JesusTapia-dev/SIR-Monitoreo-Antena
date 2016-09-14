#!/usr/bin/python


import sys, os, os.path
import traceback
import cgi, Cookie
import time, datetime
import types
import numpy
import numpy.fft
import scipy.linalg
import scipy.special
from StringIO import StringIO
#import Numeric

import Misc_Routines
import TimeTools
import JroAntSetup
import Graphics_OverJro
import Astro_Coords

class JroPattern():
    def __init__(self,pattern=0,path=None,filename=None,nptsx=101,nptsy=101,maxphi=5,fftopt=0, \
        getcut=0,dcosx=None,dcosy=None,eomwl=6,airwl=4, **kwargs):
        """
        JroPattern class creates an object to represent the useful parameters for beam mode-
        lling of the Jicamarca VHF radar.

        Parameters
        ----------
        pattern = An integer (See JroAntSetup to know the available values) to load a prede-
          fined configuration. The default value  is 0. To use a  user-defined configuration
          pattern  must be None.
        path = A string giving the directory that contains the user-configuration file. PATH
          will work if pattern is None.
        filename = A string giving the  name of the  user-configuration  file. FILENAME will
          work if pattern is None.
        nptsx = A scalar to specify the number of points  used to define the angular resolu-
          tion in the "x" axis. The default value is 101.
        nptsy = A scalar to specify the number of points  used to define the angular resolu-
          tion in the "x" axis. The default value is 101.
        maxphi = A scalar giving the maximum (absolute) angle (in degree) to model the ante-
          nna pattern. The default value is 5 degrees.
        fftopt = Set this input  to 1 to model  the beam using FFT.  To model  using antenna
          theory set to 0 (default value).
        getcut = Set to 1 to show an antenna cut instead of a contour plot of itself (set to
          0). The defautl value is 0.
        dcosx = An array giving the directional cosines for the  x-axis. DCOSX  will work if
          getcut is actived.
        dcosy = An array giving the directional cosines for the  y-axis. DCOSY  will work if
          getcut is actived.
        eomwl = A scalar giving the radar wavelength. The default value is 6m (50 MHZ).
        airwl = Set this input to float (or intger) to specify the wavelength (in meters) of
          the transmitted EOM wave in the air. The default value is 4m.

        Modification History
        --------------------
        Converted to Object-oriented Programming by Freddy Galindo, ROJ, 20 September 2009.
        """



        # Getting antenna configuration.
        if filename:
            setup = JroAntSetup.ReturnSetup(path=path,filename=filename,pattern=pattern)
    
            ues = setup["ues"]
            phase = setup["phase"]
            gaintx = setup["gaintx"]
            gainrx = setup["gainrx"]
            justrx = setup["justrx"]
            self.title = setup["title"]
        else:
            ues = kwargs["ues"]
            phase = kwargs["phases"]
            gaintx = kwargs["gain_tx"]
            gainrx = kwargs["gain_rx"]
            justrx = kwargs["just_rx"]
            self.title = kwargs.get("title", "JRO Pattern")

        # Defining attributes for JroPattern class.
        # Antenna configuration
        
        self.uestx = ues
        self.phasetx = phase
        self.gaintx = gaintx
        self.uesrx = ues
        self.phaserx = phase
        self.gainrx = gainrx
        self.justrx = justrx

        # Pattern resolution & method to model
        self.maxphi = maxphi
        self.nptsx = nptsx
        self.nptsy = nptsy
        self.fftopt = fftopt

        # To get a cut of the pattern.
        self.getcut = getcut

        maxdcos = numpy.sin(maxphi*Misc_Routines.CoFactors.d2r)
        if dcosx==None:dcosx = ((numpy.arange(nptsx,dtype=float)/(nptsx-1))-0.5)*2*maxdcos
        if dcosy==None:dcosy = ((numpy.arange(nptsy,dtype=float)/(nptsy-1))-0.5)*2*maxdcos
        self.dcosx = dcosx
        self.dcosy = dcosy
        self.nx = dcosx.size
        self.ny = dcosy.size*(getcut==0) + (getcut==1)

        self.eomwl = eomwl
        self.airwl = airwl

        self.kk = 2.*numpy.pi/eomwl

        self.pattern = None
        self.meanpos = None
        self.norpattern = None
        self.maxpattern = None

        

        self.getPattern()

    def getPattern(self):
        """
        getpattern method returns the modeled total antenna pattern and its mean position.

        Return
        ------
        pattern = An array giving the Modelled antenna pattern.
        mean_pos = A 2-elements array giving the mean position of the main beam.

        Examples
        --------
        >> [pattern, mean_pos] = JroPattern(pattern=2).getPattern()
        >> print meanpos
        [  8.08728085e-14  -4.78193873e-14]

        Modification history
        --------------------
        Developed by Jorge L. Chau.
        Converted to Python by Freddy R. Galindo, ROJ, 20 September 2009.
        """

        if (self.fftopt>0) and (self.getcut>0):
            #print  "Conflict bewteen fftopt and getcut"
            #print  "To get a cut of the antenna pattern uses ffopt=0"
            return None, None

        if (self.fftopt==0):
            # Getting antenna pattern using the array method
            self.pattern = self.__usingArray(rx=1)
            if (self.justrx==0):self.pattern = self.pattern*self.__usingArray(rx=0)

        elif (self.fftopt>0):
            # Getting antenna pattern using FFT method
            self.pattern = self.__usingFFT(rx=1)
            if (self.justrx==0):self.pattern = self.pattern*self.__usingFFT(rx=0)

        self.maxpattern = numpy.nanmax(self.pattern)
        self.norpattern = self.pattern/self.maxpattern
        if self.getcut==0:self.__getBeamPars()

    def __usingArray(self,rx):
        """
        __usingArray method returns the Jicamarca antenna pattern computed using array model

        pattern = dipolepattern x modulepattern

        Parameters
        ----------
        rx = Set to 1 to use the Rx information. Otherwise set to 0 for Tx.

        Return
        ------
        pattern = An array giving the modelled antenna pattern using the array model.

        Modification history
        --------------------
        Developed by Jorge L. Chau.
        Converted to Python by Freddy R. Galindo, ROJ, 20 September 2009.
        """

        if rx==1:
            ues = self.uesrx
            phase = self.phaserx
            gain = self.gainrx
        elif rx==0:
            ues = self.uestx
            phase = self.phasetx
            gain = self.gaintx

        ues = ues*360./self.airwl
        phase = phase*360./self.airwl

        for ii in range(4):
            if ii==0:dim = numpy.array([4,0,8,4])   # WEST
            elif ii==1:dim = numpy.array([0,0,4,4]) # NORTH
            elif ii==2:dim = numpy.array([0,4,4,8]) # EAST
            elif ii==3:dim = numpy.array([4,4,8,8]) # SOUTH
            xi = dim[0]; xf = dim[2]; yi = dim[1]; yf = dim[3]
            phase[xi:xf,yi:yf] = phase[xi:xf,yi:yf] + ues[ii]

        phase = -phase

        ar = self.eomwl*numpy.array([[0.5,6., 24.5],[0.5,6.,24.5]])
        nr = numpy.array([[12.,4.,2.],[12.,4.,2.]])
        lr = 0.25*self.eomwl*numpy.array([[0,0.,0],[0.,0,0]])

        # Computing module and dipole patterns.
        pattern = (numpy.abs(self.__dipPattern(ar,nr,lr)*self.__modPattern(phase,gain)))**2

        return pattern

    def __usingFFT(self,rx):
        """
        __usingFFT method returns the Jicamarca antenna pattern computed using The Fast Fou-
        rier Transform.

        pattern = iFFT(FFT(gain*EXP(j*phase)))

        Parameters
        ----------
        rx = Set to 1 to use the Rx information. Otherwise set to 0 for Tx.

        Return
        ------
        pattern = An array giving the modelled antenna pattern using the array model.

        Modification history
        --------------------
        Developed by Jorge L. Chau.
        Converted to Python by Freddy R. Galindo, ROJ, 20 September 2009.
        """

        if rx==1:
            ues = self.uesrx
            phase = self.phaserx
            gain = self.gainrx
        elif rx==0:
            ues = self.uestx
            phase = self.phasetx
            gain = self.gaintx

        ues = ues*360./self.airwl
        phase = phase*360./self.airwl

        for ii in range(4):
            if ii==0:dim = numpy.array([4,0,8,4])   # WEST
            elif ii==1:dim = numpy.array([0,0,4,4]) # NORTH
            elif ii==2:dim = numpy.array([0,4,4,8]) # EAST
            elif ii==3:dim = numpy.array([4,4,8,8]) # SOUTH
            xi = dim[0]; xf = dim[2]; yi = dim[1]; yf = dim[3]
            phase[xi:xf,yi:yf] = phase[xi:xf,yi:yf] + ues[ii]

        phase = -phase

        delta_x = self.eomwl/2.
        delta_y = self.eomwl/2.

        nxfft = 2048
        nyfft = 2048
        dcosx = (numpy.arange(nxfft) - (0.5*nxfft))/(nxfft*delta_x)*self.eomwl
        dcosy = (numpy.arange(nyfft) - (0.5*nyfft))/(nyfft*delta_y)*self.eomwl

        fft_gain = numpy.zeros((nxfft,nyfft))
        fft_phase = numpy.zeros((nxfft,nyfft))

        nx = 8
        ny = 8
        ndx =12
        ndy =12
        for iy in numpy.arange(ny):
            for ix in numpy.arange(nx):
                ix1 = nxfft/2-self.nx/2*ndx+ix*ndx
                if ix<(nx/2):ix1 = ix1 - 1
                if ix>=(nx/2):ix1 = ix1 + 1

                iy1 = nyfft/2-ny/2*ndx+iy*ndy
                if iy<(ny/2):iy1 = iy1 - 1
                if iy>=(ny/2):iy1 = iy1 + 1

                fft_gain[ix1:ix1+ndx-1,iy1:iy1+ndy-1] = gain[ix,ny-1-iy]
                fft_phase[ix1:ix1+ndx-1,iy1:iy1+ndy-1] = phase[ix,ny-1-iy]


        fft_phase = fft_phase*Misc_Routines.CoFactors.d2r

        pattern = numpy.abs(numpy.fft.fft2(fft_gain*numpy.exp(numpy.complex(0,1)*fft_phase)))**2
        pattern = numpy.fft.fftshift(pattern)

        xvals = numpy.where((dcosx>=(numpy.min(self.dcosx))) & (dcosx<=(numpy.max(self.dcosx))))
        yvals = numpy.where((dcosy>=(numpy.min(self.dcosy))) & (dcosy<=(numpy.max(self.dcosy))))

        pattern = pattern[xvals[0][0]:xvals[0][-1],yvals[0][0]:yvals[0][-1]]

        return pattern

    def __readAttenuation(self):
        """
        _readAttenuation reads the attenuations' file and returns an array giving  these va-
        lues (dB). The ext file must be in the directory "resource".

        Return
        ------
        attenuation = An array giving attenuation values read from the text file.

        Modification history
        --------------------
        Developed by Jorge L. Chau.
        Converted to Python by Freddy R. Galindo, ROJ, 20 September 2009.
        """

        attenuation = None
#        foldr = sys.path[-1] + os.sep + "resource" + os.sep
        base_path = os.path.dirname(os.path.abspath(__file__))
        #foldr = './resource'
        #filen = "attenuation.txt"
        attenuationFile = os.path.join(base_path,"resource","attenuation.txt")
        #ff = open(os.path.join(foldr,filen),'r')
        ff = open(attenuationFile,'r')
        exec(ff.read())
        ff.close()

        return attenuation

    def __dipPattern(self,ar,nr,lr):
        """
        _dipPattern function computes the dipole's pattern to  the Jicamarca radar. The next
        equation defines the pattern as a function of the mainlobe direction:

        sincx = SIN(k/2*n0x*(a0x*SIN(phi)*COS(alpha)))/SIN(k/2*(a0x*SIN(phi)*COS(alpha)))
        sincy = SIN(k/2*n0y*(a0y*SIN(phi)*SIN(alpha)))/SIN(k/2*(a0y*SIN(phi)*SIN(alpha)))
        A0(phi,alpha) = sincx*sincy
        Parameters
        ----------
        ar = ?
        nr = ?
        lr = ?

        Return
        ------
        dipole = An array giving antenna pattern from the dipole point of view..

        Modification history
        --------------------
        Developed by Jorge L. Chau.
        Converted to Python by Freddy R. Galindo, ROJ, 20 September 2009.
        """

        dipole = numpy.zeros((self.nx,self.ny),dtype=complex)
        for iy in range(self.ny):
            for ix in range(self.nx):
                yindex = iy*(self.getcut==0) + ix*(self.getcut==1)

                argx = ar[0,0]*self.dcosx[ix] - lr[0,0]
                if argx == 0.0:    
                    junkx = nr[0,0]
                else:
                    junkx = numpy.sin(0.5*self.kk*nr[0,0]*argx)/numpy.sin(0.5*self.kk*argx)
                

                argy = ar[1,0]*self.dcosy[yindex] - lr[1,0]
                if argy == 0.0: 
                    junky = nr[1,0]
                else:
                    junky = numpy.sin(0.5*self.kk*nr[1,0]*argy)/numpy.sin(0.5*self.kk*argy)
                

                dipole[ix,iy] = junkx*junky

        return dipole

    def __modPattern(self,phase,gain):
        """
        ModPattern computes the module's pattern to the Jicamarca radar.  The next equation
        defines    the pattern as a function mainlobe direction:

        phasex = pos(x)*SIN(phi)*COS(alpha)
        phasey = pos(y)*SIN(phi)*SIN(alpha)

        A1(phi,alpha) = TOTAL(gain*EXP(COMPLEX(0,k*(phasex+phasey)+phase)))

        Parameters
        ----------
        phase = Bidimensional array (8x8) giving the phase (in meters) of each module.
        gain  = Bidimensional array (8x8) giving to  define modules  will be active  (ones)
          and which will not (zeros).

        Return
        ------
        module = An array giving antenna pattern from the module point of view..

        Modification history
        --------------------
        Developed by Jorge L. Chau.
        Converted to Python by Freddy R. Galindo, ROJ, 20 September 2009.
        """

        pos = self.eomwl*self.__readAttenuation()
        posx = pos[0,:,:]
        posy = pos[1,:,:]

        phase = phase*Misc_Routines.CoFactors.d2r
        module = numpy.zeros((self.nx,self.ny),dtype=complex)
        for iy in range(self.ny):
            for ix in range(self.nx):
                yindex = iy*(self.getcut==0) + ix*(self.getcut==1)
                phasex = posx*self.dcosx[ix]
                phasey = posy*self.dcosy[yindex]
                tmp = gain*numpy.exp(numpy.complex(0,1.)*(self.kk*(phasex+phasey)+phase))
                module[ix,iy] = tmp.sum()

        return module

    def __getBeamPars(self):
        """
        _getBeamPars computes the main-beam parameters of the antenna.

        Modification history
        --------------------
        Developed by Jorge L. Chau.
        Converted to Python by Freddy R. Galindo, ROJ, 20 September 2009.
        """

        dx = self.dcosx[1] - self.dcosx[0]
        dy = self.dcosy[1] - self.dcosy[0]

        amp = self.norpattern

        xx =  numpy.resize(self.dcosx,(self.nx,self.nx)).transpose()
        yy =  numpy.resize(self.dcosy,(self.ny,self.ny))

        mm0 = amp[numpy.where(amp > 0.5)]
        xx0 = xx[numpy.where(amp > 0.5)]
        yy0 = yy[numpy.where(amp > 0.5)]

        xc = numpy.sum(mm0*xx0)/numpy.sum(mm0)
        yc = numpy.sum(mm0*yy0)/numpy.sum(mm0)
        rc = numpy.sqrt(mm0.size*dx*dy/numpy.pi)

        nnx = numpy.where(numpy.abs(self.dcosx - xc) < rc)
        nny = numpy.where(numpy.abs(self.dcosy - yc) < rc)

        mm1 = amp[numpy.min(nnx):numpy.max(nnx)+1,numpy.min(nny):numpy.max(nny)+1]
        xx1 = self.dcosx[numpy.min(nnx):numpy.max(nnx)+1]
        yy1 = self.dcosy[numpy.min(nny):numpy.max(nny)+1]

        # fitting data into the main beam.
        import gaussfit
        params = gaussfit.fitgaussian(mm1)

        # Tranforming from indexes to axis' values
        xcenter = xx1[0] + (((xx1[xx1.size-1] - xx1[0])/(xx1.size -1))*(params[1]))
        ycenter = yy1[0] + (((yy1[yy1.size-1] - yy1[0])/(yy1.size -1))*(params[2]))
        xwidth  = ((xx1[xx1.size-1] - xx1[0])/(xx1.size-1))*(params[3])*(1/Misc_Routines.CoFactors.d2r)
        ywidth  = ((yy1[yy1.size-1] - yy1[0])/(yy1.size-1))*(params[4])*(1/Misc_Routines.CoFactors.d2r)
        meanwx = (xwidth*ywidth)
        meanpos = numpy.array([xcenter,ycenter])

        #print  'Position: %f %f' %(xcenter,ycenter)
        #print  'Widths:   %f %f' %(xwidth, ywidth)
        #print  'BWHP:     %f' %(2*numpy.sqrt(2*meanwx)*numpy.sqrt(-numpy.log(0.5)))

        self.meanpos = meanpos


class BField():
    def __init__(self,year=None,doy=None,site=1,heights=None,alpha_i=90):
        """
        BField class creates an object to get  the Magnetic  field for a  specific date and
        height(s).

        Parameters
        ----------
        year = A scalar giving the desired year.  If the value is None (default value) then
          the current year will be used.
        doy = A scalar giving the desired day of the year. If the value is None (default va-
          lue) then the current doy will be used.
        site = An integer to choose the geographic coordinates of the place where the magne-
          tic field will be computed. The default value is over Jicamarca (site=1)
        heights = An array giving the heights (km) where the magnetic field will be modeled By default the magnetic field will be computed at 100, 500 and 1000km.
        alpha_i = Angle to interpolate the magnetic field.

        Modification History
        --------------------
        Converted to Object-oriented Programming by Freddy Galindo, ROJ, 07 October 2009.
        """

        tmp = time.localtime()
        if year==None: year = tmp[0]
        if doy==None:  doy = tmp[7]
        self.year = year
        self.doy = doy
        self.site = site
        if heights==None:heights = numpy.array([100,500,1000])
        self.heights = heights
        self.alpha_i = alpha_i

    def getBField(self,maglimits=numpy.array([-7,-7,7,7])):
        """
        getBField models the magnetic field for a different heights in a specific date.

        Parameters
        ----------
        maglimits = An 4-elements array giving ..... The default value is [-7,-7,7,7].

        Return
        ------
        dcos = An 4-dimensional array giving the directional cosines of the magnetic field
          over the desired place.
        alpha = An 3-dimensional array giving the angle of the magnetic field over the desi-
          red place.

        Modification History
        --------------------
        Converted to Python by Freddy R. Galindo, ROJ, 07 October 2009.
        """

        x_ant = numpy.array([1,0,0])
        y_ant = numpy.array([0,1,0])
        z_ant = numpy.array([0,0,1])
        
        if self.site==0:
            title_site = "Magnetic equator"
            coord_site = numpy.array([-76+52./60.,-11+57/60.,0.5])
        elif self.site==1:
            title_site = 'Jicamarca'
            coord_site = [-76-52./60.,-11-57/60.,0.5]
            theta = (45+5.35)*numpy.pi/180.      # (50.35 and 1.46 from Fleish Thesis)
            delta = -1.46*numpy.pi/180

            x_ant1 = numpy.roll(self.rotvector(self.rotvector(x_ant,1,delta),3,theta),1)
            y_ant1 = numpy.roll(self.rotvector(self.rotvector(y_ant,1,delta),3,theta),1)
            z_ant1 = numpy.roll(self.rotvector(self.rotvector(z_ant,1,delta),3,theta),1)

            ang0 = -1*coord_site[0]*numpy.pi/180.
            ang1 = coord_site[1]*numpy.pi/180.
            x_ant = self.rotvector(self.rotvector(x_ant1,2,ang1),3,ang0)
            y_ant = self.rotvector(self.rotvector(y_ant1,2,ang1),3,ang0)
            z_ant = self.rotvector(self.rotvector(z_ant1,2,ang1),3,ang0)
        else:
#            print "No defined Site. Skip..."
            return None

        nhei = self.heights.size
        pt_intercep = numpy.zeros((nhei,2))
        nfields = 1

        grid_res = 0.5
        nlon = int(numpy.int(maglimits[2] - maglimits[0])/grid_res + 1)
        nlat = int(numpy.int(maglimits[3] - maglimits[1])/grid_res + 1)

        location = numpy.zeros((nlon,nlat,2))
        mlon = numpy.atleast_2d(numpy.arange(nlon)*grid_res + maglimits[0])
        mrep = numpy.atleast_2d(numpy.zeros(nlat) + 1)
        location0 = numpy.dot(mlon.transpose(),mrep)

        mlat = numpy.atleast_2d(numpy.arange(nlat)*grid_res + maglimits[1])
        mrep = numpy.atleast_2d(numpy.zeros(nlon) + 1)
        location1 = numpy.dot(mrep.transpose(),mlat)

        location[:,:,0] = location0
        location[:,:,1] = location1

        alpha = numpy.zeros((nlon,nlat,nhei))
        rr = numpy.zeros((nlon,nlat,nhei,3))
        dcos = numpy.zeros((nlon,nlat,nhei,2))

        global first_time

        first_time = None
        for ilon in numpy.arange(nlon):
            for ilat in numpy.arange(nlat):
                outs = self.__bdotk(self.heights,
                                    self.year + self.doy/366.,
                                    coord_site[1],
                                    coord_site[0],
                                    coord_site[2],
                                    coord_site[1]+location[ilon,ilat,1],
                                    location[ilon,ilat,0]*720./180.)

                alpha[ilon, ilat,:] = outs[1]
                rr[ilon, ilat,:,:] = outs[3]

                mrep = numpy.atleast_2d((numpy.zeros(nhei)+1)).transpose()
                tmp = outs[3]*numpy.dot(mrep,numpy.atleast_2d(x_ant))
                tmp = tmp.sum(axis=1)
                dcos[ilon,ilat,:,0] = tmp/numpy.sqrt((outs[3]**2).sum(axis=1))

                mrep = numpy.atleast_2d((numpy.zeros(nhei)+1)).transpose()
                tmp = outs[3]*numpy.dot(mrep,numpy.atleast_2d(y_ant))
                tmp = tmp.sum(axis=1)
                dcos[ilon,ilat,:,1] = tmp/numpy.sqrt((outs[3]**2).sum(axis=1))

        return dcos, alpha, nlon, nlat


    def __bdotk(self,heights,tm,gdlat=-11.95,gdlon=-76.8667,gdalt=0.0,decd=-12.88, ham=-4.61666667):

        global first_time
        # Mean Earth radius in Km WGS 84
        a_igrf = 6371.2

        bk = numpy.zeros(heights.size)
        alpha = numpy.zeros(heights.size)
        bfm = numpy.zeros(heights.size)
        rr = numpy.zeros((heights.size,3))
        rgc = numpy.zeros((heights.size,3))

        ObjGeodetic = Astro_Coords.Geodetic(gdlat,gdalt)
        [gclat,gcalt] = ObjGeodetic.change2geocentric()

        gclat = gclat*numpy.pi/180.
        gclon = gdlon*numpy.pi/180.

        # Antenna position from center of Earth
        ca_vector = [numpy.cos(gclat)*numpy.cos(gclon),numpy.cos(gclat)*numpy.sin(gclon),numpy.sin(gclat)]
        ca_vector = gcalt*numpy.array(ca_vector)

        dec = decd*numpy.pi/180.

        # K  vector respect to the center of earth.
        klon = gclon + ham*numpy.pi/720.
        k_vector = [numpy.cos(dec)*numpy.cos(klon),numpy.cos(dec)*numpy.sin(klon),numpy.sin(dec)]
        k_vector = numpy.array(k_vector)

        for ih in numpy.arange(heights.size):
            # Vector from Earth's center to volume of interest
            rr[ih,:] = k_vector*heights[ih]
            cv_vector = numpy.squeeze(ca_vector) + rr[ih,:]

            cv_gcalt = numpy.sqrt(numpy.sum(cv_vector**2.))
            cvxy = numpy.sqrt(numpy.sum(cv_vector[0:2]**2.))

            radial = cv_vector/cv_gcalt
            east = numpy.array([-1*cv_vector[1],cv_vector[0],0])/cvxy
            comp1 = east[1]*radial[2] - radial[1]*east[2]
            comp2 = east[2]*radial[0] - radial[2]*east[0]
            comp3 = east[0]*radial[1] - radial[0]*east[1]
            north = -1*numpy.array([comp1, comp2, comp3])

            rr_k = cv_vector - numpy.squeeze(ca_vector)
            u_rr = rr_k/numpy.sqrt(numpy.sum(rr_k**2.))

            cv_gclat = numpy.arctan2(cv_vector[2],cvxy)
            cv_gclon = numpy.arctan2(cv_vector[1],cv_vector[0])

            bhei = cv_gcalt-a_igrf
            blat = cv_gclat*180./numpy.pi
            blon = cv_gclon*180./numpy.pi
            bfield = self.__igrfkudeki(bhei,tm,blat,blon)

            B = (bfield[0]*north + bfield[1]*east - bfield[2]*radial)*1.0e-5

            bfm[ih] = numpy.sqrt(numpy.sum(B**2.)) #module
            bk[ih] = numpy.sum(u_rr*B)
            alpha[ih] = numpy.arccos(bk[ih]/bfm[ih])*180/numpy.pi
            rgc[ih,:] = numpy.array([cv_gclon, cv_gclat, cv_gcalt])

        return bk, alpha, bfm, rr, rgc


    def __igrfkudeki(self,heights,time,latitude,longitude,ae=6371.2):
        """
        __igrfkudeki calculates the International Geomagnetic Reference Field for given in-
        put conditions based on IGRF2005 coefficients.

        Parameters
        ----------
        heights = Scalar or vector giving the height above the Earth  of the point in ques-
          tion in kilometers.
        time = Scalar or vector giving the decimal year of time in question (e.g. 1991.2).
        latitude = Latitude of point in question in decimal degrees. Scalar or vector.
        longitude = Longitude of point in question in decimal degrees. Scalar or vector.
        ae =
        first_time =

        Return
        ------
        bn =
        be =
        bd =
        bmod =
        balpha =
        first_time =

        Modification History
        --------------------
        Converted to Python by Freddy R. Galindo, ROJ, 03 October 2009.
        """

        global first_time
        global gs, hs, nvec, mvec, maxcoef

        heights = numpy.atleast_1d(heights)
        time = numpy.atleast_1d(time)
        latitude = numpy.atleast_1d(latitude)
        longitude = numpy.atleast_1d(longitude)

        if numpy.max(latitude)==90:
#            print "Field calculations are not supported at geographic poles"
            pass

        # output arrays
        bn = numpy.zeros(heights.size)
        be = numpy.zeros(heights.size)
        bd = numpy.zeros(heights.size)

        if first_time==None:first_time=0

        time0 = time[0]
        if time!=first_time:
            #print "Getting coefficients for", time0
            [periods,g,h ] = self.__readIGRFcoeff()
            top_year = numpy.max(periods)
            nperiod = (top_year - 1900)/5 + 1

            maxcoef = 10
            if time0>=2000:maxcoef = 12


            # Normalization array for Schmidt fucntions
            multer = numpy.zeros((2+maxcoef,1+maxcoef)) + 1
            for cn in (numpy.arange(maxcoef)+1):
                for rm in (numpy.arange(cn)+1):
                    tmp = numpy.arange(2*rm) + cn - rm + 1.
                    multer[rm+1,cn] = ((-1.)**rm)*numpy.sqrt(2./tmp.prod())

            schmidt = multer[1:,1:].transpose()

            # n and m arrays
            nvec = numpy.atleast_2d(numpy.arange(maxcoef)+2)
            mvec = numpy.atleast_2d(numpy.arange(maxcoef+1)).transpose()

            # Time adjusted igrf g and h with Schmidt normalization
            # IGRF coefficient arrays: g0(n,m), n=1, maxcoeff,m=0, maxcoeff, ...
            if time0<top_year:
                dtime = (time0 - 1900) % 5
                ntime = (time0 - 1900 - dtime)/5
            else:
                # Estimating coefficients for times > top_year
                dtime = (time0 - top_year) + 5
                ntime = g[:,0,0].size - 2

            g0 = g[ntime,1:maxcoef+1,:maxcoef+1]
            h0 = h[ntime,1:maxcoef+1,:maxcoef+1]
            gdot = g[ntime+1,1:maxcoef+1,:maxcoef+1]-g[ntime,1:maxcoef+1,:maxcoef+1]
            hdot = h[ntime+1,1:maxcoef+1,:maxcoef+1]-h[ntime,1:maxcoef+1,:maxcoef+1]
            gs = (g0 + dtime*(gdot/5.))*schmidt[:maxcoef,0:maxcoef+1]
            hs = (h0 + dtime*(hdot/5.))*schmidt[:maxcoef,0:maxcoef+1]

            first_time = time0

        for ii in numpy.arange(heights.size):
            # Height dependence array rad = (ae/(ae+height))**(n+3)
            rad = numpy.atleast_2d((ae/(ae + heights[ii]))**(nvec+1))

            # Sin and Cos of m times longitude phi arrays
            mphi = mvec*longitude[ii]*numpy.pi/180.
            cosmphi = numpy.atleast_2d(numpy.cos(mphi))
            sinmphi = numpy.atleast_2d(numpy.sin(mphi))

            # Cos of colatitude theta
            c = numpy.cos((90 - latitude[ii])*numpy.pi/180.)

            # Legendre functions p(n,m|c)
            [p,dp]= scipy.special.lpmn(maxcoef+1,maxcoef+1,c)
            p = p[:,:-1].transpose()
            s = numpy.sqrt((1. - c)*(1 + c))

            # Generate derivative array dpdtheta = -s*dpdc
            dpdtheta = c*p/s
            for m in numpy.arange(maxcoef+2):    dpdtheta[:,m] = m*dpdtheta[:,m]
            dpdtheta = dpdtheta + numpy.roll(p,-1,axis=1)

            # Extracting arrays required for field calculations
            p = p[1:maxcoef+1,:maxcoef+1]
            dpdtheta = dpdtheta[1:maxcoef+1,:maxcoef+1]

            # Weigh p and dpdtheta with gs and hs coefficients.
            gp = gs*p
            hp = hs*p
            gdpdtheta = gs*dpdtheta
            hdpdtheta = hs*dpdtheta
            # Calcultate field components
            matrix0 = numpy.dot(gdpdtheta,cosmphi)
            matrix1 = numpy.dot(hdpdtheta,sinmphi)
            bn[ii] = numpy.dot(rad,(matrix0 + matrix1))
            matrix0 = numpy.dot(hp,(mvec*cosmphi))
            matrix1 = numpy.dot(gp,(mvec*sinmphi))
            be[ii] = numpy.dot((-1*rad),((matrix0 - matrix1)/s))
            matrix0 = numpy.dot(gp,cosmphi)
            matrix1 = numpy.dot(hp,sinmphi)
            bd[ii] = numpy.dot((-1*nvec*rad),(matrix0 + matrix1))

        bmod = numpy.sqrt(bn**2. + be**2. + bd**2.)
        btheta = numpy.arctan(bd/numpy.sqrt(be**2. + bn**2.))*180/numpy.pi
        balpha = numpy.arctan(be/bn)*180./numpy.pi

        #bn : north
        #be : east
        #bn : radial
        #bmod : module


        return bn, be, bd, bmod, btheta, balpha

    def str2num(self, datum):
        try:
            return int(datum)
        except:
            try:
                return float(datum)
            except:
                return datum

    def __readIGRFfile(self, filename):
        list_years=[]
        for i in range(1,24):
            list_years.append(1895.0 + i*5)

        epochs=list_years
        epochs.append(epochs[-1]+5)
        nepochs = numpy.shape(epochs)

        gg = numpy.zeros((13,14,nepochs[0]),dtype=float)
        hh = numpy.zeros((13,14,nepochs[0]),dtype=float)

        coeffs_file=open(filename)
        lines=coeffs_file.readlines()

        coeffs_file.close()

        for line in lines:
            items = line.split()
            g_h = items[0]
            n = self.str2num(items[1])
            m = self.str2num(items[2])

            coeffs = items[3:]

            for i in range(len(coeffs)-1):
                coeffs[i] = self.str2num(coeffs[i])

            #coeffs = numpy.array(coeffs)
            ncoeffs = numpy.shape(coeffs)[0]

            if g_h == 'g':
    #            print n," g ",m
                gg[n-1,m,:]=coeffs
            elif g_h=='h':
    #            print n," h ",m
                hh[n-1,m,:]=coeffs
    #        else :
    #            continue

    #    Ultimo Reordenamiento para  almacenar .
        gg[:,:,nepochs[0]-1] = gg[:,:,nepochs[0]-2] + 5*gg[:,:,nepochs[0]-1]
        hh[:,:,nepochs[0]-1] = hh[:,:,nepochs[0]-2] + 5*hh[:,:,nepochs[0]-1]

#        return numpy.array([gg,hh])
        periods = numpy.array(epochs)
        g = gg
        h = hh
        return periods, g, h


    def __readIGRFcoeff(self,filename="igrf10coeffs.dat"):
        """
        __readIGRFcoeff reads the coefficients from  a binary file which is located  in the
        folder "resource."

        Parameter
        ---------
        filename = A string to specify the name of the file which contains thec coeffs. The
        default value is "igrf10coeffs.dat"

        Return
        ------
        periods = A lineal array giving...
        g1 =
        h1 =

        Modification History
        --------------------
        Converted to Python by Freddy R. Galindo, ROJ, 03 October 2009.
        """

# #        igrfile = sys.path[-1] + os.sep + "resource" + os.sep + filename
#         igrfile = os.path.join('./resource',filename)
#         f = open(igrfile,'rb')
#         #f = open(os.getcwd() + os.sep + "resource" + os.sep + filename,'rb')
#
#         # Reading SkyNoise Power (lineal scale)
#         periods = numpy.fromfile(f,numpy.dtype([('var','<f4')]),23)
#         periods = periods['var']
#
#         g = numpy.fromfile(f,numpy.dtype([('var','<f8')]),23*14*14)
#         g = g['var'].reshape((14,14,23)).transpose()
#
#         h = numpy.fromfile(f,numpy.dtype([('var','<f8')]),23*14*14)
#         h = h['var'].reshape((14,14,23)).transpose()
#
#         f.close()
        base_path = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(base_path,"resource","igrf11coeffs.txt")

        period_v, g_v, h_v = self.__readIGRFfile(filename)
        g2 = numpy.zeros((14,14,24))
        h2 = numpy.zeros((14,14,24))
        g2[1:14,:,:] = g_v
        h2[1:14,:,:] = h_v

        g = numpy.transpose(g2, (2,0,1))
        h = numpy.transpose(h2, (2,0,1))
        periods = period_v.copy()

        return periods, g, h

    def rotvector(self,vector,axis=1,ang=0):
        """
        rotvector function returns the new vector generated rotating the rectagular coords.

        Parameters
        ----------
        vector = A lineal 3-elements array (x,y,z).
        axis = A integer to specify  the axis used to rotate the coord systems. The default
          value is 1.
            axis = 1 -> Around "x"
            axis = 2 -> Around "y"
            axis = 3 -> Around "z"
        ang = Angle of rotation (in radians). The default value is zero.

        Return
        ------
        rotvector = A lineal array of 3 elements giving the new coordinates.

        Modification History
        --------------------
        Converted to Python by Freddy R. Galindo, ROJ, 01 October 2009.
        """

        if axis==1:
            t = [[1,0,0],[0,numpy.cos(ang),numpy.sin(ang)],[0,-numpy.sin(ang),numpy.cos(ang)]]
        elif axis==2:
            t = [[numpy.cos(ang),0,-numpy.sin(ang)],[0,1,0],[numpy.sin(ang),0,numpy.cos(ang)]]
        elif axis==3:
            t = [[numpy.cos(ang),numpy.sin(ang),0],[-numpy.sin(ang),numpy.cos(ang),0],[0,0,1]]

        rotvector = numpy.array(numpy.dot(numpy.array(t),numpy.array(vector)))

        return rotvector


class overJroShow:

#    __serverdocspath = '/usr/local/www/htdocs'
#    __tmpDir = 'overJro/tempReports'
#     __serverdocspath = '/Users/dsuarez/Pictures'
#     __tmpDir = 'overjro'
    __serverdocspath = ''
    __tmpDir = ''

    def __init__(self, title=''):
        self.year = None
        self.month = None
        self.dom = None
        self.pattern = None
        self.maxphi = None
        self.heights = None
        self.filename = None
        self.showType = None
        self.path = None
        self.objects = None
        self.nptsx = 101
        self.nptsy = 101
        self.fftopt = 0
        self.site = 1
        self.dcosx = 1
        self.dcosy = 1
        self.dcosxrange = None
        self.dcosyrange = None
        self.maxha_min= 0.
        self.show_object = None
        self.dcosx_mag = None
        self.dcosy_mag = None
        self.ha_mag = None
        self.time_mag = None
        self.main_dec = None
        self.ObjC = None
        self.ptitle = title
        self.path4plotname = None
        self.plotname0 = None
        self.plotname1 = None
        self.plotname2 = None
        self.scriptHeaders = 0
        self.glat = -11.95
        self.glon = -76.8667
        self.UT = 5 #timezone

        self.glat = -11.951481
        self.glon = -76.874383
#       self.outputHead('Show Plot')
#        self.printBody()

    def setScriptState(self):
        self.madForm = cgi.FieldStorage()

        if self.madForm.has_key('serverdocspath'):
            self.__serverdocspath = self.madForm.getvalue('serverdocspath')#'/usr/local/www/htdocs'

        if self.madForm.has_key('tmpdir'):
            self.__tmpDir = self.madForm.getvalue('tmpdir')#'overJro/tempReports'

        if self.madForm.has_key('showType'):
            self.showType = int(self.madForm.getvalue('showType'))

        if self.showType == 0 or self.showType == 1:

#             if self.madForm.has_key('year') and \
#                 self.madForm.has_key('month') and \
#                 self.madForm.has_key('dom') and \
#                 self.madForm.has_key('pattern') and \
#                 self.madForm.has_key('maxphi') and \
#                 self.madForm.has_key('objects') and \
#                 self.madForm.has_key('heights'):

            if self.madForm.has_key('year') and \
                self.madForm.has_key('month') and \
                self.madForm.has_key('dom') and \
                self.madForm.has_key('maxphi') and \
                self.madForm.has_key('objects') and \
                self.madForm.has_key('heights'):

                    self.year = int(self.madForm.getvalue('year'))
                    self.month = int(self.madForm.getvalue('month'))
                    self.dom = int(self.madForm.getvalue('dom'))
                    self.maxphi = float(self.madForm.getvalue('maxphi'))

                    if self.madForm.has_key('pattern'):

                        tmp_pattern = self.madForm.getvalue('pattern') #pattern es predifinido en listado o definido por el usuario
                        self.pattern=[]
                        if tmp_pattern[0] == '[':
                            tmp_pattern=tmp_pattern[1:]

                        if tmp_pattern[-1] == ']':
                            tmp_pattern=tmp_pattern[0:len(tmp_pattern)-1]

                        for s in tmp_pattern.split(','):
                            self.pattern.append(float(s))
                    elif self.madForm.has_key('filename'):
                        if self.madForm.has_key('filename'):
                            self.filename = self.madForm.getvalue('filename') # nombre de archivo: patron de radiacion definido por el usuario

                        if self.madForm.has_key('path'):
                            self.path = self.madForm.getvalue('path') #path donde se encuentra el archivo: patron de radiacion del usuario

                    else:
                        print "Content-Type: text/html\n"
                        print '<h3> This cgi plot script was called without the proper arguments.</h3>'
                        print '<p> This is a script used to plot Antenna Cuts over Jicamarca Antenna</p>'
                        print '<p> Required arguments:</p>'
                        print '<p>    pattern - chekbox indicating objects over jicamarca antenna</p>'
                        print '<p> or'
                        print '<p>    filename - The pattern defined by users is a file text'
                        print '<p>    path - folder with pattern files'
                        sys.exit(0)


                    tmp_heights = self.madForm.getvalue('heights')
                    self.heights=[]
                    if tmp_heights[0] == '[':
                        tmp_heights=tmp_heights[1:]

                    if tmp_heights[-1] == ']':
                        tmp_heights=tmp_heights[0:len(tmp_heights)-1]

                    for s in tmp_heights.split(','):
                        self.heights.append(float(s))
                    self.heights = numpy.array(self.heights)

                    tmp_objects = self.madForm.getvalue('objects') #lista con los objetos a graficar en el patron de radiacion
                    self.objects=[]
                    if tmp_objects[0] == '[':
                        tmp_objects=tmp_objects[1:]

                    if tmp_objects[-1] == ']':
                        tmp_objects=tmp_objects[0:len(tmp_objects)-1]

                    for s in tmp_objects.split(','):
                        self.objects.append(int(s))

                    if self.showType == 1:
                        if numpy.sum(self.objects) == 0:
                            if  self.scriptHeaders == 0:
                                print "Content-Type: text/html\n"
                            print '<h3> This cgi plot script was called without the proper arguments.</h3>'
                            print '<p> This is a script used to plot Antenna Cuts over Jicamarca Antenna</p>'
                            print '<p> Required arguments:</p>'
                            print '<p>    objects - chekbox indicating objects over jicamarca antenna</p>'
                            print '<p> Please, options in "Select Object" must be checked'
                            sys.exit(0)

                    #considerar para futura implementacion
                    if self.madForm.has_key('filename'):
                        self.filename = self.madForm.getvalue('filename') # nombre de archivo: patron de radiacion definido por el usuario

                    if self.madForm.has_key('path'):
                        self.path = self.madForm.getvalue('path') #path donde se encuentra el archivo: patron de radiacion del usuario


            else:
                if  self.scriptHeaders == 0:
                    print "Content-Type: text/html\n"

                print '<h3> This cgi plot script was called without the proper arguments.</h3>'
                print '<p> This is a script used to plot Pattern Field and Celestial Objects over Jicamarca Antenna</p>'
                print '<p> Required arguments:</p>'
                print '<p>    year - year of event</p>'
                print '<p>    month - month of event</p>'
                print '<p>    dom - day of month</p>'
                print '<p>    pattern - pattern is defined by "Select an Experiment" list box</p>'
                print '<p>    maxphi - maxphi is defined by "Max Angle" text box</p>'
                print '<p>    objects - objects is a list defined by checkbox in "Select Object"</p>'
                print '<p>    heights - heights is defined by "Heights" text box, for default heights=[100,500,1000]</p>'
                print '<p>    showType - showType is a hidden element for show plot of Pattern&Object or Antenna Cuts or Sky Noise</p>'

                sys.exit(0)

        if self.showType == 2:
            if self.madForm.has_key('year') and \
                self.madForm.has_key('month') and \
                self.madForm.has_key('dom'):

                self.year = int(self.madForm.getvalue('year'))
                self.month = int(self.madForm.getvalue('month'))
                self.dom = int(self.madForm.getvalue('dom'))

            else:
                if  self.scriptHeaders == 0:
                    print "Content-Type: text/html\n"
                print '<h3> This cgi plot script was called without the proper arguments.</h3>'
                print '<p> This is a script used to plot Sky Noise over Jicamarca Antenna</p>'
                print '<p> Required arguments:</p>'
                print '<p>    year - year of event</p>'
                print '<p>    month - month of event</p>'
                print '<p>    dom - day of month</p>'

                sys.exit(0)


    def initParameters1(self):

        gui=1
        if self.pattern==None:
            if gui==1: self.filename = self.filename.split(',')

        pattern = numpy.atleast_1d(self.pattern)
        filename = numpy.atleast_1d(self.filename)

        npatterns = numpy.max(numpy.array([pattern.size,filename.size]))

        self.pattern = numpy.resize(pattern,npatterns)
        self.filename = numpy.resize(filename,npatterns)

        self.doy = datetime.datetime(self.year,self.month,self.dom).timetuple().tm_yday


        if self.objects==None:
            self.objects=numpy.zeros(5)
        else:
            tmp = numpy.atleast_1d(self.objects)
            self.objects = numpy.zeros(5)
            self.objects[0:tmp.size] = tmp

        self.show_object = self.objects

        self.maxha_min = 4*self.maxphi*numpy.sqrt(2)*1.25


        if self.heights==None:
            self.heights = numpy.array([100.,500.,1000.])



        #ROJ geographic coordinates and time zone
        self.glat = -11.95
        self.glon = -76.8667
        self.UT = 5 #timezone

        self.glat = -11.951481
        self.glon = -76.874383


        self.junkjd = TimeTools.Time(self.year,self.month,self.dom).change2julday()
        self.junklst = TimeTools.Julian(self.junkjd).change2lst(longitude=self.glon)

        # Finding RA of observatory for a specific date
        self.ra_obs = self.junklst*Misc_Routines.CoFactors.h2d

    def initParameters(self):

        # Defining plot filenames
        self.path4plotname = os.path.join(self.__serverdocspath,self.__tmpDir)
        self.plotname0 = 'over_jro_0_%i.png'% (time.time()) #plot pattern & objects
        self.plotname1 = 'over_jro_1_%i.png'% (time.time()) #plot antenna cuts
        self.plotname2 = 'over_jro_2_%i.png'% (time.time()) #plot sky noise

        # Defining antenna axes respect to geographic coordinates (See Ochs report).
#        alfa = 1.46*Misc_Routines.CoFactors.d2r
#        theta = 51.01*Misc_Routines.CoFactors.d2r

        alfa = 1.488312*Misc_Routines.CoFactors.d2r
        th = 6.166710 + 45.0
        theta = th*Misc_Routines.CoFactors.d2r

        sina = numpy.sin(alfa)
        cosa = numpy.cos(alfa)
        MT1 = numpy.array([[1,0,0],[0,cosa,-sina],[0,sina,cosa]])
        sinb = numpy.sin(theta)
        cosb = numpy.cos(theta)
        MT2 = numpy.array([[cosb,sinb,0],[-sinb,cosb,0],[0,0,1]])
        self.MT3 = numpy.array(numpy.dot(MT2, MT1)).transpose()

        self.xg = numpy.dot(self.MT3.transpose(),numpy.array([1,0,0]))
        self.yg = numpy.dot(self.MT3.transpose(),numpy.array([0,1,0]))
        self.zg = numpy.dot(self.MT3.transpose(),numpy.array([0,0,1]))    

    def plotPattern2(self, date, phases, gain_tx, gain_rx, ues, just_rx):
        # Plotting Antenna patterns.
        
        self.initParameters()
        self.doy = datetime.datetime(date.year,date.month,date.day).timetuple().tm_yday
        self.junkjd = TimeTools.Time(self.year,self.month,self.dom).change2julday()
        self.junklst = TimeTools.Julian(self.junkjd).change2lst(longitude=self.glon)
        self.ra_obs = self.junklst*Misc_Routines.CoFactors.h2d
        
        date = TimeTools.Time(date.year,date.month,date.day).change2strdate(mode=2)

        mesg = 'Over Jicamarca: ' + date[0]
        
        ObjAnt = JroPattern(pattern=0,
                            filename=None,
                            path=None,
                            nptsx=self.nptsx,
                            nptsy=self.nptsy,
                            #maxphi=self.maxphi,
                            fftopt=self.fftopt,
                            phases=numpy.array(phases),
                            gain_tx=numpy.array(gain_tx),
                            gain_rx=numpy.array(gain_rx),
                            ues=numpy.array(ues),
                            just_rx=just_rx
                            )        
        
        dum = Graphics_OverJro.AntPatternPlot()
        
        dum.contPattern(iplot=0,
                        gpath=self.path4plotname,
                        filename=self.plotname0,
                        mesg=mesg,
                        amp=ObjAnt.norpattern,
                        x=ObjAnt.dcosx,
                        y=ObjAnt.dcosy,
                        getCut=ObjAnt.getcut,
                        title=self.ptitle,
                        save=False)

        
        dum.plotRaDec(gpath=self.path4plotname,
                      filename=self.plotname0,
                      jd=self.junkjd, 
                      ra_obs=self.ra_obs, 
                      xg=self.xg, 
                      yg=self.yg, 
                      x=ObjAnt.dcosx, 
                      y=ObjAnt.dcosy,
                      save=False)

        ObjB = BField(self.year,self.doy,1,self.heights)
        [dcos, alpha, nlon, nlat] = ObjB.getBField()
        
        dum.plotBField('', '',dcos,alpha,nlon,nlat,
                       self.dcosxrange,
                       self.dcosyrange,
                       ObjB.heights,
                       ObjB.alpha_i, 
                       save=False)
        
        return dum.fig


    def plotPattern(self):
        # Plotting Antenna patterns.
        npatterns = numpy.size(self.pattern)

        if npatterns==1:
            if self.pattern[0] == None: npatterns = self.filename.__len__()

        date = TimeTools.Time(self.year,self.month,self.dom).change2strdate(mode=2)

        mesg = 'Over Jicamarca: ' + date[0]

        title = ''

        for ii in numpy.arange(npatterns):
            ObjAnt = JroPattern(pattern=self.pattern[ii],
                                filename=self.filename[ii],
                                path=self.path,
                                nptsx=self.nptsx,
                                nptsy=self.nptsy,
                                maxphi=self.maxphi,
                                fftopt=self.fftopt)

            title += ObjAnt.title
            # Plotting Contour Map
            
            self.path4plotname = '/home/jespinoza/workspace/radarsys/trunk/webapp/apps/abs/static/images'            
            dum = Graphics_OverJro.AntPatternPlot()
            dum.contPattern(iplot=ii,
                                                        gpath=self.path4plotname,
                                                        filename=self.plotname0,
                                                        mesg=mesg,
                                                        amp=ObjAnt.norpattern,
                                                        x=ObjAnt.dcosx,
                                                        y=ObjAnt.dcosy,
                                                        getCut=ObjAnt.getcut,
                                                        title=title)
#                                                         title=ObjAnt.title)
#             self.ptitle = ObjAnt.title

            if ii != (npatterns-1):
                title += '+'


            vect_ant = numpy.array([ObjAnt.meanpos[0],ObjAnt.meanpos[1],numpy.sqrt(1-numpy.sum(ObjAnt.meanpos**2.))])

            vect_geo = numpy.dot(scipy.linalg.inv(self.MT3),vect_ant)

            vect_polar = Misc_Routines.Vector(numpy.array(vect_geo),direction=1).Polar2Rect()

            [ra,dec,ha] = Astro_Coords.AltAz(vect_polar[1],vect_polar[0],self.junkjd).change2equatorial()

            print'Main beam position (HA(min), DEC(degrees)): %f %f'%(ha*4.,dec)

            self.main_dec = dec

        self.ptitle = title

        Graphics_OverJro.AntPatternPlot().plotRaDec(gpath=self.path4plotname,
                                                    filename=self.plotname0,
                                                    jd=self.junkjd, 
                                                    ra_obs=self.ra_obs, 
                                                    xg=self.xg, 
                                                    yg=self.yg, 
                                                    x=ObjAnt.dcosx, 
                                                    y=ObjAnt.dcosy)

        self.dcosx = ObjAnt.dcosx

        self.dcosy = ObjAnt.dcosy

        self.dcosxrange = [numpy.min(self.dcosx),numpy.max(self.dcosx)]

        self.dcosyrange = [numpy.min(self.dcosy),numpy.max(self.dcosy)]

    def plotBfield(self):

        if self.show_object[0]>0:
            # Getting B field
            ObjB = BField(self.year,self.doy,self.site,self.heights)


            [dcos, alpha, nlon, nlat] = ObjB.getBField()

            # Plotting B field.
#            print "Drawing magnetic field over Observatory"

            Obj = Graphics_OverJro.BFieldPlot()

            Obj.plotBField(self.path4plotname,self.plotname0,dcos,alpha,nlon,nlat,self.dcosxrange,self.dcosyrange,ObjB.heights,ObjB.alpha_i)

            if self.show_object[0]>1:

                Bhei = 0

                dcosx = Obj.alpha_location[:,0,Bhei]

                dcosy = Obj.alpha_location[:,1,Bhei]

                vect_ant = [dcosx,dcosy,numpy.sqrt(1.-(dcosx**2. + dcosy**2.))]

                vect_ant = numpy.array(vect_ant)

                vect_geo = numpy.dot(scipy.linalg.inv(self.MT3),vect_ant)

                vect_geo = numpy.array(vect_geo).transpose()

                vect_polar = Misc_Routines.Vector(vect_geo,direction=1).Polar2Rect()

                [ra,dec,ha] = Astro_Coords.AltAz(vect_polar[1,:],vect_polar[0,:],self.junkjd).change2equatorial()

                val = numpy.where(ha>=180)

                if val[0].size>0:ha[val] = ha[val] -360.

                val = numpy.where(numpy.abs(ha)<=self.maxphi)

                if val[0].size>2:

                    self.dcosx_mag = dcosx[val]

                    self.dcosy_mag = dcosy[val]

                    self.ha_mag = ha[val]

                    self.time_mag = 0

    def plotCelestial(self):

        ntod = 24.*16.

        tod = numpy.arange(ntod)/ntod*24.

        [month,dom] = TimeTools.Doy2Date(self.year,self.doy).change2date()

        jd = TimeTools.Time(self.year,month,dom,tod+self.UT).change2julday()

        if numpy.sum(self.show_object[1:]>0)!=0:

            self.ObjC = Graphics_OverJro.CelestialObjectsPlot(jd,self.main_dec,tod,self.maxha_min,self.show_object)

            self.ObjC.drawObject(self.glat,
                            self.glon,
                            self.xg,
                            self.yg,
                            self.dcosxrange,
                            self.dcosyrange,
                            self.path4plotname,
                            self.plotname0)

    def plotAntennaCuts(self):
#        print "Drawing antenna cuts"

        incha = 0.05 # min
        nha = numpy.int32(2*self.maxha_min/incha) + 1.
        newha = numpy.arange(nha)/nha*2.*self.maxha_min - self.maxha_min
        nha_star = numpy.int32(200./incha)
        star_ha = (numpy.arange(nha_star) - (nha_star/2))*nha_star

        #Init ObjCut for PatternCutPlot()
        view_objects = numpy.where(self.show_object>0)
        subplots = len(view_objects[0])
        ObjCut = Graphics_OverJro.PatternCutPlot(subplots)

        for io in (numpy.arange(5)):
            if self.show_object[io]==2:
                if io==0:
                    if self.dcosx_mag.size!=0:
                        dcosx = self.dcosx_mag
                        dcosy = self.dcosy_mag
                        dcosz = 1 - numpy.sqrt(dcosx**2. + dcosy**2.)

                        # Finding rotation of B respec to antenna coords.
                        [mm,bb] = scipy.polyfit(dcosx,dcosy,1)
                        alfa = 0.0
                        theta = -1.*numpy.arctan(mm)
                        sina = numpy.sin(alfa); cosa = numpy.cos(alfa)
                        MT1 = [[1,0,0],[0,cosa,-sina],[0,sina,cosa]]
                        MT1 = numpy.array(MT1)
                        sinb = numpy.sin(theta); cosb = numpy.cos(theta)
                        MT2 = [[cosb,sinb,0],[-sinb,cosb,0],[0,0,1]]
                        MT2 = numpy.array(MT2)
                        MT3_mag = numpy.dot(MT2, MT1)
                        MT3_mag = numpy.array(MT3_mag).transpose()
                        # Getting dcos respec to B coords
                        vector = numpy.array([dcosx,dcosy,dcosz])
                        nvector = numpy.dot(MT3_mag,vector)
                        nvector = numpy.array(nvector).transpose()

##                        print 'Rotation (deg) %f'%(theta/Misc_Routines.CoFactors.d2r)

                        yoffset = numpy.sum(nvector[:,1])/nvector[:,1].size
#                        print 'Dcosyoffset %f'%(yoffset)

                        ha = self.ha_mag*4.
                        time = self.time_mag
                        width_star = 0.1 # half width in minutes
                        otitle = 'B Perp. cut'
#                    else:
#                        print "No B perp. over Observatory"
#
#
                elif io==1:
                    if self.ObjC.dcosx_sun.size!=0:
                        dcosx = self.ObjC.dcosx_sun
                        dcosy = self.ObjC.dcosy_sun
                        ha = self.ObjC.ha_sun*4.0
                        time = self.ObjC.time_sun
                        width_star = 2. # half width in minutes
                        otitle = 'Sun cut'
#                    else:
#                        print "Sun is not passing over Observatory"

                elif io==2:
                    if self.ObjC.dcosx_moon.size!=0:
                        dcosx = self.ObjC.dcosx_moon
                        dcosy = self.ObjC.dcosy_moon
                        ha = self.ObjC.ha_moon*4
                        time = self.ObjC.time_moon
                        m_distance = 404114.6  # distance to the Earth in km
                        m_diameter = 1734.4    # diameter in km.
                        width_star = numpy.arctan(m_distance/m_diameter)
                        width_star = width_star/2./Misc_Routines.CoFactors.d2r*4.
                        otitle = 'Moon cut'
#                    else:
#                        print "Moon is not passing over Observatory"

                elif io==3:
                    if self.ObjC.dcosx_hydra.size!=0:
                        dcosx = self.ObjC.dcosx_hydra
                        dcosy = self.ObjC.dcosy_hydra
                        ha = self.ObjC.ha_hydra*4.
                        time = self.ObjC.time_hydra
                        width_star = 0.25 # half width in minutes
                        otitle = 'Hydra cut'
#                    else:
#                        print "Hydra is not passing over Observatory"

                elif io==4:
                    if self.ObjC.dcosx_galaxy.size!=0:
                        dcosx = self.ObjC.dcosx_galaxy
                        dcosy = self.ObjC.dcosy_galaxy
                        ha = self.ObjC.ha_galaxy*4.
                        time = self.ObjC.time_galaxy
                        width_star = 25. # half width in minutes
                        otitle = 'Galaxy cut'
#                    else:
#                        print "Galaxy center is not passing over Jicamarca"
#
#
                hour = numpy.int32(time)
                mins = numpy.int32((time - hour)*60.)
                secs = numpy.int32(((time - hour)*60. - mins)*60.)

                ObjT = TimeTools.Time(self.year,self.month,self.dom,hour,mins,secs)
                subtitle = ObjT.change2strdate()

                star_cut = numpy.exp(-(star_ha/width_star)**2./2.)

                pol = scipy.polyfit(ha,dcosx,3.)
                polx = numpy.poly1d(pol); newdcosx = polx(newha)
                pol = scipy.polyfit(ha,dcosy,3.)
                poly = numpy.poly1d(pol);newdcosy = poly(newha)

                patterns = []
                for icut in numpy.arange(self.pattern.size):
                    # Getting Antenna cut.
                    Obj = JroPattern(dcosx=newdcosx,
                                        dcosy=newdcosy,
                                        getcut=1,
                                        pattern=self.pattern[icut],
                                        path=self.path,
                                        filename=self.filename[icut])

                    Obj.getPattern()

                    patterns.append(Obj.pattern)


                ObjCut.drawCut(io,
                               patterns,
                               self.pattern.size,
                               newha,
                               otitle,
                               subtitle,
                               self.ptitle)

        ObjCut.saveFig(self.path4plotname,self.plotname1)

    def plotSkyNoise(self):
#       print 'Creating SkyNoise map over Jicamarca'
        dom = self.dom
        month = self.month
        year = self.year

        julian = TimeTools.Time(year,month,dom).change2julday()

        [powr,time, lst] = Astro_Coords.CelestialBodies().skyNoise(julian)

        Graphics_OverJro.SkyNoisePlot([year,month,dom],powr,time,lst).getPlot(self.path4plotname,self.plotname2)


    def outputHead(self,title):
        print "Content-Type: text/html"
        print
        self.scriptHeaders = 1
        print '<html>'
        print '<head>'
        print '\t<title>' + title + '</title>'
        print '<style type="text/css">'
        print 'body'
        print '{'
        print 'background-color:#ffffff;'
        print '}'
        print 'h1'
        print '{'
        print 'color:black;'
        print 'font-size:18px;'
        print 'text-align:center;'
        print '}'
        print 'p'
        print '{'
        print 'font-family:"Arial";'
        print 'font-size:16px;'
        print 'color:black;'
        print '}'
        print '</style>'
#        self.printJavaScript()
        print '</head>'

    def printJavaScript(self):
        print

    def printBody(self):
        print '<body>'
#        print '<h1>Test Input Parms</h1>'
#        for key in self.madForm.keys():
#                #print '<p> name=' + str(key)
#                if type(self.madForm.getvalue(key)) == types.ListType:
#                    for value in self.madForm.getvalue(key):
#                        print '<p> name=' + str(key) + \
#                              ' value=' + value + ''
#                else:
#                    print '<p> name=' + str(key) + \
#                              ' value=' + str(cgi.escape(self.madForm.getvalue(key))) + ''

        print '<form name="form1" method="post" target="showFrame">'
        print '    <div align="center">'
        print '        <table width=98% border="1" cellpadding="1">'
        print '            <tr>'
        print '                <td colspan="2" align="center">'
        if self.showType == 0:
            print '                    <IMG SRC="%s" BORDER="0" >'%(os.path.join(os.sep + self.__tmpDir,self.plotname0))
        if self.showType == 1:
            print '                    <IMG SRC="%s" BORDER="0" >'%(os.path.join(os.sep + self.__tmpDir,self.plotname1))
        if self.showType == 2:
            print '                    <IMG SRC="%s" BORDER="0" >'%(os.path.join(os.sep + self.__tmpDir,self.plotname2))
        print '                </td>'
        print '            </tr>'
        print '        </table>'
        print '    </div>'
        print '</form>'

        print '</body>'
        print '</html>'

    #def execute(self, serverdocspath, tmpdir, currentdate, finalpath, showType=0, maxphi=5.0, objects="[1,1]", heights="[150,500,1000]"):
    def setInputParameters(self, serverpath, currentdate, finalpath, showType=0, maxphi=5.0, objects="[1,1]", heights="[150,500,1000]"):
        self.objects=[]
        self.heights=[]
        #self.__serverdocspath = serverdocspath
        self.__serverdocspath = os.path.split(serverpath)[0]
        #self.__tmpDir = tmpdir
        self.__tmpDir = os.path.split(serverpath)[1]
        self.showType = int(showType)
        self.year = int(currentdate.strftime("%Y")) # Get year of currentdate
        self.month = int(currentdate.strftime("%m")) # Get month of currentdate
        self.dom = int(currentdate.strftime("%d")) # Get day of currentdate
        self.filename = os.path.split(finalpath)[1]
        self.path = os.path.split(finalpath)[0]
        self.maxphi = float(maxphi)

        tmp_objects = (objects.replace("[","")).replace("]","")
        for s in tmp_objects.split(','):
            self.objects.append(int(s))

        tmp_heights = (heights.replace("[","")).replace("]","")
        for s in tmp_heights.split(','):
            self.heights.append(float(s))
        self.heights = numpy.array(self.heights)

    def setupParameters(self):
        self.initParameters()

    def initParametersCGI(self):
        self.setScriptState()
        self.initParameters()

    def execute(self):
        if self.showType == 0 or self.showType == 1:
            self.initParameters1()
            self.plotPattern()

            if numpy.sum(self.show_object>0) != 0:
                self.plotBfield()
                self.plotCelestial()

            if numpy.sum(self.show_object>1) != 0:
                self.plotAntennaCuts()

        if self.showType == 2:
            self.plotSkyNoise()

    def getPlot(self):
        
        return os.path.join(self.__serverdocspath,self.__tmpDir,self.plotname0)


if __name__ == '__main__':

    # Script overJroShow.py
    # This script only calls the init function of the class overJroShow()
    # All work is done by the init function
    
    phases = numpy.array([[2.0,0.0,1.5,1.5,1.0,1.0,1.0,0.5],
            [2.0,2.5,2.5,3.5,0.5,1.0,1.0,1.0],
            [2.5,2.5,1.0,1.0,0.5,0.5,0.5,0.5],
            [1.0,1.0,1.0,1.0,0.5,0.5,0.5,1.0],
            [0.5,0.5,0.5,0.5,0.5,0.0,0.0,0.0],
            [0.5,0.5,1.0,0.5,0.0,0.0,0.0,0.0],
            [0.5,0.5,0.5,1.0,0.0,0.0,0.0,0.0],
            [0.5,0.5,0.5,0.5,0.0,0.0,0.0,0.0]])

    gain_tx = numpy.array([[0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,1,1,1,1],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0]])

    gain_rx = numpy.array([[0,0,0,0,0,0,0,0],
            [0,0,1,0,0,0,0,0],
            [0,0,1,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0]])
    
    jro = overJroShow()
        
    fig = jro.plotPattern2(datetime.datetime.today(),
                           phases=phases, 
                           gain_tx=gain_tx, 
                           gain_rx=gain_rx, 
                           ues=numpy.array([0.0,0.0,0.0,0.0]), 
                           just_rx=0)
    
    fig.savefig('./pat.png')
    
