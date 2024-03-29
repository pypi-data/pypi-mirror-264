# SkinSegmentator

This repository is adapted from [TotalSegmentator](https://github.com/wasserth/TotalSegmentator/)

### Installation

SkinSegmentator works on Ubuntu, Mac, and Windows and on CPU and GPU.

Install dependencies:
* Python >= 3.9
* [Pytorch](http://pytorch.org/) >= 2.0.0

Install SkinSegmentator
```
pip install skinsegmentator
```


### Usage
```
SkinSegmentator -i mr.nii.gz -o segmentations
```
> Note: A Nifti file or a folder with all DICOM slices of one patient is allowed as input

> Note: If you run on CPU use the option `--fast` to greatly improve runtime.

> Note: This is not a medical device and is not intended for clinical usage.



### Python API
You can run SkinSegmentator via Python:
```python
import nibabel as nib
from skinsegmentator.python_api import skinsegmentator

if __name__ == "__main__":
    input_path = 'test/Validation_T1_001_0000.nii.gz'
    output_path = 'test/skin.nii.gz'
    # option 1: provide input and output as file paths
    skinsegmentator(input_path, output_path) 

    input_path = 'test/Validation_T1_001_0000.nii.gz'
    output_dir = 'test/'
    # option 2: provide input file path and output dir
    skinsegmentator(input_path, output_dir) 

    # option 3: provide input and output nifti image objects
    input_img = nib.load(input_path)
    output_img = skinsegmentator(input_img)
    nib.save(output_img, output_path)
```
You can see all available arguments [here](https://github.com/reubendo/SkinSegmentator/blob/master/SkinSegmentator/python_api.py). Running from within the main environment should avoid some multiprocessing issues.

### Install latest master branch (contains latest bug fixes)
```
pip install git+https://github.com/reubendo/SkinSegmentator.git
```

### Typical problems

**ITK loading Error**
When you get the following error message
```
ITK ERROR: ITK only supports orthonormal direction cosines. No orthonormal definition was found!
```
you should do
```
pip install SimpleITK==2.0.2
```

Alternatively you can try
```
fslorient -copysform2qform input_file
fslreorient2std input_file output_file
```


### Reference
TODO

