import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python-wordchain",
    author="Shaun Hegarty",
    author_email="shaunhegarty@proton.me",
    description="A small package for building word chains",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shaunhegarty/wordchain",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)