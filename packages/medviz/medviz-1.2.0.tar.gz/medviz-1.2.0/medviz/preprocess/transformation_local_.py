from pathlib import Path

import numpy as np
import pydicom

p = Path("/storage/sync/git/test/multi/unzip")

for pp in p.glob("**/*.dcm"):
    dicom_file = pydicom.dcmread(pp)
    pixel_array = dicom_file.pixel_array
    rescale_slope = dicom_file.RescaleSlope
    rescale_intercept = dicom_file.RescaleIntercept

    # print(rescale_slope, rescale_intercept)
    # HU=Pixel Value×Rescale Slope+Rescale Intercept

    hu_image = pixel_array * rescale_slope + rescale_intercept

    save_path = pp.with_suffix(".npz")
    np.savez_compressed(save_path, hu_image=hu_image)

    # exit()
