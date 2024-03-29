# setup.py

from setuptools import setup, find_packages

setup(
    name='dis_bg_remover',
    version='0.1.1',
    author='Amit',
    author_email='amit@pulpdata.com.au',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'opencv-python',
        'onnxruntime',
    ],
    description='Highly Accurate Dichotomous Image Segmentation',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
