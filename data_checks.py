##### data checks


import numpy as np
import os




 
def initial_check(filename,fid_filepath,satellite):
    year = int(filename[41:45])
    first_day = int(filename[37:40])
    last_day = int(filename[46:49])
    ftime = datetime.datetime(year,1,2) + datetime.timedelta(first_day)
    ltime = datetime.datetime(year,1,2) + datetime.timedelta(last_day)
    fday = int(ftime.strftime('%d'))
    lday = int(ltime.strftime('%d'))
    fmon = int(ftime.strftime('%m'))
    lmon = int(ltime.strftime('%m'))
    fid_check = 0
    if fmon == lmon:
       for i in xrange(fday,lday):
           full_file = fid_filepath+satellite+'/'+str(year)+'/'+str(fmon).zfill(2)+'/'+str(i).zfill(2)
           try:
               os.listdir(full_file)
           except:
               print full_file, " doesn't exist"
           else:
               fid_check = 1
               print full_file, " exists"
               return fid_check
    else:
       print "Check cannot be performed - months cross"
 
       
    return fid_check




def channel_3_check(f3split_file,fiduceo_file_match,fid_pathway,epoch_time):
    print "Doing a 3a/3b check"
    full_file = fid_pathway+fiduceo_file_match
    try:
        dataS = Dataset(full_file,'r')
    except:
        try: 
            dataS = Dataset(fid_pathway+f3split_file,'r')

        except:
            print "Both files failed: ", full_file

    if '3A' in fiduceo_file_match: 
        Ch3_data = dataS.variables['Ch3a'][:]

        file_times = dataS.variables['Time'][:]
        for i in xrange(0,len(file_times)):
            if epoch_time == int(np.ma.getdata(file_times[i])):
                print "Time has matched"
                if np.nanmax(Ch3_data[i]) == 0.0:
                    which_channel = '3B'
                    which_file = "3Split"
                else:
                    which_channel = '3A'
                    which_file = "fid_file"
                dataS.close()
                return which_channel,which_file
                     
    elif '3B' in fiduceo_file_match:
        Ch3_data = dataS.variables['Ch3b'][:]
        file_times = dataS.variables['Time'][:]
        for i in xrange(0,len(file_times)):
            if epoch_time == int(np.ma.getdata(file_times[i])):
                print "Time has matched"
                if np.nanmax(Ch3_data[i]) < 20.0:
                    which_channel = '3A'
                    which_file = "3Split"
                else:
                    which_channel = '3B'
                    which_file = "fid_file"
                dataS.close()
                return which_channel,which_file   

    data.close()
    return which_channel,which_file