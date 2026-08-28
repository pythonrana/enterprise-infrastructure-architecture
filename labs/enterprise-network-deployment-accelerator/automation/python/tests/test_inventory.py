import pytest

from metrics import calculate_improvement

from jinja2 import Environment, FileSystemLoader

from validators import (
    validate_inventory,
    validate_topology,
    validate_generated_configuration,
)

@pytest.fixture
def sample_devices():
    return [
        {
            "hostname": "spine-01",
            "role": "spine",
            "platform": "cisco",
            "management_ip": "192.0.2.11",
        },
        {
            "hostname": "spine-02",
            "role": "spine",
            "platform": "cisco",
            "management_ip": "192.0.2.12",
        },
        {
            "hostname": "leaf-01",
            "role": "leaf",
            "platform": "cisco",
            "management_ip": "192.0.2.21",
        },
        {
            "hostname": "leaf-02",
            "role": "leaf",
            "platform": "cisco",
            "management_ip": "192.0.2.22",
        },
    ]
@pytest.fixture
def sample_network():
    return {
        "network": {
            "links": [
                {
                    "id": "spine01-leaf01",
                    "source": "spine-01",
                    "source_interface": "Ethernet1/1",
                    "destination": "leaf-01",
                    "destination_interface": "Ethernet1/1",
                },
                {
                    "id": "spine01-leaf02",
                    "source": "spine-01",
                    "source_interface": "Ethernet1/2",
                    "destination": "leaf-02",
                    "destination_interface": "Ethernet1/1",
                },
                {
                    "id": "spine02-leaf01",
                    "source": "spine-02",
                    "source_interface": "Ethernet1/1",
                    "destination": "leaf-01",
                    "destination_interface": "Ethernet1/2",
                },
                {
                    "id": "spine02-leaf02",
                    "source": "spine-02",
                    "source_interface": "Ethernet1/2",
                    "destination": "leaf-02",
                    "destination_interface": "Ethernet1/2",
                },
            ]
        }
    }

def test_valid_inventory():
    devices = [
        {
            "hostname": "spine-01",
            "role": "spine",
            "platform": "cisco",
            "management_ip": "192.0.2.11",
        },
        {
            "hostname": "leaf-01",
            "role": "leaf",
            "platform": "cisco",
            "management_ip": "192.0.2.21",
        },
    ]

    errors = validate_inventory(devices)

    assert errors == []
def test_duplicate_hostname():
    devices = [
        {
            "hostname": "spine-01",
            "role": "spine",
            "platform": "cisco",
            "management_ip": "192.0.2.11",
        },
        {
            "hostname": "spine-01",
            "role": "spine",
            "platform": "cisco",
            "management_ip": "192.0.2.12",
        },
    ]

    errors = validate_inventory(devices)

    assert any("Duplicate hostname" in error for error in errors)


def test_invalid_role():
    devices = [
        {
            "hostname": "router-01",
            "role": "router",
            "platform": "cisco",
            "management_ip": "192.0.2.31",
        }
    ]

    errors = validate_inventory(devices)

    assert any("invalid role" in error for error in errors)


def test_missing_management_ip():
    devices = [
        {
            "hostname": "leaf-01",
            "role": "leaf",
            "platform": "cisco",
        }
    ]

    errors = validate_inventory(devices)

    assert any("missing management IP" in error for error in errors)
def test_valid_topology(sample_devices, sample_network):
    errors = validate_topology(
        sample_devices,
        sample_network
    )

    assert errors == []

def test_broken_topology(sample_devices, sample_network):
    broken_network = {
        "network": {
            "links": sample_network["network"]["links"][:-1]
        }
    }

    errors = validate_topology(
        sample_devices,
        broken_network
    )

    assert any(
        "spine-02" in error
        for error in errors
    )

    assert any(
        "leaf-02" in error
        for error in errors
    )
def test_valid_generated_configuration():
    device = {
        "hostname": "leaf-01",
        "management_ip": "192.0.2.21",
    }

    configuration = """
!
! Generated configuration
!
hostname leaf-01
!
interface Loopback0
 description Management Loopback
 ip address 192.0.2.21
!
end
"""

    errors = validate_generated_configuration(
        device,
        configuration
    )

    assert errors == []
def test_invalid_generated_configuration():
    device = {
        "hostname": "leaf-01",
        "management_ip": "192.0.2.21",
    }

    configuration = """
!
! Generated configuration
!
hostname WRONG-leaf-01
!
interface Loopback0
 description Management Loopback
 ip address 192.0.2.21
!
end
"""

    errors = validate_generated_configuration(
        device,
        configuration
    )

    assert any(
        "hostname configuration is missing" in error
        for error in errors
    )
def test_sample_topology(sample_devices, sample_network):
    errors = validate_topology(
        sample_devices,
        sample_network
    )

    assert errors == []
def test_configuration_generation(sample_devices):
    template_environment = Environment(
        loader=FileSystemLoader("../templates")
    )

    template = template_environment.get_template(
        "device_config.j2"
    )

    device = sample_devices[0]

    configuration = template.render(device=device)

    assert "hostname spine-01" in configuration
    assert "192.0.2.11" in configuration
    assert "interface Loopback0" in configuration
def test_full_configuration_workflow(sample_devices):
    template_environment = Environment(
        loader=FileSystemLoader("../templates")
    )

    template = template_environment.get_template(
        "device_config.j2"
    )

    for device in sample_devices:
        configuration = template.render(device=device)

        errors = validate_generated_configuration(
            device,
            configuration
        )

        assert errors == []
def test_calculate_improvement():
    metrics = {
        "deployment_metrics": {
            "baseline": {
                "duration_minutes": 360
            },
            "automated": {
                "duration_minutes": 70
            }
        }
    }

    time_saved, percentage_reduction = calculate_improvement(metrics)

    assert time_saved == 290
    assert round(percentage_reduction, 2) == 80.56