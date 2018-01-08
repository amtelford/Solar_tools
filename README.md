# Solar Tools
Tools for various calculations on solar PV systems

* Tool 1: PV_output_calculator_1_0. This is a simple application to calculate the monthly output of PV panels given their geographical location (in the US), power rating and area. The user can chose between setups optimised for various seasons in the year.
The tool accounte for typical losses in a PV system (see https://solarcalculator.com.au/solar-panel-output/).
The tool relies on solar irradiance data from the National Renewable Energy Laboratory (NREL), which are imported automatically (https://developer.nrel.gov/docs/solar/solar-resource-v1/).
In order to access these data, the user requires an API key to access solar data from NREL, which can be obtained instantly by registering to their developer website (https://developer.nrel.gov/signup/ ).
