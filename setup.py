# setup.py
from pathlib import Path

from setuptools import find_packages, setup

readme_path = Path(__file__).parent / "README.md"
try:
    long_description = readme_path.read_text(encoding="utf-8")
except FileNotFoundError:
    long_description = ""

setup(
    name="task_refiner_llm",
    version="2025.9.92037",
    description="Refine unstructured briefs into implementation-ready JSON via LLM7 and llmatch.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Eugene Evstafev",
    author_email="hi@eugene.plus",
    packages=find_packages(exclude=("tests*", "examples*")),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.11",
)
