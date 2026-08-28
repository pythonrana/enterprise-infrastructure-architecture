VALID_ROLES = {"spine", "leaf"}
VALID_PLATFORMS = {"cisco"}

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
