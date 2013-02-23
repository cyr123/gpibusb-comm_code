#!/usr/bin/python
# Filename: keithley2015.py

# Author: Erik Gustavsson (cyrano@area26.se)
# Based on "agilent34410a.py" by Steven Casagrande (stevencasagrande@gmail.com)
# 2013

# This work is released under the Creative Commons Attribution-Sharealike 3.0 license.
# See http://creativecommons.org/licenses/by-sa/3.0/ or the included license/LICENSE.TXT file for more information.

# Attribution requirements can be found in license/ATTRIBUTION.TXT

from instrument.instrument import Instrument

class Keithley2015(Instrument):
    def __init__(self, port, address,timeout_length):
        super(Keithley2015, self).__init__(port,address,timeout_length)
    
    # Measurement
    def measure(self,mode):
        '''
        This command combines all of the other signal oriented measurement
        commands to perform a one-shot measurement and acquire the reading.
        When this command is sent, the following commands execute in the order
        that they are presented.
        :ABORt:CONFigure:<mode>:READ?
        
        Function returns a float.
        
        mode: Desired measurement mode
        mode = {CONTinuity|CURRent:AC|CURRent:DC|DIODe|DISTortion|FREQuency|FRESistance|PERiod|RESistance|TEMPerature|VOLTage:AC|VOLTage:DC},string
        '''
        if not isinstance(mode,str):
            raise Exception('Measurement mode must be a string.')
        mode = mode.lower()
        
        valid = ['cont','curr:ac','curr:dc','diod','dist','freq','fres','per','res','temp','volt:ac','volt:dc']
        valid2 = ['continuity','current:ac','current:dc','diode','distortion','frequency','fresistance','period','resistance','temperature','voltage:ac','voltage:dc']
        
        if mode in ['4res','4 res','four res','f res']:
            mode = 'fres'
        
        if mode in valid2:
            mode = valid[valid2.index(mode)]
        elif mode not in valid:
            raise Exception('Valid measurement modes are: ' + str(valid2))
        
        return float( self.query( 'MEAS:' + mode.upper() + '?' ) )
    
    # Configure measurement mode, using default parameters    
    def configure(self,mode):
        '''
        This command configures the instrument for subsequent measurements on
        the specified function. Basically, this command places the instrument in a
        one-shot measurement mode.

        When this command is sent, the Model 2015 will be configured as follows:
        - The function specified by this command is selected.
        - All controls related to the selected function are defaulted to the *RST values.
        - Continuous initiation is disabled (:INITiate:CONTinuous OFF).
        - The control source of the Trigger Model is set to Immediate.
        - The count values of the Trigger Model are set to one.
        - The delay of the Trigger Model is set to zero.
        - The Model 2015 is placed in the idle state.
        - All math calculations are disabled.
        - Buffer operation is disabled. A storage operation currently in process will be aborted.
        - Autozero is set to the *RST default value.
        - All operations associated with switching cards (scanning) are disabled.
       
        mode: Desired measurement mode
        mode = {CONTinuity|CURRent:AC|CURRent:DC|DIODe|DISTortion|FREQuency|FRESistance|PERiod|RESistance|TEMPerature|VOLTage:AC|VOLTage:DC},string
        '''

        if not isinstance(mode,str):
            raise Exception('Measurement mode must be a string.')
        mode = mode.lower()
        
        valid = ['cont','curr:ac','curr:dc','diod','dist','freq','fres','per','res','temp','volt:ac','volt:dc']
        valid2 = ['continuity','current:ac','current:dc','diode','distortion','frequency','fresistance','period','resistance','temperature','voltage:ac','voltage:dc']
        
        if mode in ['4res','4 res','four res','f res']:
            mode = 'fres'
        
        if mode in valid2:
            mode = valid[valid2.index(mode)]
        elif mode not in valid:
            raise Exception('Valid measurement modes are: ' + str(valid2))
        
        return float( self.query( 'CONF:' + mode.upper() ) )
        
    # Fetch
    def fetch(self):
        '''
        This query command requests the latest post- processed reading. After
        sending this command and addressing the Model 2015 to talk, the reading is
        sent to the computer. This command does not affect the instrument setup.
        This command does not trigger a measurement. The command simply
        requests the last available reading. Note that this command can repeatedly
        return the same reading. Until there is a new reading, this command
        continues to return the old reading. If your application requires a fresh
        reading, use the :DATA:FRESh? command (see the SENSe Subsystem command).

        Returns a float of the data read from the instrument.
        '''
        return float( self.query('FETC?') )
    
    # Init: Set to "Wait-for-trigger" state        
    def init(self):
        '''
        This command takes the Model 2015 out of the idle state. After all
        programmed operations are completed, the instrument returns to the idle state
        '''
        self.write('INIT')
    
    # Read
    def read(self):
        '''
        Typically, this command is used with the instrument in the one-shot
        measurement mode to trigger and acquire a specified number of readings.
        The :SAMPle:COUNt command is used to specify the number of readings
        (see Trigger Subsystem). Note that the readings are stored in the buffer.
        When this command is sent, the following commands execute in the order
        that they are presented:
        :ABORt
        :INITiate
        :FETCh?
        
        Returns a float of the data read from the instrument.
        '''
        return float( self.query('READ?') )
        
    
    # Set Trigger Source
    def triggerSource(self,source=None):
        '''
        These commands are used to select the event control source.
        A specific event can be used to control operation. With EXTernal selected,
        operation continues when an External Trigger is received.
        With TIMer selected, the event occurs at the beginning of the timer interval,
        and every time it times out. For example, if the timer is programmed for a
        30 second interval, the first pass through the control source occurs
        immediately. Subsequent scan events will then occur every 30 seconds. The
        interval for the timer is set using the :TIMer command.
        With MANual selected, the event occurs when the TRIG key is pressed.
        With BUS selected, the event occurs when a GET or *TRG command is sent
        over the bus.
       
        If no source is specified, function queries the instrument for the current setting. This is returned as a string. An example value is "EXT", without quotes.
            
        source: Desired trigger source
        source = {IMMediate|EXTernal|TIMer|MANual|BUS},string
        '''
        if source == None: # If source was not specified, perform query.
            return self.query('TRIG:SOUR?')
        
        if not isinstance(source,str):
            raise Exception('Parameter "source" must be a string.')
        source = source.lower()
        
        valid = ['immediate','external','timer','manual','bus']
        valid2 = ['imm','ext','tim','man','bus']
        
        if source in valid:
            source = valid2[valid.index(source)]
        elif source not in valid2:
            raise Exception('Trigger source must be "immediate", "external", "timer", "manual" or "bus".')
        
        self.write('TRIG:SOUR ' + source)
        
    # Trigger Count
    def triggerCount(self,count = None):
        '''
        This command is used to specify how many times operation loops around in
        the trigger operation. For example, if the count is set to 10, operation
        continues to loop around until 10 device actions are performed. After the
        10th action, operation proceeds back up to the start of the trigger model. Note
        that each loop places operation at the control source where it waits for the
        programmed event.
        
        If count is not specified, function queries the instrument for the current trigger count setting. This is returned as an integer.
            
        count: Number of triggers before returning to an "idle" trigger state.
        count = {<count>|MINimum|MAXimum|DEFault|INF},integer/string
        '''
        if count == None: # If count not specified, perform query.
            return int( self.query('TRIG:COUN?') )
        
        if isinstance(count,str):
            count = count.lower()
            valid = ['minimum','maximum','default','inf']
            valid2 = ['min','max','def','inf']
            if count in valid:
                count = valid2[valid.index(count)]
            elif count not in valid2:
                raise Exception('Valid trigger count values are "minimum", "maximum", "default", and "inf" when specified as a string.')
        elif isinstance(count,int):
            if count < 1:
                raise Exception('Trigger count must be a positive integer.')
            count = str(count)
        else:
            raise Exception('Trigger count must be a string or an integer.')
        
        self.write( 'TRIG:COUN ' + str(count) )
        
    # Trigger delay
    def triggerDelay(self,period=None):
        '''
        The delay is used to delay operation of the trigger model. After the
        programmed event occurs, the instrument waits until the delay period expires
        before performing the Device Action in the Trigger Model.
     
        If no period is specified, function queries the instrument for the current trigger delay and returns a float.
        
        period: Time between receiving a trigger event and the instrument taking the reading. Values range from 0s to 999999.999s
        period = {<seconds>|MINimum|MAXimum|DEFault},float/string 
        '''
        if period == None: # If no period is specified, perform query.
            return float( self.query('TRIG:DEL?') )
        
        if isinstance(period,str):
            period = period.lower()
            valid = ['minimum','maximum','default']
            valid2 = ['min','max','def']
            if period in valid:
                period = valid2[valid.index(period)]
            elif period not in valid2:
                raise Exception('Valid trigger delay values are "minimum", "maximum", and "default" when specified as a string.')
        elif isinstance(period,int) or isinstance(period,float):
            if period < 0 or period > 999999.999:
                raise Exception('The trigger delay needs to be between 0 and 999999.999 seconds.')
        
        self.write( 'TRIG:DEL ' + str(period) )

    # Trigger timer
    def triggerTimer(self,period=None):
        '''
        These commands are used to set the interval for the timer. Note that the timer
        is in effect only if the timer is the selected control source.
     
        If no period is specified, function queries the instrument for the current trigger timer and returns a float.
        
        period: Timer interval in seconds. Values range from 0.001s to 999999.999s
        period = {<seconds>},float 
        '''
        if period == None: # If no period is specified, perform query.
            return float( self.query('TRIG:TIM?') )
        
        if isinstance(period,int) or isinstance(period,float):
            if period < 0.001 or period > 999999.999:
                raise Exception('The trigger timer period needs to be between 0.001 and 999999.999 seconds.')
        
        self.write( 'TRIG:TIM ' + str(period) )

    # Trigger 
    def triggerSignal(self):
        '''
        This action command is used to bypass the specified control source when you
        do not wish to wait for the programmed event. Keep in mind that the
        instrument must be waiting for the appropriate event when the command is
        sent. Otherwise, an error occurs and this command is ignored.

        '''
        self.write( 'TRIG:SIGN' )
    
    # Sample Count
    def sampleCount(self,count = None):
        '''
	This command specifies the sample count. The sample count defines how many
	times operation loops around in the trigger model to perform a device action.
                    
        If count is not specified, function queries the instrument for the current smaple count and returns an integer.
            
        count: Number of triggers before returning to an "idle" trigger state.
        count = {<count>},integer
        '''
        if count == None: # If count is not specified, perform query.
            return int( self.query('SAMP:COUN?') )
        
        if isinstance(count,int):
            if count < 1:
                raise Exception('Trigger count must be a positive integer.')
            count = str(count)
        else:
            raise Exception('Trigger count must be an integer.')
        
        self.write( 'SAMP:COUN ' + str(count) )
   
    # Abort Measurements
    def abort(self):
        '''
        Abort a measurements currently in progress.
        '''
        self.write('ABOR')
        
        
        
        
        
        
        
        
        
        
        
        
        
