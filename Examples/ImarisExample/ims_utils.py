import h5py as h5

def load_ims(ims_file, resolution_level, channel=0):
    with h5.File(ims_file, "r") as ims:
        image_data= ims["DataSet"]["ResolutionLevel "+str(resolution_level)]['TimePoint 0']['Channel '+str(channel)]["Data"]
        volume= image_data[:]
        
    return volume