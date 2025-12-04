
'''
Work out the size of an array needed
to give a short effective-dead time
'''

from scipy.constants import c
from scipy.stats import norm
import argparse


##########################################

def readCommands():
  '''
  Read commandline arguments
  '''
  p = argparse.ArgumentParser(description=("Gives probability of detecting all photons for different pixel numbers for a given detector dead-time and signal rate"))
  p.add_argument("--nPhotons",dest="nPhotons",type=int,default=205,help=("Number of expected signal photons\nDefault 205"))
  p.add_argument("--window",dest="window",type=float,default=20,help=("Measurement window in metres, eg. tree height\nDefault 20 m"))
  p.add_argument("--deadtime",dest="deadtime",type=float,default=2,help=("Pixel deadtime in ns\nDefault 2 ns"))
  cmdargs = p.parse_args()
  return cmdargs


##########################################

if __name__ == '__main__':
  '''Main block'''

  # read the command line and set parameters
  cmd=readCommands()
  nPhotons=cmd.nPhotons
  window=cmd.window*2/c         # convert to two way time
  mu=window/nPhotons            # distribtion mean. It's a Poisson so stdev=mu
  deadtime=cmd.deadtime*10**-9  # convert to seconds



  meanSep=window/nPhotons
  probDeadPer=norm.cdf((deadtime-mu)/mu)

  # loop over number of pixels
  for nPix in range(1,100):
    probDeadArr=1-nPhotons*probDeadPer/nPix**2   # probability that no two photons are within the dead time of each other on the same pixel
    print(nPix,'ProbArrive',round(probDeadPer,4),'probAll',round(probDeadArr,2))

