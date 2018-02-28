"""
The module GRAPHICS_OVERJRO.py gathers classes or/and functions to create graphics from OVER-JRO
project (e.g. antenna patterns, skynoise, ...).

MODULES CALLED:
TIME, NUMPY, MATPLOTLIB, TIMETOOLS

MODIFICATION HISTORY:
Created by Ing. Freddy Galindo (frederickgalindo@gmail.com). ROJ Oct 18, 2009.
"""

import time
import numpy
import sys
import os

# set HOME environment variable to a directory the httpd server can write to
#os.environ[ 'HOME' ] = '/usr/local/www/htdocs/overJro/tempReports'
#os.environ[ 'HOME' ] = '/home/dsuarez/Pictures'
#os.environ[ 'HOME' ] = '/tmp/'
import matplotlib
#if ide==1:
#    matplotlib.use('Qt4Agg')
#elif ide==2:
#    matplotlib.use("Agg")
#else:
#    matplotlib.use('TKAgg')
matplotlib.use("Agg")
#matplotlib.interactive(1)
import matplotlib.pyplot
#import Numeric
#import scipy
import scipy.interpolate

import Astro_Coords
import TimeTools
import Graphics_Miscens

import Misc_Routines

class AntPatternPlot:
    def __init__(self):
        """
        AntPatternPlot creates an object to call methods to plot the antenna pattern.

        Modification History
        --------------------
        Created by Freddy Galindo, ROJ, 06 October 2009.
        """
        
        self.fig = matplotlib.pyplot.figure(figsize=(8,8), facecolor='white')
        self.ax = self.fig.add_subplot(111)        

    def contPattern(self,iplot=0,gpath='',filename='',mesg='',amp=None ,x=None ,y=None ,getCut=None,title='', save=True):
        """
        contPattern plots a contour map of the antenna pattern.

        Parameters
        ----------
        iplot = A integer to specify if the plot is  the first, second, ...  The default va-
          lue is 0.

        Examples
        --------
        >> Over_Jro.JroPattern(pattern=2).contPattern()

        Modification history
        --------------------
        Converted to Python by Freddy R. Galindo, ROJ, 06 October 2009.
        """

        if getCut == 1:
            return

        xmax = numpy.max(x)
        xmin = numpy.min(x)
        ymax = numpy.max(y)
        ymin = numpy.min(y)

        levels = numpy.array([1e-3,1e-2,1e-1,0.5,1.0])
        tmp = numpy.round(10*numpy.log10(levels),decimals=1)
        labels = range(5)
        for i in numpy.arange(5):labels[i] = str(numpy.int(tmp[i]))


        colors = ((0,0,1.),(0,170/255.,0),(127/255.,1.,0),(1.,109/255.,0),(128/255.,0,0))
        CS = self.ax.contour(x,y,amp.transpose(),levels,colors=colors)
        fmt = {}
        for l,s in zip(CS.levels,labels):
            fmt[l] = s

        self.ax.annotate('Ng',xy=(-0.05,1.04),xytext=(0.01,0.962),xycoords='axes fraction',arrowprops=dict(facecolor='black', width=1.,shrink=0.2),fontsize=15.)
        self.ax.annotate(mesg,xy=(0,0),xytext=(0.01,0.01),xycoords='figure fraction')
        self.ax.clabel(CS,CS.levels,inline=True,fmt=fmt,fontsize=10)
        self.ax.set_xlim(xmin,xmax)
        self.ax.set_ylim(ymin,ymax)
        self.ax.set_title("Total Pattern: " + title)
        self.ax.set_xlabel("West to South")
        self.ax.set_ylabel("West to North")
        self.ax.grid(True)      
        
        if save:
            save_fig = os.path.join(gpath,filename)
            self.fig.savefig(save_fig,format='png')

        

    def close(self):
        
        matplotlib.pyplot.close(self.fig)

    def plotRaDec(self,gpath=None,filename=None,jd=2452640.5,ra_obs=None,xg=None,yg=None,x=None,y=None, save=True):
        """
        plotRaDec draws right ascension and declination lines on a JRO plane. This function
        must call after conPattern.

        Parameters
        ----------
        jd = A scalar giving the Julian date.
        ra_obs = Scalar giving the right ascension of the observatory.
        xg = A 3-element array to specify ..
        yg = A 3-element array to specify ..

        Examples
        --------
        >> Over_Jro.JroPattern(pattern=2).contPattern()
        >> Over_Jro.JroPattern(pattern=2).plotRaDec(jd=jd,ra_obs=ra_obs,xg=xg,yg=yg)

        Modification history
        --------------------
        Converted to Python by Freddy R. Galindo, ROJ, 06 October 2009.
        """

        # Finding RA of observatory for a specific date
        if ra_obs is None:ra_obs = numpy.array([23.37060849])
        if xg is None:xg = numpy.array([0.62918474,-0.77725579,0.])
        if yg is None:yg = numpy.array([0.77700346,0.62898048,0.02547905])

        # Getting HA and DEC axes
        mindec = -28; maxdec = 4; incdec = 2.
        ndec = numpy.int((maxdec - mindec)/incdec) + 1

        minha = -20; maxha = 20; incha = 2.
        nha = numpy.int((maxha - minha)/incha) + 1

        #mcosx = numpy.zeros((nha,ndec))
        #mcosy = numpy.zeros((nha,ndec))

        ha_axes = numpy.reshape(numpy.arange(nha)*incha + minha,(nha,1))
        ones_dec = numpy.reshape(numpy.zeros(ndec) + 1,(ndec,1))
        ha_axes = numpy.dot(ha_axes,ones_dec.transpose())
        ha_axes2 = numpy.array(ra_obs - ha_axes)

        dec_axes = numpy.reshape(numpy.arange(ndec)*incdec + mindec,(ndec,1))
        ones_ra = numpy.reshape(numpy.zeros(nha) + 1,(nha,1))
        dec_axes = numpy.dot(ones_ra,dec_axes.transpose())
        dec_axes2 = numpy.array(dec_axes)

        ObjHor = Astro_Coords.Equatorial(ha_axes2,dec_axes2,jd)
        [alt,az,ha] = ObjHor.change2AltAz()

        z = numpy.transpose(alt)*Misc_Routines.CoFactors.d2r  ; z = z.flatten()
        az = numpy.transpose(az)*Misc_Routines.CoFactors.d2r  ; az = az.flatten()

        vect = numpy.array([numpy.cos(z)*numpy.sin(az),numpy.cos(z)*numpy.cos(az),numpy.sin(z)])

        xg = numpy.atleast_2d(xg)
        dcosx = numpy.array(numpy.dot(xg,vect))
        yg = numpy.atleast_2d(yg)
        dcosy = numpy.array(numpy.dot(yg,vect))

        mcosx = dcosx.reshape(ndec,nha)
        mcosy = dcosy.reshape(ndec,nha)

        # Defining NAN for points outof limits.
        xmax = numpy.max(x)
        xmin = numpy.min(x)
        ymax = numpy.max(y)
        ymin = numpy.min(y)

        factor = 1.3
        noval = numpy.where((mcosx>(xmax*factor)) | (mcosx<(xmin*factor)))
        if noval[0].size>0:mcosx[noval] = numpy.nan
        noval = numpy.where((mcosy>(ymax*factor)) | (mcosy<(ymin*factor)))
        if noval[0].size>0:mcosy[noval] = numpy.nan

        # Plotting HA and declination grid.
        iha0 = numpy.int((0 - minha)/incha)
        idec0 = numpy.int((-14 - mindec)/incdec)

        colorgrid = (1.,109/255.,0)
        self.ax.plot(mcosx.transpose(),mcosy.transpose(),color=colorgrid,linestyle='--')
        for idec in numpy.arange(ndec):
            if idec != idec0:
                valx = (mcosx[idec,iha0]<=xmax) & (mcosx[idec,iha0]>=xmin)
                valy = (mcosy[idec,iha0]<=ymax) & (mcosy[idec,iha0]>=ymin)
                if valx & valy:
                    text = str(numpy.int(mindec + incdec*idec))+'$^o$'
                    self.ax.text(mcosx[idec,iha0],mcosy[idec,iha0],text)

        matplotlib.pyplot.plot(mcosx,mcosy,color=colorgrid,linestyle='--')
        for iha in numpy.arange(nha):
            if iha != iha0:
                valx = (mcosx[idec0,iha]<=xmax) & (mcosx[idec0,iha]>=xmin)
                valy = (mcosy[idec0,iha]<=ymax) & (mcosy[idec0,iha]>=ymin)
                if valx & valy:
                    text = str(4*numpy.int(minha + incha*iha))+"'"
                    self.ax.text(mcosx[idec0,iha],mcosy[idec0,iha],text)
        
        if save:
            save_fig = os.path.join(gpath,filename)
            matplotlib.pyplot.savefig(save_fig,format='png')


    def plotBField(self,gpath,filename,dcos,alpha, nlon, nlat, dcosxrange, dcosyrange, heights, alpha_i, save=True):
        """
        plotBField draws the magnetic field in a directional cosines plot.

        Parameters
        ----------
        dcos = An 4-dimensional array giving the directional cosines of the magnetic field
          over the desired place.
        alpha = An 3-dimensional array giving the angle of the magnetic field over the desi-
          red place.
        nlon = An integer to specify the number of elements per longitude.
        nlat = An integer to specify the number of elements per latitude.
        dcosxrange = A 2-element array giving the range of the  directional cosines  in the
          "x" axis.
        dcosyrange = A 2-element array giving the range of the  directional cosines  in the
          "y" axis.
        heights = An array giving the heights (km) where the magnetic field will be modeled               By default the magnetic field will be computed at 100, 500 and 1000km.
        alpha_i = Angle to interpolate the magnetic field.
        Modification History
        --------------------
        Converted to Python by Freddy R. Galindo, ROJ, 07 October 2009.
        """

        handles = []
        objects = []
        colors = ['k','m','c','b','g','r','y']
        marker = ['-+','-*','-D','-x','-s','->','-o','-^']

        alpha_location = numpy.zeros((nlon,2,heights.size))

        for ih in numpy.arange(heights.size):
            alpha_location[:,0,ih] = dcos[:,0,ih,0]
            for ilon in numpy.arange(nlon):
                myx = (alpha[ilon,:,ih])[::-1]
                myy = (dcos[ilon,:,ih,0])[::-1]
                tck = scipy.interpolate.splrep(myx,myy,s=0)
                mydcosx = scipy.interpolate.splev(alpha_i,tck,der=0)

                myx = (alpha[ilon,:,ih])[::-1]
                myy = (dcos[ilon,:,ih,1])[::-1]
                tck = scipy.interpolate.splrep(myx,myy,s=0)
                mydcosy = scipy.interpolate.splev(alpha_i,tck,der=0)
                alpha_location[ilon,:,ih] = numpy.array([mydcosx, mydcosy])


            ObjFig, = self.ax.plot(alpha_location[:,0,ih],alpha_location[:,1,ih],
                marker[ih % 8],color=colors[numpy.int(ih/8)],ms=4.5,lw=0.5)
            handles.append(ObjFig)
            objects.append(numpy.str(heights[ih]) + ' km')        

        self.ax.legend(handles,objects,loc="lower right", numpoints=1, handlelength=0.3,
                       handletextpad=0.02, borderpad=0.3, labelspacing=0.1)                

        if save:
            save_fig = os.path.join(gpath,filename)
            matplotlib.pyplot.savefig(save_fig,format='png')
        


class BFieldPlot:
    def __init__(self):
        """
        BFieldPlot creates an object for drawing magnetic Field lines over Jicamarca.

        Modification History
        --------------------
        Created by Freddy Galindo, ROJ, 07 October 2009.
        """

        self.alpha_location = 1
#        pass

    def plotBField(self,gpath,filename,dcos,alpha, nlon, nlat, dcosxrange, dcosyrange, heights, alpha_i):
        """
        plotBField draws the magnetic field in a directional cosines plot.

        Parameters
        ----------
        dcos = An 4-dimensional array giving the directional cosines of the magnetic field
          over the desired place.
        alpha = An 3-dimensional array giving the angle of the magnetic field over the desi-
          red place.
        nlon = An integer to specify the number of elements per longitude.
        nlat = An integer to specify the number of elements per latitude.
        dcosxrange = A 2-element array giving the range of the  directional cosines  in the
          "x" axis.
        dcosyrange = A 2-element array giving the range of the  directional cosines  in the
          "y" axis.
        heights = An array giving the heights (km) where the magnetic field will be modeled               By default the magnetic field will be computed at 100, 500 and 1000km.
        alpha_i = Angle to interpolate the magnetic field.
        Modification History
        --------------------
        Converted to Python by Freddy R. Galindo, ROJ, 07 October 2009.
        """

        handles = []
        objects = []
        colors = ['k','m','c','b','g','r','y']
        marker = ['-+','-*','-D','-x','-s','->','-o','-^']

        alpha_location = numpy.zeros((nlon,2,heights.size))

        for ih in numpy.arange(heights.size):
            alpha_location[:,0,ih] = dcos[:,0,ih,0]
            for ilon in numpy.arange(nlon):
                myx = (alpha[ilon,:,ih])[::-1]
                myy = (dcos[ilon,:,ih,0])[::-1]
                tck = scipy.interpolate.splrep(myx,myy,s=0)
                mydcosx = scipy.interpolate.splev(alpha_i,tck,der=0)

                myx = (alpha[ilon,:,ih])[::-1]
                myy = (dcos[ilon,:,ih,1])[::-1]
                tck = scipy.interpolate.splrep(myx,myy,s=0)
                mydcosy = scipy.interpolate.splev(alpha_i,tck,der=0)
                alpha_location[ilon,:,ih] = numpy.array([mydcosx, mydcosy])


            ObjFig, = matplotlib.pyplot.plot(alpha_location[:,0,ih],alpha_location[:,1,ih], \
                marker[ih % 8],color=colors[numpy.int(ih/8)],ms=4.5,lw=0.5)
            handles.append(ObjFig)
            objects.append(numpy.str(heights[ih]) + ' km')

        matplotlib.pyplot.xlim(dcosxrange[0],dcosxrange[1])
        matplotlib.pyplot.ylim(dcosyrange[0],dcosyrange[1])

        try:
            ObjlegB = matplotlib.pyplot.legend(handles,objects,loc="lower right", numpoints=1, handlelength=0.3, \
                                handletextpad=0.02, borderpad=0.3, labelspacing=0.1)
        except:
            ObjlegB = matplotlib.pyplot.legend(handles,objects,loc=[0.01,0.75], numpoints=1, handlelength=0, \
            pad=0.015, handletextsep=0.02,labelsep=0.01)

        matplotlib.pyplot.setp(ObjlegB.get_texts(),fontsize='small')
        matplotlib.pyplot.gca().add_artist(ObjlegB)

        save_fig = os.path.join(gpath,filename)
        matplotlib.pyplot.savefig(save_fig,format='png')
        self.alpha_location = alpha_location


class CelestialObjectsPlot:
    def __init__(self,jd,dec,tod,maxha_min,show_object=None):

        self.jd = jd
        self.dec = dec
        self.tod = tod
        self.maxha_min = maxha_min

        if show_object==None:show_object=numpy.zeros(4)+2
        self.show_object = show_object

        self.dcosx_sun = 1
        self.dcosy_sun = 1
        self.ha_sun = 1
        self.time_sun = 1

        self.dcosx_moon = 1
        self.dcosy_moon = 1
        self.ha_moon = 1
        self.time_moon = 1

        self.dcosx_hydra = 1
        self.dcosy_hydra = 1
        self.ha_hydra = 1
        self.time_hydra = 1

        self.dcosx_galaxy = 1
        self.dcosy_galaxy = 1
        self.ha_galaxy = 1
        self.time_galaxy = 1

    def drawObject(self,glat,glon,xg,yg,dcosxrange,dcosyrange,gpath='',filename=''):

        jd = self.jd
        main_dec = self.dec
        tod = self.tod
        maxha_min = self.maxha_min

        mesg = "Drawing celestial objects over Observatory"
#        print mesg
#        if textid!=None:textid.append(mesg)

        maxlev = 24; minlev = 0; maxcol = 39; mincol = 10
        handles = []
        objects = ['$Sun$','$Moon$','$Hydra$','$Galaxy$']
        marker = ['--^','--s','--*','--o']

        # Getting RGB table to plot celestial object over Jicamarca
        colortable = Graphics_Miscens.ColorTable(table=1).readTable()

        for io in (numpy.arange(4)+1):
            if self.show_object[io]!=0:
                ObjBodies = Astro_Coords.CelestialBodies()
                if io==1:
                    [ra,dec,sunlon,sunobliq] = ObjBodies.sunpos(jd)
                elif io==2:
                    [ra,dec,dist,moonlon,moonlat] = ObjBodies.moonpos(jd)
                elif io==3:
                    [ra,dec] = ObjBodies.hydrapos()
                elif io==4:
                    [maxra,ra] = ObjBodies.skynoise_jro(dec_cut=main_dec)
                    ra = maxra*15.
                    dec = main_dec

                ObjEq = Astro_Coords.Equatorial(ra,dec,jd,lat=glat,lon=glon)
                [alt, az, ha] = ObjEq.change2AltAz()
                vect = numpy.array([az,alt]).transpose()
                vect = Misc_Routines.Vector(vect,direction=0).Polar2Rect()

                dcosx = numpy.array(numpy.dot(vect,xg))
                dcosy = numpy.array(numpy.dot(vect,yg))
                wrap = numpy.where(ha>=180.)
                if wrap[0].size>0:ha[wrap] = ha[wrap] - 360.

                val = numpy.where((numpy.abs(ha))<=(maxha_min*0.25))
                if val[0].size>2:
                    tod_1 = tod*1.
                    shift_1 = numpy.where(tod>12.)
                    tod_1[shift_1] = tod_1[shift_1] - 24.
                    tod_2 = tod*1.
                    shift_2 = numpy.where(tod<12.)
                    tod_2[shift_2] = tod_2[shift_2] + 24.

                    diff0 = numpy.nanmax(tod[val])  -  numpy.nanmin(tod[val])
                    diff1 = numpy.nanmax(tod_1[val]) - numpy.nanmin(tod_1[val])
                    diff2 = numpy.nanmax(tod_2[val]) - numpy.nanmin(tod_2[val])

                    if ((diff0<=diff1) & (diff0<=diff2)):
                        tod_0 = tod
                    elif ((diff1<diff0) & (diff1<diff2)):
                        tod_0 = tod_1
                    else:
                        tod_0 = tod_2

                    if io==1:
                        self.dcosx_sun = dcosx[val]
                        self.dcosy_sun = dcosy[val]
                        self.ha_sun = ha[val]
                        self.time_sun = numpy.median(tod_0[val])
                    elif io==2:
                        self.dcosx_moon = dcosx[val]
                        self.dcosy_moon = dcosy[val]
                        self.ha_moon = ha[val]
                        self.time_moon = numpy.median(tod_0[val])
                    elif io==3:
                        self.dcosx_hydra = dcosx[val]
                        self.dcosy_hydra = dcosy[val]
                        self.ha_hydra = ha[val]
                        self.time_hydra = numpy.mean(tod_0[val])
                    elif io==4:
                        self.dcosx_galaxy = dcosx[val]
                        self.dcosy_galaxy = dcosy[val]
                        self.ha_galaxy = ha[val]
                        self.time_galaxy = numpy.mean(tod_0[val])

                    index = numpy.mean(tod_0[val]) - minlev
                    index = (index*(maxcol - mincol)/(maxlev - minlev)) + mincol
                    index = numpy.int(index)
                    figobjects, = matplotlib.pyplot.plot(dcosx[val],dcosy[val],marker[io-1],\
                      lw=1,ms=7,mew=0,color=tuple(colortable[:,index]))
                    handles.append(figobjects)

        xmax = numpy.max(dcosxrange[1])
        xmin = numpy.min(dcosxrange[0])
        ymax = numpy.max(dcosyrange[1])
        ymin = numpy.min(dcosyrange[0])
        matplotlib.pyplot.xlim(xmin,xmax)
        matplotlib.pyplot.ylim(ymin,ymax)

        val = numpy.where(self.show_object[1:]>0)
        objects = numpy.array(objects)
        objects = list(objects[val])
        try:
            ObjlegC = matplotlib.pyplot.legend(handles,objects,loc="lower left", numpoints=1, handlelength=0.3, \
            borderpad=0.3, handletextpad=0.02,labelspacing=0.1)
        except:
            ObjlegC = matplotlib.pyplot.legend(handles,objects,loc=[0.01,0.75], numpoints=1, handlelength=0, \
            pad=0.015, handletextsep=0.02,labelsep=0.01)

        matplotlib.pyplot.setp(ObjlegC.get_texts(),fontsize='small')
        ObjlegC.isaxes = False
        save_fig = os.path.join(gpath,filename)
        matplotlib.pyplot.savefig(save_fig,format='png')


class PatternCutPlot:
    def __init__(self,nsubplots):
        self.nsubplots = nsubplots

        self.fig = None

        self.__plot_width  = 8

        if self.nsubplots == 5:
            self.__plot_height = 11

        if self.nsubplots == 4:
            self.__plot_height = 9

        if self.nsubplots == 3:
            self.__plot_height = 7

        if self.nsubplots == 2:
            self.__plot_height = 5

        if self.nsubplots == 1:
            self.__plot_height = 3

        self.fig = matplotlib.pyplot.figure(num = 4,figsize = (self.__plot_width, self.__plot_height))

        if self.nsubplots < 5:
            self.__height_inch = 1.1 #altura de los subplots (pulgadas)
            top_inch = 1.5/2.7 #espacio entre el primer subplot y el limite superior del plot
            self.__vspace_plot_inch = 1.0#1.5/2 # espacio vertical entre subplots
            self.__left = 0.1
        else:
            self.__height_inch = 1.1 #altura de los subplots (pulgadas)
            top_inch = 1.5/2.7 #espacio entre el primer subplot y el limite superior del plot
            self.__vspace_plot_inch = 1.0 # espacio vertical entre subplots
            self.__left = 0.1

        self.__bottom_inch = self.__plot_height - (self.__height_inch + top_inch)
        self.__height = self.__height_inch/self.__plot_height

        self.__width = 0.8


    def drawCut(self,io,patterns,npatterns,ha,otitle,subtitle,ptitle):

        t_cuts = ['B','Sun','Moon','Hydra','Galaxy']
        self.__bottom = self.__bottom_inch/self.__plot_height


        subp = self.fig.add_axes([self.__left,self.__bottom,self.__width,self.__height])

        on_axis_angle = -4.65562
        for icut in numpy.arange(npatterns):
            # Getting Antenna cut.
            pattern = patterns[icut]
            power = numpy.abs(pattern/numpy.nanmax(pattern))
            max_power_db = numpy.round(10.*numpy.log10(numpy.nanmax(pattern)),2)

            bval = numpy.where(power[:,0]==numpy.nanmax(power))
            beta = -0.25*(ha[bval[0]] + on_axis_angle)
#            print 'Angle (deg): '+"%f"%(beta)

            subp.plot(ha,power)


        xmax = numpy.max(numpy.nanmin(ha))
        xmin = numpy.min(numpy.nanmax(ha))
        ymax = numpy.max(1)
        ymin = numpy.min(0)


        subp.set_xlim(xmin, xmax)

        subp.set_ylim(ymin, ymax)

        subp.set_title(otitle + ' ' + ptitle,size="medium")

        subp.text(0.5, 1.26,subtitle[0],
         horizontalalignment='center',
         verticalalignment='center',
         transform = subp.transAxes)

        xlabels = subp.get_xticks()

        subp.set_xticklabels(xlabels,size="small")

        ylabels = subp.get_yticks()

        subp.set_yticklabels(ylabels,size="small")

        subp.set_xlabel('Hour angle (min) (+ve to West)',size="small")

        subp.set_ylabel("Power [Max: " + str(max_power_db) + ' dB]',size="small")

        subp.grid()


        self.__bottom_inch = self.__bottom_inch - (self.__height_inch + self.__vspace_plot_inch)


class SkyNoisePlot:
    def __init__(self,date,powr,time,time_lst):
        """
        SkyNoisePlot class creates an object which represents the SkyNoise Object to genera-
        te a SkyNoise map.

        Parameters
        ----------
        date = A List of 3 elements to define the desired date ([year, month, day]).
        powr = An array giving the SkyNoise power for the desired time.
        time = An array giving the number of seconds since 1970 to the desired time.
        time_lst = Set this input to an array to define the Local Sidereal Time of the desi-
          red time.

        Modification History
        --------------------
        Created by Freddy Galindo, ROJ, 18 October 2009.
        """

        self.date = date
        self.powr = powr
        self.time = time
        self.time_lst = time_lst
