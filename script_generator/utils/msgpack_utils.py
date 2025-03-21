import os
import time

import numpy as np

import json
import msgpack
from script_generator.debug.logger import log


def load_msgpack_json(output_path):
    msgpack_path = output_path
    json_path = output_path.replace(".msgpack", ".json")

    if os.path.exists(msgpack_path):
        try:
            with open(msgpack_path, "rb") as f:
                return msgpack.unpackb(f.read(), raw=False, strict_map_key=False)
        except Exception as e:
            log.error(f"Failed to load from msgpack: {e}")
            raise

    raise FileNotFoundError(f"Neither msgpack nor JSON file exists at {output_path}")

def save_msgpack_json(path, data):
    start_time = time.time()
    try:
        with open(path, "wb") as f:
            f.write(msgpack.packb(data, use_bin_type=True, default=_default_serializer))
        log.info(f"Data saved to msgpack in {(time.time() - start_time) * 1000}ms: {path}")
    except Exception as e:
        log.error(f"Failed to save to msgpack: {e}")
        raise

def _default_serializer(obj):
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    else:
        raise TypeError(f"Object of type {obj.__class__.__name__} is not msgpack serializable")
