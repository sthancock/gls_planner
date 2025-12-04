
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
  deadtime=cmd.deadtime*10**-9  # convert to seconds

  # intermediate parameters
  mu=window/nPhotons            # distribtion mean. It's a Poisson so stdev=mu
  expected=deadtime/mu   # the expected number of photons within the deadtime
  probProblem=poisson.cdf(1,expected)  # probability of more than 1 photon arriving within deadtime

  print('We expect',round(expected,1),'photons to arrive within the deadtime')
  print('The probability of not being affected by deadtime is',round(probProblem*100,2),'%')

