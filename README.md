# Lidar Mission Planner
This code is designed to accompany the [Hancock et al (2021)](https://royalsocietypublishing.org/doi/abs/10.1098/rsos.211166) paper. The paper describes the design of a constellation of lidar satellites needed to give continuous global coverage: A Global Lidar System (GLS) and forms part of the UK Space Agency funded Global Lidar Altimetry MISsion (GLAMIS) project.

[Hancock, S., McGrath, C., Lowe, C., Davenport, I. and Woodhouse, I., 2021. Requirements for a global lidar system: spaceborne lidar with wall-to-wall coverage. Royal Society Open Science, 8(12), p.211166.](https://royalsocietypublishing.org/doi/abs/10.1098/rsos.211166)

**AMENDMENT: Note** that Hancock et al (2021) assumed isotropic reflectance from the ground, rather than the more correct Lambertian reflectance. For Lambertian reflectance the returned energy to a detector at nadir is twice that of an isotropic reflector. The code has been modified to represent Lambertian reflectors and so will give an answer double that of the equation in the paper. The swath width equation is now:

$s = \frac{P_{pay} L_{e}}{E_{det}} \frac{A}{\pi h^{2}} Q \rho \tau^{2} \frac{ r^{2} \left(R + h \right)^{\frac{3}{2}}}{R \sqrt{GM}}$

Where $s$ is swath width a lidar satellite can achieve, payload power, $P_{pay}$, laser efficiency, $L_{e}$, detected energy needed, $E_{det}$, altitude, $h$, resolution ,$r$, telescope area, $A$, detector efficiency, $Q$, surface reflectance, $\rho$, and atmospheric transmissivity, $\tau$.



A script to estimate the number of lidar satellites with different system characteristics needed to cover the world at a given spatial and temporal resolution. There is one script

    glsPlanner.py

It takes satellite, lidar and data product parameters and then calculates the swath width achievable per satellite and then the number of satellites needed to achieve global coverage within a given timeframe.

Command line options are:

    -h, --help          show this help message and exit
    --A A               Mirror area in m2 Default 0.5 m^2
    --D D               Instead of A above, mirror diameter can be defined in metres
    --alt H             Satellite altitude in metres Default 400,000 m
    --r RES             Ground resoltuion in metres Default 30m
    --Le LE             Laser efficiency, as a fraction Default 0.08
    --Q Q               Detector efficiency, as a fraction Default 0.45
    --Edet EDET         Amount of energy detected per shot, in Joules\Default
                        0.562*10**-15
    --photDet NPHOTONS  Amount of energy detected per shot, in photons.
                        Overrides Edet Default: Not used
    --waveLen WAVELEN   Laser wavelength in nm default 850 nm
    --Ppay PPAY         Payload power in W Default 240 W
    --cFrac CFRAC       Average cloud cover fraction Default 0.55
    --obsProb OBSPROB   Desired probability of a cloud free observation Default
                        0.8
    --tRes TRES         Time to global coverage in years Default 5 years
    --lat LAT           Latitude Default 0 degrees
    --samp s            Spatial sampling density (0-1). Default 1
    --Psigma PSIGMA     Pulse width in metres Default 5 m
    --optEff OPTEFF     Optical efficienct Default 1
    --pointErr POINTERR Pointing error in degrees Default 0
    --dutyCyc DUTYCYC   Duty cycle as a fraction Default 1



The code outputs the number of satellites needed for global coverage for the chosen parameters, as well as the swath width per satellite. An example usage is (in this case using the default parameters and a 15 m ground resolution):

    python3 glsPlanner.py --r 30

Which returns

    This configuration would need 5 satellites to cover the world within 5 years, giving a 80.0 % chance of viewing each point
    The satellite dwells over each pixel for 4.15 ms
    The total amount of laser energy emitted per pixel must be 9.76 mJ, giving a continuous laser output power of 2.35 W
    The swath width is 383 m made up of 13 ground tracks


### Dead time
Photon-counting detectors offer the potential for low-noise, high sensitivity detection. However they suffer from dead-time, which will distort the signal if photons arrive too close together. This is sometimes called "first photon bias". For this reason systems like ICEsat-2 use an [array detector](https://www.spiedigitallibrary.org/conference-proceedings-of-spie/11151/111510C/ICESat-2-mission-overview-and-early-performance/10.1117/12.2534938.full). In addition to the the energy liimts above it is important to test whether a given detector will be able to measure all signal photon without deadtime effects.

All detectors should have the dead-time specified. That can be put into this script along with the signal to determine probability of the signal being distorted by dead-time.

    checks/checkDeadtime.py

Input options are:

    --nPhotons NPHOTONS  Number of expected signal photons Default 205
    --window WINDOW      Measurement window in metres, eg. tree height Default 20 m
    --deadtime DEADTIME  Pixel deadtime in ns Default 2 ns
    --maxProb MAXPROB    Maximum acceptable probability of missing a photon as a fraction Default 0.02

It outputs the mean number of photons expected within the dead-time, the probability that two or more will arrive within this time and the number of pixels needed to keep the probability of missing a photon less than maxProb.


## A note on input parameters

This tool was developed for lidar mission design. The value for Edet can be found using a lidar signal simulator, such as the [GEDI simulator](https://bitbucket.org/StevenHancock/gedisimulator). Other parameters can be found from satellite and lidar manufacturers. The defaults are based on [GEDI](https://www.sciencedirect.com/science/article/pii/S2666017220300018) and [ICESat-2](https://www.spiedigitallibrary.org/conference-proceedings-of-spie/11151/111510C/ICESat-2-mission-overview-and-early-performance/10.1117/12.2534938.short?SSO=1) and are explained in the accompanying [paper](https://royalsocietypublishing.org/doi/abs/10.1098/rsos.211166).


## A note on physical limits

The code above includes functions to estimate total laser shot energy, noise rates and power peak. Note that some laser sources are not capable of supporting some of the peak powers required.


## Licensing

This code is open-source, under the Gnu Public License.

