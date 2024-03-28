from pathlib import Path

from setuptools import find_packages, setup

parent_dir = Path(__file__).resolve().parent

setup(
    name="geojson-validator",
    version="0.5.2",
    author="Christoph Rieke",
    author_email="christoph.k.rieke@gmail.com",
    description="Validates and fixes GeoJSON",
    long_description=parent_dir.joinpath("README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/chrieke/geojson-validator",
    license="MIT",
    packages=find_packages(exclude=("tests", "streamlit-webapp", "docs", "examples")),
    data_files=[
        (
            "",
            ["requirements.txt"],
        ),
    ],
    include_package_data=True,
    zip_safe=False,
    install_requires=parent_dir.joinpath("requirements.txt").read_text().splitlines(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
    ],
    python_requires=">=3.8",
)
