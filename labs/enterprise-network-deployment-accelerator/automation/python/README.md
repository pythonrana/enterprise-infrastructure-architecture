# Python Automation

This directory contains Python automation used by the network deployment
accelerator.

## Current Capability

`inventory.py` reads the network device inventory from the YAML source of
truth and produces a human-readable inventory summary.

## Data Flow

```text
devices.yml
     |
     v
inventory.py
     |
     v
Inventory Summary