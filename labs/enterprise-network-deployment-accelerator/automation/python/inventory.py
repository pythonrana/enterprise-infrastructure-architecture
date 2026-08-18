import yaml


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


def display_inventory(devices):
    print(f"Total devices: {len(devices)}")
    print()

    for device in devices:
        print(
            f"{device['hostname']:10} "
            f"{device['role']:8} "
            f"{device['platform']:8} "
            f"{device['management_ip']}"
        )


def main():
    inventory = load_inventory()

    devices = inventory.get("devices", [])

    display_inventory(devices)

    print()
    print("Validating inventory...")

    errors = validate_inventory(devices)

    if errors:
        print()
        print("VALIDATION FAILED")

        for error in errors:
            print(f"- {error}")

    else:
        print("VALIDATION PASSED")


if __name__ == "__main__":
    main()
