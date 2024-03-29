"""Functions to define, validate and generate presets."""

import os
import json

DEFAULT_PRESETS = pdict = {
    "color_seq": ["blue", "red", "green", "orange"],
    "linestyle_seq": ["-", "--", ":", "-."],
    "m": {
        "width": 15,
        "height": 10,
        "fontfamily": "sans-serif",
        "fontsize": 12,
        "linewidth": 2,
    },
    "s": {
        "width": 10,
        "height": 8,
        "fontfamily": "sans-serif",
        "fontsize": 12,
        "linewidth": 2,
    },
    "l": {
        "width": 20,
        "height": 15,
        "fontfamily": "sans-serif",
        "fontsize": 12,
        "linewidth": 3,
    },
    "ol": {
        "width": 8,
        "height": 6,
        "fontfamily": "serif",
        "fontsize": 9,
        "linewidth": 1,
    },
    "oe": {
        "width": 12,
        "height": 8,
        "fontfamily": "serif",
        "fontsize": 10,
        "linewidth": 1,
    },
    "square": {
        "width": 10,
        "height": 10,
        "fontfamily": "serif",
        "fontsize": 10,
        "linewidth": 1,
    },
    "colors": {
        "blue": [33, 101, 146],
        "red": [218, 4, 19],
        "green": [70, 173, 52],
        "orange": [235, 149, 0],
        "yellow": [255, 242, 0],
        "grey": [64, 64, 64],
    },
}


def define_presets(presets=None):
    """Define default presets for fast_fig."""
    # define defaults in preset dictionary
    pdict = DEFAULT_PRESETS.copy()

    # Overwrite defaults with presets from fast_fig_presets.json
    if os.path.isfile("fast_fig_presets.json"):
        pdict.update(load_json("fast_fig_presets.json"))

    # Overwrite defaults with presets from given JSON file
    if isinstance(presets, str) and os.path.isfile(presets):
        pdict.update(load_json(presets))

    # Overwrite defaults with specific values
    if isinstance(presets, dict):
        pdict.update(presets)

    for key in pdict:
        if key not in ["colors", "color_seq", "linestyle_seq", "linewidth_seq"]:
            pdict[key] = validate_preset(pdict[key])

    return pdict


def validate_preset(preset):
    """Validate preset and set defaults"""
    preset.setdefault("width", 15)
    preset.setdefault("height", 10)
    preset.setdefault("fontfamily", "sans-serif")
    preset.setdefault("fontsize", 12)
    preset.setdefault("linewidth", 2)
    return preset


def load_json(filepath):
    """loads a preset from a JSON file

    Args:
        filepath (str, optional): JSON file path. Defaults to "fast_fig_presets.json".
    """
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"File not found: '{filepath}'")
    except IOError as e:
        print(f"IOError when reading '{filepath}': {e}")
    except json.JSONDecodeError as e:
        print(f"An unexpected error occurred while reading '{filepath}': {e}")

    return data


def generate_example(filepath="fast_fig_presets_example.json"):
    """generates a preset example that can be modified for custom presets

    Args:
        filepath (str, optional): JSON file path. Defaults to "fast_fig_presets_example.json".
    """

    example_dict = define_presets()
    # write example_dict to JSON file
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(example_dict, file)
