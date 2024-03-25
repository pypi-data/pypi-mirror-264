from distutils.core import setup

setup(
    name="math_spec_mapping",
    version="0.2.6",
    author="Sean McOwen",
    author_email="Sean@Block.Science",
    description="A library for easy mapping of mathematical specifications.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://example.com/math_spec_mapping",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=["graphviz>=0.20.1", "ipython>=7.7.0", "pandas>=1.4"],
)
