"""yaml_config.build"""
import argparse
import sys
import textwrap
from typing import Dict

import yaml
from jinja2 import Environment, PackageLoader, StrictUndefined
from jinja2.exceptions import UndefinedError

from yaml_config.settings import REQUIRED_VARS, TEMPLATES


def validate_template(template_type: str, site_info: Dict[str, str]) -> str:
    """
    Validate the template type matches with site information
    """
    model = site_info["ion_model"]
    inet2 = site_info["inet2"]

    # Validate Model
    if template_type in ("1K1C", "1K2C"):
        if str(model) != "1000":
            print(
                f"\nError, using model type {model} on template type: {template_type}, unsupported.\n"
            )
            sys.exit()
    if template_type in ("2K1C", "2K2C"):
        if str(model) != "2000":
            print(
                f"\nError, using model type {model} on template type: {template_type}, unsupported.\n"
            )
            sys.exit()

    # Validate secondary circuits if needed
    if template_type.endswith("2C"):
        for key, value in inet2.items():
            if not value and key not in ("full_duplex", "upload", "download"):
                print(
                    f"\nError: Template type: {template_type} selected but missing inet2.{key}\n"
                )
                sys.exit()

    # Validate everything else exists
    error = False
    for key, value in site_info.items():
        if key == "inet2":
            continue
        if key == "inet1":
            for inet_var, inet_value in site_info[key].items():
                if inet_var in ("full_duplex", "upload", "download"):
                    continue
                if not inet_value:
                    error = True
                    print(f"Error: Missing {key}.{inet_var}!")
        else:
            if not value:
                error = True
                print(f"Error: Missing {key}!")
    if error:
        print("Exiting..")
        sys.exit()

    return TEMPLATES[template_type]


def prompt_for_site_information() -> Dict[str, str]:
    """
    Prompt for user input if yaml file is not used
    """
    my_site_info = {}
    for var in REQUIRED_VARS:
        if "inet" not in var and not my_site_info.get(var):
            my_site_info[var] = input(f"{var}: ")
        else:
            my_site_info[var] = {}
            for inet_var in REQUIRED_VARS[var]:
                my_site_info[var][inet_var] = input(f"{var}.{inet_var}: ")

    return my_site_info


def get_site_information(filename: str = None) -> Dict[str, str]:
    """
    Get Site information
    """
    # filename = site-information.yml
    try:
        with open(filename) as fin:
            my_site_info = yaml.safe_load(fin)
    except FileNotFoundError:
        response = input(
            f"\nFile '{filename}' not found! Enter Site Information Maunally? (y/n): "
        )
        if response.lower() not in ("y", "yes"):
            print("Exiting..\n")
            sys.exit()
        else:
            my_site_info = REQUIRED_VARS
            my_site_info = prompt_for_site_information()

    # Set physical port to 100/full if circuit is 100m/100m
    for inet in ("inet1", "inet2"):
        if (
            str(my_site_info[inet].get("download")) == "100"
            and str(my_site_info[inet].get("upload")) == "100"
        ):
            my_site_info[inet]["speed"] = "100"
            my_site_info[inet]["full_duplex"] = True
        else:
            my_site_info[inet]["speed"] = "0"
            my_site_info[inet]["full_duplex"] = False

    return my_site_info


def build_site(args: argparse.Namespace) -> None:
    """
    Load data and output new site.yml file
    """
    print(f"\nBuilding site using {args.t} template type..")

    # Get site information & template
    my_site_info = get_site_information(filename=args.info)
    template_name = validate_template(args.t, my_site_info)

    # Load template
    j2_env = Environment(
        loader=PackageLoader("yaml_config", "templates"),
        lstrip_blocks=True,
        trim_blocks=True,
        undefined=StrictUndefined,
    )
    new_site = j2_env.get_template(template_name)

    # Render config
    try:
        new_site = new_site.render(**my_site_info)
    except UndefinedError as e:
        print(
            f"\nInvalid site information file! Check example for required attributes.\n{e}\n"
        )
        sys.exit()

    # Save output
    output_file = f"{args.n}.yml"
    if args.n.lower() != my_site_info["site_name"].lower():
        print(
            f"\nWarning: '{args.n}' does not match site_name in {output_file} ({my_site_info['site_name']})"
        )
    with open(output_file, "w") as fout:
        fout.write(new_site)
    print(f"\nSuccess!\n{output_file} created in local directory.\n")


def go():
    """
    CLI Settings for build_site
    """
    parser = argparse.ArgumentParser(
        description="Build YAML config file for new site.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """\
        Template Types:
        1K1C    -   ION 1000, 1 Circuit (default)
        1K2C    -   ION 1000, 2 Circuits
        2K1C    -   ION 2000, 1 Circuit (untested)
        2K2C    -   ION 2000, 2 Circuits (untested)
    """
        ),
    )
    parser.add_argument(
        "-n",
        help="Optional Site Name for Output File (default: my-new-site)",
        metavar="Site_name",
        default="my-new-site",
    )
    parser.add_argument(
        "-t",
        help="Optional Template Type (default: 1K1C)",
        default="1K1C",
        choices=["1K1C", "1K2C", "2K1C", "2K2C"],
    )
    parser.add_argument(
        "-i",
        "--info",
        help="Optional Filename containing Site Information (default: site-information.yml)",
        metavar="filename.yml",
        default="site-information.yml",
    )

    args = parser.parse_args()

    build_site(args)


if __name__ == "__main__":
    go()
