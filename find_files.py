import numpy as np
import datetime
import os



def fiduceo_linenumber_find(file_index,l1b_linenumber,fid_l1b_file_number,fid_l1b_scanlines):
    #import time
    fid_line_comp = "False"
    for i in xrange(0,len(fid_l1b_file_number)):
        try:
            if int(fid_l1b_file_number[i]) == int(file_index) and int(fid_l1b_scanlines[i]) == int(l1b_linenumber):
                print "I didn't fail"
                fid_line_comp=i
                return fid_line_comp               
        except:
            print "Masked array - cannot compute"
    return fid_line_comp


def find_FIDUCEO_file(year,month,day,avhrr,hour,minute,second,fiduceo_pathway):

    fiduceo_folder = fiduceo_pathway + avhrr +'/'+year+'/'+month+'/'+day+'/'
    f3split = 'False'
    f3split_file = 'False'
    try: 
        list_of_files = os.listdir(fiduceo_folder)
    except:
        print "No files exist for ",year,'/',month,'/',day
        file_matched = 'NotThere'
        return fiduceo_folder, file_matched, fiduceo_folder
    time = int(hour+minute+second)
    print time
    file_matched = 'False'
    #check if first file time is before original time, last file time is after
    first_file = list_of_files[0]
    last_file = list_of_files[-1]
    if int(last_file[53:59]) < 060000 and time > int(last_file[38:44]):
        print "Last file extends to next day with comparison inside"
        file_matched = last_file
    # else if time is earlier than first start time
    elif int(first_file[38:44]) > time:
        print "Time comparison in previous days file"
        if int(day) > 1: 
            day = str(int(day)-1)
            fiduceo_folder = fiduceo_pathway + avhrr +'/'+year+'/'+month+'/'+day+'/'
            list_of_files = os.listdir(fiduceo_folder)
            last_file = list_of_files[-1]
            if int(last_file[53:59]) > time:
                file_matched = last_file
            else:
                print "File missing from end of previous day - no match"   





    # if time is between first start time and last endtime    
    elif int(first_file[38:44]) < time and int(last_file[53:59]) > time:
        for files in list_of_files:
            print files[38:45],files[53:60]
        
            if int(files[38:44]) < time and int(files[53:59]) > time:


                #### DETERMINE IF FILE CONTAINS ALL CHANNELS, OR JUST 3A/3B
                if 'ALL' in files: 
                    file_matched = files


                elif '3A' in files:
                    file_matched = files
                    all_3b_files = [s for s in list_of_files if "3B" in s]
                    for f3b_file in all_3b_files:
                        if int(f3b_file[38:44]) < time and int(f3b_file[53:59]) > time:                  
                            f3split = 'True'
                            f3split_file = f3b_file


                elif '3B' in files:
                    file_matched = files
                    all_3a_files = [s for s in list_of_files if "3A" in s]
                    for f3a_file in all_3a_files:
                        if int(f3a_file[38:44]) < time and int(f3a_file[53:59]) > time:
                            f3split = 'True'                      
                            f3split_file = f3a_file
    
    print file_matched
    return fiduceo_folder,file_matched,fiduceo_folder,f3split,f3split_file
	
	
	
def find_mmd_files(mmd_filepath,avhrr_sat,insitu_name):
    full_mmd_obs_path = mmd_filepath+avhrr_sat+'/'+insitu_name+'_'+avhrr_sat
    mmd_files = os.listdir(full_mmd_obs_path)
	
    return mmd_files,full_mmd_obs_path
	
	

def find_l1b_l1c_files(ver_no,l1c_file):
    #print ver_no
    ver_num = ver_no[0:5]
    for i in xrange(0,len(ver_num)):
        if i == 0:
            ver_tog = str(ver_num[i])
        elif i == 1:
            print "I didn't do this because it's a silly 0"
        else:
            ver_tog = ver_tog+str(ver_num[i]) 

    for i in xrange(0,44):
        if i == 0:
            l1c_file_ex = str(l1c_file[i])
        elif np.ma.is_masked(i):
            print "- found, not used" 
        else:
            l1c_file_ex = l1c_file_ex + str(l1c_file[i])
    with open('/gws/nopw/j04/esacci_sst/validation/map_l1c_l2p/l1c_'+ver_tog+'.txt', 'r') as comparison_file:
        for line in comparison_file:
            #print l1c_file_ex, "l1c_file"
            #print line, "lien"
            if l1c_file_ex in line:
                l1b_file = line
                break
				
    #l1c_l1b_map = {line.split()[0]:line.split()[1] for line in open(comparison_file)}
				
    return l1b_file
	
def fiduceo_file_ident(level1b_fid_files,l1b_mmd_file):
    print l1b_mmd_file
    file_index = 999
    for files in level1b_fid_files:
        print files
        print l1b_mmd_file
        if files == l1b_mmd_file:
            file_index = int(level1b_fid_files.index(files)+1)
            break	
		   
    return file_index