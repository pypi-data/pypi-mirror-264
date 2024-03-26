import pathlib
import setuptools

setuptools.setup(
    name="AbdelrahmanReisha",
    version="0.1.1",
    description=" basic data preprocessing package",
    long_description=pathlib.Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://testwebsite.xyz",
    author="AbdelrahmanReisha",
    author_email="abdelrahmanrisha@gmail.com",
    license="The Unlicsense",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.11",
        "Topic :: Utilities",
    ],
    python_requires=">=3.11",
    install_requires=["requests", "pandas>=2.0"],
    packages=setuptools.find_packages(),
    include_package_data=True,
)