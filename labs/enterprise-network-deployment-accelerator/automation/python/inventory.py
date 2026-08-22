import os

import yaml
from jinja2 import Environment, FileSystemLoader


VALID_ROLES = {"spine", "leaf"}
VALID_PLATFORMS = {"cisco"}


def load_inventory():
    with open("../../data/devices.yml", "r") as file:
        return yaml.safe_load(file)
def load_network():
    with open("../../data/network.yml", "r") as file:
        return yaml.safe_load(file)


def validate_inventory(devices):
    errors = []

    hostnames = set()

    for device in devices:
        hostname = device.get("hostname")
        role = device.get("role")
        platform = device.get("platform")
        management_ip = device.get("management_ip")

        if not hostname:
            errors.append("Device is missing hostname.")

        elif hostname in hostnames:
            errors.append(f"Duplicate hostname: {hostname}")

        else:
            hostnames.add(hostname)

        if role not in VALID_ROLES:
            errors.append(
                f"{hostname}: invalid role '{role}'."
            )

        if platform not in VALID_PLATFORMS:
            errors.append(
                f"{hostname}: unsupported platform '{platform}'."
            )

        if not management_ip:
            errors.append(
                f"{hostname}: missing management IP."
            )

    return errors

def validate_topology(devices, network):
    errors = []

    device_map = {
        device["hostname"]: device
        for device in devices
    }

    links = network.get("network", {}).get("links", [])

    link_ids = set()
    connection_counts = {
        hostname: 0
        for hostname in device_map
    }

    for link in links:
        link_id = link.get("id")
        source = link.get("source")
        destination = link.get("destination")
        source_interface = link.get("source_interface")
        destination_interface = link.get("destination_interface")

        # Check duplicate link IDs
        if link_id in link_ids:
            errors.append(f"Duplicate link ID: {link_id}")
        else:
            link_ids.add(link_id)

        # Check devices exist
        if source not in device_map:
            errors.append(
                f"{link_id}: source device '{source}' does not exist."
            )

        if destination not in device_map:
            errors.append(
                f"{link_id}: destination device '{destination}' does not exist."
            )

        # Check self-connections
        if source == destination:
            errors.append(
                f"{link_id}: source and destination cannot be the same device."
            )

        # Check interfaces
        if not source_interface:
            errors.append(
                f"{link_id}: missing source interface."
            )

        if not destination_interface:
            errors.append(
                f"{link_id}: missing destination interface."
            )

        # Count valid connections
        if source in connection_counts:
            connection_counts[source] += 1

        if destination in connection_counts:
            connection_counts[destination] += 1

    # Validate expected spine/leaf connectivity
    for hostname, device in device_map.items():
        role = device.get("role")
        connection_count = connection_counts[hostname]

        if role in {"spine", "leaf"} and connection_count != 2:
            errors.append(
                f"{hostname}: expected 2 topology connections, "
                f"found {connection_count}."
            )

    return errors

def validate_generated_configuration(device, configuration):
    errors = []

    hostname = device.get("hostname")
    loopback_ip = device.get("management_ip")

    if f"hostname {hostname}" not in configuration:
        errors.append(
            f"{hostname}: hostname configuration is missing."
        )

    if "interface Loopback0" not in configuration:
        errors.append(
            f"{hostname}: Loopback0 configuration is missing."
        )

    if loopback_ip and loopback_ip.split("/")[0] not in configuration:
        errors.append(
            f"{hostname}: management IP is missing from configuration."
        )

    if not configuration.strip().endswith("end"):
        errors.append(
            f"{hostname}: configuration does not end with 'end'."
        )

    return errors

def generate_configurations(devices):
    template_environment = Environment(
        loader=FileSystemLoader("../templates")
    )

    template = template_environment.get_template("device_config.j2")

    output_directory = "../configs"

    generated_configurations = {}

    print("Generating configurations...")
    print()

    # Generate and validate all configurations first
    for device in devices:
        configuration = template.render(device=device)

        validation_errors = validate_generated_configuration(
            device,
            configuration
        )

        if validation_errors:
            print("CONFIGURATION VALIDATION FAILED")

            for error in validation_errors:
                print(f"- {error}")

            return False

        generated_configurations[device["hostname"]] = configuration

        print(
            f"Configuration validation passed: "
            f"{device['hostname']}"
        )

    print()
    print("All configurations validated successfully.")
    print()

    # Write configurations only after all validations pass
    os.makedirs(output_directory, exist_ok=True)

    for hostname, configuration in generated_configurations.items():
        filename = os.path.join(
            output_directory,
            f"{hostname}.cfg"
        )

        with open(filename, "w") as file:
            file.write(configuration)

        print(f"Generated: {filename}")

    return True

def main():
    inventory = load_inventory()
    network = load_network()

    devices = inventory.get("devices", [])

    print(f"Total devices: {len(devices)}")
    print()

    print("Validating inventory...")

    errors = validate_inventory(devices)

    if errors:
        print()
        print("INVENTORY VALIDATION FAILED")

        for error in errors:
            print(f"- {error}")

        return

    print("INVENTORY VALIDATION PASSED")
    print()

    print("Validating topology...")

    topology_errors = validate_topology(devices, network)

    if topology_errors:
        print()
        print("TOPOLOGY VALIDATION FAILED")

        for error in topology_errors:
            print(f"- {error}")

        return

    print("TOPOLOGY VALIDATION PASSED")
    print()

    generation_success = generate_configurations(devices)

    if not generation_success:
        print()
        print("Configuration generation stopped.")
        return

    print()
    print("Configuration generation complete.")


if __name__ == "__main__":
    main()