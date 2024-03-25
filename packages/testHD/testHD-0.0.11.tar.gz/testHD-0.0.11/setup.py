
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="testHD", ## project name
    version="0.0.11", ## __version__.py 파일과 맞춰주기
    author="HaeDream", ## 
    author_email="jhj990203@gmail.com", ##
    description="This is a package for test HD", ##
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jhj0203/Portfolio.git", ##
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)