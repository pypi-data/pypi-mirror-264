from setuptools import setup, find_packages
setup(
    name='NordicUARTSerialDriver',
    version='0.1.1',
    author='Lidor Shimoni',
    author_email='lidor.shim@gmail.com',
    description='A virtual serial interface for communications over NordicUART',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

