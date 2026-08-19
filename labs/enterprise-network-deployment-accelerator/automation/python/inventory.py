import os

import yaml
from jinja2 import Environment, FileSystemLoader


VALID_ROLES = {"spine", "leaf"}
VALID_PLATFORMS = {"cisco"}


def load_inventory():
    with open("../../data/devices.yml", "r") as file:
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


def generate_configurations(devices):
    template_environment = Environment(
	loader=FileSystemLoader("../templates")
    )

    template = template_environment.get_template("device_config.j2")

    output_directory = "../configs"

    os.makedirs(output_directory, exist_ok=True)

    for device in devices:
        configuration = template.render(device=device)

        filename = os.path.join(
            output_directory,
            f"{device['hostname']}.cfg"
        )

        with open(filename, "w") as file:
            file.write(configuration)

        print(f"Generated: {filename}")


def main():
    inventory = load_inventory()

    devices = inventory.get("devices", [])

    print(f"Total devices: {len(devices)}")
    print()

    print("Validating inventory...")

    errors = validate_inventory(devices)

    if errors:
        print()
        print("VALIDATION FAILED")

        for error in errors:
            print(f"- {error}")

        return

    print("VALIDATION PASSED")
    print()

    print("Generating configurations...")
    print()

    generate_configurations(devices)

    print()
    print("Configuration generation complete.")


if __name__ == "__main__":
    main()
