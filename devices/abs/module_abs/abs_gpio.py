"""
This script should run in the abs module embedded system.
It uses gpio class to write or read the pins values.
"""

import sys
import time


try:
#------------------Write-OUT----------------
    #----------------DOWN-------------------
    #GPIO116-PIN37-PC20 (--)
    pin = open("/sys/class/gpio/export","w")
    pin.write(str(116))
    pin.close()
    #GPIO118-PIN39-PC22
    pin = open("/sys/class/gpio/export","w")
    pin.write(str(118))
    pin.close()
    #GPIO120-PIN41-PC24 (++)
    pin = open("/sys/class/gpio/export","w")
    pin.write(str(120))
    pin.close()

    #-----------------UP--------------------
    #GPIO122-PIN43-PC26 (--)
    pin = open("/sys/class/gpio/export","w")
    pin.write(str(122))
    pin.close()
    #GPIO124-PIN45-PC28
    pin = open("/sys/class/gpio/export","w")
    pin.write(str(124))
    pin.close()
    #GPIO126-PIN47-PC30 (++)
    pin = open("/sys/class/gpio/export","w")
    pin.write(str(126))
    pin.close()
    #--------------DIRECTION----------------
    #----------------DOWN-------------------
    pin_direct = open("/sys/class/gpio/gpio116/direction","w")
    pin_direct.write("out")
    pin_direct.close()

    pin_direct = open("/sys/class/gpio/gpio118/direction","w")
    pin_direct.write("out")
    pin_direct.close()

    pin_direct = open("/sys/class/gpio/gpio120/direction","w")
    pin_direct.write("out")
    pin_direct.close()
    #-----------------UP--------------------
    pin_direct = open("/sys/class/gpio/gpio122/direction","w")
    pin_direct.write("out")
    pin_direct.close()

    pin_direct = open("/sys/class/gpio/gpio124/direction","w")
    pin_direct.write("out")
    pin_direct.close()

    pin_direct = open("/sys/class/gpio/gpio126/direction","w")
    pin_direct.write("out")
    pin_direct.close()
#------------------Read-IN------------------
    #----------------DOWN-------------------
    #GPIO86-PIN17-PB22 (--)
    pin = open("/sys/class/gpio/export","w")
    pin.write(str(86))
    pin.close()
    #GPIO88-PIN19-PB24
    pin = open("/sys/class/gpio/export","w")
    pin.write(str(88))
    pin.close()
    #GPIO94-PIN21-PB30 (++)
    pin = open("/sys/class/gpio/export","w")
    pin.write(str(94))
    pin.close()
    #-----------------UP--------------------
    #GPIO84-PIN15-PB20 (--)
    pin = open("/sys/class/gpio/export","w")
    pin.write(str(84))
    pin.close()
    #GPIO82-PIN13-PB18
    pin = open("/sys/class/gpio/export","w")
    pin.write(str(82))
    pin.close()
    #GPIO80-PIN11-PB16 (++)
    pin = open("/sys/class/gpio/export","w")
    pin.write(str(80))
    pin.close()
    #--------------DIRECTION----------------
    #----------------DOWN-------------------
    pin_direct = open("/sys/class/gpio/gpio86/direction","w")
    pin_direct.write("in")
    pin_direct.close()

    pin_direct = open("/sys/class/gpio/gpio88/direction","w")
    pin_direct.write("in")
    pin_direct.close()

    pin_direct = open("/sys/class/gpio/gpio94/direction","w")
    pin_direct.write("in")
    pin_direct.close()
    #-----------------UP--------------------
    pin_direct = open("/sys/class/gpio/gpio84/direction","w")
    pin_direct.write("in")
    pin_direct.close()

    pin_direct = open("/sys/class/gpio/gpio82/direction","w")
    pin_direct.write("in")
    pin_direct.close()

    pin_direct = open("/sys/class/gpio/gpio80/direction","w")
    pin_direct.write("in")
    pin_direct.close()

except:
    pass

def abs_write(address,value):
    try:
       pin_value = open("/sys/class/gpio/gpio"+str(address)+"/value","w")
       pin_value.write(str(value))
       pin_value.close()
       return 1
    except:
       return 0
    #return 1

def abs_read(address):
    try:
        pin_value = open("/sys/class/gpio/gpio"+str(address)+"/value","r")
        valor     = pin_value.read()
        pin_value.close()
        return valor
    except:
        return ""
