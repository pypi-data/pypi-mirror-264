# COSMOPharm

<p align="center">
  <img src=https://github.com/ivanantolo/cosmopharm/raw/main/TOC.png alt="TOC Figure" width="500"/>
</p>


Welcome to the COSMOPharm repository, accompanying [our paper in *J. Chem. Theory Comput.*](https://dx.doi.org/10.1021/acs.jctc.9b01016). This project and its associated publication offer insights and a practical toolkit for researching drug-polymer and drug-solvent systems, aiming to provide the scientific community with the means to reproduce our findings and further the development of COSMO-SAC-based models.

## About 

COSMOPharm is a Python package designed to streamline the predictive modeling of drug-polymer compatibility, crucial for the development of pharmaceutical amorphous solid dispersions. Apart from that, it can also be used for the miscibility/solubility of drugs with/in common solvents. Leveraging the COSMO-SAC (Conductor-like Screening Model Segment Activity Coefficient) model, COSMOPharm offers a robust platform for scientists and researchers to predict solubility, miscibility, and phase behavior in drug formulation processes.

## Features

- **Compatibility Prediction**: Utilize open-source COSMO-SAC model for prediction of drug-polymer compatibility.
- **Solubility Calculation**: Calculate drug-polymer solubilities to guide the selection of suitable polymers for drug formulations.
- **Miscibility and Phase Behavior Analysis**: Analyze the miscibility of drug-polymer pairs and understand their phase behavior under various conditions.
- **User-friendly Interface**: Easy-to-use functions and comprehensive documentation to facilitate research and development in pharmaceutical sciences.

## Installation

### Quick Installation
For most users, the quickest and easiest way to install COSMOPharm is via pip, which will manage all dependencies for you. Ensure you have already installed the `cCOSMO` library by following the instructions on the [COSMOSAC GitHub page](https://github.com/usnistgov/COSMOSAC).

Once `cCOSMO` is installed, you can install COSMOPharm directly from [PyPI](https://pypi.org/project/cosmopharm/):

```
pip install cosmopharm
```

### Advanced Installation Options

For users who need more control over the installation process (e.g., for development purposes or when integrating with other projects), COSMOPharm can also be installed by cloning the repository and installing manually. 

#### Step 1: Clone the Repository

First, clone the COSMOPharm repository:
```
git clone https://github.com/ivanantolo/cosmopharm
```

#### Step 2: Navigate to the Repository Directory

```
cd cosmopharm
```

#### Option 1: Using pip to Install from Local Source

This method installs COSMOPharm and manages all dependencies efficiently:

```
pip install .
```


#### Option 2: Using setup.py for Installation

Alternatively, you can run the setup script directly:

```
python setup.py install
```

While this method is straightforward, using `pip` is generally preferred for its dependency management capabilities.

Please note: Before proceeding with either advanced installation option, ensure the `cCOSMO` library is installed as described at the beginning of this section.

## Quick Start

Get started with COSMOPharm using the minimal example below, which demonstrates how to calculate the solubility of a drug in a polymer. This example succinctly showcases the use of COSMOPharm for solubility calculations:


```python
import cCOSMO
from cosmopharm import SLE, COSMOSAC
from cosmopharm.utils import create_components, read_params

# Define components - replace 'DrugName' and 'PolymerName' with your actual component names
names = ['DrugName', 'PolymerName']
params_file = "path/to/your/params.xlsx"

# Load parameters and create components
parameters = read_params(params_file)
components = create_components(names, parameters)

# Initialize COSMO-SAC model - replace paths with your local paths to COSMO profiles
db = cCOSMO.DelawareProfileDatabase(
    "path/to/your/complist/complist.txt",
    "path/to/your/profiles/")

for name in names:
    iden = db.normalize_identifier(name)
    db.add_profile(iden)
COSMO = cCOSMO.COSMO3(names, db)

# Setup the COSMO-SAC model with components
model = COSMOSAC(COSMO, components=components)

# Calculate solubility (SLE)
sle = SLE(solute=components[0], solvent=components[1], actmodel=model)
solubility = sle.solubility(mix='real')

# Output the solubility
print(solubility[['T', 'w', 'x']].to_string(index=False))
```
Replace 'DrugName', 'PolymerName', and file paths with your actual data and files.

For a more comprehensive demonstration, including advanced functionalities and plotting results, please see the [example_usage.py](https://github.com/ivanantolo/cosmopharm/blob/main/example_usage.py) script in this repository. This detailed example walks through the process of setting up COSMOPharm, initializing models, and visualizing the results of solubility and miscibility calculations.

## Contributing / Getting Help

Contributions to COSMOPharm are welcome! We accept contributions via pull requests to the [GitHub repository](https://github.com/ivanantolo/cosmopharm). 

For bugs, feature requests, or other queries, please [open an issue](https://github.com/ivanantolo/cosmopharm/issues) on GitHub.


## Citation

If you use COSMOPharm in your research, please consider citing it. You can find the citation format in [CITATION.md](https://github.com/ivanantolo/cosmopharm/CITATION.md).


## License

COSMOPharm is released under the MIT License. See the [LICENSE](https://github.com/ivanantolo/cosmopharm/LICENSE) file for more details.