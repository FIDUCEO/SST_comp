### DATA_EXTRACTION

from netcdf4 import Dataset
import numpy as np
import os





def mmd_data_extract(filename,obs_variable_names,other_variables):
    
	# Read data from a netcdf and extract in-situ obs, 
    data = Dataset(filename)
    data_dict = {}
    all_variables = obs_variable_names + other_variables
    for i in all_variables:
        print i
        data_dict[i] = data.variables[i][:]
    data.close()
	
    return data_dict
	
	
def fiduceo_filenames_extract(filename):

    data = Dataset(filename)
    l1b_file_number=data.variables['scanline_map_to_origl1bfile'][:]
    l1b_scanline = data.variables['scanline_origl1b'][:]
    level1b_source = data.source
    level1b_files = level1b_source.split(',')
    data.close()
	
    return l1b_file_number, l1b_scanline, level1b_files
	
	
	
def fiduceo_return_value(fiduceo_named_variables,fid_line_comp,x_value,fid_file):

    if fid_file == 'MaskedData':
        fid_data = {}
        for variable in fiduceo_named_variables:
            fid_data[variable] = -999.99
    else:
        data = Dataset(fid_file)
        fid_data = {}
        for variable in fiduceo_named_variables:
            fid_data[variable] = data.variables[variable][fid_line_comp,x_value]
        data.close()
		
    return fid_data
	
	
	
def fiduceo_data_extract(filename,bt_variable,reflect_var_list,l1b):

    data = Dataset(filename)
    var_data_dict = {}
    for var in reflect_var_list:
        var_data_dict['%s'%(var)] = data.variables['%s'%(var)][:]
    data.close()	
	
    return var_data_dict
	
