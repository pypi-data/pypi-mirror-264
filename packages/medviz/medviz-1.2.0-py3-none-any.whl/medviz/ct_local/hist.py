import matplotlib.pyplot as plt
import numpy as np
import SimpleITK as sitk


def hu_hist(image_path):
    # Read the image
    image = sitk.ReadImage(image_path)

    # Convert the image to a NumPy array
    image_array = sitk.GetArrayFromImage(image)

    # Create a histogram
    plt.figure(figsize=(10, 6))
    plt.hist(image_array.flatten(), bins=50, color="c")
    plt.title("Histogram of Hounsfield Units (HU)")
    plt.xlabel("Hounsfield Units (HU)")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.show()
