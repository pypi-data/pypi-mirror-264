from setuptools import setup, find_packages
import glob

with open("requirements.txt") as file_open:
     requirements = file_open.read().splitlines()

with open("README.md") as file_open:
     README = file_open.read()

setup(
    name="plasmidCC",
    setup_requires=[
        "setuptools>=38.6.0",
        "setuptools_scm",
        "setuptools_scm_git_archive",
    ],
    use_scm_version={"version_file":"plasmidCC/version.py"},
    #version="1.0.0",
    description="A Centrifuge based plasmid prediction tool",
    long_description=README,
    long_description_content_type='text/markdown',
    scripts=[script for script in glob.glob("plasmidCC/scripts/*.py")],
    packages=find_packages(),
    install_requires=requirements,
    include_package_data=True,
    entry_points={
        'console_scripts': ["plasmidCC = plasmidCC.plasmid_CC:main"]
    }
)
