# Setting Up the smart_recon_apps Project Runtime

> **Note**: For a beginner-friendly explanation of runtime environments and why they matter, see [Runtime Environments Explained](./runtime_environments_explained.md).
>
> **Note**: Curious about NumPy and other Python libraries? See [Python Libraries Explained](./python_libraries_explained.md).

## Prerequisites

- Anaconda or Miniconda installed on your system
- Access to a terminal or command prompt

## Setup Instructions

### 1. Create the Conda Environment

Open your terminal or command prompt and run:

```bash
conda create -n smart_recon_apps python=3.9
```

### 2. Activate the Environment

```bash
conda activate smart_recon_apps
```

### 3. Install Required Packages

Install all dependencies using conda (preferred method):

```bash
conda install -c conda-forge pandas
conda install -c conda-forge faker
```

### 4. Verify Installation

Verify that the packages were installed correctly:

```bash
conda list
```

## Running the Financial Data Generator

With the environment activated, navigate to the project directory:

```bash
cd c:\Users\so_ho\Desktop\00_PythonWIP\Smart_Recon
```

Run the script:

```bash
python generate_financial_data.py
```

## Environment Management

### Deactivate the Environment

When you're done working on the project:

```bash
conda deactivate
```

### Export Environment Configuration

To share or recreate this environment later:

```bash
conda env export -n smart_recon_apps > smart_recon_environment.yml
```

### Recreate from Configuration File

```bash
conda env create -f smart_recon_environment.yml
```
