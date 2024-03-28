from setuptools import setup, find_packages

# Read requirements.txt and use it for the install_requires parameter
with open('requirements.txt') as f:
    requirements_list = f.read().splitlines()

setup(
    name='cleankit',
    version='0.0.2',
    author='Sacha Ichbiah',
    author_email='sacha@cu6e.com',
    description='Simple operations for navigation',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/cubelogistics/cleankit',
    project_urls={
        'Team website': 'https://github.com/cubelogistics'
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
        'Intended Audience :: Science/Research'
    ],
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.6',
    install_requires=requirements_list,
    package_data={
        'cleankit': ['data/*.csv'],
    },
    include_package_data=True
)