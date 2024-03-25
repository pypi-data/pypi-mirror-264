import importlib
from .values import engineering_values, real_values


class test:
    def __init__(self, name: str = ""):
        """The class to menage tensile test results

        This class allows to initialize the tensile test parameter of the sample class. In initialization method only
        name of the sample is required, though normally it is defined by sample class

        Parameters
        ----------
        name : str
            name of the sample

        Examples
        --------
        FIXME: Add docs.

        """
        self.name = name

    def define(self, material_group: str, standard: str):
        """Method of the tensile_test class to define actual test

        This method is used to define the basic parameters of tensile tests like standard as well as material group
        (metals, plastics etc.)

        Parameters
        ----------
        material_group : str
            this parameter sets the actual sample material group like plastic or metal, it is used to choose proper standard
        standard : str
            standard is an parameter to define the standard used in this method. For now only ISO527 is implemented

        Examples
        --------
        FIXME: Add docs.

        """

        self.material_group = material_group.lower()
        self.standard = standard.upper()
        self.standards = self._find_standards()
        module_name = ".".join(
            [
                ".standards",
                self.material_group,
                self.standard,
            ]
        )
        try:
            self._standard_module = importlib.import_module(
                module_name, package=__package__
            )
        except ModuleNotFoundError:
            raise ModuleNotFoundError(
                f"Module {self.material_group}.{self.standard} not found"
            )
        if not isinstance(self, tests):
            self.engineering_values = engineering_values(
                self._standard_module, self.name
            )
            self.real_values = real_values(self.engineering_values, self.name)

    # TODO: ADD EXCEPTION WHEN WRONG STANDARD/MATERIAL GROUP
    # IS CHOSEN
    # TODO: ADD METHODS TO PRINT AVAILABLE MATERIAL GROUPS
    # AND STANDARDS
    @classmethod
    def _find_standards(self):
        from glob import glob
        import os, sys

        path = os.path.join("tensile", "standards", "*", "**.py")

        standards = {}
        for standard in glob(path):
            aux = os.path.split(standard)
            standard = os.path.splitext(aux[1])[0]

            material_group = os.path.split(aux[0])[1]

            try:
                standards[material_group].append(standard)
            except KeyError:
                standards[material_group] = [standard]

        return standards


class tests(test):
    def __init__(self, name):
        """Class to manage multiple tensile_module.test objects

        TODO

        Parameters
        ----------
        name : str
            The general name of whole test object

        Examples
        --------
        FIXME: Add docs.

        """
        self.name = name
        self.results = []

    def _define_handler(self):
        try:
            self.define(self.material_group, self.standard)
        except AttributeError:
            raise AttributeError(
                "You need to define the test before the test appending by using define method"
            )
        tensile_test = test(self.name)
        tensile_test.define(self.material_group, self.standard)
        return tensile_test

    def add(self, tensile_test=None):
        if tensile_test is None:
            self.results.append(self._define_handler())
        elif isinstance(tensile_test, int):
            for test_id in range(tensile_test):
                self.results.append(self._define_handler())
        elif isinstance(tensile_test, test):
            self.results.append(tensile_test)
        elif isinstance(tensile_test, list):
            isValid = all([isinstance(x, test) for x in tensile_test])
        else:
            raise ValueError(
                "Object passed to tests class must be test instance or a list"
            )
