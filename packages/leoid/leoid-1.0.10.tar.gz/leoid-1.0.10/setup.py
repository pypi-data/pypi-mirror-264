from setuptools import setup

setup(
    name = 'leoid',
    version = '1.0.10',
    author = 'Jay Ticku',
    description = 'LEOID Python Package',
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
