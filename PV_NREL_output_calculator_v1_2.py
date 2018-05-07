
# coding: utf-8

# In[22]:


## coding: utf-8
## Author: Andrew M. Telford
## Version: 1.2
## Date: 20/03/2018

## Simple application to calculate the monthly output of PV panels given their 
## geographical location (in the US), power rating and area. The user can chose between setups
## optimised for various seasons in the year.
## The user requires an API key to access solar data from NREL.

from tkinter import *
from tkinter import ttk
import pandas as pd
import numpy as np
import json
import requests
from calendar import month_abbr
from math import sin, radians
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class App:
## Defines an object containing the GUI with all its inputs, outputs and action buttons
    def __init__(self, master):  
        ## Setup of Input frame
        self.frameIn = Frame(master, 
                             bd=3, 
                             relief=SUNKEN) 
        self.frameIn.pack(side=LEFT,
                          fill=BOTH,
                          expand=1)
        
        ## Setup of latitude input
        Label(self.frameIn, text="Latitude [deg]: ").grid(row=0, 
                                                          column=0)
        self.latitude = Entry(self.frameIn)
        self.latitude.grid(row=0, column=1)
        
        ## Setup of longitude input
        Label(self.frameIn, text="Longitude [deg]: ").grid(row=1, 
                                                           column=0)
        self.longitude = Entry(self.frameIn)
        self.longitude.grid(row=1, 
                            column=1)
                
        ## Setup of power rating input
        Label(self.frameIn, text="Power rating [kW]: ").grid(row=2, 
                                                             column=0)
        self.Prating = Entry(self.frameIn)
        self.Prating.grid(row=2, 
                          column=1)
        
        ## Setup of area input
        Label(self.frameIn, text="Area [m2]: ").grid(row=3, 
                                                     column=0)
        self.area = Entry(self.frameIn)
        self.area.grid(row=3, 
                       column=1)
        
        ## Setup of tilt optimisation input
        opt_list = ["All Year Round", "Summer", "Winter"]
        self.opt_setting = StringVar()
        self.opt_setting.set(opt_list[0]) ## default value
        Label(self.frameIn, text="Optimised for: ").grid(row=4, 
                                                         column=0)
        self.opt_selec = OptionMenu(self.frameIn, 
                                    self.opt_setting, 
                                    *opt_list)
        self.opt_selec.grid(row=4, 
                            column=1, 
                            sticky="ew") ## Sticky argument
        ## keeps the widget's width constant
        
        ## Setup of NREL API input
        Label(self.frameIn, text="NREL API: ").grid(row=5, 
                                                    column=0)
        self.api = Entry(self.frameIn)
        self.api.grid(row=5, 
                      column=1)
        
        ## Setup of CALCULATE button action
        self.calculate = Button(self.frameIn,
                                text="CALCULATE",
                                fg="black",
                                font=("Times", 10, "bold"),
                                command=self.calculate) 
        self.calculate.grid(row=6, 
                            column=0)        
        
        ## Setup of QUIT button action
        self.exit = Button(self.frameIn,
                           text="QUIT",
                           fg="red",
                           font=("Times", 10, "bold"),
                           command=master.quit)
        self.exit.grid(row=6, 
                       column=1)
        
        ## Setup of Output frame
        self.frameOut = Frame(master, 
                              bd=3, 
                              relief=SUNKEN) 
        self.frameOut.pack(side=LEFT)

        ## Setup of error message
        self.data_present=False
	         
		## Setup of Output frame
        self.frameOut = Frame(master, 
                             bd=3, 
                             relief=SUNKEN) 
        self.frameOut.pack(side=RIGHT,  fill=BOTH, expand=1)
		
        ## Plot setup
        self.fig = plt.Figure()
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, self.frameOut)
        self.canvas.show()
        self.canvas.get_tk_widget().pack()           
                
## Function list:    
    def calc_tilt(self):
    ## Calculates optimal solar panel tilt for the user-defined season    
        if self.opt_setting.get() == "All Year Round":
            if float(self.latitude.get()) >= 0:
                self.tilt = float(self.latitude.get())
            else:
                self.tilt = 90+float(self.latitude.get())
        elif self.opt_setting.get() == "Summer":
            if float(self.latitude.get()) >= 0:
                self.tilt = float(self.latitude.get())- 23.45
            else:
                self.tilt = 90-float(self.latitude.get()) + 23.45
        elif self.opt_setting.get() == "Winter":
            if float(self.latitude.get()) >= 0:
                self.tilt = float(self.latitude.get())+ 23.45
            else:
                self.tilt = 90-float(self.latitude.get()) - 23.45
    
    def check_nrel_data(self):
        url = 'https://developer.nrel.gov/api/solar/solar_resource/v1.json?api_key='+str(self.api.get())+'&lat='+str(self.latitude.get())+'&lon='+str(self.longitude.get())
        req = requests.get(url)
        self.nrel_data = json.loads(req.content)
        if (self.nrel_data["outputs"]["avg_ghi"]!="no data"): ## Checks that the data is present  
            self.data_present=True
        else:
            self.data_present=False
            
    def import_ghi_data(self):
    ## Imports Global Horizontal Irradiance (GHI) data from NREL    
            ghi = []
            for i in range(1,13):
                ghi += [self.nrel_data["outputs"]["avg_ghi"]["monthly"][(month_abbr[i]).lower()]]
            self.irr.data["GHI[kWh/m2/day]"] = pd.Series(ghi,index=self.irr.data.index)            
            
    def calc_efficiency(self):
    ## Calculates the efficiency of the solar panel based on its rated power output and its area   
        self.eff = (float(self.Prating.get())/float(self.area.get()))*(1-0.28)
        ## The formula should include dividing the result by the power density
        ## used in standard testing conditions, which is 1 kW/m2 (and hence omitted)
        ## The formula accounts for typical losses in a PV system

    def build_irradiance_table(self):
    ## Calculates sun elevation, actual irradiance on the solar panel, and solar panel power output.
    ## Builds a dataframe containing all the data for each month of the year.
        self.calc_efficiency()
        self.calc_tilt()
        self.irr = irradiance_data()
        self.irr.data["Elevation[deg]"] = self.irr.data.apply(calc_elev,
                                                              args=(float(self.latitude.get()),),
                                                              axis=1) 
        self.import_ghi_data()
        self.irr.data["act_irr[kWh/m2/day]"] = self.irr.data.apply(calc_actual_irr,
                                                                   args=(self.tilt,),
                                                                   axis=1) 
        self.irr.data["PV_out[kWh/day]"] = self.irr.data.apply(calc_PV_output,
                                                               args=(self.eff,float(self.area.get()),),
                                                               axis=1)
    
    def calculate(self):
        ## Calculates the PV power output
        self.check_nrel_data()
        if (self.data_present==True):
            self.build_irradiance_table()
        else:
            print("ERROR: no data present in the NREL database.\nPlease try a different set of coordinates in the US.")
            return   
        ## Plot output
        self.ax.cla()
        self.ax.set_title("DC Power Output from PV Module")
        self.ax.set_ylabel("DC Power Output (KWh/day)")
        self.ax.tick_params(labelrotation=45)
        self.ax.plot(self.irr.data["Month"], self.irr.data["PV_out[kWh/day]"])
        self.canvas.draw()
                    
class irradiance_data:
## Defines an object containing a dataframe with all the calculated data.
    def __init__(self):
        month = ["Jan",
                 "Feb", 
                 "Mar", 
                 "Apr", 
                 "May", 
                 "Jun", 
                 "Jul",
                 "Aug",
                 "Sep", 
                 "Oct", 
                 "Nov", 
                 "Dec"]
        declination = [-20.8471721,
                     -13.32525687,
                     -2.38917861,
                     9.493197789,
                     18.80581803,
                     23.07705882,
                     21.10146737,
                     13.29604132,
                     1.993572635,
                     -9.848545141,
                     -19.05050905,
                     -23.09560549]
        self.data = pd.DataFrame(np.transpose(month), 
                                 columns=["Month"])
        self.data["Declination[deg]"] = pd.Series(declination, 
                                                  index=self.data.index)
        
## Auxiliary functions for dataframe calculations:
def calc_elev(df, lat):
## Calculates sun elevation    
    if (lat >= 0):
        return 90 - lat + df["Declination[deg]"]
    else:
        return 90 + lat - df["Declination[deg]"]

def calc_actual_irr(df, tilt):
## Calculates actual irradiance on the solar panel from GHI
    return df["GHI[kWh/m2/day]"]*sin(radians(df["Elevation[deg]"]+float(tilt)))/            sin(radians(df["Elevation[deg]"]))
    
def calc_PV_output(df, eff, area):
## Calculates the power output of the solar panel    
    return df["act_irr[kWh/m2/day]"] * eff * area

##Main body
root = Tk()
app = App(root)
root.mainloop()
root.destroy() # Required in Windows! Otherwise the app cannot be exited.

