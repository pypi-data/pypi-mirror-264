# -*- coding: utf-8 -*-
import csv
import logging
import os
import re
import sys
import pathlib

from datetime import datetime
from typing import Any, Dict, List

from jinja2 import Environment, FileSystemLoader

DEFAULT_VERBOSE = True

MAX_UNIQUE_VALUES_FOR_EXAMPLES = 4

class Manager:
    """Class for managing the creation of the validation modules."""

    def __init__(self, **kwargs):
        """Constructor for Manager."""
        self.config = kwargs.get("config", None)
        self.config_file = kwargs.get("config_file", None)
        self.data_file_type = kwargs.get("data_file_type", None)
        self.logfile = kwargs.get("logfile", None)
        self.namespace = kwargs.get("namespace", None)
        self.outdir = kwargs.get("outdir", None)
        self.template_path = kwargs.get("template_path", None)
        self.verbose = kwargs.get("verbose", DEFAULT_VERBOSE)

        # Define a regular expression pattern to match special characters
        self.pattern = r"[^a-zA-Z0-9\s]"  # This pattern will keep alphanumeric characters and whitespace

        self.column_name_to_attribute_name_lookup = {}
        self.max_equality_values = self.config["max_equality_values"]

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

    def generate_validation_modules(self, infile: str) -> None:
        """Generate the validation modules for the specified file.

        Args:
            infile (str): the input tab-delimited or csv file
        Returns:
            None
        """
        logging.info(
            f"Will attempt to generate validation modules for input file '{infile}'"
        )
        if not os.path.exists(infile):
            raise Exception(f"file '{infile}' does not exist")

        extension = os.path.splitext(infile)[1]

        if extension == ".csv":
            self._generate_validation_modules_for_tsv_file(infile, is_tsv=False)
        elif extension == ".tsv" or extension == ".txt":
            self._generate_validation_modules_for_tsv_file(infile, is_tsv=True)
        else:
            logging.error(
                f"Support does not exist for files with extension '{extension}'"
            )
            sys.exit(1)

    def _generate_validation_modules_for_tsv_file(self, infile: str, is_tsv: bool = True) -> None:
        """Generate the validation modules for the specified .tsv or .csv file.

        Args:
            infile (str): the input .tsv or .csv file
            is_tsv (bool): True if the file is a .tsv file, False if it is a .csv file
        Returns:
            None
        """
        header_to_position_lookup = {}

        header_to_position_lookup = self._derive_column_headers_for_tsv_file(infile, is_tsv=is_tsv)

        self._generate_validator_class(header_to_position_lookup, infile)
        self._generate_parser_class(header_to_position_lookup, infile)
        self._generate_main_script(self.data_file_type, self.namespace, infile)
        self._process_columns_for_tsv_file(infile, header_to_position_lookup, is_tsv=is_tsv)

    def _generate_main_script(self, data_file_type: str, namespace: str, infile: str) -> None:
        """Generate the main script that will be used to execute the validation.

        Args:
            data_file_type (str): the type of data file to be processed
            namespace (str): the namespace where the modules will be located
            infile (str): the source input file that was used to generate this validation component
        """
        namespace_temp_dir = f"{namespace.lower().replace('.', '-')}-validator"
        template_name = "validate_file.py"

        lookup = {
            "namespace": namespace,
            "namespace_temp_dir": namespace_temp_dir,
            "data_file_type": data_file_type
        }

        output = self._generate_output_from_template(template_name, lookup)

        outfile = os.path.join(self.outdir, template_name)

        self._write_class_file_from_template(template_name, outfile, output, infile)

    def _generate_validator_class(
        self, header_to_position_lookup: Dict[str, int], infile: str
    ) -> None:
        """Generate the validation module that will contain the Validator class that will drive the validation.

        Args:
            header_to_position_lookup (dict): key is the header name, value is the index position
            infile (str): the source input file that was used to generate this validation component
        """

        # Specify the name of the template file
        template_name = "validator.py"

        # Create a dictionary with data to be passed to the template
        lookup = {}

        for column_name, column_position in header_to_position_lookup.items():
            attribute_name = self.column_name_to_attribute_name_lookup[column_name]
            lookup[attribute_name] = column_position

        data = {"field_lookup": lookup, "file_type": self.data_file_type}

        output = self._generate_output_from_template(template_name, data)

        namespace_dir = self.namespace.lower().replace(".", "/")
        outdir = os.path.join(self.outdir, namespace_dir)
        if not os.path.exists(outdir):
            pathlib.Path(outdir).mkdir(parents=True, exist_ok=True)
            logging.info(f"Created output directory '{outdir}'")

        outfile = os.path.join(outdir, template_name)

        self._write_class_file_from_template(template_name, outfile, output, infile)

    def _generate_parser_class(
        self, header_to_position_lookup: Dict[str, int], infile: str
    ) -> None:
        """Generate the parser module that will contain the Parser class that will provide a way to parse/read the file.

        Args:
            header_to_position_lookup (dict): key is the header name, value is the index position
            infile (str): the source input file that was used to generate this parser.py file/module
        """

        # Specify the name of the template file
        template_name = "parser.py"

        # Create a dictionary with data to be passed to the template
        lookup = {}

        for column_name, column_position in header_to_position_lookup.items():
            attribute_name = self.column_name_to_attribute_name_lookup[column_name]
            lookup[attribute_name] = column_position

        data = {"field_lookup": lookup, "file_type": self.data_file_type}

        output = self._generate_output_from_template(template_name, data)

        namespace_dir = self.namespace.lower().replace(".", "/")
        outdir = os.path.join(self.outdir, namespace_dir)
        if not os.path.exists(outdir):
            pathlib.Path(outdir).mkdir(parents=True, exist_ok=True)
            logging.info(f"Created output directory '{outdir}'")

        outfile = os.path.join(outdir, template_name)

        self._write_class_file_from_template(template_name, outfile, output, infile)

    def _process_columns_for_tsv_file(
        self,
        infile: str,
        header_to_position_lookup: Dict[str, int],
        is_tsv: bool = True
    ) -> None:
        """TBD."""
        lookup = {}
        enum_lookup = {}

        for column_name, column_position in header_to_position_lookup.items():
            attribute_name = self.column_name_to_attribute_name_lookup[column_name]
            logging.info(
                f"Processing column name '{column_name}' (with attribute name '{attribute_name}') at column position '{column_position}'"
            )

            if attribute_name not in lookup:
                class_name = self._derive_class_name_for_column_name(column_name)

                lookup[attribute_name] = {
                    "datatype": "str",
                    "column_name": column_name,
                    "column_position": column_position + 1,
                    "class_name": class_name,
                    "examples": []
                }

            uniq_val_lookup = {}
            uniq_val_ctr = 0
            uniq_val_list = []

            delimiter="\t"
            if not is_tsv:
                delimiter = ","

            with open(infile) as f:
                reader = csv.reader(f, delimiter=delimiter)
                row_ctr = 0
                for row in reader:
                    row_ctr += 1
                    if row_ctr == 1:
                        continue
                    else:
                        if len(row) == 0:
                            # Blank line to be skipped?
                            continue
                        # print(f"{row=}")
                        val = row[column_position]
                        if val is None or val == "":
                            # Skip empty values
                            continue
                        if val not in uniq_val_lookup:
                            uniq_val_lookup[val] = 0
                            uniq_val_list.append(val)
                            if (len(lookup[attribute_name]["examples"]) < MAX_UNIQUE_VALUES_FOR_EXAMPLES):
                                lookup[attribute_name]["examples"].append(val)
                            uniq_val_ctr += 1
                        uniq_val_lookup[val] += 1

            if uniq_val_ctr == 0:
                lookup[attribute_name]["required"] = False
            else:
                lookup[attribute_name]["required"] = True

            datatype = self._determine_datatype(uniq_val_list)

            if datatype == "different":
                lookup[attribute_name]["datatype"] = "str"
            else:
                lookup[attribute_name]["datatype"] = datatype


            str_len_min = 0
            str_len_max = 0

            if uniq_val_ctr <= self.max_equality_values:
                logging.info(
                    f"Will generate enum class for attribute '{attribute_name}' for column '{column_name}' because the max unique values is '{uniq_val_ctr}'"
                )
                class_name = lookup[attribute_name]["class_name"]
                self._load_enum_lookup(uniq_val_lookup, enum_lookup, class_name)
                lookup[attribute_name]["uniq_values"] = []
                for uniq_val in uniq_val_lookup:
                    lookup[attribute_name]["uniq_values"].append(uniq_val)
                    if datatype == "str":
                        str_len = len(uniq_val)
                        if str_len_min == 0 or str_len < str_len_min:
                            str_len_min = str_len
                        if str_len > str_len_max:
                            str_len_max = str_len
                    elif datatype == "int" or datatype == "float":
                        if datatype == "int":
                            uniq_val = int(uniq_val)
                        elif datatype == "float":
                            uniq_val = float(uniq_val)
                        if "min" not in lookup[attribute_name]:
                            lookup[attribute_name]["min"] = uniq_val
                        elif uniq_val < lookup[attribute_name]["min"]:
                            lookup[attribute_name]["min"] = uniq_val
                        if "max" not in lookup[attribute_name]:
                            lookup[attribute_name]["max"] = uniq_val
                        elif uniq_val > lookup[attribute_name]["max"]:
                            lookup[attribute_name]["max"] = uniq_val
                if datatype == "str":
                    lookup[attribute_name]["min"] = str_len_min
                    lookup[attribute_name]["max"] = str_len_max

            self._write_column_report_file(
                column_name,
                column_position,
                infile,
                uniq_val_ctr,
                uniq_val_lookup,
                row_ctr,
            )

        self._generate_record_class(lookup, enum_lookup, infile)

    def _load_enum_lookup(self, uniq_val_lookup, enum_lookup, class_name) -> None:
        """Load values into the enum lookup for this class.

        Args:
            TODO
        """
        if class_name not in enum_lookup:
            enum_lookup[class_name] = {}

        for val in uniq_val_lookup:
            enum_name = self._derive_attribute_name(val)

            enum_name = enum_name.upper()

            if len(enum_name) == 1 or re.search(r"^\d", val):
                enum_name = f"{class_name.upper()}_{val.upper()}"

            logging.info(f"{enum_name=} {val=}")

            enum_name = (
                enum_name.replace(" ", "")
                .replace("*", "")
                .replace("\\", "")
                .replace("/", "_")
                .replace("|", "_")
                .replace("(", "_")
                .replace(")", "_")
                .replace(".", "_")
                .replace("-", "_")
            )

            enum_lookup[class_name][enum_name] = val

    def _write_column_report_file(
        self,
        column_name,
        column_position,
        infile,
        uniq_val_ctr,
        uniq_val_lookup,
        row_ctr,
    ) -> None:
        """Write the report file for the column.

        Args:
            TODO
        Returns:
            None
        """
        outfile = self._derive_column_outfile(column_name, column_position)

        total_row_count = row_ctr - 1

        with open(outfile, "w") as of:
            of.write(f"## method-created: {os.path.abspath(__file__)}\n")
            of.write(
                f"## date-created: {str(datetime.today().strftime('%Y-%m-%d-%H%M%S'))}\n"
            )
            of.write(f"## created-by: {os.environ.get('USER')}\n")
            of.write(f"## infile: {infile}\n")
            of.write(f"## logfile: {self.logfile}\n")

            of.write(f"Column name: '{column_name}'\n")
            of.write(f"Column position: '{column_position}'\n")
            of.write(f"Number of data rows: '{total_row_count}'\n")
            of.write(f"Here are the unique '{uniq_val_ctr}' values:\n")

            for val, count in uniq_val_lookup.items():
                percent = count / total_row_count * 100
                of.write(f"value: '{val}'; count: {count}; percentage: {percent}\n")

        logging.info(f"Wrote column report file '{outfile}'")
        if self.verbose:
            print(f"Wrote column report file '{outfile}'")

    def _derive_column_outfile(self, column_name: str, column_position: int) -> str:
        """Derive the output file for the column-specific values.

        Args:
            column_name (str): the column name
        Returns:
            str: the output file
        """
        basename = (
            column_name.replace(" ", "")
            .replace("*", "")
            .replace("\\", "")
            .replace("/", "_")
            .replace("|", "_")
            .replace("(", "_")
            .replace(")", "_")
        )
        outfile = os.path.join(self.outdir, f"{column_position}_{basename}.tsv")
        return outfile

    def _derive_column_headers_for_tsv_file(self, infile: str, is_tsv: bool = True) -> Dict[str, int]:
        """Derive the column headers for the input .tsv file.

        Args:
            infile (str): the file to be parsed
        Returns:
            dict: column header is the key and column number is the value
        """
        lookup = {}
        column_ctr = 0
        column_name_to_attribute_name_lookup = {}

        delimiter="\t"
        if not is_tsv:
            delimiter = ","

        with open(infile) as f:
            reader = csv.reader(f, delimiter=delimiter)
            row_ctr = 0
            for row in reader:
                row_ctr += 1
                if row_ctr == 1:
                    for field in row:
                        lookup[field] = column_ctr
                        attribute_name = self._derive_attribute_name(field)
                        column_name_to_attribute_name_lookup[field] = attribute_name
                        column_ctr += 1
                    logging.info(f"Processed the header of .tsv file '{infile}'")
                    break
        logging.info(f"Found '{column_ctr}' columns in file '{infile}'")
        self.column_name_to_attribute_name_lookup = column_name_to_attribute_name_lookup
        return lookup

    def _derive_attribute_name(self, column_name: str) -> str:
        """Derive the attribute name for the column name.

        This will remove special characters and spaces and lowercase the string.
        Args:
            column_name (str): the column name
        Returns:
            str: the attribute name
        """
        # Use re.sub to replace all matches with an empty string
        attribute_name = re.sub(self.pattern, "", column_name)
        attribute_name = attribute_name.lower().replace(" ", "")
        return attribute_name

    def _snake_to_upper_camel(self, class_name: str):
        words = class_name.split("_")
        camel_case_words = [word.capitalize() for word in words]
        return "".join(camel_case_words)

    def _derive_class_name_for_column_name(self, column_name: str) -> str:
        """Derive the class name for the column name.

        This will remove special characters and spaces.
        Args:
            column_name (str): the column name
        Returns:
            str: the class name
        """
        class_name = (
            column_name.replace(" ", "_")
            .replace("*", "")
            .replace("#", "")
            .replace("\\", "")
            .replace("/", "_")
            .replace("|", "_")
            .replace("(", "_")
            .replace(")", "_")
        )

        return self._snake_to_upper_camel(class_name)

    def _generate_record_class(
        self,
        lookup: Dict[str, Dict[str, str]],
        enum_lookup: Dict[str, Dict[str, str]],
        infile: str,
    ) -> None:
        """TODO."""
        # Specify the name of the template file
        template_name = "record.py"

        if "validation_functions" in self.config:
            lookup["validation_functions"] = self.config["validation_functions"]
            logging.info(f"Added the validation functions to the lookup dictionary from the configuration file '{self.config_file}'")
        else:
            logging.warning(f"Did not find any validation functions in the configuration file '{self.config_file}'")

        # Create a dictionary with data to be passed to the template
        data = {
            "lookup": lookup,
            "file_type": self.data_file_type,
            "enum_lookup": enum_lookup,
        }

        output = self._generate_output_from_template(template_name, data)

        namespace_dir = self.namespace.lower().replace(".", "/")
        outdir = os.path.join(self.outdir, namespace_dir)
        if not os.path.exists(outdir):
            pathlib.Path(outdir).mkdir(parents=True, exist_ok=True)
            logging.info(f"Created output directory '{outdir}'")

        outfile = os.path.join(outdir, template_name)

        self._write_class_file_from_template(template_name, outfile, output, infile)

    def _generate_output_from_template(
        self, template_name: str, data: Dict[str, Dict]
    ) -> str:
        """TODO."""
        # Load the template
        template = self.env.get_template(template_name)
        # Render the template with the data
        output = template.render(data)

        return output

    def _write_class_file_from_template(
        self, template_name: str, outfile: str, output: str, infile: str
    ) -> None:
        with open(outfile, "w") as of:
            of.write(f'""" method-created: {os.path.abspath(__file__)}\n')
            of.write(
                f"date-created: {str(datetime.today().strftime('%Y-%m-%d-%H%M%S'))}\n"
            )
            of.write(f"created-by: {os.environ.get('USER')}\n")
            of.write(f"infile: {infile}\n")
            of.write(f'logfile: {self.logfile}\n"""\n')

            of.write(f"{output}\n")

        logging.info(f"Wrote {template_name} file '{outfile}'")
        if self.verbose:
            print(f"Wrote {template_name} file '{outfile}'")

    def _determine_datatype(self, values: List[Any]) -> str:
        # Check if the array is not empty
        if not values:
            logging.warning("The values array is empty so returning 'str' as the datatype.")
            return "str"

        first_value = values[0]
        first_datatype = None
        first_datatype_clean = None

        if self._is_convertible_to_int(first_value):
            first_value = int(first_value)
            first_datatype = "int"
            first_datatype_clean = "int"
        elif self._is_convertible_to_float(first_value):
            first_value = float(first_value)
            first_datatype = "float"
            first_datatype_clean = "float"
        else:
            # Get the datatype of the first element
            first_datatype = type(first_value)
            first_datatype_clean = str(type(values[0])).split("'")[1]

        different = True

        # Iterate through the array starting from the second element
        for value in values[1:]:
            current_datatype = None
            # Check if the datatype of the current element matches the first datatype
            if self._is_convertible_to_int(value):
                value = int(value)
                if first_datatype == "int":
                    continue
            elif self._is_convertible_to_float(value):
                value = float(value)
                if first_datatype == "float":
                    continue

            if type(value) != first_datatype:
                logging.info(
                    f"values does not have a consistent datatype. Expected {first_datatype}, but found {type(value)}."
                )
                return "different"

        # If the loop completes without returning, all elements have the same datatype
        logging.info(
            f"All elements in the values array have the datatype: {first_datatype}"
        )
        return first_datatype_clean

    def _is_convertible_to_int(self, value):
        try:
            # Try converting the string to an integer
            int_value = int(value)
            logging.info(f"{value} can be safely converted into an integer value")
            return True
        except ValueError:
            # Conversion failed
            logging.info(f"{value} cannot be safely converted into an integer value")
            return False

    def _is_convertible_to_float(self, value):
        try:
            # Try converting the string to a float
            float_value = float(value)
            logging.info(f"{value} can be safely converted into an float value")
            return True
        except ValueError:
            # Conversion failed
            logging.info(f"{value} cannot be safely converted into an float value")
            return False
