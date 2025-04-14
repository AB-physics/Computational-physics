# 🧠 MicrOMEGAs 6.2.3 Setup Guide (Dark Matter Analysis)
This repo includes instructions to install and run **MicrOMEGAs**, one of the most powerful tools for dark matter and BSM model analysis.
## 📥 Download

Download the latest version from:

🔗 [https://zenodo.org/records/14978911](https://zenodo.org/records/14978911)

## Installing and Running
```
conda create -n micromegas python=3.12

conda activate micromegas
```
```
conda deactivate
```

#### Go to the download location and extract the compressed file using the command:
``` 
tar -zxvf micromegas_6.2.3.tgz
```
#### Then move into the extracted folder:
```
cd micromegas_6.2.3
```
#### Run the general compilation command (required for all models):
```
make
```
#### MicrOMEGAs 6 comes with several predefined models. To compile and run any model:
```
cd MSSM
```

or any other model

```
make main=main.c
```
```
./main input.slha
```

or ```./main data1.par``` or ```./main mssm1.par```

#### Predefined models include:

MSSM / NMSSM

IDM, Z3IDM, Z4IDSM, Z5M, Z7M

Z′Portal, SingletDM

LLL_scalar, STFM, RDM

LHM, RHNM, UMSSM, CPVMSSM

#### To create your own (custom) model:

```
./newProject MyModel
```
run in the root directory
```
cd MyModel
```
```
make main=main.c
```
```
./main input.par
```
The ```MyModel/``` directory will be automatically created with all sample files.

### Optional cleanup:

#### To clean everything:
```
./clean
```
from the root directory
#### To clean files inside a specific model:
```
make clean
```
run inside the model directory

# requirements
Versions used on my system:

gcc: 7.5.0

make: 4.3

gfortran: 10.5.0

libx11-dev: 2:1.7.5-1ubuntu0.3

OS: Ubuntu 22.04 LTS

```
pip install smodels
```
‍‍‍```
pip install torch

```
