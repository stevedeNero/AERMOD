"""
Created on Wed Apr 28 09:04:09 2021
Edited on Dec 28 2021

@author: steven
"""
# =============================================================================
# class UTMCoordinate(object):
#     """
#     Coordinate class to track UTM E and UTM N pairs
#     """
#     def __init__(self, UTME, UTMN)
# =============================================================================

class Source(object):
    """
    A wrapper object for points, flares, volumes, and areas
    """
    def __init__(self, UTME, UTMN, srcType=None):
        """
        initialize the UTM location of source
        """
        self.UTME = UTME
        self.UTMN = UTMN
        self.srcType = srcType
    def get_UTME(self):
        return self.UTME
    def get_UTMN(self):
        return self.UTMN
    def get_UTMs(self):
        return [self.UTME, self.UTMN]
    def get_srcType(self):
        return self.srcType
    def set_UTME(self,UTME):
        self.UTME = float(UTME)
    def set_UTMN(self,UTMN):
        self.UTMN = float(UTMN)
    def set_UTMs(self,UTME,UTMN):
        self.UTME = float(UTME)
        self.UTMN = float(UTMN)
    def set_srcType(self,srcType):
        self.srcType = srcType
        
    def __str__(self):  
        return self.srcType + " Source: [%0.3f, %0.3f]" % (self.UTME, self.UTMN)

# =============================================================================

class Point(Source):
    """
    Point Sources have height, diameter, velocity, and temperature
    - Height in Meters
    - Diameter in Meters
    - Velocity in Meters/Sec
    - Temperature in Kelvin
    """
    def __init__(self, UTME, UTMN, srcType="Point", Hgt=None, Dia=None, Vel=None, Tem=None):
        """
        Initialize the Point Source release parameters
        """
        Source.__init__(self, UTME, UTMN, srcType="Point")
        self.Hgt = Hgt
        self.Dia = Dia
        self.Vel = Vel
        self.Tem = Tem
    def get_Height(self):
        return self.Hgt
    def get_Diameter(self):
        return self.Dia
    def get_Velocity(self):
        return self.Vel
    def get_Temperature(self):
        return self.Tem
    def set_Height(self, Hgt, Units="m"):
        assert Units == "m" or Units == "ft", "Enter Height in units of ft or m"
        if Units == "ft":
            self.Hgt = Hgt * 0.3048
        else:
            self.Hgt = float(Hgt)
    def set_Diameter(self, Dia,Units="m"):
        assert Units == "m" or Units == "ft", "Enter Diameter in units of ft or m"
        if Units == "ft":
            self.Dia = Dia * 0.3048
        else:
            self.Dia = float(Dia)
    def set_Velocity(self, Vel, Units="m/s"):
        assert Units == "m/s" or Units == "ft/s", "Enter Velocity in units of ft/s or m/s"
        if Units == "ft":
            self.Vel = Vel * 0.3048
        else:
            self.Vel = float(Vel        )
    def set_Temperature(self, Tem, Units="K"):
        assert Units == "F" or Units == "K", "Enter Temperature in units of F or K"
        if Units == "ft":
            self.Tem = ((Tem-32)*(5/9))+273.15
        else:
            self.Tem = float(Tem)
    def __str__(self):  
        return self.srcType + " Source: [%0.3f, %0.3f]" % (self.UTME, self.UTMN) \
            + "\n Height (m): " + str(self.Hgt) \
            + "\n Diameter (m): " + str(self.Dia) \
            + "\n Exit Velocity (m/s): " + str(self.Vel) \
            + "\n Exhaust Temp (K): " + str(self.Tem)
            
            # + "\n Height (m): [%0.4f]" % str(self.Hgt) \
            # + "\n Diameter (m): [%0.4f]" % str(self.Dia) \
            # + "\n Exit Velocity (m/s): [%0.4f]" % str(self.Vel) \
            # + "\n Exhaust Temp (K): [%0.4f]" % str(self.Tem)


# =============================================================================

class Flare(Point):
    """
    Flare Sources have pre-established velocity and temperature, and have calculated effective diameter
    - Diameter in Meters
    - Velocity in Meters/Sec
    - Temperature in Kelvin
    """
    def __init__(self, UTME, UTMN, Hgt=None, Dia=None):
        """
        Initialize the Point Source release parameters
        """
        Point.__init__(self, UTME, UTMN)
        self.Vel = 20.00
        self.Tem = 1273.00
    def set_Diameter(self, MW, HeatRate, Units = "cal/sec"):
        assert Units == "MMBtu/hr" or Units == "cal/sec", "Enter Heat Rate in either MMBTU/Hr or cal/sec"
        if Units == "cal/sec":
            Q = HeatRate
        elif Units == "MMBtu/hr":
            Q = HeatRate*(1000000*252/3600)
        Qn = Q*(1-0.048*(MW**0.5)) 
        self.Dia = (0.000001*Qn)**0.5
            
# =============================================================================

class Volume(Source):
    """
    Volume Sources have release height, side length, Initial X Dimension, and Initial Y Dimension
    - Height in Meters
    - Side length in Meters
    - InitX in Meters
    - InitY in Meters
    """
    def __init__(self, UTME, UTMN, srcType="Volume", Hgt=None, SideLen=None, SigY=None, SigZ=None):
        """
        Initialize the Point Source release parameters
        """
        Source.__init__(self, UTME, UTMN, srcType = "Volume")
        self.Hgt = Hgt
        self.SideLen = SideLen
        self.SigY = SigY
        self.SigZ = SigZ
    def get_Height(self):
        return self.Hgt
    def get_SideLength(self):
        return self.SideLen
    def get_InitX(self):
        return self.SigY
    def get_InitY(self):
        return self.SigZ
    def set_Height(self, Hgt, Units="m"):
        assert Units == "m" or Units == "ft", "Enter Height in units of ft or m"
        if Units == "ft":
            self.Hgt = Hgt * 0.3048
        else:
            self.Hgt = float(Hgt)
    def set_SideLength(self, SideLen, Units="m"):
        assert Units == "m" or Units == "ft", "Enter Side Length in units of ft or m"
        if Units == "ft":
            self.SideLen = SideLen * 0.3048
        else:
            self.SideLen = float(SideLen)
    def set_InitX(self, SigY, Units="m"):
        assert Units == "m" or Units == "ft", "Enter Initial X Coeff in units of ft or m"
        if Units == "ft":
            self.SigY = SigY * 0.3048
        else:
            self.SigY = float(SigY)
    def set_InitY(self, SigZ, Units="K"):
        assert Units == "m" or Units == "ft", "Enter Initial Y Coeff in units of ft or m"
        if Units == "ft":
            self.SigZ = SigZ*0.3048
        else:
            self.SigZ = float(SigZ)
    def calc_InitX(self, SideLen, HZType="SV", SrcSep=1):
        HZType = str.upper(HZType)
        assert HZType == "SV" or HZType == "M_Adj" or HZType == "M_Sep", \
            "Enter Type of Volume Source: Single (SV), Multiple Adjacent (M_Adj), or Multiple Separated (M_Sep)"
        assert SrcSep >= 1, "Source Separation must be at LEAST 1. Your Entry Doesnt Make Sense."
        if HZType == "SV":
            self.SigY = SideLen / 4.3
        elif HZType == "M_Adj":
            self.SigY = SideLen / 2.15
        elif HZType == "M_Sep":
            self.SigY = SrcSep * SideLen / 2.15    
    def calc_InitY(self, Hgt, VType="SF", BldHgt=1):
        VType = str.upper(VType)
        assert VType == "SF" or VType == "EA" or VType == "EN", \
            "Enter Type of Volume Source: Surface (SF), Elevated & On/Adjacent to Bldg (EA), or Elevated & Not Adjacent to Bldg (EN)"
        assert BldHgt >= 0, "Need a valid building height"
        if VType == "SF":
            self.SigZ = Hgt / 2.15
        elif VType == "EA":
            self.SigZ = BldHgt / 2.15
        elif VType == "EN":
            self.SigZ = BldHgt / 4.3
    def __str__(self):  
        return self.srcType + " Source: [%0.3f, %0.3f]" % (self.UTME, self.UTMN) \
            + "\n Height (m): " + str(self.Hgt) \
            + "\n Side Length (m): " + str(self.SideLen) \
            + "\n Sigma-Y (m): " + str(self.SigY) \
            + "\n Sigma-Z (m): " + str(self.SigZ) 

# TODO how to get this print statement to round like the UTMs.

           
# =============================================================================

class Area(Source):
    """
    Area Sources have release height, X-length, Y-length, and orientation
    - Height in Meters
    - X-length in Meters
    - Y-length in Meters
    - Orientation in degrees
    """
    def __init__(self, UTME, UTMN, srcType="Volume", Hgt=None, XLen=None, YLen=None, Size=None, Orient=None):
        """
        Initialize the Point Source release parameters
        """
        Source.__init__(self, UTME, UTMN, srcType = "Area")
        self.Hgt = Hgt
        self.XLen = XLen
        self.YLen = YLen
        self.Orient = Orient
        self.Size = Size
    def get_Height(self):
        return self.Hgt
    def get_XLen(self):
        return self.XLen
    def get_YLen(self):
        return self.YLen
    def get_Orient(self):
        return self.Orient
    def set_Height(self, Hgt, Units="m"):
        assert Units == "m" or Units == "ft", "Enter Height in units of ft or m"
        if Units == "ft":
            self.Hgt = Hgt * 0.3048
        else:
            self.Hgt = float(Hgt)
    def set_XLen(self, XLen, Units="m"):
        assert Units == "m" or Units == "ft", "Enter Area X-axis length in units of ft or m"
        if Units == "ft":
            self.XLen = XLen * 0.3048
        else:
            self.XLen = float(XLen)
    def set_YLen(self, YLen, Units="m"):
        assert Units == "m" or Units == "ft", "Enter Area Y-axis length in units of ft or m"
        if Units == "ft":
            self.YLen = YLen * 0.3048
        else:
            self.YLen = float(YLen)
    def set_Orient(self, Orient, Units="deg"):
        assert Units == "deg", "Enter Area Orientation from North in degrees only (deg). Not Radians"
        self.Orient = float(Orient)
    def calc_Size(self):
        if self.XLen is not None and self.YLen is not None: #Could this be cleaner with an "assert" instead?
            self.Size = self.XLen * self.YLen    
    def __str__(self):  
        return self.srcType + " Source: [%0.3f, %0.3f]" % (self.UTME, self.UTMN) \
            + "\n Height (m): " + str(self.Hgt) \
            + "\n X Length (m): " + str(self.XLen) \
            + "\n Y Length (m): " + str(self.YLen) \
            + "\n Footprint Size (m^2): " + str(self.Size) \
            + "\n Orient (deg): " + str(self.Orient) 
