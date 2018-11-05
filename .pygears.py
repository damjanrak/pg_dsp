import os
import dsp_hw_designs
from pygears.conf.registry import registry

svlib_dir = os.path.join(
    os.path.dirname(dsp_hw_designs.__file__), 'utils', 'custom_gears', 'svlib')

registry('svgen/sv_paths').append(svlib_dir)
