"""
Setup script for SmartRecon - Intelligent Financial Reconciliation Assistant
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README file
readme_file = Path(__file__).parent / "README.md"
if readme_file.exists():
    with open(readme_file, "r", encoding="utf-8") as f:
        long_description = f.read()
else:
    long_description = "SmartRecon - Intelligent Financial Reconciliation Assistant"

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
if requirements_file.exists():
    with open(requirements_file, "r", encoding="utf-8") as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]
else:
    requirements = [
        "pandas>=1.5.0",
        "numpy>=1.21.0",
        "openpyxl>=3.0.9",
        "xlrd>=2.0.1",
        "fuzzywuzzy>=0.18.0",
        "python-Levenshtein>=0.12.2",
        "matplotlib>=3.5.0",
        "seaborn>=0.11.0",
        "click>=8.0.0",
        "colorama>=0.4.4",
        "tqdm>=4.62.0",
        "jsonschema>=4.0.0",
        "chardet>=5.0.0",
        "python-dateutil>=2.8.0"
    ]

setup(
    name="smartrecon",
    version="1.0.0",
    author="SmartRecon Development Team",
    author_email="info@smartrecon.com",
    description="Intelligent Financial Reconciliation Assistant",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/organization/smartrecon",
    project_urls={
        "Bug Tracker": "https://github.com/organization/smartrecon/issues",
        "Documentation": "https://smartrecon.readthedocs.io/",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial :: Accounting",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
        ],
        "docs": [
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "smartrecon=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "smartrecon": [
            "config/*.json",
            "templates/*.json",
        ],
    },
    zip_safe=False,
)
