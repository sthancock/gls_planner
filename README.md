# Lidar Mission Planner
*This code is designed to accompany a paper which is currently in review. The paper link will be added once it is accepted*. The paper describes the design of a constellation of lidar satellites needed to give continuous global coverage: A Global Lidar System (GLS).

A script to estimate the number of lidar satellites with different system characteristics needed to cover the world at a given spatial and temporal resolution. There is one script

    glsPlanner.py

It takes satellite, lidar and data product parameters and then calculates the swath width achievable per satellite and then the number of satellites needed to achieve global coverage within a given timeframe.

Command line options are:

    -h, --help          show this help message and exit
    --A A               Mirror area in m2 Default 0.5 m^2
    --alt H             Satellite altitude in metres Default 400,000 m
    --r RES             Ground resoltuion in metres Default 30m
    --Le LE             Laser efficiency, as a fraction Default 0.08
    --Q Q               Detector efficiency, as a fraction Default 0.45
    --Edet EDET         Amount of energy detected per shot, in Joules\Defaukt
                        0.562*10**-15
    --photDet NPHOTONS  Amount of energy detected per shot, in photons.
                        Overrides Edet Default: Not used
    --waveLen WAVELEN   Laser wavelength in nm default 850 nm
    --Ppay PPAY         Payload power in W Default 240 W
    --cFrac CFRAC       Average cloud cover fraction Default 0.55
    --obsProb OBSPROB   Desired probability of a cloud free observation Default
                        0.8
    --tRes TRES         Time to global coverage in years Default 5 years

The code outputs the number of satellites needed for global coverage for the chosen parameters. An example usage is (in this case using the default parameters and a 15 m ground resolution):

    python3 glsPlanner.py --r 15

Which returns

    This configuration would need 20 satellites to cover the world within 5 years, giving a 80.0 % chance of viewing each point


## A note on input parameters

This tool was developed for lidar mission design. The value for Edet can be found using a lidar signal simulator, such as the [GEDI simulator](https://bitbucket.org/StevenHancock/gedisimulator). Other parameters can be found from satellite and lidar manufacturers. The defaults are based on [GEDI](https://www.sciencedirect.com/science/article/pii/S2666017220300018) and [ICESat-2](https://www.spiedigitallibrary.org/conference-proceedings-of-spie/11151/111510C/ICESat-2-mission-overview-and-early-performance/10.1117/12.2534938.short?SSO=1) and are explained in the accompanying paper (available when review is complete).


## A note on physical limits

The code above includes functions to estimate total laser shot energy, noise rates and instantaneous power. Note that some laser sources are not capable of supporting some of the instantaneous powers required.


