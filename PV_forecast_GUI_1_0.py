# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 15:47:54 2018

@author: Andrew M Telford

"""

##-----------------------------------------------------------------------------
## 1. SETUP
##-----------------------------------------------------------------------------
## built-in python modules
import datetime
## scientific python add-ons
import pandas as pd
## plotting 
import matplotlib.pyplot as plt
## pvlib library (tools from Sandia National Laboratories)
from pvlib.forecast import GFS
## GUI builder
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

##-----------------------------------------------------------------------------
## 2. LOAD IRRADIANCE FORECAST DATA
##-----------------------------------------------------------------------------
def irr_forecast(model, days=7, lat=-33.865143, long=151.209900, tz='Australia/Sydney',
                   surf_tilt=33.865143, surf_azm=0, albedo=0.2):
    ## Define times.
    start = pd.Timestamp(datetime.date.today(), 
						 tz=tz) ## today's date
    end = start + pd.Timedelta(days=days) ## 7 days from today
    ## Define forecast model, e.g. GFS
    ## Retrieve data
    forecast_data = model.get_processed_data(lat, long, start, end)
    return (forecast_data)

##-----------------------------------------------------------------------------
## 3. CALCULATE SOLAR POSITION
##-----------------------------------------------------------------------------
## retrieve time and location parameters
def sol_pos(forecast_data, model):
    time = forecast_data.index
    a_point = model.location
    solpos = a_point.get_solarposition(time)
    return (solpos)

##-----------------------------------------------------------------------------
## 4. CALCULATE EXTRATERRESTRIAL IRRADIANCE
##-----------------------------------------------------------------------------
def calc_dnix(model):
    dni_extra = irradiance.extraradiation(model.time)
    return (dni_extra)

##-----------------------------------------------------------------------------
## 5. CALCULATE POA SKY DIFFUSED IRRADIANCE
##-----------------------------------------------------------------------------
def poa_sd(forecast_data, solpos, dni_extra, surf_tilt=33.865143, 
           surf_azm=0):
    poa_sky_diffuse = irradiance.haydavies(surf_tilt, surf_azm,
                                           forecast_data['dhi'],
                                           forecast_data['dni'], dni_extra,
                                           solpos['apparent_zenith'],
                                           solpos['azimuth'])
    return(poa_sky_diffuse)
    
##-----------------------------------------------------------------------------
## 6. CALCULATE POA GROUND DIFFUSED IRRADIANCE
##-----------------------------------------------------------------------------
def poa_gd(forecast_data, surf_tilt=33.865143, albedo=0.2):
    poa_ground_diffuse = irradiance.grounddiffuse(surf_tilt, 
                                              forecast_data["ghi"], 
                                              albedo=albedo)
    return(poa_ground_diffuse)

##-----------------------------------------------------------------------------
## 7. CALCULATE SOLAR ANGLE OF INCIDENCE ONTO MODULE
##-----------------------------------------------------------------------------
def AOI(surf_tilt, surf_azm, solpos):
    aoi = irradiance.aoi(surf_tilt, 
                     surf_azm, 
                     solpos['apparent_zenith'], 
                     solpos['azimuth'])
    return (aoi)

##-----------------------------------------------------------------------------
## 8. CALCULATE TOTAL POA IRRADIANCE
##-----------------------------------------------------------------------------
def poa_tot(aoi, forecast_data, poa_sky_diffuse, poa_ground_diffuse):
    poa_irrad = irradiance.globalinplane(aoi, 
                                     forecast_data['dni'], 
                                     poa_sky_diffuse, 
                                     poa_ground_diffuse)
    return (poa_irrad)

##-----------------------------------------------------------------------------
## 9. CALCULATE CELL AND MODULE TEMPERATURES
##-----------------------------------------------------------------------------
def temp(poa_irrad, forecast_data):
    pvtemps = pvsystem.sapm_celltemp(poa_irrad['poa_global'], 
                                 forecast_data['wind_speed'], 
                                 forecast_data['temp_air'])
    return (pvtemps)

##-----------------------------------------------------------------------------
## 10. CALCULATE DC OUTPUT OF MODULE
##-----------------------------------------------------------------------------
def DC_out(solpos, poa_irrad, aoi, pvtemps):  
    ## First calculate airmass
    airmass = atmosphere.relativeairmass(solpos['apparent_zenith'])
    ## Get list of modules
    sandia_modules = pvsystem.retrieve_sam('SandiaMod')
    ## Choose model (e.g. CS5P_220M___2009)
    sandia_module = sandia_modules.Canadian_Solar_CS5P_220M___2009_
    ## Run SAPM model
    effective_irradiance = pvsystem.sapm_effective_irradiance(
        poa_irrad.poa_direct, poa_irrad.poa_diffuse, airmass, aoi, 
        sandia_module)
    p_dc = pvsystem.sapm(effective_irradiance, pvtemps['temp_cell'],
                         sandia_module)
    return (p_dc)

##-----------------------------------------------------------------------------
## 11. CALCULATE AC OUTPUT OF INVERTER
##-----------------------------------------------------------------------------
def AC_out(p_dc):
    ## Get list of inverters
    sapm_inverters = pvsystem.retrieve_sam('sandiainverter')
    ## Choose inverter (e.g. ABB__MICRO_0_25_I_OUTD_US_208_208V__CEC_2014)
    sapm_inverter = sapm_inverters[
            'ABB__MICRO_0_25_I_OUTD_US_208_208V__CEC_2014_']
    ## Run SAPM model
    p_ac = pvsystem.snlinverter(p_dc.v_mp, p_dc.p_mp, sapm_inverter)
    return (p_ac)

##-----------------------------------------------------------------------------
## GUI
##----------------------------------------------------------------------------- 
class App:
## Defines an object containing the GUI with all its inputs, outputs and action
## buttons
    def __init__(self, master):  
        ## Setup of Input frame
        self.frameIn = tk.Frame(master, 
                             bd=3, 
                             relief=tk.SUNKEN) 
        self.frameIn.pack(side=tk.LEFT,
                          fill=tk.BOTH,
                          expand=1)
        
        ## Setup of latitude input
        tk.Label(self.frameIn, text="Latitude [decimal]: ").grid(row=0, 
                column=0)
        self.lat = tk.Entry(self.frameIn)
        self.lat.grid(row=0, column=1)
        
        ## Setup of longitude input
        tk.Label(self.frameIn, text="Longitude [decimal]: ").grid(row=1,
                column=0)
        self.long = tk.Entry(self.frameIn)
        self.long.grid(row=1, column=1)
                
        ## Setup of timezone input
        tk.Label(self.frameIn, text="Timezone (Region/City): ").grid(row=2, 
                column=0)
        self.tz = tk.Entry(self.frameIn)
        self.tz.grid(row=2, column=1)
        
        ## Setup of tilt input
        tk.Label(self.frameIn, text="PV panel tilt (N/S) [deg]: ").grid(row=3,
                column=0)
        self.surf_tilt = tk.Entry(self.frameIn)
        self.surf_tilt.grid(row=3, column=1)
          
        ## Setup of azimuth input
        tk.Label(self.frameIn, text="PV panel azimuth (E/W) [deg]: ").grid(row=5, 
                column=0)
        self.surf_azm = tk.Entry(self.frameIn)
        self.surf_azm.grid(row=5, column=1)
        
        ## Setup of albedo input
        tk.Label(self.frameIn, text="Albedo: ").grid(row=6, column=0)
        self.albedo = tk.Entry(self.frameIn)
        self.albedo.grid(row=6, column=1)
        
        ## Setup of forecast length input
        tk.Label(self.frameIn, text="Forecast (days, max 16): ").grid(row=7, 
                column=0)
        self.days = tk.Entry(self.frameIn)
        self.days.grid(row=7, column=1)        
        
        ## Setup of CALCULATE button action
        self.calculate = tk.Button(self.frameIn,
                                text="CALCULATE",
                                fg="black",
                                font=("Times", 10, "bold"),
                                command=self.calculate) 
        self.calculate.grid(row=8, column=0)        
        
        ## Setup of QUIT button action
        self.exit = tk.Button(self.frameIn,
                           text="QUIT",
                           fg="red",
                           font=("Times", 10, "bold"),
                           command=master.quit)
        self.exit.grid(row=8, column=1) 
        
        ## Setup of Output frame
        self.frameOut = tk.Frame(master, 
                             bd=3, 
                             relief=tk.SUNKEN) 
        self.frameOut.pack(side=tk.LEFT,
                          fill=tk.BOTH,
                          expand=1)
        
        ## Plot setup
        self.fig = plt.Figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("Forecast of AC Power Output from Inverter")
        self.canvas = FigureCanvasTkAgg(self.fig, self.frameOut)
        self.canvas.show()
        self.canvas.get_tk_widget().pack()
        
    def calculate(self):
        ## Load forecasted irradiance
        model=GFS()
        forecast_data = irr_forecast(model, float(self.days.get()),
                                     float(self.lat.get()),
                                     float(self.long.get()), self.tz.get(),
                                     float(self.surf_tilt.get()),
                                     float(self.surf_azm.get()),
                                     float(self.albedo.get()))

        ## Calculate solar position
        solpos = sol_pos(forecast_data, model)
        ## Calculate extraterrestrial irradiance
        dni_extra = calc_dnix(model=model)
        ## Calculate POA sky diffused irradiance
        poa_sky_diffuse = poa_sd(forecast_data, solpos, dni_extra, 
                                 float(self.surf_tilt.get()),
                                 float(self.surf_azm.get()))
        ## Calculate POA ground diffused irradiance
        poa_ground_diffuse = poa_gd(forecast_data, float(self.surf_tilt.get()),
                                    float(self.albedo.get()))
        ## Calcualte AOI
        aoi = AOI(float(self.surf_tilt.get()), float(self.surf_azm.get()),
                  solpos)
        ## Calculate total POA irradiance
        poa_irrad = poa_tot(aoi, forecast_data, poa_sky_diffuse, 
                            poa_ground_diffuse)
        ## Calculate cell and module temperatures
        pvtemps = temp(poa_irrad, forecast_data)
        ## Calculate DC power output of module
        p_dc = DC_out(solpos, poa_irrad, aoi, pvtemps)
        ## Calculate AC power output of inverter
        p_ac = AC_out(p_dc)
        ## Plot AC output
        self.ax.cla()
        self.ax.set_ylabel('AC Power (W)')
        self.ax.plot(p_ac)
        self.canvas.draw()


##-----------------------------------------------------------------------------
## MAIN BODY
##-----------------------------------------------------------------------------
root = tk.Tk()
app = App(root)
root.mainloop()
root.destroy() ## Required in Windows! Otherwise the app cannot be exited.

