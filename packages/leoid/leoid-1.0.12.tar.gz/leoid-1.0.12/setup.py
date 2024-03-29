from setuptools import setup

setup(
    name = 'leoid',
    version = '1.0.12',
    author = 'Jay Ticku',
    description = 'LEOID Python Package',
    long_descrition =
"""\
## Python Package for Machine Learning Model LEOID (Level-based Ensemble for Overcoming Inbalanced Data)
\
More information about LEOID and example usage is available on Kaggle. [LEOID on Kaggle](https://www.kaggle.com/models/jayticku/leoid)
""",
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
