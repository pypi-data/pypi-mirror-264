import logging
import os
import textwrap

import yaml
from deepmerge import Merger
from jinja2 import Environment, Undefined
from yaml.parser import ParserError
from yaml.scanner import ScannerError

logger = logging.getLogger(__name__)


class SilentUndefined(Undefined):
    """Do not error out if a value is not found"""

    def _fail_with_undefined_error(self, *args, **kwargs):
        return ""


def jinja_dict_to_yaml(*obj, **options) -> str:
    """
    Convert dict to yaml in human readable format.

    This writes the yaml in full format, for better parsing of jinja includes

    Args:
        obj: the object to present as yaml
        options: optional parameters to pass on to yaml.safe_dump function

    Return:
        A human readable yaml presentation of the original input

    """
    if options.get('indent'):
        indent = options['indent']
        del options['indent']
        return textwrap.indent(yaml.safe_dump(*obj, indent=2, allow_unicode=True, default_flow_style=False, **options),
                               ' ' * indent)

    return yaml.safe_dump(*obj, indent=4, allow_unicode=True, default_flow_style=False, **options)


class ParseJinja:
    """Parser for all jinja related files, and allows you to merge the output with initial parameters"""

    def __init__(self):
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.jinja2env = Environment(undefined=SilentUndefined)
        self.jinja2env.filters['to_yaml'] = jinja_dict_to_yaml

    @staticmethod
    def merge(parameters_left: dict, parameters_right: dict) -> dict:
        """Combines 2 dicts with a merger

        Args:
            parameters_left (dict): low prio dict
            parameters_right (dict): high prio dict

        Returns:
            dict: merged dict
        """
        my_merger = Merger(
            [  # merger strategy
                (list, ["append"]),
                (dict, ["merge"]),
            ],
            ["override"],  # fallback strategies,
            ["override"],  # conflict strategy
        )
        return my_merger.merge(parameters_left, parameters_right)

    @staticmethod
    def get_yaml_filenames(path: str) -> list[str]:
        """get all yaml files in specified path

        Args:
            path (str): path to a directory

        Returns:
            list[str]: list of yaml files found
        """
        return [os.path.join(path, filename) for filename in os.listdir(f"{path}") if filename.endswith(".yaml")]

    def parse_directory(self, path: str, parameters: dict = None) -> dict:
        """parse all yaml files in the directory and return their merged value as dict
            results get merged with parameters before return

        Args:
            path (str): path to a directory
            parameters (dict, optional): parameters to merge the dict with. Defaults to {}.

        Returns:
            dict: merged dict of all parsed files and provided parameters
        """
        if parameters is None:
            parameters = {}
        for filename in self.get_yaml_filenames(path=path):
            parameters = self.parse_file(filename=filename, parameters=parameters)
        return parameters

    def parse_file(self, filename: str, parameters=None) -> dict:
        """parse a specific file and merge its result with parameters

        Args:
            filename (str): _description_
            parameters (dict, optional): parameters to merge the dict with. Defaults to {}.

        Raises:
            FileNotFoundError: file was not found

        Returns:
            dict: merged dict of all parsed file and provided parameters
        """
        if parameters is None:
            parameters = {}
        print(f"parsing file: {filename}")
        with open(filename, encoding="utf-8") as file:
            j2 = file.read()
            output = self.jinja2env.from_string(j2).render(env=os.environ, **parameters)
            logger.debug(f"output: {output}")
            try:
                y = yaml.safe_load(output)
            except ParserError as e:
                raise ParserError(f"in content:\n{output}\nerror: {e}")
            except ScannerError as e:
                raise ParserError(f"in content:\n{output}\nerror: {e}")
            if not y:
                return parameters
            return self.merge(parameters, y)
