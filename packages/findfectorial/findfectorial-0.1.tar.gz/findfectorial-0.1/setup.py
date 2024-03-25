from setuptools import setup, find_packages

setup(
    name='findfectorial',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'fectorial = fectorial.fectorial:main'
        ]
    },
    author='Sajal Sisodia',
    author_email='sajal89304@gmail.com',
    description='A package for calculating factorial.',
    url='https://github.com/Sam-Sisodia/fectorial_calculate.git',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
