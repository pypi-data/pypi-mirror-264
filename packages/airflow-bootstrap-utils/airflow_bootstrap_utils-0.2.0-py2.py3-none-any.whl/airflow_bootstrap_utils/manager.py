# -*- coding: utf-8 -*-
import logging
import os
import pathlib
import sys
import yaml

from datetime import datetime
from typing import Any, Dict, List, Union
from simple_template_toolkit import STTManager

from . import constants
from .file_utils import check_infile_status
from .template.manager import Manager as TemplateManager

DEFAULT_OPERATOR_TYPE = "bash"
DEFAULT_DAG_TEMPLATE_NAME = "dag_template.py"
DEFAULT_TRACE_ENABLED = False

class Manager:
    """Class for managing the creation of Airflow DAG Python files."""

    def __init__(self, **kwargs):
        """Constructor for Manager."""
        self.config = kwargs.get("config", None)
        self.config_file = kwargs.get("config_file", None)
        self.control_file = kwargs.get("control_file", None)
        self.logfile = kwargs.get("logfile", None)
        self.outdir = kwargs.get("outdir", None)
        self.outfile = kwargs.get("outfile", None)
        self.template_dir = kwargs.get("template_dir", None)
        self._trace_enabled = kwargs.get("trace_enabled", DEFAULT_TRACE_ENABLED)
        self.verbose = kwargs.get("verbose", constants.DEFAULT_VERBOSE)

        self.template_manager = TemplateManager(**kwargs)

        logging.info(f"Instantiated Manager in file '{os.path.abspath(__file__)}'")

    def _get_config(
            self,
            name: str,
            lookup: Dict[str, Any]
        ) -> Union[str, Dict[str, Any]]:

        if name not in lookup:
            raise ValueError(f"'{name}' was not found in control file '{self.control_file}'")
        return lookup[name]

    def _check_user(
            self,
            lookup: Dict[str, Any],
            key: str = "%USER%"
        ) -> None:

        if lookup[key] is None or lookup[key] == "":
            lookup[key] = os.getenv("USER")
            logging.info(f"{key} was not specified and therefore was set to '{lookup[key]}'")

    def _check_timestamp(
            self,
            lookup: Dict[str, Any],
            key: str = "%TIMESTAMP%"
        ) -> None:

        if lookup[key] is None or lookup[key] == "":
            lookup[key] = constants.DEFAULT_TIMESTAMP
            logging.info(f"{key} was not specified and therefore was set to '{lookup[key]}'")

    def _check_master_outdir(
            self,
            lookup: Dict[str, Any],
            key: str = "%MASTER_OUTDIR%"
        ) -> None:
        if lookup[key] is None or lookup[key] == "":
            lookup[key] = os.path.join(
                "/tmp",
                os.getenv("USER"),
                constants.DEFAULT_PROJECT,
                lookup["%TIMESTAMP%"]
            )

            logging.info(f"{key} was not specified and therefore was set to '{lookup[key]}'")

    def generate_dag_file(self) -> None:
        """Generate the Airflow DAG Python file."""
        logging.info(
            f"Will attempt to generate Airflow DAG Python file '{self.outfile}'"
        )
        check_infile_status(self.control_file, extension="yaml")

        logging.info(f"Will load contents of control file '{self.control_file}'")
        self.control_lookup = yaml.safe_load(pathlib.Path(self.control_file).read_text())

        datasets_lookup = self._get_config("datasets", self.control_lookup)

        dag_lookup = self._get_config("dag", self.control_lookup)

        substitutions_lookup = self._get_config("substitutions", self.control_lookup)

        common_lookup = self._get_config("common", substitutions_lookup)

        key_placeholder = self._get_config("%KEY%", common_lookup)

        tasks_lookup = self._get_config("tasks", dag_lookup)

        tasks_order = self._get_config("tasks_order", dag_lookup)

        if "%DAG_NAME%" not in common_lookup:
            raise ValueError(f"'%DAG_NAME%' was not found in common_lookup '{common_lookup}'")

        self._check_timestamp(common_lookup)

        self._check_master_outdir(common_lookup)

        self._check_user(common_lookup)


        if "name" not in dag_lookup:
            raise ValueError(f"'name' was not found in dag '{dag_lookup}'")

        if "description" not in dag_lookup:
            dag_lookup["description"] = "N/A"

        if "start_date" not in dag_lookup:
            dag_lookup["start_date"] = datetime.today().strftime("%Y, %m, %d")

        if "schedule_interval" not in dag_lookup:
            dag_lookup["schedule"] = "None"

        if "catchup" not in dag_lookup:
            dag_lookup["catchup"] = "False"

        if "template_name" not in dag_lookup:
            dag_lookup["template_name"] = self.config.get("default_dag_template_name", DEFAULT_DAG_TEMPLATE_NAME)

        airflow_dag_script_list = []

        # Process each dataset.
        # Note that a dataset corresponds with a dictionary in
        # the 'datasets' list in the configuration YAML file.
        for dataset_ctr, dataset in enumerate(datasets_lookup, start=1):

            if key_placeholder not in dataset:
                raise ValueError(f"key_placeholder '{key_placeholder}' was not found in dataset '{dataset}'")

            key = dataset[key_placeholder]

            logging.info(f"Processing dataset number: {dataset_ctr} with key '{key}': {dataset}")

            # Update the dataset with the common_lookup dictionary.
            dataset.update(dag_lookup)
            dataset.update(common_lookup)
            dataset["tasks_order"] = tasks_order
            dataset["tasks"] = []

            # Process each task definition.
            # Note that each task corresponds with a dictionary
            # in the 'tasks' list in the configuration YAML file.
            # Each of these tasks will be converted into an
            # Airflow DAG task.

            uniq_task_name_lookup = {}

            for task_ctr, task in enumerate(tasks_lookup, start=1):
                logging.info(f"Processing task number '{task_ctr}': {task}")

                if "name" not in task:
                    raise ValueError(f"'name' was not found in task '{task}'")

                task_name = task["name"]
                if task_name in uniq_task_name_lookup:
                    raise ValueError(f"task_name '{task_name}' was found more than once in tasks_lookup")
                uniq_task_name_lookup[task_name] = task_name

                task["name"] = task_name.replace(" ", "_")

                if "operator_type" not in task:
                    task["operator_type"] = self.config.get("default_operator_type", DEFAULT_OPERATOR_TYPE)

                if "command" not in task:
                    raise ValueError(f"'command' was not found in task '{task}'")

                # if "template_file" not in task or task["template_file"] is None or task == "":
                #     if common_template_file is None:
                #         raise ValueError(f"task['template_file'] was not defined for task with name '{task['name']}'")
                #     task["template_file"] = common_template_file
                #     logging.info(f"task['template_file'] was not defined and therefore was set to common template file '{common_template_file}'")

                dataset["tasks"].append(task)

            self._perform_inplace_substitutions(dataset)

            dataset["template_name"] = dag_lookup["template_name"]

            dataset_dag_file = os.path.join(
                dataset['%MASTER_OUTDIR%'],
                key,
                f"{dataset['%DAG_NAME%']}.yaml"
            )


            # Write the dataset dictionary to a YAML file.
            self._write_dataset_dag_to_file(dataset, dataset_dag_file)

            airflow_dag_python_file = os.path.join(
                dataset['%MASTER_OUTDIR%'],
                key,
                f"{dataset['%DAG_NAME%']}.airflow.dag.py"
            )

            self.template_manager.generate_outfile_from_template_file(
                template_name=dataset["template_name"],
                lookup=dataset,
                outfile=airflow_dag_python_file,
                infile=self.control_file,
            )

            airflow_dag_script_list.append(airflow_dag_python_file)

        self._write_dag_script_list_to_file(
            airflow_dag_script_list,
            dataset['%MASTER_OUTDIR%']
        )



    def _write_dag_script_list_to_file(
            self,
            airflow_dag_script_list: List[str],
            outdir: str
        ) -> None:
        """Write the Airflow DAG script list to a file.

        Args:
            airflow_dag_script_list (List[str]): The list of Airflow DAG Python scripts.
            outdir (str): The output directory.
        """
        outfile = os.path.join(outdir, "airflow_dag_scripts.txt")

        with open(outfile, "w") as of:
            of.write(f"## method-created: {os.path.abspath(__file__)}\n")
            of.write(f"## date-created: {str(datetime.today().strftime('%Y-%m-%d-%H%M%S'))}\n")
            of.write(f"## created-by: {os.environ.get('USER')}\n")
            of.write(f"## control-file: {self.control_file}\n")
            of.write(f"## logfile: {self.logfile}\n")

            for script in airflow_dag_script_list:
                of.write(f"{script}\n")

        print(f"Wrote Airflow DAG Python script list to file '{outfile}'")
        logging.info(f"Wrote Airflow DAG Python script list to file '{outfile}'")

    def _perform_inplace_substitutions(
            self,
            lookup: Dict[str, Any]
        ) -> None:
        """Perform the placeholder substitutions among the values in the job definition lookup.

        Args:
            lookup (Dict[str, Any]): The job definition lookup.
        """
        if self._trace_enabled:
            logging.info(f"Before: {lookup}\n\n")
        for _ in range(5):
            for key in lookup:
                for current_key, val in lookup.items():
                    if key == current_key:
                        continue
                    if self._trace_enabled:
                        logging.info(f"{key=} {current_key=} {val=}")
                    # Check if val is a string
                    if isinstance(val, str):
                        if key in val:
                            if self._trace_enabled:
                                logging.info(f"Will attempt replacement because {key=} is in {val=}")
                            lookup[current_key] = val.replace(key, lookup[key])
                            if self._trace_enabled:
                                logging.info(f"Now {lookup[current_key]=}")
                    elif isinstance(val, dict):
                        for sub_key, sub_val in val.items():
                            if key in sub_val:
                                lookup[current_key][sub_key] = sub_val.replace(key, lookup[key])
                                if self._trace_enabled:
                                    logging.info(f"Now {lookup[current_key][sub_key]=}")
                    elif isinstance(val, list):
                        for idx, item in enumerate(val):
                            if isinstance(item, dict):
                                for sub_key, sub_val in item.items():
                                    if key in sub_val:
                                        lookup[current_key][idx][sub_key] = sub_val.replace(key, lookup[key])
                                        if self._trace_enabled:
                                            logging.info(f"Now {lookup[current_key][idx][sub_key]=}")
                            else:
                                if key in item:
                                    lookup[current_key][idx] = item.replace(key, lookup[key])
                                    if self._trace_enabled:
                                        logging.info(f"Now {lookup[current_key][idx]=}")


        if self._trace_enabled:
            logging.info(f"\n\nAfter: {lookup}")


    def _write_dataset_dag_to_file(
            self,
            dataset: Dict[str, Any],
            outfile: str
        ) -> None:
        """Write the dataset to a file.

        Args:
            dataset (Dict[str, Any]): The dataset dictionary with all substitutions performed.
            outfile (str): The output YAML file to write the dataset dictionary to.
        """
        dirname = os.path.dirname(outfile)
        if not os.path.exists(dirname):
            pathlib.Path(dirname).mkdir(parents=True, exist_ok=True)
            logging.info(f"Created directory '{dirname}'")

        with open(outfile, "w") as file:
            yaml.dump(dict(dataset), file)

