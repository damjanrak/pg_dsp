import os
import pg_dsp
from pygears.conf.registry import registry, bind

svlib_dir = os.path.join(
    os.path.dirname(pg_dsp.__file__), 'utils', 'custom_gears', 'svlib')

registry('svgen/sv_paths').append(svlib_dir)
# bind('svgen/debug_intfs', ['*'])
