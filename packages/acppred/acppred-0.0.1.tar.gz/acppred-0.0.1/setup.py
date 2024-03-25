from setuptools import setup, find_packages

setup(
    name="acppred",
    version="0.0.1",
    description="Screening anticancer peptide from amino acid sequence data",
    author="zolee",
    author_email="blee.inf@gmail.com",
    url="https://github.com/bzlee-bio/con_ACP",
    install_requires=["torch"],
    packages=find_packages(exclude=[]),
    keywords=["anticancer peptide", "sequence data", "deep learning"],
    python_requires=">=3.6",
    package_data={},
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
