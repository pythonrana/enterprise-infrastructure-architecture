import os

from jinja2 import Environment, FileSystemLoader

from validators import validate_generated_configuration

def generate_configurations(devices):
    template_environment = Environment(
        loader=FileSystemLoader("../templates")
    )

    template = template_environment.get_template("device_config.j2")

    output_directory = "../configs"

    generated_configurations = {}

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
