from setuptools import setup, find_packages

try:
    from pypandoc import convert
    def read_markdown(file):
        return convert(file, "rst")
except ImportError:
    def read_markdown(file):
        return open(file, "r").read()

setup(
    name="gatk_cwl_generator",
    version="1.0.0",
    packages=find_packages(exclude=["tests", "examples"]),
    install_requires=open("requirements.txt", "r").readlines(),
    url="https://github.com/wtsi-hgi/gatk-cwl-generator",
    license="MIT",
    description="Generates CWL files from the GATK documentation Edit",
    long_description=read_markdown("README.md"),
    entry_points={
        "console_scripts": [
            "gatk_cwl_generator=gatkcwlgenerator.main:main",
        ]
    }
)