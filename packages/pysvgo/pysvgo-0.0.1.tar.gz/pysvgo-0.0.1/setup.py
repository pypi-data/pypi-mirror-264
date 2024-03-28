import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

pack_name = "pysvgo"
pack_version = "0.0.1"
pack_description = "SVG optimizer"

INSTALL_REQUIRES = []
PYTHON_REQUIRES = ">=3.7"

setuptools.setup(

    name=pack_name,  # project name /folder
    version=pack_version,
    author="René Horn",
    author_email="rene_horn@gmx.net",
    description=pack_description,
    long_description=long_description,
    license='MIT License',
    long_description_content_type="text/markdown",
    include_package_data=True,
    packages=setuptools.find_packages(),
    install_requires=INSTALL_REQUIRES,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
    ],
    python_requires=PYTHON_REQUIRES,
)
