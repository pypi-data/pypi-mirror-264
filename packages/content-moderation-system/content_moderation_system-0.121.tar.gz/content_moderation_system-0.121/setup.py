from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="content_moderation_system",
    version="0.121",
    author="Tanmay Jain",
    author_email="tanmay5tj@gmail.com",
    description="A Python library for interacting with CMS APIs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tanmaydoesai/content_moderation_system",
    # packages=find_packages(),
    packages=find_packages(include=["content_moderation_system", "content_moderation_system.*"]),
    install_requires=["requests"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)