# -*- coding: utf-8 -*-
import logging
import os
import sys

from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from typing import Any, Dict, Optional

from .. import constants


class Manager:
    """Class for managing the creation of files using jinja templating."""

    def __init__(self, **kwargs):
        """Constructor for Manager."""
        self.config = kwargs.get("config", None)
        self.config_file = kwargs.get("config_file", None)
        self.logfile = kwargs.get("logfile", None)
        self.outdir = kwargs.get("outdir", None)
        self.template_path = kwargs.get("template_dir", constants.DEFAULT_TEMPLATES_DIR)
        self.verbose = kwargs.get("verbose", constants.DEFAULT_VERBOSE)

        self._init_templating_system()

        logging.info(f"Instantiated Manager in file '{os.path.abspath(__file__)}'")

    def _init_templating_system(self) -> None:
        """Initialize the Jinja2 templating loader and environment."""
        # Specify the path to the templates directory
        template_path = self.template_path

        if not os.path.exists(template_path):
            logging.error(f"template path '{template_path}' does not exist")
            sys.exit(1)

        # Create a FileSystemLoader and pass the template path to it
        loader = FileSystemLoader(template_path)

        # Create a Jinja2 Environment using the loader
        self.env = Environment(loader=loader)

    def _generate_output_from_template(
        self,
        template_name: str,
        data: Dict[str, Dict]
    ) -> str:
        """TODO."""
        # Load the template
        template = self.env.get_template(template_name)
        # Render the template with the data
        output = template.render(data)

        return output

    def generate_outfile_from_template_file(
        self,
        template_name: str,
        lookup: Dict[str, Any],
        outfile: str,
        infile: Optional[str] = None,
    ) -> None:
        """Generate the output file from the jinja2 template file specified by template_name.

        Args:
            template_name (str): The name of the jinja2 template file.
            lookup (Dict[str, Any]): The dictionary containing the data to be passed to the template.
            outfile (str): The output file to write the final content to.
            infile (str): The source input file that was used to generate this output file.
        """
        output = self._generate_output_from_template(template_name, lookup)

        self._write_file_from_template(
            template_name,
            outfile,
            output,
            infile,
        )

    def _write_file_from_template(
        self,
        template_name: str,
        outfile: str,
        output: str,
        infile: Optional[str] = None,
    ) -> None:
        with open(outfile, "w") as of:
            of.write(f'"""\nmethod-created: {os.path.abspath(__file__)}\n')
            of.write(
                f"date-created: {str(datetime.today().strftime('%Y-%m-%d-%H%M%S'))}\n"
            )
            of.write(f"created-by: {os.environ.get('USER')}\n")

            if infile is not None or infile != "":
                of.write(f"infile: {infile}\n")

            of.write(f'logfile: {self.logfile}\n"""\n')

            of.write(f"{output}\n")

        logging.info(f"Wrote {template_name} file '{outfile}'")
        if self.verbose:
            print(f"Wrote {template_name} file '{outfile}'")

