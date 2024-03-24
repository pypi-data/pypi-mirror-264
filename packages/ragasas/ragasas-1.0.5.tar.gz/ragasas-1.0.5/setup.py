from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ragasas",
    version="1.0.5",
    packages=[
        "ragasas",
        "ragasas._core",
        "ragasas._core.embedder",
        "ragasas._core.llm",
        "ragasas._core.vector_store",
    ],
    install_requires=[
        # List any dependencies your package requires
    ],
    author="Eric Gustin",
    author_email="ericgustin44@gmail.com",
    description="A package that can be used to create RAGs with a single line of code.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/yourpackage",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/yourpackage/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
