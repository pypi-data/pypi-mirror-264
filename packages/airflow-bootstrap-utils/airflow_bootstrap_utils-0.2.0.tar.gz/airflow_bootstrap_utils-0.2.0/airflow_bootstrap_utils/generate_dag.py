"""Parse the control file and generate the Airflow DAG Python file."""
import click
import logging
import os
import pathlib
import sys
import yaml

from datetime import datetime
from pathlib import Path

from rich.console import Console

from .console_helper import print_yellow, print_green
from .file_utils import check_infile_status
from .manager import Manager
from . import constants


DEFAULT_OUTDIR = os.path.join(
    constants.DEFAULT_OUTDIR_BASE,
    os.path.splitext(os.path.basename(__file__))[0],
    constants.DEFAULT_TIMESTAMP,

)

error_console = Console(stderr=True, style="bold red")

console = Console()



def validate_verbose(ctx, param, value):
    """Validate the validate option.

    Args:
        ctx (Context): The click context.
        param (str): The parameter.
        value (bool): The value.

    Returns:
        bool: The value.
    """

    if value is None:
        click.secho("--verbose was not specified and therefore was set to 'True'", fg='yellow')
        return constants.DEFAULT_VERBOSE
    return value




@click.command()  # type: ignore
@click.option(
    "--config_file",
    type=click.Path(exists=True),
    help=f"Optional: The configuration file for this project - default is '{constants.DEFAULT_CONFIG_FILE}'",
)  # type: ignore
@click.option(
    "--control_file",
    type=click.Path(exists=True),
    help="Required: The control file that defines the Airflow DAG",
)  # type: ignore

@click.option("--logfile", help="Optional: The log file")  # type: ignore
@click.option(
    "--outdir",
    help=f"Optional: The output directory where the output files will be written to - default is '{DEFAULT_OUTDIR}'",
)  # type: ignore
@click.option("--outfile", help="Optional: The output Airflow DAG Python file")  # type: ignore
@click.option(
    "--template_dir",
    help=f"Optional: The directory containing the Jinja2 template files - default is '{constants.DEFAULT_TEMPLATES_DIR}'",
)  # type: ignore
@click.option(
    '--verbose',
    is_flag=True,
    help=f"Will print more info to STDOUT - default is '{constants.DEFAULT_VERBOSE}'.",
    callback=validate_verbose
)  # type: ignore
def main(
    config_file: str,
    control_file: str,
    logfile: str,
    outdir: str,
    outfile: str,
    template_dir: str,
    verbose: bool,
) -> None:
    """Parse the control file and generate the Airflow DAG Python file."""
    error_ctr = 0

    if control_file is None:
        error_console.print("--control_file was not specified")
        error_ctr += 1

    if error_ctr > 0:
        sys.exit(1)

    check_infile_status(control_file, extension="yaml")

    if config_file is None:
        config_file = constants.DEFAULT_CONFIG_FILE
        print_yellow(
            f"--config_file was not specified and therefore was set to '{config_file}'"
        )

    check_infile_status(config_file, extension="yaml")

    if outdir is None:
        outdir = DEFAULT_OUTDIR
        print_yellow(
            f"--outdir was not specified and therefore was set to '{outdir}'"
        )

    if not os.path.exists(outdir):
        pathlib.Path(outdir).mkdir(parents=True, exist_ok=True)
        print_yellow(f"Created output directory '{outdir}'")

    if template_dir is None:
        template_dir = constants.DEFAULT_TEMPLATES_DIR
        print_yellow(
            f"--template_dir was not specified and therefore was set to '{template_dir}'"
        )

    if not os.path.exists(template_dir):
        error_console.print(
            f"template_dir '{template_dir}' does not exist"
        )
        sys.exit(1)

    if not os.path.isdir(template_dir):
        error_console.print(
            f"template_dir '{template_dir}' is not a regular directory"
        )
        sys.exit(1)

    if verbose is None:
        verbose = constants.DEFAULT_VERBOSE
        print_yellow(f"--verbose was not specified and therefore was set to '{verbose}'")

    if logfile is None:
        logfile = os.path.join(
            outdir, os.path.splitext(os.path.basename(__file__))[0] + ".log"
        )
        print_yellow(
            f"--logfile was not specified and therefore was set to '{logfile}'"
        )

    logfile = os.path.abspath(logfile)

    if outfile is None:
        outfile = os.path.join(
            outdir, os.path.splitext(os.path.basename(control_file))[0] + ".py"
        )
        print_yellow(
            f"--outfile was not specified and therefore was set to '{outfile}'"
        )


    logging.basicConfig(
        format=constants.DEFAULT_LOGGING_FORMAT,
        level=constants.DEFAULT_LOGGING_LEVEL,
        filename=logfile,
    )

    # Read the configuration from the YAML file and
    # load into dictionary.
    logging.info(f"Loading configuration from '{config_file}'")

    logging.info("Will load contents of config file 'config_file'")
    config = yaml.safe_load(Path(config_file).read_text())

    manager = Manager(
        config=config,
        config_file=config_file,
        control_file=control_file,
        logfile=logfile,
        outdir=outdir,
        outfile=outfile,
        template_dir=template_dir,
        verbose=verbose,
    )

    manager.generate_dag_file()

    if verbose:
        console.print(f"The log file is '{logfile}'")
        print_green(f"Execution of '{os.path.abspath(__file__)}' completed")


if __name__ == "__main__":
    main()
