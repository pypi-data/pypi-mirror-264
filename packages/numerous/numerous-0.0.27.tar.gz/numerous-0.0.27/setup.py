from setuptools import setup
import re


def get_version():
    version_file = "src/numerous/__init__.py"
    with open(version_file, "r") as f:
        version_content = f.read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_content, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(version=get_version())
