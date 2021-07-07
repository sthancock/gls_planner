

###########################################

'''
A script to calculate the number of lidar satellites needed
to achieve global coverage at a given spatial and temporal
resolution

S Hancock        2021
'''
###########################################


from math import pi,sqrt,log10,floor


###########################################
# read the command line

if __name__ == '__main__':
  import argparse

  def readCommands():
    '''
    Read commandline arguments
    '''
    p = argparse.ArgumentParser(description=("Writes out properties of GEDI waveform files"))
    p.add_argument("--A",dest="A",type=float,default=0.4**2*pi,help=("Mirror area in m2"))
    p.add_argument("--h",dest="h",type=float,default=400000,help=("Satellite altitude in metres"))
    cmdargs = p.parse_args()
    return cmdargs



##################################################

class lidar():
  '''Object to hold lidar parameters'''

  def __init__(self,A=0.5,Edet=0.281*10**-15,Le=0.08,maxP=5):
    '''Initialiser'''

    # save parameters
    self.A=A
    self.Edet=Edet
    self.Le=Le
    self.maxP=maxP

    # Universal constants
    self.r=30
    self.h=400000
    self.rho=0.4
    self.tau=0.8
    self.Q=0.45
    self.R=6370000
    self.G=6.6726*10**-11
    self.M=5.98*10**24
    self.c=2.998*10**8

    # pulse parameters
    self.unambigR=150   # unambiguous range

    # derived values
    self.findEshot(self.A)
    self.findDwellT()
    if(maxP>0):
      self.maxP=maxP
    else:
      self.maxP=self.dwellT*self.c/2
    self.findPeakP()
    self.goodness=self.Le/self.Edet

    return


  #########################

  def findPeakP(self):
    '''Find peak power'''

    self.peakP=self.Eshot*self.unambigR/(self.maxP*self.dwellT)

    return


  #########################

  def findDwellT(self):
    '''Find dwell time'''
    self.dwellT=self.r*(self.R+self.h)**1.5/(self.R*sqrt(self.G*self.M))
    return


  #########################

  def findEshot(self,A):
    '''Calculate energy needed per pixel'''

    self.Eshot=(self.Edet/self.Q)*(2*pi*self.h**2/A)*1.0/(self.rho*self.tau**2)

    return


  ########################

  def writeThings(self,lType):
    '''Write out results'''
    print(lType,'peakPower',roundIt(self.peakP),'Eshot',roundIt(self.Eshot),"Edet",roundIt(self.Edet),"Le/Edet",roundIt(self.goodness*10**-15))

    return



##################################################

def roundIt(x):
  '''Round a number to x dp'''
  return(round(x,-int(floor(log10(abs(x)/100)))))
 
##################################################

def photToE(nPhot,lam=850*10**-9):
  '''Convert photons to energy'''

  h=6.6260755*10**-34
  c=2.998*10**8

  Edet=nPhot*h*c/lam

  return(Edet)


##################################################

if __name__ == "__main__":
  '''Main block'''

  # read command line
  cmd=readCommands()

  # constants across setups
  A=cmd.A
  dNoiseRate=400/10**6        # dark count in counts/microsecond
  nNoiserate=0.012-dNoiseRate  # night background light in counts/microsecond for 80 cm telescope


  # solid state
  lSolid=lidar(A=A,Le=0.08,Edet=0.281*10**-15,maxP=400000)
  lSolid.writeThings('Solid')


  # diode-PCL
  lPCL=lidar(A=A,Le=0.25,Edet=photToE(cmd.photPCL),maxP=-1)
  lPCL.writeThings('PCL')


  # diode-train
  lTrain=lidar(A=A,Le=0.25,Edet=photToE(cmd.photTrain),maxP=5)
  lTrain.writeThings('Ptrain')


  totNoise=(A/(0.4**2*pi))*nNoiserate*1/0.03*(lTrain.Q/0.15)+dNoiseRate   #*481000**2/cmd.h**2
  print("tot Noise",roundIt(totNoise),"with repeats",roundIt(totNoise*lTrain.c*lTrain.dwellT/(lTrain.unambigR*2)),'nReps',roundIt(lTrain.c*lTrain.dwellT/(lTrain.unambigR*2)))


