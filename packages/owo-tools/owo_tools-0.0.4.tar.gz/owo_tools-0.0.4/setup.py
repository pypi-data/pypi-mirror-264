import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

# open __init__.py and read __version__
with open("owo_tools/__init__.py", "r", encoding="utf-8") as f:
    for line in f:
        if "__version__" in line:
            exec(line)


setuptools.setup(
    name="owo_tools",
    version=__version__,
    author="Ryan Liu",
    author_email="pm@owomail.cc",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Keycatowo/owo_tools",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
          'console_scripts': [
              'convert_chinese = owo_tools.convert_chinese:main',
          ],
      }
)
