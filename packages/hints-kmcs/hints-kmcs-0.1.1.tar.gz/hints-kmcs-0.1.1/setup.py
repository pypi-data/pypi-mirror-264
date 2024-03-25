from setuptools import setup, find_packages

def get_requirements():
    with open('requirements.txt') as req:
        return req.read().splitlines()

setup(
    name='hints-kmcs',
    version='0.1.1',
    author='Amin Akhshi',
    author_email='amin.akhshi@gmail.com',
    description='A package for calculating pairwise and higher-order interactions of N-dimensional state variables from measured time series',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/aminakhshi/hints',
    packages = find_packages(),
    install_requires=get_requirements(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Mathematics',
        'License :: OSI Approved :: MIT License', 
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    # package_dir = {"": "hints"},
    python_requires='>=3.8.1',
)
