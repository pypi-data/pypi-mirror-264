# PyAnaSolution

## Introduction
PyAnaSolution is a comprehensive package that includes analytical solution programs for benchmark test cases widely 
utilized in numerical simulation algorithm research.
Our objective is to provide a resource that spares new researchers in the field from the time-consuming process of 
understanding analytical solution calculations.

This package encompasses analytical solutions for various scenarios, including:

* Convection
  * Convection (3D)
* Diffusion
  * Diffusion (3D)
* Convection Diffusion Equation (CDE)
  * CD Irregular
  * Channel Cos Flow
  * Gaussian Hill (2D)
  * Gaussian Hill (3D)
  * Poiseuille Flow
  * Semi Infinite Flow (1D)
  * Uniform Flow
* Geothermal Analysis
  * Fracture Flow (1D)
  * Fracture Thermal Flow
  * Reinjection (1D)
  * Reinjection (2D)
* Hydrology Studies
  * Theis

Example programs for each analytical solution can be found in the 'examples' directory.

We are committed to continually enhancing this library and encourage contributions of new analytical solution programs.


## Installation Guide
To install PyAnaSolution for the first time, use the following command:
```
pip install pyanasolution
```
To update PyAnaSolution to the latest version, run:
```
pip install --upgrade pyanasolution
```

## Analytical solutions

To obtain settable parameters for the calculation of analytical solutions, a universal approach is to call the 'doc'
method of the analytical solution class. For instance, to understand the parameters of the Theis solution, you can use
the following code:

```python
import pyanasolution as pas

theis = pas.Theis()
theis.doc()
```

```
[PyAnaSolution - Theis]
 * The Theis model is a seminal mathematical solution in the field of hydrogeology for quantifying transient groundwater flow in a confined aquifer. (Provided by ChatGPT)
[Parameters]
 * ----------------------|---------|---------|--------------------|------------------------------------------------|
 *  PARAMETERS NAME      | UNIT    | VALUE   | TYPE               | INTRODUCTION                                   |
 * ----------------------|---------|---------|--------------------|------------------------------------------------|
 *  Flow rate            | m^3/s   | 0       | float              | The injection well is positive and vice versa. |
 *  Gravity acceleration | m/(s^2) | 9.8     | float              | The gravity acceleration.                      |
 *  Initial head         | m       | 0       | float              | The initial head of the field.                 |
 *  Permeability         | m^2     | 0       | float              |                                                |
 *  Storage              | m^(-1)  | 0       | float              |                                                |
 *  Thick                | m       | 1       | float              | The aquifer thick.                             |
 *  Time                 | s       | 0       | float              | The operation time.                            |
 *  Fluid density        | kg/m^3  | 1000    | float              |                                                |
 *  Fluid viscosity      | Pa∙s    | 0.00101 | float              |                                                |
 *  Well coordinate      | m       | [0. 0.] | list or np.ndarray |                                                |
 * ----------------------|---------|---------|--------------------|------------------------------------------------|
```
### Convection

#### Convection (3D)

![Convection 3D](resources/images/convection_3d.gif)

### Diffusion

#### Diffusion (3D)

![Diffusion 3D](resources/images/diffusion_3d.gif)

### Covection Diffusion Equation (CDE)

#### CD Irregular

![Irregular CD](resources/images/cd_irregular.gif)

#### Channel Cos Flow

![Channel Cos Flow](resources/images/channel_cos_flow.jpg)

#### Gaussian Hill (2D)

![Gaussian Hill](resources/images/gaussian_hill_2d.gif)

#### Gaussian Hill (3D)

![Gaussian Hill](resources/images/gaussian_hill_3d.gif)

#### Poiseuille Flow

![Poiseuille Flow](resources/images/poiseuille_flow.jpeg)

#### Semi Infinite Flow (1D)

![Semi Infinite Flow 1D](resources/images/semi_infinite_flow_1d.gif)

#### Uniform Flow

![Uniform Flow](resources/images/uniform_flow.jpeg)

### Geothermal Analysis

#### Fracture Flow (1D) 

![Fracture Flow 1D](resources/images/fracture_flow_1d.gif)

#### Fracture Thermal Flow

![Fracture Thermal Flow](resources/images/fracture_thermal_flow_contour.jpeg)

#### Reinjection (1D)

![Reinjection 1D](resources/images/reinjection_1d.gif)

#### Reinjection (2D)

![Reinjection 2D](resources/images/reinjection_2d.gif)

### Hydrology Studies
#### Theis

![Theis](resources/images/theis_contour.jpg)

## Contact Us
For any inquires, please contact us at frankhp921@163.com.