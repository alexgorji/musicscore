import setuptools

setuptools.setup(
    name="musicscore",
    version="1.3.9",
    author="Alex Gorji",
    author_email="aligorji@hotmail.com",
    description="generating musicxml",
    url="https://github.com/alexgorji/musicscore.git",
    packages=setuptools.find_packages(),
    install_requires=['lxml',
                      'quicktions'
                      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)
