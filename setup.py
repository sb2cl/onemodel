import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="onemodel",
    version="0.0.2",
    author="Fernando Nobel Santos Navarro",
    author_email="fersann1@upv.es",
    description="OneModel package description.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FernandoNobel/onemodel",
    project_urls={
        "Bug Tracker": "https://github.com/FernandoNobel/onemodel/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    scripts=['bin/onemodel-cli.py'],
    include_package_data=True,
)
