# Network Data Model

This directory contains the source-of-truth data used by the network
deployment automation.

## Files

### `devices.yml`

Defines network devices and their attributes.

### `network.yml`

Defines shared network parameters such as:

- Autonomous System Numbers
- Loopback addresses
- VLANs
- Network-wide parameters

## Design Principle

Configuration data is separated from automation logic.

The goal is to allow the same automation framework to generate
configurations for different environments by changing data rather
than rewriting automation logic.