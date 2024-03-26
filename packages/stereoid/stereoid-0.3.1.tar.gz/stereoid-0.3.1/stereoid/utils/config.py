"""config provides functionality related to reading .ini config files"""
import configparser
import pathlib
import typing


def parse(
    config_file_path: pathlib.Path = pathlib.Path(__file__).parent.parent.parent
    / "./PAR/user.cfg",
    section: str = "Paths",
    datatypes: typing.Optional[dict] = None,
) -> typing.Dict[str, typing.Any]:
    """
    parse initialises the configuration parser, reads the file
    and returns a dictionary with the parsed parameters.
    the ssa model.

    Adapted from ssafullpol.
    Parameters
    ----------
    config_file_path : str or pathlib.Path
        path to the config file
        (Default value = Path("../PAR/model_parameters.ini"))
    section : str
        section of the config to read from
    datatypes : dict
        keys are variable names, values are strings describing the
        type. Possible values include "int", "float", "list", "bool".
        (Default value = None)

    Returns
    -------
    typed_config : dict
        configuration read from the file.
    """
    project_root = pathlib.Path(__file__).parent.parent.parent
    print(project_root, config_file_path)
    if not (config_file_path.exists() and config_file_path.is_file()):
        config_file_path = project_root / "./PAR/user_defaults.cfg"
        if not (config_file_path.exists() and config_file_path.is_file()):
            raise FileNotFoundError(
                "No default paths.cfg file was found and the fallback default_paths_sample.cfg was not found either. Please check your PAR/ folder"
            )
    default_types = dict.fromkeys(("main", "data", "par", "plot"), "path")
    if datatypes is None:
        datatypes = default_types
    else:
        # merge the user supplied types with the defaults, giving precedence to the user supplied keys
        datatypes = {**default_types, **datatypes}

    def parse_path(p):
        if p.startswith("."):
            path = project_root / p
        else:
            path = pathlib.Path(p).expanduser()
        return path

    config = configparser.ConfigParser(
        delimiters=("=", ":"),
        comment_prefixes=("#", ";"),
        interpolation=configparser.BasicInterpolation(),
        converters={
            "list": lambda x: [i.strip(" []") for i in x.split(",")],
            "path": parse_path,
        },
    )
    config.read(config_file_path)
    typed_config = {}
    # if section is paths, assume all variables are of type "path"
    if section == "Paths":
        for variable in config[section]:
            value = config[section].getpath(variable)
            typed_config[variable] = value
    else:
        for variable, variable_type in datatypes.items():
            if variable_type == "path":
                value = config[section].getpath(variable)
            elif variable_type == "int":
                value = config[section].getint(variable)
            elif variable_type == "float":
                value = config[section].getfloat(variable)
            elif variable_type == "list":
                value = config[section].getlist(variable)
                # need to cast the elements of the list if we want to have
                # them casted to their types, as it is they're added as
                # strings
            elif variable_type == "bool":
                value = config[section].getboolean(variable)
            else:
                value = config[section][variable]
            typed_config[variable] = value
    return typed_config
