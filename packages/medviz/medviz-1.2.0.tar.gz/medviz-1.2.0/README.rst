==============
MedViz
==============

MedViz is a Python package for medical image visualization. It provides a set of functions for visualizing medical images and masks. The package is built on top of the `matplotlib` and `nibabel` packages.

Installation
------------

To install the package, use pip:

.. code-block:: bash

    pip install medviz


Usage
-----

To use the package, import it in your Python code:

.. code-block:: python

    import medviz

    medviz.layered_plot(image_path="dataset/1-1.nii", mask_paths=["dataset/small_bowel.nii", "dataset/1-1-label.nii"], mask_colors=["red", "yellow"], title="Layered Plot")

The `layered_plot` function creates a layered plot of an image and one or more masks. The masks are overlaid on top of the image using the specified colors. The resulting plot can be used to visualize the location of structures or regions of interest in the image.


.. code-block:: python

    import medviz

    medviz.gif(
        image_path="dataset/1-1.nii",
        mask_paths=[
            "dataset/small_bowel.nii",
            "dataset/1-1-label.nii",
            "dataset/vertebrae_L3.nii.gz",
            "dataset/vertebrae_L4.nii.gz",
            "dataset/vertebrae_L5.nii.gz",
        ],
        mask_colors=["red", "yellow", "green", "blue", "purple"],
        title="Expert Annotations",
        interval=70,
        start_slice=30,
        end_slice=130,
        save_path="animation.gif",
    )

The `gif` function creates an animated GIF of an image and one or more masks. The masks are overlaid on top of the image using the specified colors. The resulting GIF can be used to visualize the location of structures or regions of interest in the image.

GitHub repository: [https://github.com/mohsenhariri/medviz](https://github.com/mohsenhariri/medviz)
