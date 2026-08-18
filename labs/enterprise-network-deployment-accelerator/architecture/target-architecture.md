# Target Architecture

## Objective

Create a standardized and repeatable network deployment architecture that
can be validated and automated before production deployment.

## Reference Environment

The fictional enterprise environment contains:

- Campus networks
- Data center networks
- Cloud connectivity
- Remote and edge locations

## Network Model

The initial lab will focus on a simplified data center environment using a
spine-leaf architecture.

```text
                 Spine-1          Spine-2
                  /  \             /  \
                 /    \           /    \
                /      \         /      \
             Leaf-1    Leaf-2   Leaf-3    Leaf-4
                |        |         |        |
              Hosts    Hosts     Hosts    Hosts