from setuptools import setup, find_packages

import pathlib

with open("binjector/README.md", "r", encoding="utf-8") as f:
    long_description = f.read()
with open("binjector/requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read()
setup(
    name = 'binjector',
    version = '0.1.6',
    author = 'Seongchuel Ahn',
    author_email = 'aciddust20@gmail.com',
    license = 'MIT',
    description="Inject your data into an image",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    keywords = 'steganography, forensic',
    url="https://github.com/dev4hobby/image-steganography/tree/release",
    packages = find_packages(),
    install_requires = [requirements],
    python_requires='>=3.6',
    entry_points = '''
        [console_scripts]
        binjector=binjector.__main__:cli
    ''',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
