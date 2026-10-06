# Imaris Registration Tool

The Imaris Registration Tool is a graphical application for 3D microscopy image registration using Imaris (`.ims`) files and Elastix.

The tool was developed as part of the ClearMap Adjustments project to provide a simple workflow for loading microscopy volumes, configuring registration steps, running Elastix, and evaluating the resulting alignment.

## Features

- Load Imaris (`.ims`) microscopy files
- Select resolution level and image channel
- Configure multi-step registration pipelines
- Translation registration
- Rigid registration
- Affine registration
- Automatic registration using Elastix
- Alignment evaluation using MAE, MSE, and NCC
- Automatic saving of registration inputs and outputs
- Graphical user interface
- Background registration to keep the application responsive during processing


# Installation

## 1. Requirements

The following software is required:

- Python
- Git
- Elastix
- Python packages listed in `requirements.txt`

The application was developed using Python and PySide6.

## 2. Download the Project

Open Command Prompt or a terminal and clone the repository:

```bash
git clone https://github.com/HSHuangLab/ClearMap_Adjustments.git