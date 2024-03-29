
# ADAPTED FROM TotalSegmentator: https://github.com/wasserth/TotalSegmentator/tree/master/totalsegmentator

from pathlib import Path
from typing import Union
from nibabel.nifti1 import Nifti1Image
import torch
from skinsegmentator.libs import download_pretrained_weights
from skinsegmentator.config import setup_nnunet, setup_skinseg
from skinsegmentator.config import get_config_key, set_config_key


def skinsegmentator(input: Union[str, Path, Nifti1Image], 
                     output: Union[str, Path, None]=None, 
                     nr_thr_resamp=1, nr_thr_saving=6,
                     fast=False, task="skin",
                     output_type="nifti", quiet=False, verbose=False,
                     skip_saving=False, device="gpu"):
    """
    Run SkinSegmentator from within python.

    For explanation of the arguments see description of command line
    arguments in bin/SkinSegmentator.

    Return: multilabel Nifti1Image
    """
    if not isinstance(input, Nifti1Image):
        input = Path(input)

    if output is not None:
        output = Path(output)
    else:
        skip_saving = True
        # raise ValueError("Output path is required.")

    # available devices: gpu | cpu | mps
    if device == "gpu": device = "cuda"
    if device == "cuda" and not torch.cuda.is_available():
        print("No GPU detected. Running on CPU. This can be very slow. The '--fast' option can help to reduce runtime.")
        device = "cpu"

    setup_nnunet()
    setup_skinseg()

    if not get_config_key("statistics_disclaimer_shown"):  # Evaluates to True is variable not set (None) or set to False
        print("SkinSegmentator sends anonymous usage statistics. If you want to disable it check the documentation.")
        set_config_key("statistics_disclaimer_shown", True)

    from skinsegmentator.nnunet import nnUNet_predict_image  # this has to be after setting new env vars

    crop_addon = [3, 3, 3]  # default value

    if task == "skin":
        if fast:
            task_id = 1
            resample = 3.0
            trainer = "nnUNetTrainer"
            if not quiet: print("Using 'fast' option: resampling to lower resolution (3mm)")
        else:
            task_id = 1
            resample = None
            trainer = "nnUNetTrainer"
            crop = None
        model = "3d_fullres"
        folds = ['all']

    if isinstance(input, Nifti1Image):
        img_type = "nifti"
    else:
        img_type = "nifti" if str(input).endswith(".nii") or str(input).endswith(".nii.gz") else "dicom"

    # fast statistics are calculated on the downsampled image
    download_pretrained_weights(task_id)

    folds = ['all']  # None
    seg_img = nnUNet_predict_image(input, output, task_id, model=model, folds=folds,
                            trainer=trainer, tta=False, resample=resample,
                            task_name=task,
                            nr_threads_resampling=nr_thr_resamp, nr_threads_saving=nr_thr_saving,
                            output_type=output_type,
                            quiet=quiet, verbose=verbose, skip_saving=skip_saving, device=device)

    return seg_img
