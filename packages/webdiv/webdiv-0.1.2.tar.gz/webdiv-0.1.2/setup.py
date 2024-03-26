from setuptools import setup, find_packages

with open("README.md", "r") as file:
    description = file.read()


setup(
    name="webdiv",
    version="0.1.2",
    packages=find_packages(),
    install_requires=[
        'uvicorn'
    ],
    long_description=description,
    long_description_content_type="text/markdown"
)

build = "python3 setup.py sdist bdist_wheel"
upload = "twine upload dist/*"