# Network Automation Workflow

```text
┌──────────────────────┐
│    NETWORK INTENT    │
│                      │
│ Architecture        │
│ Standards            │
│ Device Roles         │
│ Deployment Patterns  │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│   SOURCE OF TRUTH    │
│                      │
│ devices.yml          │
│ network.yml          │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  VALIDATION ENGINE   │
│                      │
│ Python               │
│                      │
│ • Inventory          │
│ • Device Roles       │
│ • Management IP      │
└──────────┬───────────┘
           │
           │ VALIDATION PASSED
           ▼
┌──────────────────────┐
│ CONFIGURATION ENGINE │
│                      │
│ Jinja2               │
│ device_config.j2     │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│   GENERATED OUTPUT   │
│                      │
│ spine-01.cfg         │
│ spine-02.cfg         │
│ leaf-01.cfg          │
│ leaf-02.cfg          │
└──────────────────────┘