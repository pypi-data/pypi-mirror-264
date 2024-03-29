from setuptools import setup, find_packages

VERSION = '0.0.5' 
DESCRIPTION = 'A navigation calculator that is compatible with the CITROS Data Analysis package'
LONG_DESCRIPTION = 'this navigation calculator has a variaty of functions that giving different navigation errors such as angular errors, vector erros, axes transformations etc.'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="citrosNavigationCalc", 
        version=VERSION,
        author="Boaz Gavriel",
        author_email="<boaz@lulav.space>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)