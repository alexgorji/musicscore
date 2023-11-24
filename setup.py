import setuptools
from pathlib import Path

long_description = (Path(__file__).parent / "README.rst").read_text()
setuptools.setup(
    name="musicscore",
    version="2.0.2",
    author="Alex Gorji",
    author_email="aligorji@hotmail.com",
    description="Generating musicxml files.",
    url="https://github.com/alexgorji/musicscore.git",
    packages=setuptools.find_packages(),
    install_requires=['musicxml==1.4', 'quicktions'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    long_description=long_description,
    long_description_content_type='text/x-rst',
    include_package_data=True
)
