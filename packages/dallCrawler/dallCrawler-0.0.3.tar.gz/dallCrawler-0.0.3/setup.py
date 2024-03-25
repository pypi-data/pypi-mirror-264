from setuptools import setup, find_packages

VERSION = '0.0.3' 
DESCRIPTION = 'Crawler for crawling sites'
LONG_DESCRIPTION = 'Dall company crawler'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="dallCrawler", 
        version=VERSION,
        author="Mostafa Amiri",
        author_email="<mostafa.amiri.62@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        readme = "README.md",
        packages=find_packages(),
        install_requires=['requests'], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'crawler', 'dall company'],
        classifiers= [
                "Programming Language :: Python :: 3",
                "License :: OSI Approved :: MIT License",
                "Operating System :: OS Independent",
        ]
)