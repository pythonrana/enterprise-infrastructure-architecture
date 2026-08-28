import yaml


def load_inventory():
    with open("../../data/devices.yml", "r") as file:
        return yaml.safe_load(file)


def load_network():
    with open("../../data/network.yml", "r") as file:
        return yaml.safe_load(file)