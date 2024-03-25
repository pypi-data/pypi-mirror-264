import numpy as np
import pandas as pd

from typing import Union
import importlib
from . import tensile

__all__ = ["sample"]


class sample:
    def __init__(
        self,
        name: str,
        comments: str = None,
        manufactured_method: str = None,
    ):
        """The class to manage your specimen, actual base class of MatAn

        This class should be used as base MatAn's class, to define your
        specimens, with its composition, modification etc.

        Parameters
        ----------
        name : str
            name of the class
        comments : str
            comments for the sample
        manufactured_method : str
            manufactured method of the sample

        Raises
        ------
        NameError
            when name is not defined

        Examples
        --------
        FIXME: Add docs.

        """

        self.name = name
        self.comments = comments
        self.tensile = tensile.tests(self.name)

    def composition_from_name(
        self, delimiter: str = "-", percent_sign: str = "p"
    ) -> dict:
        """Method to obtain information about composition from name

        This method allows to obtain the composition of your sample
        from its name. For example when name of the sample is
        10pX-20pY, after using this method your sample class will have
        composition paramter of {X:10, Y:20}. This method can also
        return this dictionary

        Parameters
        ----------
        delimiter : str
            delimiter of each compound, if example was 10pX-20pY, then
            delimiter will be "-". "-" is the default value
        percent_sign : str
            percent sign symbol, in example case of 10pX-20pY it was
            "p". "p" is the default value

        Examples
        --------
        FIXME: Add docs.

        Returns
        --------
            composition
        """

        from .files.manager import files

        name = self.name
        self.composition = files.find_composition(name, delimiter, percent_sign)
        return self.composition

    def modification_from_name(self, mods: list, place: int = 0):
        """Function that finds if the sample was somehow modified, for example by thermal annealing

        This can be useful in case you are testing modified samples, and you marked your filename with the letter
        describing it.  By default describing letter is

        Parameters
        ----------
        mods : list
            that is the list of potential modification you have used, for example A for annealing
        place : int
            That is placement of your describing letter in the modification name. By default it is 0, so for **A**nnealing it will be A

        Examples
        --------
        FIXME: Add docs.

        """
        from files.manager import find_modification

        try:
            self.modification = find_modification(self.name, mods, place)
        except NameError:
            raise NameError("Sample name is not defined")

    def method_from_name(self, delimiter: str = "-", placement: int = 0):
        """Find the technique how the material was created

        Find the method how the material was created, what methods were used to modify it, etc. To do so it is using
        first letters of filename, so for extruded parts you can use EXT, for annealed extruded parts you can use aEXT
        etc.
                    For example if you obtained your material by FDM method containing 90pPET10prPET, you can use FDM-90pPET10prPET name, and it will set instance method variable to FDM

        Parameters
        ----------
        methods : list
            what methods you have used on your set
        delimiter : str
            what sign you wanna use to finish your method string. By default it is -

        Raises
        ------
        NameError
            when Sample name is not defined

        Examples
        --------
        FIXME: Add docs.

        """
        try:
            self.method = self.name.split(delimiter)[placement]
            return self.method
        except NameError:
            raise NameError("Sample name is not defined")
