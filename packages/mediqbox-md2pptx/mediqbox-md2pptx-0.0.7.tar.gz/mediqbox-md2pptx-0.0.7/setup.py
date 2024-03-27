from setuptools import setup, find_namespace_packages

with open("README.md", "r") as fp:
  long_description = fp.read()

setup(
  name='mediqbox-md2pptx',
  version='0.0.7',
  description="A mediqbox component to generate pptx from markdown",
  long_description=long_description,
  long_description_content_type="text/markdown",
  package_dir={"": "src"},
  packages=find_namespace_packages(
    where="src", include=["mediqbox.*"]
  ),
  install_requires=[
    "mediqbox-abc >= 0.0.4",
    "python-pptx",
    "cairosvg",
    "graphviz"
  ]
)