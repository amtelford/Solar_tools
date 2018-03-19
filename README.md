# Solar Tools
Tools for various calculations on solar PV systems

* Tool 1: PV_NREL_output_calculator_1_1. This is an application to calculate the monthly output of PV panels given their geographical location (in the US), power rating and area. The user can chose between setups optimised for various seasons in the year.
The tool accounte for typical losses in a PV system (see https://solarcalculator.com.au/solar-panel-output/).
The tool relies on solar irradiance data from the National Renewable Energy Laboratory (NREL), which are imported automatically through the NREL API (https://developer.nrel.gov/docs/solar/solar-resource-v1/).
In order to access these data, the user requires an API key to access solar data from NREL, which can be obtained instantly by registering to their developer website (https://developer.nrel.gov/signup/ ).

* Tool 2: PV_forecast_GUI_1_1. This is an application to calculate AC power output at the inverter in a solar PV installation. It is based on highly accurate forecast models found in the package 'pvlib'. At the moment, the tool uses set PV module and inverter.
Credits and disclaimer: this graphical user interface uses the package 'pvlib' from Sandia National Laboratories, which is distributed under a 3-clause BSD licence. Details can be found ibelow.
----------------------------------------------
Copyright (c) 2013, Sandia National Labs
All rights reserved.
Copyright (c) 2014-2016, PVLIB Python Developers
All rights reserved.
Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:
1.  Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.
2.  Redistributions in binary form must reproduce the above copyright notice, this
  list of conditions and the following disclaimer in the documentation and/or
  other materials provided with the distribution.
3.  Neither the name of the {organization} nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
----------------------------------------------
