"""
This module stores the placeholder arguments who's job it is to convert
arguments from the Dataset level `mpi`,  `omp`, `nodes`, etc. to what the
scheduler is expecting within a jobscript.

.. note::
    Placeholders without a `value` are "falsy". So checking their value in an
    if statement will return `True` if they have a value, `False` otherwise.
"""
from typing import Union, Any

from remotemanager.connection.computers.dynamicvalue import DynamicMixin
from remotemanager.logging import LoggingMixin
from remotemanager.utils import ensure_list


class Resource(LoggingMixin, DynamicMixin):
    """
    Stub class to sit in place of an option within a computer.

    Args:
        name (str):
            name under which this arg is stored
        flag (str):
            Flag to append value to e.g. `--nodes`, `--walltime`
        separator (str):
            Override the separator between flag and value (defaults to "=")
        tag (str):
            Override the tag preceding the flag (defaults to "--")
        default (Any, None):
            Default value, marks this Resource as optional if present
        optional (bool):
            Marks this resource as Optional. Required as there are actually
            three states:
                - Required input, required by scheduler.
                - Optional input, required by scheduler.
                - Optional input, optional by scheduler.
        requires (str, list):
            Stores the name(s) of another variable which is required alongside this one
        replaces (str, list):
            Stores the name(s) of another variable which is replaced by this one
        min (int):
            Minimum value for numeric inputs
        max (int):
            Maximum value for numeric inputs
        format (str):
            Expected format for number. Allows None, "time" or "float"
    """

    __slots__ = [
        "_name",
        "_flag",
        "_requires",
        "_replaces",
        "_optional",
        "format",
        "pragma",
        "tag",
        "separator",
    ]

    def __init__(
        self,
        name: str,
        flag: Union[str, None] = None,
        tag: Union[str, None] = None,
        separator: Union[str, None] = None,
        default: Union[Any, None] = None,
        optional: bool = True,
        requires: Union[str, list, None] = None,
        replaces: Union[str, list, None] = None,
        min: Union[int, None] = None,
        max: Union[int, None] = None,
        format: Union[str, None] = None,
    ):
        super().__init__(
            assignment=name,
            default=default,
            format=format,
            min=min,
            max=max)

        self._name = name
        self._flag = flag
        self._optional = optional

        self._requires = ensure_list(requires)
        self._replaces = ensure_list(replaces)

        self.pragma = None
        self.tag = tag
        self.separator = separator

    def __hash__(self):
        return hash(self._flag)

    def __repr__(self):
        return str(self.value)

    def __bool__(self):
        """
        Makes objects "falsy" if no value has been set, "truthy" otherwise
        """
        return self.value is not None and self.flag is not None

    @property
    def optional(self):
        """Returns True if this Resource is optional at Dataset level"""
        return self._value.default is not None or self._optional

    @property
    def replaces(self) -> list:
        """
        List of arguments whom are no longer considered `required` if this
        resource is specified
        """
        return self._replaces

    @property
    def requires(self) -> list:
        """
        List of requirements if this resource is specified.
        e.g. nodes for mpi_per_node
        """
        return self._requires

    @property
    def name(self) -> str:
        """Returns the name under which this resource is stored"""
        return self._name

    @property
    def flag(self):
        """Returns the flag set for the jobscript"""
        return self._flag

    @property
    def value(self):
        """Returns the set value, otherwise returns the default"""
        val = super().value
        return val

    @value.setter
    def value(self, val):
        super().set_value(val)

    @property
    def resource_line(self) -> str:
        """
        Shortcut to output a suitable resource request line

        Returns:
            str: resource request line
        """
        pragma = f"{self.pragma} " if self.pragma is not None else ""
        tag = self.tag if self.tag is not None else "--"
        separator = self.separator if self.separator is not None else "="

        return f"{pragma}{tag}{self.flag}{separator}{self.value}"

    @property
    def reduced(self):
        return self._value.reduced

    def pack(self) -> dict:
        data = {"flag": self.flag}

        if self.min is not None:
            data["min"] = self.min
        if self.max is not None:
            data["max"] = self.max
        if getattr(self, "default", None) is not None:
            try:
                data["default"] = self.default.reduced
            except AttributeError:
                data["default"] = self.default
        if not self.optional:
            data["optional"] = False
        if len(self.requires) != 0:
            data["requires"] = self.requires
        if len(self.replaces) != 0:
            data["replaces"] = self.replaces
        if self.format is not None:
            data["format"] = self.format
        if self.tag is not None:
            data["tag"] = self.tag
        if self.separator is not None:
            data["separator"] = self.separator

        return data


class runargs(dict):
    """
    Class to contain the dataset run_args in a way that won't break any loops
    over the resources

    Args:
        args (dict):
            Dataset run_args
    """

    _accesserror = (
        "\nParser is attempting to access the flag of the run_args, you "
        "should add an `if {option}: ...` catch to your parser."
        "\nRemember that placeholders without an argument are 'falsy', "
        "see the docs for more info. https://l_sim.gitlab.io/remotemanager"
        "/remotemanager.connection.computers.options.html"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __bool__(self):
        return False

    @property
    def value(self):
        """
        Prevents an AttributeError when a parser attempts to access the value.

        Returns:
            (dict): internal dict
        """
        return self.__dict__

    @property
    def flag(self):
        """
        Parsers should not access the flag method of the run_args, doing so likely
        means that a loop has iterated over this object and is attempting to insert
        it into a jobscript.

        Converts an AttributeError to one more tailored to the situation.

        Returns:
            RuntimeError
        """
        raise RuntimeError(runargs._accesserror)


class Resources:
    """
    Container class to store Resource objects for use by a parser
    """

    __slots__ = ["_names", "_resources", "_run_args", "pragma"]

    def __init__(self, resources, pragma, tag, separator, run_args):
        self._names = []
        self._resources = resources
        self._run_args = run_args

        self.pragma = pragma

        for resource in self._resources:
            self._names.append(resource.name)
            # add pragma to Resource for resource_line property
            resource.pragma = pragma
            if resource.tag is None:
                resource.tag = tag
            if resource.separator is None:
                resource.separator = separator

    def __iter__(self):
        return iter(self._resources)

    def __getitem__(self, item: str) -> Union[Resource, dict]:
        """
        Need to enable Resources["mpi"], for example

        Args:
            item:
                name of resource to get

        Returns:
            Resource
        """
        if item == "run_args":
            return self.run_args
        try:
            return self._resources[self._names.index(item)]
        except ValueError:
            raise ValueError(f"{self} has no resource {item}")

    def get(self, name: str, default: any = "_unspecified"):
        """Allows resource.get(name)"""
        if default == "_unspecified":
            return getattr(self, name)
        return getattr(self, name, default)

    @property
    def run_args(self) -> dict:
        """Returns the stored run_args"""
        return self._run_args
