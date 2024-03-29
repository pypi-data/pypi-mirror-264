from setuptools import setup, find_packages

setup(
name='test_app_1001',
version='0.1.0',
author='Hamze',
author_email='hamze.najeeb@gmail.com',
description='testing the distribution procedure',
packages=find_packages(),
classifiers=[
'Programming Language :: Python :: 3',
'Operating System :: OS Independent',
],
python_requires='>=3.6',
entry_points={"console_scripts": ["test_app = test_app.test_app:add_one"]},
)