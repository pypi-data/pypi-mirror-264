from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="enigmator",
    version="1.0.3",
    description="Package for decrypting messages with an enigma machine",
    package_dir={"": "app"},
    packages=find_packages(where="app"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/gitstetter/enigma',
    author="Andreas Fussstetter",
    author_email="a.fussstetter@hotmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
    ],
    extras_require={
        "dev": ["pytest>=5.4.1", "twine>=4.0.2"],
    },
    python_requires=">=3.7.7",
)
