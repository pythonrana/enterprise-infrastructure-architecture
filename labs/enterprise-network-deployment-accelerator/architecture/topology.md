# Reference Network Topology

## High-Level Topology

```mermaid
flowchart TD
    A[Enterprise] --> B[Data Center]

    B --> C[Spine 1]
    B --> D[Spine 2]

    C --> E[Leaf 1]
    C --> F[Leaf 2]

    D --> E
    D --> F

    E --> G[Server Group 1]
    F --> H[Server Group 2]