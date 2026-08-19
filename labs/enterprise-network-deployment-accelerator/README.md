# Enterprise Network Deployment Accelerator

A reference implementation for reducing enterprise network deployment effort through standardized architecture, source-of-truth data, configuration generation, and pre-deployment validation.

## Overview

Enterprise network deployments often involve repetitive manual activities across:

- Device inventory
- Configuration development
- Validation
- Change preparation
- Testing
- Deployment

This project explores how infrastructure-as-code principles and reusable automation patterns can improve deployment consistency, reduce manual effort, and lower operational risk.

The current implementation demonstrates a simple workflow:

```text
Source of Truth
      |
      v
Inventory Validation
      |
      v
Jinja2 Configuration Templates
      |
      v
Generated Device Configurations

## Current Architecture

The current implementation follows a source-of-truth driven automation model.

```text
                 NETWORK INTENT
                       |
                       v
              +------------------+
              |  Source of Truth  |
              |   devices.yml     |
              |   network.yml     |
              +--------+---------+
                       |
                       v
              +------------------+
              |    Validation     |
              |      Python       |
              |                  |
              | Inventory checks  |
              | Role validation   |
              | IP validation     |
              +--------+---------+
                       |
                VALIDATION PASSED
                       |
                       v
              +------------------+
              | Configuration     |
              |     Engine        |
              |     Jinja2        |
              +--------+---------+
                       |
                       v
              +------------------+
              | Generated Configs |
              |                  |
              | spine-01.cfg      |
              | spine-02.cfg      |
              | leaf-01.cfg       |
              | leaf-02.cfg       |
              +------------------+