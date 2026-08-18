import yaml


def load_inventory():
    with open("../../data/devices.yml", "r") as file:
        return yaml.safe_load(file)


def main():
    inventory = load_inventory()

    devices = inventory.get("devices", [])

    print(f"Total devices: {len(devices)}")
    print()

    for device in devices:
        print(
            f"{device['hostname']:10} "
            f"{device['role']:8} "
            f"{device['platform']:8} "
            f"{device['management_ip']}"
        )


if __name__ == "__main__":
    main()
