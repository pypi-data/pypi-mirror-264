import nibabel as nib
from skinsegmentator.python_api import skinsegmentator
from pathlib import Path

if __name__ == "__main__":
    input_path = '/Users/reubendo/Documents/repo/SkinSegmentator/test/Validation_T1_001_0000.nii.gz'
    output_path = '/Users/reubendo/Documents/repo/SkinSegmentator/test./'
    # option 1: provide input and output as file paths
    skinsegmentator(input_path, output_path)
    
    # import os
    # print(os.path.basename(input_path))
    
    # input_path = Path(input_path)
    # print(input_path.stem)
    # print(input_path.parent)

    # # option 2: provide input and output as nifti image objects
    # input_img = nib.load(input_path)
    # output_img  = skinsegmentator(input_img)
    # nib.save(output_img, output_path)