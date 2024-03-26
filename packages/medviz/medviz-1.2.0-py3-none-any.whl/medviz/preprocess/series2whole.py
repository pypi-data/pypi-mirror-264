import os

import nibabel as nib
import numpy as np
import pydicom


def _create_affine(slices):
    spacing = map(float, ([slices[0].SliceThickness] + slices[0].PixelSpacing))
    spacing = np.array(list(spacing))
    affine = np.diag(np.append(spacing, [1]))

    return affine


def series2whole(dicom_dir, save_path):
    try:
        slices = [
            pydicom.dcmread(os.path.join(dicom_dir, f)) for f in os.listdir(dicom_dir)
        ]
        slices.sort(key=lambda x: float(x.ImagePositionPatient[2]))

        images = np.stack([s.pixel_array for s in slices])

        transposed_images = np.transpose(images, (1, 2, 0))

        nib.save(nib.Nifti1Image(transposed_images, np.eye(4)), save_path)

    except Exception as e:
        print(e)
