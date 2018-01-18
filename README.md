# Solar Tools
Tools for various calculations on solar PV systems

* Tool 1: PV_output_calculator_1_1. This is an application to calculate the monthly output of PV panels given their geographical location (in the US), power rating and area. The user can chose between setups optimised for various seasons in the year.
The tool accounte for typical losses in a PV system (see https://solarcalculator.com.au/solar-panel-output/).
The tool relies on solar irradiance data from the National Renewable Energy Laboratory (NREL), which are imported automatically through the NREL API (https://developer.nrel.gov/docs/solar/solar-resource-v1/).
In order to access these data, the user requires an API key to access solar data from NREL, which can be obtained instantly by registering to their developer website (https://developer.nrel.gov/signup/ ).

* Tool 2: PV_forecast_GUI_1_0. This is an application to calculate AC power output at the inverter in a solar PV installation. It is based on highly accurate forecast models found in the package 'pvlib'.
Credits and disclaimer: this graphical user interface uses the package 'pvlib' from Sandia National Laboratories, which is distributed under a 3-clause BSD licence. Details can be found in the 'LICENCE' file of this repository.
