import setuptools
from pathlib import Path

long_description = (Path(__file__).parent / "README.rst").read_text()
setuptools.setup(
    name="musicscore2",
    version="1.3",
    author="Alex Gorji",
    author_email="aligorji@hotmail.com",
    description="Generating musicxml files.",
    url="https://github.com/alexgorji/musicscore2.git",
    packages=setuptools.find_packages(),
    install_requires=['musicxml', 'quicktions'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    long_description=long_description,
    long_description_content_type='text/x-rst',
    include_package_data=True
)
