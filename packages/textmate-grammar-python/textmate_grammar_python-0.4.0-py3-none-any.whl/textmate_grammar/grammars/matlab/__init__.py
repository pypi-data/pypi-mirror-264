from __future__ import annotations

import plistlib
from pathlib import Path

import yaml

tmLanguageFile = (
    Path(__file__).parents[3]
    / "syntaxes"
    / "matlab"
    / "Matlab.tmbundle"
    / "Syntaxes"
    / "MATLAB.tmLanguage"
)
tmLanguageYAML = Path(__file__).parent / "grammar.yaml"


if tmLanguageFile.exists():
    with open(tmLanguageFile, "rb") as file:
        GRAMMAR = plistlib.load(file, fmt=plistlib.FMT_XML)
    with open(tmLanguageYAML, "w") as f:
        f.write(yaml.dump(GRAMMAR, indent=2))
else:
    with open(tmLanguageYAML) as file:
        try:
            GRAMMAR = yaml.load(file.read(), Loader=yaml.CLoader)
        except ImportError:
            GRAMMAR = yaml.load(file.read(), Loader=yaml.Loader)
