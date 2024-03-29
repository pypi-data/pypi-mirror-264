from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = 'leoid',
    version = '1.0.13',
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
