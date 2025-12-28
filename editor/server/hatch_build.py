import glob
import os
import shutil
from pathlib import Path
from typing import Any

from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class CustomBuildHook(BuildHookInterface):
    def initialize(self, version: str, build_data: dict[str, Any]):
        src = Path(self.root).parent.parent / 'examples' / '*.json'
        dst = Path(self.root) / 'app' / 'data' / 'examples'
        os.makedirs(dst, exist_ok=True)
        for file in glob.glob(str(src)):
            print(f'Copy {file} to {dst}')
            shutil.copy(file, dst)
