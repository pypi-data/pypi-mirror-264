import os

import setuptools

current_dir = os.path.dirname(__file__)

# Read description
with open(f"{current_dir}/USAGE.md", "r") as f:
    long_description = f.read()

with open(f"{current_dir}/src/fastapi_openid_google/VERSION", "r") as f:
    version = f.read().strip()

# Creates the setup config for the package
# We only look for code into the "Modules" folder
setuptools.setup(
    name="fastapi_openid_google",
    version=version,
    author="svaponi",
    description="Google OpenID integration for FastAPI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/svaponi/fastapi_openid_google",
    install_requires=[
        "fastapi",
        "oauthlib",
        "requests",
    ],
    extras_require={
        "local": [
            "uvicorn",
            "python-dotenv",
        ],
    },
    packages=setuptools.find_packages(
        where="src", exclude=["*.tests", "*.tests.*", "tests.*", "tests"]
    ),
    package_dir={"": "src"},
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # TODO SELECT A LICENSE
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
)

# Command to generate the distributions and the whl
# python3 setup.py sdist bdist_wheel
