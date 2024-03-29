# ADAPTED FROM TotalSegmentator: https://github.com/wasserth/TotalSegmentator/tree/master/totalsegmentator

import os
import random
import json
import string
from pathlib import Path
import pkg_resources


def get_skinseg_dir():
    skinseg_dir = Path(__file__).parent.resolve()
    return skinseg_dir


def get_weights_dir():
    skinseg_dir = get_skinseg_dir()
    config_dir = skinseg_dir / "weights/results"
    return config_dir


def setup_nnunet():
    # check if environment variable skinsegmentator_config is set
    config_dir = get_skinseg_dir()
    weights_dir = config_dir / "weights/results"

    # This variables will only be active during the python script execution. Therefore
    # we do not have to unset them in the end.
    os.environ["nnUNet_raw"] = str(weights_dir)  # not needed, just needs to be an existing directory
    os.environ["nnUNet_preprocessed"] = str(weights_dir)  # not needed, just needs to be an existing directory
    os.environ["nnUNet_results"] = str(weights_dir)


def setup_skinseg(totalseg_id=None):
    skinseg_dir = get_skinseg_dir()
    skinseg_dir.mkdir(exist_ok=True)
    totalseg_config_file = skinseg_dir / "config.json"

    if totalseg_config_file.exists():
        with open(totalseg_config_file) as f:
            config = json.load(f)
    else:
        if totalseg_id is None:
            totalseg_id = "totalseg_" + ''.join(random.Random().choices(string.ascii_uppercase + string.digits, k=8))
        config = {
            "totalseg_id": totalseg_id,
            "send_usage_stats": True,
            "prediction_counter": 0
        }
        with open(totalseg_config_file, "w") as f:
            json.dump(config, f, indent=4)

    return config


def increase_prediction_counter():
    skinseg_dir = get_skinseg_dir()
    totalseg_config_file = skinseg_dir / "config.json"
    if totalseg_config_file.exists():
        with open(totalseg_config_file) as f:
            config = json.load(f)
        config["prediction_counter"] += 1
        with open(totalseg_config_file, "w") as f:
            json.dump(config, f, indent=4)
        return config


def get_version():
    try:
        return pkg_resources.get_distribution("skinsegmentator").version
    except pkg_resources.DistributionNotFound:
        return "unknown"


def get_config_key(key_name):
    skinseg_dir = get_skinseg_dir()
    totalseg_config_file = skinseg_dir / "config.json"
    if totalseg_config_file.exists():
        with open(totalseg_config_file) as f:
            config = json.load(f)
        if key_name in config:
            return config[key_name]
    return None


def set_config_key(key_name, value):
    skinseg_dir = get_skinseg_dir()
    totalseg_config_file = skinseg_dir / "config.json"
    if totalseg_config_file.exists():
        with open(totalseg_config_file) as f:
            config = json.load(f)
        config[key_name] = value
        with open(totalseg_config_file, "w") as f:
            json.dump(config, f, indent=4)
        return config
    else:
        print("WARNING: Could not set config key, because config file not found.")

