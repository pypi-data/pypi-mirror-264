from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name = 'leoid',
    version = '1.0.14',
    author = 'Jay Ticku',
    description = 'LEOID Python Package',
    long_descrition = long_description,
    long_description_content_type='text/markdown',
    install_requires = [
        'imbalanced-learn==0.12.0'
    ],
    classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: Apache Software License',
    'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
    include_package_data = True
)
