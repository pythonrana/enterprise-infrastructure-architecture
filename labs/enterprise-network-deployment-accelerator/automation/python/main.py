from loaders import load_inventory, load_network, load_metrics
from validators import validate_inventory, validate_topology
from generator import generate_configurations
from metrics import calculate_improvement


def main():
    inventory = load_inventory()
    network = load_network()
    metrics = load_metrics()

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

    print("Generating configurations...")
    print()

    generate_configurations(devices)

    print()
    print("Configuration generation complete.")

    time_saved, percentage_reduction = calculate_improvement(metrics)

    print()
    print("Deployment Metrics")
    print("------------------")
    print(
        f"Baseline deployment: {metrics['deployment_metrics']['baseline']['duration_minutes']} minutes"
        )
    print(
        f"Automated workflow: {metrics['deployment_metrics']['automated']['duration_minutes']} minutes"
        )
    print(f"Time saved: {time_saved} minutes")
    print(f"Reduction: {percentage_reduction:.2f}%")


if __name__ == "__main__":
    main()  