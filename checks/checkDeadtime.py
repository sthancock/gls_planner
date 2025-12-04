
'''
Work out the size of an array needed
to give a short effective-dead time
'''

from scipy.constants import c
from scipy.stats import norm,poisson
import argparse


##########################################

def readCommands():
  '''
  Read commandline arguments
  '''
  p = argparse.ArgumentParser(description=("Gives probability of not detecting all photons for a given detector dead-time and signal rate"))
  p.add_argument("--nPhotons",dest="nPhotons",type=int,default=205,help=("Number of expected signal photons per laser shot\nDefault 205"))
  p.add_argument("--window",dest="window",type=float,default=20,help=("Measurement window in metres, eg. tree height\nDefault 20 m"))
  p.add_argument("--deadtime",dest="deadtime",type=float,default=2,help=("Pixel deadtime in ns\nDefault 2 ns"))
  p.add_argument("--maxProb",dest="maxProb",type=float,default=0.02,help=("Maximum acceptable probability of missing a photon as a fraction\nDefault 0.02"))
  cmdargs = p.parse_args()
  return cmdargs


##########################################

def howManyPix(expected,maxProb):
  '''Find how many pixels are needed to give less than a prob'''

  nPix=1
  while((1-poisson.cdf(1,expected/nPix))>=maxProb):
    nPix+=1

  return(nPix)


##########################################

if __name__ == '__main__':
  '''Main block'''

  # read the command line and set parameters
  cmd=readCommands()
  nPhotons=cmd.nPhotons
  window=cmd.window*2/c         # convert to two way time
  deadtime=cmd.deadtime*10**-9  # convert to seconds

  # intermediate parameters
  mu=window/nPhotons            # distribtion mean. It's a Poisson so stdev=mu
  expected=deadtime/mu   # the expected number of photons within the deadtime
  probProblem=1-poisson.cdf(1,expected)  # probability of more than 1 photon arriving within deadtime

  print('\n')
  print(round(expected,4),'photons are expected to arrive within the deadtime')
  print(round(probProblem*100,3),'% is the probability of a single detector being affected by deadtime')

  # determine how many pixels needed to give less than a certain probability of failure
  nPix=howManyPix(expected,cmd.maxProb)
  print(nPix,'pixels are needed to ensure no more than a',round(cmd.maxProb*100,1),'% chance of missing a photon for a per-pixel deadtime of',round(cmd.deadtime,2),'ns\n')

