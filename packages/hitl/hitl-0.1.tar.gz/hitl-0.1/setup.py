from setuptools import setup, find_packages

setup(
    name="hitl",
    version="0.1",
    packages=find_packages(),
    install_requires=["requests"],
    license="MIT",
    author="Luke Connolly",
    author_email="luke.connolly2@ucdconnect.ie",
    description="An uploader tool for the HITL platform.",
)
