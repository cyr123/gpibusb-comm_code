#!/usr/bin/python
# Filename: agilent6632b.py

# Author: Erik Gustavsson (cyrano@area26.se)
# Based on "agilent34410a.py" by Steven Casagrande (stevencasagrande@gmail.com)
# 2013

# This work is released under the Creative Commons Attribution-Sharealike 3.0 license.
# See http://creativecommons.org/licenses/by-sa/3.0/ or the included license/LICENSE.TXT file for more information.

# Attribution requirements can be found in license/ATTRIBUTION.TXT

from instrument.instrument import Instrument

class Agilent6632b(Instrument):
    def __init__(self, port, address,timeout_length):
        super(Agilent6632b, self).__init__(port,address,timeout_length)
    
    # Measurement
    def measure(self,mode):
        '''
	This command returns the measured output current or voltage.
        
        Function returns a float.
        
        mode: Desired measurement mode
        mode = {CURRent|VOLTage},string
        '''
        if not isinstance(mode,str):
            raise Exception('Measurement mode must be a string.')
        mode = mode.lower()
        
        valid = ['curr','volt']
        valid2 = ['current','voltage']
        
        if mode in valid2:
            mode = valid[valid2.index(mode)]
        elif mode not in valid:
            raise Exception('Valid measurement modes are: ' + str(valid2))
        
        return float( self.query( 'MEAS:' + mode.upper() + '?' ) )    
 
    # Enable/disable output
    def output(self,state = None):
        '''
        This command turns the output ON of OFF (1 or 0).
        
        If state is not specified, function queries the instrument for the current state. This is returned as an integer.
                    
        state = {1|0|ON|OFF},integer/string
        '''
        if state == None:
            return int( self.query('OUTP?') )
        
        if isinstance(state,str):
            state = state.lower()
            valid = ['on','off']
            if state not in valid:
                raise Exception('Valid state values are "on" and "off" when specified as a string.')
        elif isinstance(state,int):
            if state < 0 or state > 1:
                raise Exception('Valid state values are 1 or 0 when specified as an integer.')
        else:
            raise Exception('Output state must be a string or an integer.')
        
        self.write( 'OUTP ' + str(state) )   
        
    # Output current
    def current(self,value=None):
        '''
	This command sets the output current limit.
        
        If no value is specified, function queries the instrument for the current setting.
        
        value: Current limit setting in amps.
        value = {<amps>},integer/float 
        '''
        if value == None:
            return float( self.query('CURR?') )
        
        if isinstance(value,int) or isinstance(value,float):
            if value < 0:
                raise Exception('The value must be positive')
        
        self.write( 'CURR ' + str(value) )       
                
    # Output voltage
    def voltage(self,value=None):
        '''
	This command sets the output voltage.
        
        If no value is specified, function queries the instrument for the current setting.
        
        value: Output voltage setting in volts.
        value = {<volts>},integer/float 
        '''
        if value == None:
            return float( self.query('VOLT?') )
        
        if isinstance(value,int) or isinstance(value,float):
            if value < 0:
                raise Exception('The value must be positive')
        
        self.write( 'VOLT ' + str(value) )       
        
