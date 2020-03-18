""" Formats and sets the required units of observations displayed on the 
Raspberry Pi Python console for Weather Flow Smart Home Weather Stations. 
Copyright (C) 2018-2019  Peter Davis

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.
"""

# Import required modules
from lib  import derivedVariables as derive
import math

def Units(Obs,Unit):

    """ Sets the required observation units
	
	INPUTS: 
		Obs				Observations with current units
		Unit			Required output unit
		
	OUTPUT: 
        cObs            Observation converted into required unit
	"""

    # Convert temperature observations
    cObs = Obs[:]
    if Unit in ['f','c']:
        for ii,T in enumerate(Obs):
            if T == 'c':
                if Unit == 'f':
                    cObs[ii-1] = Obs[ii-1] * 9/5 + 32
                    cObs[ii] = ' [sup]o[/sup]F'
                else:
                    cObs[ii-1] = Obs[ii-1]
                    cObs[ii] = ' [sup]o[/sup]C'

    # Convert pressure and pressure trend observations
    elif Unit in ['inhg','mmhg','hpa','mb']:
        for ii,P in enumerate(Obs):
            if P in ['mb','mb/hr']:
                if Unit == 'inhg':
                    cObs[ii-1] = Obs[ii-1] * 0.0295301
                    if P == 'mb':
                        cObs[ii] = ' inHg'
                    else:
                        cObs[ii] = ' inHg/hr'
                elif Unit == 'mmhg':
                    cObs[ii-1] = Obs[ii-1] * 0.750063
                    if P == 'mb':
                        cObs[ii] = ' mmHg'
                    else:
                        cObs[ii] = ' mmHg/hr'
                elif Unit == 'hpa':
                    cObs[ii-1] = Obs[ii-1]
                    if P == 'mb':
                        cObs[ii] = ' hpa'
                    else:
                        cObs[ii] = ' hpa/hr'
                else:
                    cObs[ii-1] = Obs[ii-1]
                    if P == 'mb':
                        cObs[ii] = ' mb'
                    else:
                        cObs[ii] = ' mb/hr'

    # Convert windspeed observations
    elif Unit in ['mph','lfm','kts','kph','bft','mps']:
        for ii,W in enumerate(Obs):
            if W == 'mps':
                if Unit == 'mph' or Unit == 'lfm':
                    cObs[ii-1] = Obs[ii-1] * 2.2369362920544
                    cObs[ii] = 'mph'
                elif Unit == 'kts':
                    cObs[ii-1] = Obs[ii-1] * 1.9438
                    cObs[ii] = 'kts'
                elif Unit == 'kph':
                    cObs[ii-1] = Obs[ii-1] * 3.6
                    cObs[ii] = 'km/h'
                elif Unit == 'bft':
                    cObs[ii-1] = derive.BeaufortScale(Obs[ii-1:ii+1])[4]
                    cObs[ii] = 'bft'
                else:
                    cObs[ii-1] = Obs[ii-1]
                    cObs[ii] = 'm/s'

    # Convert wind direction observations
    elif Unit in ['degrees','cardinal']:
        for ii,W in enumerate(Obs):
            if W == 'degrees':
                if cObs[ii-1] is None:
                    cObs[ii-1] = 'Calm'
                    cObs[ii] = ''
                elif Unit == 'cardinal':
                    cObs[ii-1] = derive.CardinalWindDirection(Obs[ii-1:ii+1])[2]
                    cObs[ii] = ''
                else:
                    cObs[ii-1] = Obs[ii-1]
                    cObs[ii] = '[sup]o[/sup]'

    # Convert rain accumulation and rain rate observations
    elif Unit in ['in','cm','mm']:
        for ii,Prcp in enumerate(Obs):
            if Prcp in ['mm','mm/hr']:
                if Unit == 'in':
                    cObs[ii-1] = Obs[ii-1] * 0.0393701
                    if Prcp == 'mm':
                        cObs[ii] = '"'
                    else:
                        cObs[ii] = ' in/hr'
                elif Unit == 'cm':
                    cObs[ii-1] = Obs[ii-1] * 0.1
                    if Prcp == 'mm':
                        cObs[ii] = ' cm'
                    else:
                        cObs[ii] = ' cm/hr'
                else:
                    cObs[ii-1] = Obs[ii-1]
                    if Prcp == 'mm':
                        cObs[ii] = ' mm'
                    else:
                        cObs[ii] = ' mm/hr'

    # Convert distance observations
    elif Unit in ['km','mi']:
        for ii,Dist in enumerate(Obs):
            if Dist == 'km':
                if Unit == 'mi':
                    cObs[ii-1] = Obs[ii-1] * 0.62137
                    cObs[ii] = 'miles'

    # Return converted observations
    return cObs
    
def Format(Obs,Type):

    """ Formats the observation for display on the console
	
	INPUTS: 
		Obs				Observations with units
		Type			Observation type
		
	OUTPUT: 
        cObs            Formatted observation based on specified type
	"""

    # Format temperature observations
    cObs = Obs[:]
    if Type == 'Temp':
        for ii,T in enumerate(Obs):
            if isinstance(T,str) and T.strip() in ['[sup]o[/sup]F','[sup]o[/sup]C']:
                if math.isnan(cObs[ii-1]):
                    cObs[ii-1] = '-'
                elif cObs[ii-1] == 0:
                    cObs[ii-1] = '{:.1f}'.format(abs(cObs[ii-1]))
                else:
                    cObs[ii-1] = '{:.1f}'.format(cObs[ii-1])

    # Format pressure observations
    elif Type == 'Pressure':
        for ii,P in enumerate(Obs):
            if isinstance(P,str) and P.strip() in ['inHg/hr','inHg','mmHg/hr','mmHg','hpa/hr','mb/hr','hpa','mb']:
                if math.isnan(cObs[ii-1]):
                    cObs[ii-1] = '-'
                else:
                    if P.strip() in ['inHg/hr','inHg']:
                        cObs[ii-1] = '{:2.3f}'.format(cObs[ii-1])
                    elif P.strip() in ['mmHg/hr','mmHg']:
                        cObs[ii-1] = '{:3.2f}'.format(cObs[ii-1])
                    elif P.strip() in ['hpa/hr','mb/hr','hpa','mb']:
                        cObs[ii-1] = '{:4.1f}'.format(cObs[ii-1])

    # Format windspeed observations
    elif Type == 'Wind':
        for ii,W in enumerate(Obs):
            if isinstance(W,str) and W.strip() in ['mph','kts','km/h','bft','m/s']:
                if math.isnan(cObs[ii-1]):
                    cObs[ii-1] = '-'
                else:
                    if cObs[ii-1] < 10:
                        cObs[ii-1] = '{:.1f}'.format(cObs[ii-1])
                    else:
                        cObs[ii-1] = '{:.0f}'.format(cObs[ii-1])

    # Format wind direction observations
    elif Type == 'Direction':
        for ii,D in enumerate(Obs):
            if isinstance(D,str) and D.strip() in ['[sup]o[/sup]']:
                if math.isnan(cObs[ii-1]):
                    cObs[ii-1] = '-'
                else:
                    cObs[ii-1] = '{:.0f}'.format(cObs[ii-1])

    # Format rain accumulation and rain rate observations
    elif Type == 'Precip':
        for ii,Prcp in enumerate(Obs):
            if isinstance(Prcp,str):
                if Prcp.strip() == 'mm':
                    if math.isnan(cObs[ii-1]):
                        cObs[ii-1] = '-'
                    else:
                        if cObs[ii-1] == 0:
                            cObs[ii-1] = '{:.0f}'.format(cObs[ii-1])
                        elif cObs[ii-1] < 0.1:
                            cObs[ii-1] = 'Trace'
                            cObs[ii] = ''
                        elif cObs[ii-1] < 10:
                            cObs[ii-1] = '{:.1f}'.format(cObs[ii-1])
                        else:
                            cObs[ii-1] = '{:.0f}'.format(cObs[ii-1])            
                elif Prcp.strip() == 'mm/hr':
                    if math.isnan(cObs[ii-1]):
                        cObs[ii-1] = '-'
                    else:
                        if cObs[ii-1] == 0:
                            cObs[ii-1] = '{:.0f}'.format(cObs[ii-1])
                        elif cObs[ii-1] < 0.1:
                            cObs[ii-1] = '<0.1'
                        elif cObs[ii-1] < 10:
                            cObs[ii-1] = '{:.1f}'.format(cObs[ii-1])
                        else:
                            cObs[ii-1] = '{:.0f}'.format(cObs[ii-1])            
                elif Prcp.strip() in ['"','cm']:
                    if math.isnan(cObs[ii-1]):
                        cObs[ii-1] = '-'
                    else:
                        if cObs[ii-1] == 0:
                            cObs[ii-1] = '{:.0f}'.format(cObs[ii-1])
                        elif cObs[ii-1] < 0.01:
                            cObs[ii-1] = 'Trace'
                            cObs[ii] = ''
                        elif cObs[ii-1] < 10:
                            cObs[ii-1] = '{:.2f}'.format(cObs[ii-1])
                        elif cObs[ii-1] < 100:
                            cObs[ii-1] = '{:.1f}'.format(cObs[ii-1])
                        else:
                            cObs[ii-1] = '{:.0f}'.format(cObs[ii-1])
                elif Prcp.strip() in ['in/hr','cm/hr']:
                    if math.isnan(cObs[ii-1]):
                        cObs[ii-1] = '-'
                    else:
                        if cObs[ii-1] == 0:
                            cObs[ii-1] = '{:.0f}'.format(cObs[ii-1])
                        elif cObs[ii-1] < 0.01:
                            cObs[ii-1] = '<0.01'
                        elif cObs[ii-1] < 10:
                            cObs[ii-1] = '{:.2f}'.format(cObs[ii-1])
                        elif cObs[ii-1] < 100:
                            cObs[ii-1] = '{:.1f}'.format(cObs[ii-1])
                        else:
                            cObs[ii-1] = '{:.0f}'.format(cObs[ii-1])                            

    # Format humidity observations
    elif Type == 'Humidity':
        for ii,H in enumerate(Obs):
            if isinstance(H,str) and H.strip() == '%':
                if math.isnan(cObs[ii-1]):
                    cObs[ii-1] = '-'
                else:
                    cObs[ii-1] = '{:.0f}'.format(cObs[ii-1])

    # Format solar radiation observations
    elif Type == 'Radiation':
        for ii,Rad in enumerate(Obs):
            if isinstance(Rad,str) and Rad.strip() == 'W m[sup]-2[/sup]':
                if math.isnan(cObs[ii-1]):
                    cObs[ii-1] = '-'
                else:
                    cObs[ii-1] = '{:.0f}'.format(cObs[ii-1])

    # Format UV observations
    elif Type == 'UV':
        for ii,UV in enumerate(Obs):
            if isinstance(UV,str) and UV.strip() == 'index':
                if math.isnan(cObs[ii-1]):
                    cObs[ii-1] = '-'
                else:
                    cObs[ii-1] = '{:.1f}'.format(cObs[ii-1])

    # Format battery voltage observations
    elif Type == 'Battery':
        for ii,V in enumerate(Obs):
            if isinstance(V,str) and V.strip() == 'v':
                if math.isnan(cObs[ii-1]):
                    cObs[ii-1] = '-'
                else:
                    cObs[ii-1] = '{:.2f}'.format(cObs[ii-1])

    # Format lightning strike count observations
    elif Type == 'StrikeCount':
        for ii,L in enumerate(Obs):
            if isinstance(L,str) and L.strip() == 'count':
                if math.isnan(cObs[ii-1]):
                    cObs[ii-1] = '-'
                elif cObs[ii-1] < 1000:
                    cObs[ii-1] = '{:.0f}'.format(cObs[ii-1])
                else:
                    cObs[ii-1] = '{:.1f}'.format(cObs[ii-1]/1000) + ' k'

    # Format lightning strike distance observations
    elif Type == 'StrikeDistance':
        for ii,StrikeDist in enumerate(Obs):
            if isinstance(StrikeDist,str):
                if StrikeDist.strip() in ['km']:
                    if math.isnan(cObs[ii-1]):
                        cObs[ii-1] = '-'
                    else:
                        DistValues = [0,5,6,8,10,12,14,17,20,24,27,31,34,37,40]
                        DispValues = ['0-5','2-8','3-9','5-11','7-13','9-15','11-17','14-20','17-23','21-27','24-30','28-34','31-37','34-40','37-43']
                        cObs[ii-1] = DispValues[DistValues.index(cObs[ii-1])]
                elif StrikeDist.strip() in ['miles']:
                    if math.isnan(cObs[ii-1]):
                        cObs[ii-1] = '-'
                    else:
                        DistValues = [0,3.1,3.7,5,6.2,7.5,8.7,10.6,12.4,14.9,16.8,19.3,21.1,23,24.9]
                        DispValues = ['0-3','1-5','2-6','3-7','4-8','6-9','7-11','9-12','11-14','13-17','15-19','17-21','19-23','21-25','37-43']
                        cObs[ii-1] = DispValues[DistValues.index(round(cObs[ii-1],1))]
                        
    # Format lightning strike frequency observations
    elif Type == 'StrikeFrequency':
        for ii,StrikeFreq in enumerate(Obs):
            if isinstance(StrikeFreq,str):
                if StrikeFreq.strip() in ['/min']:
                    if math.isnan(cObs[ii-1]):
                        cObs[ii-1] = '-'
                        cObs[ii] = ' /min'
                    else:
                        cObs[ii-1] = '{:.0f}'.format(cObs[ii-1])
                        cObs[ii] = ' /min'

    # Format time difference observations
    elif Type == 'TimeDelta':
        for ii,Delta in enumerate(Obs):
            if isinstance(Delta,str) and Delta.strip() in ['s']:
                if math.isnan(cObs[ii-1]):
                    cObs = ['-','-','-','-',cObs[2]]
                else:
                    days,remainder = divmod(cObs[ii-1],86400)
                    hours,remainder = divmod(remainder,3600)
                    minutes,seconds = divmod(remainder,60)
                    if days >= 1:
                        if days == 1:
                            if hours == 1:
                                cObs = ['{:.0f}'.format(days),'day','{:.0f}'.format(hours),'hour',cObs[2]]
                            else:
                                cObs = ['{:.0f}'.format(days),'day','{:.0f}'.format(hours),'hours',cObs[2]]
                        elif days <= 99:
                            if hours == 1:
                                cObs = ['{:.0f}'.format(days),'days','{:.0f}'.format(hours),'hour',cObs[2]]
                            else:
                                cObs = ['{:.0f}'.format(days),'days','{:.0f}'.format(hours),'hours',cObs[2]]
                        elif days >= 100:
                                cObs = ['{:.0f}'.format(days),'days','-','-',cObs[2]]
                    elif hours >= 1:
                        if hours == 1:
                            if minutes == 1:
                                cObs = ['{:.0f}'.format(hours),'hour','{:.0f}'.format(minutes),'min',cObs[2]]
                            else:
                                cObs = ['{:.0f}'.format(hours),'hour','{:.0f}'.format(minutes),'mins',cObs[2]]
                        elif hours > 1:
                            if minutes == 1:
                                cObs = ['{:.0f}'.format(hours),'hours','{:.0f}'.format(minutes),'min',cObs[2]]
                            else:
                                cObs = ['{:.0f}'.format(hours),'hours','{:.0f}'.format(minutes),'mins',cObs[2]]
                    else:
                        if minutes == 0:
                            cObs = ['< 1','minute','-','-',cObs[2]]
                        elif minutes == 1:
                            cObs = ['{:.0f}'.format(minutes),'minute','-','-',cObs[2]]
                        else:
                            cObs = ['{:.0f}'.format(minutes),'minutes','-','-',cObs[2]]

    # Return formatted observations
    return cObs
