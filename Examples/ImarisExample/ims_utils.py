import h5py as h5

def read_text(attribute):
    return b"".join(attribute).decode()

def read_number(attribute):
    return float(read_text(attribute))

def load_ims(ims_file, resolution_level, channel=0):
    with h5.File(ims_file, "r") as ims:
        image_data= ims["DataSet"]["ResolutionLevel "+str(resolution_level)]['TimePoint 0']['Channel '+str(channel)]["Data"]

        size_bytes= image_data.size * image_data.dtype.itemsize
        size_gb= size_bytes/ (1024 ** 3)

        if size_gb > 1:
            raise ValueError(
             "Selected volume requires approximately "
             + str(round(size_gb, 2))
             + " GB of RAM."
            )

        volume= image_data[:]

        image_info = ims["DataSetInfo"]["Image"].attrs
        x_min = read_number(image_info["ExtMin0"])
        x_max = read_number(image_info["ExtMax0"])

        y_min = read_number(image_info["ExtMin1"])
        y_max = read_number(image_info["ExtMax1"])

        z_min = read_number(image_info["ExtMin2"])
        z_max = read_number(image_info["ExtMax2"])

        physical_x = x_max - x_min
        physical_y = y_max - y_min
        physical_z = z_max - z_min

        metadata = {
        "physical_size_um": (physical_x, physical_y, physical_z),
        "unit": read_text(image_info["Unit"])
        }
          
    return volume, metadata