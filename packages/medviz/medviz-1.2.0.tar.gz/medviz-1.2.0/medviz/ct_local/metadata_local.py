# from pathlib import Path
# from typing import Any, Dict, Optional, Union

# import nibabel as nib
# import pandas as pd
# from tabulate import tabulate

# from ..utils import path_in, save_path_file


# def metadata(
#     image_path: Union[str, Path], save_csv: Optional[Union[str, Path]] = None
# ) -> Dict[str, Any]:
#     """
#     Extracts and optionally saves metadata from a NIFTI image.

#     Parameters:
#         image_path: Union[str, Path] - The path to the NIFTI image.
#         save_csv: Optional[Union[str, Path]] - The path where to save the metadata as a CSV file.

#     Returns:
#         A dictionary containing the metadata.
#     """
#     image_path = path_in(image_path)

#     # needs refactoring, remove Any
#     image_info: Dict[str, Any] = {}

#     try:
#         image = nib.load(image_path)
#     except nib.filebasedimages.ImageFileError:
#         print(f"Error: {image_path} is not a valid NIFTI image.")
#         return image_info

#     image_data = image.get_fdata()
#     image_header = image.header
#     image_obj = image.dataobj
#     affine = image.affine

#     slope_obj, intercept_obj = image_obj.slope, image_obj.inter

#     is_hu_obj = slope_obj == 1 and intercept_obj <= 0

#     dimensions = image_data.shape
#     voxel_size = image_header.get_zooms()[:3]

#     # Get spatial and temporal units
#     spatial_units, temporal_units = image_header.get_xyzt_units()

#     # Get slope and intercept for Hounsfield Unit (HU) conversion
#     slope, intercept = image_header.get_slope_inter()[:2]

#     # Determine if the image is in HU format
#     is_hu_format = slope == 1 and intercept <= 0

#     # Check if the image is isotropic
#     is_isotropic = all(size == voxel_size[0] for size in voxel_size)

#     # Store the information in the dictionary
#     image_info["dimensions"] = dimensions
#     image_info["voxel_size"] = voxel_size
#     image_info["spatial_units"] = spatial_units
#     image_info["temporal_units"] = temporal_units
#     image_info["slope"] = slope
#     image_info["slope_obj"] = slope_obj
#     image_info["intercept"] = intercept
#     image_info["intercept_obj"] = intercept_obj
#     image_info["is_hu_obj"] = is_hu_obj
#     image_info["is_hu"] = is_hu_format
#     image_info["is_isotropic"] = is_isotropic

#     if save_csv:
#         image_info["name"] = Path(image_path).stem

#         keys = list(image_info.keys())

#         values = list(image_info.values())

#         df = pd.DataFrame([values], columns=keys)
#         csv_path = save_path_file(save_csv, suffix=".csv")

#         df.to_csv(csv_path, index=False)
#     else:
#         print(tabulate(image_info.items(), tablefmt="fancy_grid"))

#     return image_info


from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import nibabel as nib
import numpy as np
import pandas as pd
import pydicom
import SimpleITK as sitk
from tabulate import tabulate

from ..utils import path2loader, path_in, save_path_file

# def metadata_nibabel(image_and_properties):
#     image_info: Dict[str, Any] = {}

#     image_data = image_and_properties.get_fdata()
#     image_header = image_and_properties.header
#     image_obj = image_and_properties.dataobj
#     affine = image_and_properties.affine

#     slope_obj, intercept_obj = image_obj.slope, image_obj.inter

#     is_hu_obj = slope_obj == 1 and intercept_obj <= 0

#     dimensions = image_data.shape
#     voxel_size = image_header.get_zooms()[:3]

#     # Get spatial and temporal units
#     spatial_units, temporal_units = image_header.get_xyzt_units()

#     # Get slope and intercept for Hounsfield Unit (HU) conversion
#     slope, intercept = image_header.get_slope_inter()[:2]

#     # Determine if the image is in HU format
#     is_hu_format = slope == 1 and intercept <= 0

#     # Check if the image is isotropic
#     is_isotropic = all(size == voxel_size[0] for size in voxel_size)

#     # Store the information in the dictionary
#     image_info["dimensions"] = dimensions
#     image_info["voxel_size"] = voxel_size
#     image_info["spatial_units"] = spatial_units
#     image_info["temporal_units"] = temporal_units
#     image_info["slope"] = slope
#     image_info["slope_obj"] = slope_obj
#     image_info["intercept"] = intercept
#     image_info["intercept_obj"] = intercept_obj
#     image_info["is_hu_obj"] = is_hu_obj
#     image_info["is_hu"] = is_hu_format
#     image_info["is_isotropic"] = is_isotropic

#     return image_info


def _metadata_nibabel(image_and_properties: nib.Nifti1Image) -> Dict[str, Any]:
    """
    Extracts metadata from a NIfTI image using Nibabel.

    Parameters:
    image_and_properties (nib.Nifti1Image): A NIfTI image object.

    Returns:
    Dict[str, Any]: A dictionary containing image metadata.
    """
    try:
        image_info: Dict[str, Any] = {}

        image_data = image_and_properties.get_fdata()
        image_header = image_and_properties.header
        image_obj = image_and_properties.dataobj
        affine = image_and_properties.affine

        slope_obj, intercept_obj = image_obj.slope, getattr(image_obj, "inter", 0)

        is_hu_obj = slope_obj == 1 and intercept_obj <= 0

        dimensions = image_data.shape
        voxel_size = image_header.get_zooms()[:3]

        # Get spatial and temporal units
        spatial_units, temporal_units = image_header.get_xyzt_units()

        # Get slope and intercept for Hounsfield Unit (HU) conversion
        slope, intercept = image_header.get_slope_inter()[:2]

        # Determine if the image is in HU format
        is_hu_format = slope == 1 and intercept <= 0

        # Check if the image is isotropic
        is_isotropic = np.allclose(voxel_size, voxel_size[0])

        # Store the information in the dictionary
        image_info = {
            "dimensions": dimensions,
            "voxel_size": voxel_size,
            "spatial_units": spatial_units,
            "temporal_units": temporal_units,
            "slope": slope,
            "slope_obj": slope_obj,
            "intercept": intercept,
            "intercept_obj": intercept_obj,
            "is_hu_obj": is_hu_obj,
            "is_hu": is_hu_format,
            "is_isotropic": is_isotropic,
        }

        return image_info
    except AttributeError as e:
        raise ValueError(f"An attribute error occurred: {e}")


def _metadata_pydicom(image_and_properties) -> Dict[str, Any]:
    """
    Extracts extended metadata from a DICOM file using pydicom.

    Parameters:
    file_path (str): The file path to the DICOM image.

    Returns:
    Dict[str, Any]: A dictionary containing extended image metadata.
    """
    try:
        # Read the DICOM file
        ds = image_and_properties
        

        # Extracting basic metadata
        patient_id = getattr(ds, "PatientID", "N/A")
        patient_name = getattr(ds, "PatientName", "N/A")
        study_id = getattr(ds, "StudyID", "N/A")
        study_date = getattr(ds, "StudyDate", "N/A")
        series_number = getattr(ds, "SeriesNumber", "N/A")
        modality = getattr(ds, "Modality", "N/A")
        manufacturer = getattr(ds, "Manufacturer", "N/A")

        # Extracting pixel spacing, slice thickness, image position and orientation if available
        pixel_spacing = getattr(ds, "PixelSpacing", "N/A")
        slice_thickness = getattr(ds, "SliceThickness", "N/A")
        image_position = getattr(ds, "ImagePositionPatient", "N/A")
        image_orientation = getattr(ds, "ImageOrientationPatient", "N/A")

        # Extracting image dimensions
        dimensions = (
            (int(ds.Rows), int(ds.Columns))
            if "Rows" in ds and "Columns" in ds
            else "N/A"
        )

        # Store the information in the dictionary
        image_info = {
            "patient_id": patient_id,
            "patient_name": patient_name,
            "study_id": study_id,
            "study_date": study_date,
            "series_number": series_number,
            "modality": modality,
            "manufacturer": manufacturer,
            "pixel_spacing": pixel_spacing,
            "slice_thickness": slice_thickness,
            "image_position": image_position,
            "image_orientation": image_orientation,
            "dimensions": dimensions,
        }

        return image_info
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except Exception as e:
        raise RuntimeError(f"An error occurred while reading the DICOM file: {e}")


def _metadata_sitk(image_and_properties) -> Dict[str, Any]:
    """
    Extracts metadata from an image file using SimpleITK.

    Parameters:
    file_path (str): The file path to the image.

    Returns:
    Dict[str, Any]: A dictionary containing image metadata.
    """
    try:
        # Read the image file
        # image = sitk.ReadImage(file_path)
        image = image_and_properties

        # Extracting metadata
        metadata_keys = image.GetMetaDataKeys()
    
        
        # metadata = {key: image.GetMetaData(key) for key in metadata_keys}
        metadata= {}

        # Adding additional information about the image
        metadata["spacing"] = image.GetSpacing()
        metadata["origin"] = image.GetOrigin()
        metadata["direction"] = image.GetDirection()
        metadata["size"] = image.GetSize()
        metadata[
            "number_of_components_per_pixel"
        ] = image.GetNumberOfComponentsPerPixel()

        return metadata
    except RuntimeError as e:
        raise RuntimeError(f"An error occurred while reading the image file: {e}")


# Example usage:
# metadata = metadata_simpleitk('path_to_image.dcm')
# print(metadata)


def metadata(
    image_paths: Union[List[Union[str, Path]], Union[str, Path]],
    save_csv: Optional[Union[str, Path]] = None,
) -> List[Dict[str, Any]]:
    """
    Extracts and optionally saves metadata from one or more NIFTI images.

    Parameters:
        image_paths: Union[List[Union[str, Path]], Union[str, Path]] - The paths to the NIFTI images.
        save_csv: Optional[Union[str, Path]] - The path where to save the metadata as a CSV file.

    Returns:
        A list of dictionaries, each containing the metadata for one image.
    """

    if not isinstance(image_paths, list):
        image_paths = [image_paths]

    all_image_info = []

    for image_path in image_paths:
        image_path = path_in(image_path)
        # image_info: Dict[str, Any] = {}

        # try:
        #     image = nib.load(image_path)
        # except nib.filebasedimages.ImageFileError:
        #     print(f"Error: {image_path} is not a valid NIFTI image.")
        #     continue

        try:
            image_and_properties, reader, image_and_properties_itk = path2loader(
                image_path
            )

        except Exception as e:
            print("Error reading image", e)

            raise e

        print(reader)

        merged_dict = _metadata_sitk(image_and_properties_itk)

        if reader == "nibabel":
            metadata_nib = _metadata_nibabel(image_and_properties)
            merged_dict = {**merged_dict, **metadata_nib}
            

        elif reader == "pydicom":
            metadata_dicom = _metadata_pydicom(image_and_properties)
            merged_dict = {**merged_dict, **metadata_dicom}
            

        # print(merged_dict)

        # break

        #     image_data = image.get_fdata()
        #     image_header = image.header
        #     image_obj = image.dataobj
        #     affine = image.affine

        #     slope_obj, intercept_obj = image_obj.slope, image_obj.inter

        #     is_hu_obj = slope_obj == 1 and intercept_obj <= 0

        #     dimensions = image_data.shape
        #     voxel_size = image_header.get_zooms()[:3]

        #     # Get spatial and temporal units
        #     spatial_units, temporal_units = image_header.get_xyzt_units()

        #     # Get slope and intercept for Hounsfield Unit (HU) conversion
        #     slope, intercept = image_header.get_slope_inter()[:2]

        #     # Determine if the image is in HU format
        #     is_hu_format = slope == 1 and intercept <= 0

        #     # Check if the image is isotropic
        #     is_isotropic = all(size == voxel_size[0] for size in voxel_size)

        # # Store the information in the dictionary
        # image_info["dimensions"] = dimensions
        # image_info["voxel_size"] = voxel_size
        # image_info["spatial_units"] = spatial_units
        # image_info["temporal_units"] = temporal_units
        # image_info["slope"] = slope
        # image_info["slope_obj"] = slope_obj
        # image_info["intercept"] = intercept
        # image_info["intercept_obj"] = intercept_obj
        # image_info["is_hu_obj"] = is_hu_obj
        # image_info["is_hu"] = is_hu_format
        # image_info["is_isotropic"] = is_isotropic
        # image_info["name"] = image_path.stem

        # # ... (rest of your code for extracting metadata) ...

        all_image_info.append(merged_dict)

    if save_csv:
        csv_path = save_path_file(save_csv, suffix=".csv")
        df = pd.DataFrame(all_image_info)
        df.to_csv(csv_path, index=False)

    else:
        for info in all_image_info:
            print(tabulate(info.items(), tablefmt="fancy_grid"))

    return all_image_info
