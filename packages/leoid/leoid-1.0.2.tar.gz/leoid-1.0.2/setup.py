from setuptools import setup

setup(
    name = 'leoid',
    version = '1.0.2',
    author = 'Jay Ticku',
    description = 'LEOID Python Package',
    install_requires = [
        'scikit-learn>=1.4.1.post1'
    ],
    classifiers=[
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)
