from setuptools import setup, find_packages

# Package metadata
NAME = 'Calculator_tvaino'
DESCRIPTION = 'Performs basic arithmetic operations'
URL = 'https://github.com/TuringCollegeSubmissions/tvaino-DWWP.1.5/tree/master/Calculator_pack'
AUTHOR = 'Tomas Vainoras'
EMAIL = 'vainoras@gmail.com'
VERSION = '0.0.4'

# Package dependencies
INSTALL_REQUIRES = [
    # List your dependencies here
]

# Additional package metadata
CLASSIFIERS = [
    'Programming Language :: Python :: 3',
    # Add more classifiers as needed
]

# Package setup
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    url=URL,
    author=AUTHOR,
    author_email=EMAIL,
    classifiers=CLASSIFIERS,
    install_requires=INSTALL_REQUIRES,
    long_description= open('README.md').read(),
    long_description_content_type='text/markdown',
    package_dir={"": "src"},
    packages=find_packages(where="src")

    # extras_require=EXTRAS_REQUIRE,
)