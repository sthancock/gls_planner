

###########################################

'''
A script to calculate the number of lidar satellites needed
to achieve global coverage at a given spatial and temporal
resolution

S Hancock        2021
'''
###########################################


from math import pi,sqrt,log10,floor,log,ceil,cos,tan


###########################################
# read the command line

if __name__ == '__main__':
  import argparse

  def readCommands():
    '''
    Read commandline arguments
    '''
    p = argparse.ArgumentParser(description=("Writes out properties of GEDI waveform files"))
    p.add_argument("--A",dest="A",type=float,default=0.4**2*pi,help=("Mirror area in m2\nDefault 0.5 m^2"))
    p.add_argument("--D",dest="D",type=float,default=-1.0,help=("Telescope diameter in metres, instead of --A above\nDefault is to use area, above"))
    p.add_argument("--alt",dest="h",type=float,default=400000,help=("Satellite altitude in metres\nDefault 400,000 m"))
    p.add_argument("--r",dest="res",type=float,default=30,help=("Ground resoltuion in metres\nDefault 30m"))
    p.add_argument("--Le",dest="Le",type=float,default=0.08,help=("Laser efficiency, as a fraction\nDefault 0.08"))
    p.add_argument("--Q",dest="Q",type=float,default=0.45,help=("Detector efficiency, as a fraction\nDefault 0.45"))
    p.add_argument("--Edet",dest="Edet",type=float,default=0.562*10**-15,help=("Amount of energy detected per shot, in Joules\Default 0.562*10**-15"))
    p.add_argument("--photDet",dest="nPhotons",type=int,default=-1,help=("Amount of energy detected per shot, in photons. Overrides Edet\nDefault: Not used"))
    p.add_argument("--waveLen",dest="waveLen",type=float,default=850,help=("Laser wavelength in nm\ndefault 850 nm"))
    p.add_argument("--Ppay",dest="Ppay",type=float,default=240,help=("Payload power in W\nDefault 240 W"))
    p.add_argument("--cFrac",dest="cFrac",type=float,default=0.55,help=("Average cloud cover fraction\nDefault 0.55"))
    p.add_argument("--tau",dest="tau",type=float,default=0.8,help=("Atmospheric transmission\nnDefault 0.8"))
    p.add_argument("--obsProb",dest="obsProb",type=float,default=0.8,help=("Desired probability of a cloud free observation\nDefault 0.8"))
    p.add_argument("--tRes",dest="tRes",type=float,default=5,help=("Time to global coverage in years\nDefault 5 years"))
    p.add_argument("--lat",dest="lat",type=float,default=0,help=("Latitude\nDefault 0 degrees"))
    p.add_argument("--samp",dest="samp",type=float,default=1.0,help=("Sampling\nDefault 1"))
    p.add_argument("--Psigma",dest="Psigma",type=float,default=5.0,help=("pulse width in metres\nDefault 5 m"))
    p.add_argument("--optEff",dest="optEff",type=float,default=1.0,help=("Optical efficienct\nDefault 1"))
    p.add_argument("--pointErr",dest="pointErr",type=float,default=0.0,help=("Pointing error in degrees\nDefault 0"))
    p.add_argument("--dutyCyc",dest="dutyCyc",type=float,default=1.0,help=("Duty cycle as a fraction\nDefault 1"))
    p.add_argument("--unambiguousRange",dest="unAmbigR",type=float,default=150,help=("Maximum unambigious range \nDefault 150 m"))
    cmdargs = p.parse_args()
    return cmdargs



##################################################

class lidar():
  '''Object to hold lidar parameters'''

  def __init__(self,A=0.5,Edet=0.281*10**-15,Le=0.08,res=30,h=400000,Q=0.45,Ppay=240,samp=1,Psigma=5,optEff=1.0,pointErr=0.0,dutyCyc=1.0,unAmbigR=150,tau=0.8):
    '''Initialiser'''

    # save parameters
    self.A=A
    self.Edet=Edet
    self.Le=Le
    self.r=res
    self.h=h
    self.Q=Q
    self.Ppay=Ppay
    self.samp=samp
    self.optEff=optEff
    self.dutyCyc=dutyCyc

    # Universal constants
    self.rho=0.4
    self.tau=tau
    self.R=6370000
    self.G=6.6726*10**-11
    self.M=5.98*10**24
    self.c=2.998*10**8

    # pulse train properties
    self.unAmbigTime=unAmbigR*2/self.c
    self.Pwidth=Psigma*2/self.c

    # turn pointing error to distance on the ground
    self.geoErr=self.h*tan(pointErr*pi/180)

    return


  #########################

  def nSatsNeeded(self,tRes=5,lat=0):
    '''Number of satellites needed for coverage within a given temporal resolution'''
    # circumference of the Earth at this latitude
    c=2*pi*self.R*cos(lat*pi/180.0)

    # orbits per year per spacecraft
    T=2*pi*sqrt((self.R+self.h)**3/(self.M*self.G))
    pYear=2*pi*10**7/T

    self.nSat=(c/((self.swath-2*self.geoErr)*pYear*tRes)*self.cloudReps)/self.dutyCyc
    self.tRes=tRes
    return

  #########################

  def findSwath(self):
    '''Find satellite swath width'''
    self.swath=(self.Ppay*self.Le/self.Edet)*self.optEff*(self.A/(pi*self.h**2))*self.Q*self.rho*self.tau**2*self.r**2*(self.R+self.h)**1.5/(self.R*sqrt(self.G*self.M))*1//self.samp
    return

  #########################

  def cloudRepeats(self,cFrac=0.55,obsProb=0.8):
    '''Determine nuber of repeats needed for given probability of observation through cloud'''
    self.cloudReps=log(1-obsProb)/log(cFrac)
    self.obsProb=obsProb
    self.cFrac=cFrac
    return

  #########################

  def findDwellT(self):
    '''Find dwell time over a pixel'''
    self.dwellT=self.r*(self.R+self.h)**1.5/(self.R*sqrt(self.G*self.M))
    return


  #########################

  def findEshot(self):
    '''Calculate energy the laser must emit per pixel'''
    self.Eshot=(self.Edet/self.Q)*(pi*self.h**2/self.A)*1.0/(self.rho*self.tau**2)*1/self.optEff
    if(self.unAmbigTime>0.0):
      self.nPulses=self.dwellT/self.unAmbigTime
    else:
      self.nPulses=1
    self.Ppeak=(self.Eshot/self.nPulses)/self.Pwidth
    return

  #########################

  def writeResults(self):
    '''Write results to screen'''

    if(self.nSat>=0):
      print("\n\nThis configuration would need",ceil(self.nSat),"satellites to cover the world within",self.tRes,"years, giving a",round(self.obsProb*100,1),"% chance of viewing each point, with a geolocation accuracy of",round(self.geoErr,2),"m")
    else:
      print("The geolocation accuracy is such that this can never gaurantee global coverage.")
      print("The configuration would need",ceil(self.nSat),"satellites to cover the world within",self.tRes,"years, giving a",round(self.obsProb*100,1),"% chance of viewing each point, with a geolocation accuracy of",round(self.geoErr,2),"m")
    print("The satellite dwells over each pixel for",round(self.dwellT*1000,2),"ms")
    print("Peak power is",round(self.Ppeak,2),"W, with",round(self.nPulses,0),"pulses")
    print("The total amount of laser energy emitted per pixel must be",round(self.Eshot*1000,2),"mJ, giving a continuous laser output power of",round(self.Eshot/self.dwellT,2),"W")
    print("The swath width is",int(self.swath),"m made up of",floor(self.samp*self.swath/self.r),"ground tracks with a sampling of",round(100*self.samp,2),"%")
    print("Mean time between overpasses is",round(self.tRes/self.cloudReps,2),"years")
    print("\n")
    #print("Sanity power",self.Ppay,round(self.Eshot/self.dwellT*floor(self.samp*self.swath/self.r)/self.Le,2))
    #print("With an observation on average once every",round(self.tRes*self.cFrac,2),"years")
    return

##################################################

def photToE(nPhot,lam=850*10**-9):
  '''Convert number of photons to energy in Joules for a given wavelength, lam'''

  h=6.6260755*10**-34
  c=2.998*10**8

  Edet=nPhot*h*c/lam

  return(Edet)


##################################################

def runGLS(A,Edet,Le,res,h,Q,Ppay,samp,Psigma,optEff,pointErr,dutyCyc,cFrac,obsProb,tRes,lat,unAmbigR,tau):
  '''Run everything for ease of learners'''

  # set up structre
  thisLidar=lidar(A=A,Edet=Edet,Le=Le,res=res,h=h,Q=Q,Ppay=Ppay,samp=samp,Psigma=Psigma,optEff=optEff,pointErr=pointErr,dutyCyc=dutyCyc,unAmbigR=unAmbigR,tau=tau)

  # derived values
  thisLidar.findDwellT()
  thisLidar.findEshot()
  thisLidar.findSwath()

  # determine cloud repeats
  thisLidar.cloudRepeats(cFrac=cFrac,obsProb=obsProb)

  # determine number of satellites needed
  thisLidar.nSatsNeeded(tRes=tRes,lat=lat)

  # write results
  thisLidar.writeResults()

  return(thisLidar)


##################################################

if __name__ == "__main__":
  '''Main block'''

  # read command line
  cmd=readCommands()

  # if defined in photons, convert to Joules
  if(cmd.nPhotons>0):
    cmd.Edet=photToE(cmd.nPhotons,lam=cmd.waveLen*10**-9)

  # if defined in telescope diameter, change to area
  if(cmd.D>0.0):
    cmd.A=pi*(cmd.D/2.0)**2

  # set up structre
  thisLidar=lidar(A=cmd.A,Edet=cmd.Edet,Le=cmd.Le,res=cmd.res,h=cmd.h,Q=cmd.Q,Ppay=cmd.Ppay,samp=cmd.samp,Psigma=cmd.Psigma,optEff=cmd.optEff,pointErr=cmd.pointErr,dutyCyc=cmd.dutyCyc,unAmbigR=cmd.unAmbigR,tau=cmd.tau)

  # derived values
  thisLidar.findDwellT()
  thisLidar.findEshot()
  thisLidar.findSwath()

  # determine cloud repeats
  thisLidar.cloudRepeats(cFrac=cmd.cFrac,obsProb=cmd.obsProb)

  # determine number of satellites needed
  thisLidar.nSatsNeeded(tRes=cmd.tRes,lat=cmd.lat)

  # write results
  thisLidar.writeResults()

