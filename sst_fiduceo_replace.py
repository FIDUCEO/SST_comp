from netcdf4 import Dataset
import numpy as np
import os
import argparse
import datetime
import data_extraction as dex
import find_files as ff
import data_checks as check 
import create_file as create


mmd_filepath = '/gws/nopw/j04/esacci_sst/mms_new/mmd/mmd04_re01_pp/'
fiduceo_pathway = '/gws/nopw/j04/fiduceo/Data/FCDR/AVHRR/v0.2Bet/'




if __name__ in '__main__':

 
    parser = argparse.ArgumentParser()
    parser.add_argument("obs_set")
    parser.add_argument("year")
    parser.add_argument("avhrr_sat")
    args = parser.parse_args()
	
	
	
	
#### Find list of first files from mmd04


    level_1b_linenumber_variable = args.avhrr_sat[0:5]+'.'+args.avhrr_sat[6:9]+'.l1b_line_number'
    filename_variable = args.avhrr_sat[0:5]+'.'+args.avhrr_sat[6:9]+'.file_name'
    version_variable = args.avhrr_sat[0:5]+'.'+args.avhrr_sat[6:9]+'.processing_version'
    x_variable = args.avhrr_sat[0:5]+'.'+args.avhrr_sat[6:9]+'.x'
    y_variable = args.avhrr_sat[0:5]+'.'+args.avhrr_sat[6:9]+'.y'
    time_variable = args.avhrr_sat[0:5]+'.'+args.avhrr_sat[6:9]+'.acquisition_time'

    obs_variable_names,fiduceo_named_variables = create.obs_variables(args.avhrr_sat)
    other_variables = (filename_variable,version_variable,x_variable,y_variable,level_1b_linenumber_variable,time_variable)
	
	
    if args.avhrr_sat[6] == 'n':
        satellite = 'AVHRR'+args.avhrr_sat[7:9]+'_G'
    elif args.avhrr_sat[6] == 'm':
        satellite = 'AVHRRMTA_G'
    test=0

    mmd_filelists,full_mmd_path = ff.find_mmd_files(mmd_filepath,args.avhrr_sat,args.obs_set)
    new_filelist = []
    for x in mmd_filelists:
        if args.year in x:
            new_filelist.append(x)

    for filename in new_filelist:
        check_exist = check.initial_check(filename,fiduceo_pathway,satellite)
        print check_exist
        if check_exist == 1:
            pass
        else:
            break

			
        ########### MOVE TO NEW FIDUCEO/OBS_COMP ##############
        if ".nc" in filename: 
            print filename, "has been chosen"
            print '######################'
        else: 
            print "Not NETCDF - Skipping: ", filename
            print '######################'
            continue
			
			
        fileyear = filename[115:119]
        if not os.path.isdir('/gws/nopw/j04/fiduceo/Data/obs_comp/avhrr/%s/%s'%(satellite,fileyear)):
            print "Making a new diectory", satellite, fileyear
            print '######################' 
            os.makedirs('/gws/nopw/j04/fiduceo/Data/obs_comp/avhrr/%s/%s'%(satellite,fileyear))
			
			
        full_filename = full_mmd_path+'/'+filename

        os.system('cp %s /gws/nopw/j04/fiduceo/Data/obs_comp/avhrr/%s/%s'%(full_filename,satellite,fileyear))
        head,just_filename = os.path.split(full_filename)
        new_filename = '/gws/nopw/j04/fiduceo/Data/obs_comp/avhrr/%s/%s'%(satellite,fileyear)+just_filename

        print new_filename, "is where it is at now"
        print '######################'


        ########### EXTRACT NECESSARY DATA FROM MMD_FILE IN ORDER TO FIND FIDUCEO ###########

        data_dict = dex.mmd_data_extract(new_filename,obs_variable_names,other_variables)
        no_of_comparisons = len(data_dict[x_variable])

        ########## CREATE GROUP WHERE NEW FIDUCEO DATA WILL GO ###############
        new_fid_data = {}
        for var in fiduceo_named_variables:
            new_fid_data[var] = np.zeros([no_of_comparisons,7,7])

		
        ########## FOR EACH COMPARISON POINT - FIND L1C ORIGINAL FILE ##########
        for count in xrange(0,no_of_comparisons):
            testingcount = testingcount+1
            if testingcount == 100:
                break
            orig_filename = create.make_filename(data_dict[filename_variable][count])
            #print "Orig_filename: ",orig_filename

            ###### FIND CORRESPONDING L1B FILE FROM L1C FILE ########
            l1b_mmd_files = ff.find_l1b_l1c_files((make_filename(data_dict[version_variable][count])),orig_filename)
            ###### DETERMINE TIME OF COMPARISON ############
            #print np.shape(data_dict[time_variable])
            #print data_dict[time_variable][count,3,3]
            year,month,day,hour,minute,second = create.make_time(data_dict[time_variable][count,3,3])

            print "Date of mmd_file: ",year,"/",month,"/",day," ",hour,":",minute,":",second
			
			
			
			
            ###### FIND CORRESPONDING FIDUCEO FILE
            fid_avhrr = args.avhrr_sat.upper()
            fid_avhrr_sat = fid_avhrr[0:5] + fid_avhrr[7:9]
            fiduceo_folder,fiduceo_file_match,fid_pathway,f3split,f3split_file = ff.find_FIDUCEO_file(year,month,day,satellite,hour,minute,second,fiduceo_pathway)
            if fiduceo_file_match == 'False' or fiduceo_file_match == 'NotThere':
                print "Failed to find file"
                print '############' 
                continue
            else:
                if f3split == 'True':
                    which_channel,which_file = check.channel_3_check(f3split_file,fiduceo_file_match,fid_pathway,data_dict[time_variable][count,3,3])
                    if which_file == '3split':
                        full_fiduceo_file_match = fid_pathway+f3split_file
                    else:
                        full_fiduceo_file_match = fid_pathway+fiduceo_file_match
                else:
                    full_fiduceo_file_match = fid_pathway+fiduceo_file_match

  




            #Now, extract the variable data from fiduceo
            print fiduceo_file_match
			print '##############################'
			
			
            fid_l1b_file_number,fid_l1b_scanline,level1b_fid_files = dex.fiduceo_filenames_extract(fiduceo_folder+fiduceo_file_match) 
            level1b_fid_files = [str(x) for x in level1b_fid_files] 
            print level1b_fid_files, " fiduceo l1b file"
            print l1b_mmd_files, " mmd l1b file"
            l1b_mmd_files = l1b_mmd_files.split()
            l1b_mmd_file = l1b_mmd_files[0][0:-3]
            print fid_l1b_file_number, " l1b file number"
            #find the file_index (i.e, what file matches the l1b from mmd files)
            file_index = ff.fiduceo_file_ident(level1b_fid_files,l1b_mmd_file)
            #now find data and put in an empty 7x7 
            print '####################'
            print file_index
            print '####################'
            print 'This is the check'
            if file_index == 999:
               
               continue
			   
			   
            print '##############'
            print 'Check if we;re hitting this if file_index is not 999'
            print 'We have a match'
            x_value = data_dict[x_variable][count]

			
			
			
			#Find the corresponding 7 x 7 data grid around the drift buoy
            for x in xrange(-3,4):
                for y in xrange(-3,4):
                    fid_line_comp = ff.fiduceo_linenumber_find(file_index,data_dict[level_1b_linenumber_variable][count,x,y],fid_l1b_file_number,fid_l1b_scanline)
					
					
                    if fid_line_comp != 'False':
                        fid_data = dex.fiduceo_return_value(fiduceo_named_variables,fid_line_comp+y,x_value+x,full_fiduceo_file_match)
						
                        for var in fiduceo_named_variables:
                            new_fid_data[var][count,x+3,y+3] = fid_data[var]
							
							
                    else:
                        fiduceo_file_match_new = 'MaskedData'
                        fid_data = dex.fiduceo_return_value(fiduceo_named_variables,0,x_value+x,fiduceo_file_match_new) 
						
                        for var in fiduceo_named_variables:
                            print "Did I ever go here? I should be getting data from it"
                            new_fid_data[var][count,x+3,y+3] = fid_data[var]





        #####################################################
        ############  REPLACE DATA IN FILE  #################
        ############  DETERMINE IF ERRORS   #################
        #####################################################     


        if fiduceo_file_match == "False" or fiduceo_file_match == 'NotThere':
            print new_filename, 'not changed as no file available'

        elif file_index == 999:
            print new_filename, ' was not changed as l1b files do not match'
        else:
            if fiduceo_file_match_new == "MaskedData":
                print new_filename, 'contains some missing data'
            print "I should be replacing data now"
            check = create.replace_data(new_filename,obs_variable_names,fiduceo_named_variables,new_fid_data)
            print "Data replaced!"
        #replace_meta_data(new_filename,obs_variable_names)
            print check
			
			
