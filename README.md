# Multi-Robot Exploration Development Environment

This repository is an extension of the **[CMU Autonomous Exploration Development Environment](https://www.cmu-exploration.com/development-environment)**.  
Our main contribution is expanding the original **single-robot** exploration framework into a **multi-robot** exploration system.

> **Note:** This project is implemented and tested on **ROS 2 Humble**.

## Overview

The original Autonomous Exploration Development Environment was designed for single-robot exploration and development.  
Based on that foundation, this project extends the system to support **multiple robots operating in the same environment**, enabling collaborative exploration and more scalable experiments in simulation.

## Key Changes

Compared with the original single-robot version, this repository includes:

- Extension from **single robot** to **multiple robots**
- Support for **multi-robot exploration scenarios**
- Added a warehouse environment to support **multi-robot cooperative navigation** tasks

## Project Background

This work is built upon the CMU **Autonomous Exploration Development Environment** and aims to provide a more practical development and experimentation platform for multi-robot path planning research.

## Build Instructions

For the compilation and environment setup process, please refer to the following document:

- [Build / Setup Reference](https://drive.google.com/file/d/1eYbxOB5wN9iEUm5UaB_Li8Xu-4cTcqps/view)

## Usage

After completing the environment setup and compilation, you can launch the corresponding simulation and exploration modules based on your experiment configuration.

This repository supports two categories of environments:

### 1. Exploration Environments

The original five environments are preserved for exploration task testing and evaluation:

- `campus`
- `indoor`
- `garage`
- `tunnel`
- `forest`

### 2. Warehouse Environment

In addition to the original exploration environments, this repository introduces a `warehouse` environment for multi-robot cooperative navigation tasks.

The warehouse setup includes:

- a **prior** environment with relatively simple obstacle distribution
- a **ground truth** environment with local changes

To launch the system with a particular environment, replace `environment` with the desired environment name, such as `campus`, `indoor`, `garage`, `tunnel`, `forest`, or `warehouse`.

```bash
ros2 launch vehicle_simulator system_environment.launch.py
```

In `system_environment.launch.py`, you can enable vehicle visualization in Gazebo by modifying the value of `gazebo_gui`.

You can also adjust the number of vehicles by changing the value of `n_robots`.

For additional parameter settings and further modifications, please refer to the **[CMU Autonomous Exploration Development Environment](https://www.cmu-exploration.com/development-environment)**

## Repository Structure

A typical repository structure may include:

- `src/` — source code for the exploration system and simulation modules
- `vehicle_simulator/` — robot and simulation-related components
- `local_planner/` — local planning modules
- `terrain_analysis/` — terrain perception and analysis components
- `visualization_tools/` — visualization utilities
- other supporting packages for multi-robot exploration

## Notes

- This repository is an extended version of the CMU single-robot exploration development environment.
- The main focus of this project is the **multi-robot extension**.
- Please ensure all dependencies are correctly installed before building.

## Credit

If you find this work helpful, please consider citing:

```bibtex
@article{shizhe2026orion,
  title={ORION: Option-Regularized Deep Reinforcement Learning for Cooperative Multi-Agent Online Navigation},
  author={Shizhe, Zhang and Jingsong, Liang and Zhitao, Zhou and Shuhan, Ye and Yizhuo, Wang and Derek, Tan Ming Siang and Jimmy, Chiun and Yuhong, Cao and Guillaume, Sartoretti},
  journal={arXiv preprint arXiv:2601.01155},
  year={2026}
}
```

## Contributors

This project is developed and maintained by:

[Shizhe Zhang*](),
[Jingsong Liang*](https://jingsongliang.com/),
[Zhitao Zhou](),
[Shuhan Ye](),

## Acknowledgement

This project is based on the **[CMU Autonomous Exploration Development Environment](https://www.cmu-exploration.com/development-environment)**, with modifications and extensions for **multi-robot exploration**.
