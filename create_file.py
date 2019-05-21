#make_files

import numpy as np
import datetime
import os


def make_filename(filename_list):
    orig_filename = []
    for i in xrange(0,len(filename_list)):
        orig_filename.append(filename_list[i])
		
    return orig_filename
	
	
def make_time(secs_since):
    import datetime
    date = datetime.datetime.fromtimestamp(secs_since).strftime('%Y-%m-%d %H:%M:%S')
    year = date[0:4]
    month = date[5:7]
    day = date[8:10]
    hour = date[11:13]
    minute = date[14:16]
    second = date[17:19]
    return year,month,day,hour,minute,second
	
def replace_data(new_filename,obs_variable_names,fiduceo_named_variables,new_fid_data):
    dataD = Dataset(new_filename,'r+')
    switch_variable = {}
    for i in xrange(0,len(obs_variable_names)):
        switch_variable[obs_variable_names[i]]=fiduceo_named_variables[i]
    for var in obs_variable_names:
        dataD.variables[var] = new_fid_data[switch_variable[var]]
    dataD.close()
    test = 'Completed switch'		
    return test
	
	
def obs_variables(avhrr_sat):

    sat_name = avhrr_sat[0:5]+'.'+avhrr_sat[6:]
	all_channel_sats = ('avhrr-m02','avhrr-n19','avhrr-n18','avhrr-n17','avhrr-n16','avhrr-n15')
	if avhrr_sat in all_channel_sats:
        all_obs_variable_names = ('%s.reflectance_1'%(sat_name),'%s.reflectance_2'%(sat_name),'%s.reflectance_3a'%(sat_name),'%s.brightness_temperature_3b'%(sat_name),'%s.brightness_temperature_4'%(sat_name),'%s.brightness_temperature_5'%(sat_name))
	    fiduceo_named_variables = ('Ch1','Ch2','Ch3a','Ch3b','Ch4','Ch5')
	else:
        all_obs_variable_names = ('%s.reflectance_1'%(sat_name),'%s.reflectance_2'%(sat_name),'%s.brightness_temperature_3b'%(sat_name),'%s.brightness_temperature_4'%(sat_name),'%s.brightness_temperature_5'%(sat_name))
	    fiduceo_named_variables = ('Ch1','Ch2','Ch3b','Ch4','Ch5')        	
	return all_obs_variable_names, fiduceo_named_variables
	
	
	
	
	
	