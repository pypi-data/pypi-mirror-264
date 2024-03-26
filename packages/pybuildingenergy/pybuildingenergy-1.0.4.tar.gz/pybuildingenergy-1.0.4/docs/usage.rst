Usage
=====

To use pyBuildingEnergy in a project::

    import pybuildingenergy

The tool allows you to evaluate the performance of buildings in different ways: 

* by running simulations of buildings (archetypes) already preloaded in the archetypes.pickle file for different nations according to Tabula dataset (currently only Italian buildings are available, but buildings from different nations will be loaded), 

  ::

      python3 pybuildingenergy --archetype


Here it is possible, to select two options:
  

  1. Selection of archetype by providing
  
    * information on building type: single_family_house 
    * period of construction: before 1900, 1901-1920,1921-1945,1946-1960,1961-1875,1976-1990,1991-2005,2006-today 
    * location: **latitude** and **longitude**

  2. Demo Building having these features: 

     * single_family_house
     * before 1900,
     * city: Turin
     * lat: 45.071321703968124
     * long: 7.642963669564985
    

* by running best_test600 demo:

  ::

      python3 pybuildingenergy --best_test


* your own building.  For the latter, you can either upload the information from scratch or preload the information from a building archetype and then edit only the information you know.
  