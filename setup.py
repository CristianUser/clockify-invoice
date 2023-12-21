import re
import ast
# import os
# import pathlib
# import shutil
from setuptools import setup


VERSION_RE = re.compile(r"VERSION\s+=\s+(.*)")
# TEMPLATES_DIRECTORY = "invoicify/compiled_templates"

with open("invoicify/version.py", "rb") as file:
    VERSION = str(ast.literal_eval(VERSION_RE.search(file.read().decode("utf-8")).group(1)))


def readme():
    with open("README.md", "r") as readme_file:
        return readme_file.read()


if __name__ == "__main__":
    setup(
        name="invoicify",
        version=VERSION,
        description="Simple clockify invoice generator.",
        author="CristianUser",
        author_email="cristianmejia97@gmail.com",
        url="http://github.com/CristianUser/clockify-invoice",
        packages=[
            "invoicify",
            "invoicify.common",
            "invoicify.src",
            "invoicify.templates",
        ],
        include_package_data=True,
        install_requires=[
            "requests==2.22.0",
            "jinja2==3.0.3",
            "pdfkit==1.0.0",
            "pyyaml==6.0",
            "python-dateutil==2.8.2",
        ],
        long_description=readme(),
        long_description_content_type="text/markdown",
        test_suite="test",
        classifiers=[
            "Development Status :: 4 - Beta",
            "Intended Audience :: Developers",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: POSIX",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
        ],
        keywords=["Invoicify", "Clockify", "Generator", "Invoice"],
        entry_points={"console_scripts": ["invoicify = invoicify.__main__:main"]},
    )
