import setuptools

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
        name="onemodel",
        version="0.0.5",
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
        install_requires=[
            'tatsu',
            'PyQt5',
            'click',
            'importlib-resources',
            'python-libsbml',
            ],
        include_package_data=True,
        entry_points ={
            'console_scripts': [
                'onemodel-cli = onemodel.cli.cli:main',
                'onemodel-gui = onemodel.gui.app:main',
                ]
            },
        )
