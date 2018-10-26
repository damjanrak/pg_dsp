from setuptools import setup, find_packages

setup(
    name='dsp_hw_designs',
    version='0.0.1',
    description="implementation of dsp algorithms using pygears",
    packages=find_packages(exclude=['doc']),
)
