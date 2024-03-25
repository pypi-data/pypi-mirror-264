import pandas as pd
import numpy as np


class engineering_values:
    def __init__(self, standard_module, name: str):
        self._standard_module = standard_module
        self.name = name

    def calculate(
        self,
        elongation_array,
        elongation_units: str,
        force_array,
        force_units: str,
        initial_length: float,
        width: float,
        height: float,
        initial_stress: float = 0,
    ):
        """method to calculate engineering stress and strain values

        to calculate engineering stress and strain elongation and force arrays are used.

        Parameters
        ----------
        elongation_array : array
            array of elongation values, later translated into numpy array
        elongation_units : str
            units used to measure elongation
        force_array : array
            array of forces during tensile test, later translated into numpy array
        force_units : str
            force units used in tensile test
        initial_length : float
            inital length of the specimen, used to calculate strain values
        width : float
            width of the specimen used to calculate the area for stress array
        height : float
            height of the speciment's intersection

        Raises
        ------
        ValueError
            Exception used for non implemented units

        Examples
        --------
        FIXME: Add docs.

        """

        elongation_array = pd.Series(elongation_array)
        force_array = pd.Series(force_array)
        self.strain = elongation_array / initial_length
        # [elon/initial_length+initial_stress for elon in elongation_array]

        self.area = height * width
        self.stress = force_array / self.area
        # [force/self.area for force in force_array]
        self.strain = pd.Series(self.strain)
        self.stress = pd.Series(self.stress)

        if force_units.upper() != "N":
            raise ValueError("Units other than Newtons are not implemented yet")
        elif elongation_units != "mm":
            raise ValueError("Units other than mm are not implemented yet")
        else:
            self.strain_units = "mm/mm"
            self.stress_units = "MPa"

    def set(self, stress_array, stress_units: str, strain_array, strain_units: str):
        """method to set stress and strain array

        this method to set the strain and stress arrays, it is used in both engineering and real value parameter as it is inherited from engineering_values class by real_values class

        Parameters
        ----------
        stress_array : array
            stress array, to be translated into numpy array
        stress_units : str
            units used in stress array
        strain_array : array
            strain array
        strain_units : str
            units used for strain array

        Examples
        --------
        FIXME: Add docs.

        """

        self.stress = stress_array
        self.stress_units = stress_units

        self.strain = strain_array
        self.strain_units = strain_units

    def calculate_parameters(self):
        """method to generate tensile test parameters values

        this method calculates proper tensile test properties from previously set real stress and strain values, or if
        these values are not calculated or set, this metod try to calculate real values from elongation/force arrays

        Examples
        --------
        FIXME: Add docs.

        """

        try:
            self.calculate_modulus()
            self.calculate_at_break()
            self.calculate_strength()
            self.calculate_yield_strength()
        except AttributeError:
            eobj = self.engineering_values_vals_obj
            self.stress = eobj.stress
            self.stress_units = eobj.stress_units
            self.strain = eobj.strain
            self.strain_units = eobj.strain_units
            self.calculate_modulus()
            self.calculate_at_break()
            self.calculate_strength()
            self.calculate_yield_strength()

    def calculate_modulus(self, lower_limit=None, upper_limit=None):
        """this method calculate Young's modulus named also tensile modulus, according to given standard

        Parameters
        ----------
        lower_limit : float
            lower limit of the strain array to calculate tensile modulus
        upper_limit : float
            upper limit of the strain array to calculate tensile modulus

        Examples
        --------
        FIXME: Add docs.

        """

        self.modulus = self._standard_module.tensile_modulus(
            self.stress,
            self.stress_units,
            self.strain,
            self.strain_units,
            lower_limit,
            upper_limit,
        )

    def calculate_at_break(self):
        """calculate stress and strain values at break moment, according to choosen standard

        Examples
        --------
        FIXME: Add docs.

        """
        self.at_break = self._standard_module.at_break(self.stress, self.strain)

    def calculate_strength(self):
        self.strength = self._standard_module.strength(self.stress, self.strain)

    def calculate_yield_strength(self):
        self.yield_strength = self._standard_module.yield_strength(
            self.stress, self.strain
        )


class real_values(engineering_values):
    def __init__(self, engineering_values_vals_obj: engineering_values, _name: str):
        """initialization of real_values method

        Parameters
        ----------
        engineering_values_vals_obj : engineering_values
            engineering_values
        _name : str
            private variable passed from engineering_values

        Examples
        --------
        FIXME: Add docs.

        """

        self.name = "real " + _name
        self.engineering_values_vals_obj = engineering_values_vals_obj
        self._standard_module = engineering_values_vals_obj._standard_module

    def _calculate_real_strain(self, eng_strain_val: float):
        return np.log(1 + eng_strain_val)

    def calculate(self):
        """overrode calculate method of engineering_values class to calculate real values

        this method allows calculation of real stress and strain from engineering stress and strain

        Examples
        --------
        FIXME: Add docs.

        """

        self.strain = self.engineering_values_vals_obj.strain.apply(
            self._calculate_real_strain
        )
        self.stress = [
            stress_val * (1 + self.strain)
            for stress_val, self.strain in zip(
                self.engineering_values_vals_obj.stress,
                self.engineering_values_vals_obj.strain,
            )
        ]
        self.stress = pd.Series(self.stress)


#     def plot(self, show=False, *args, **kwargs):
#         """Method for plotting the results

#         This method can be used to plot your engineering stress-strain curve. If you wanna show it instantly use
#         parameter show as True

#         Parameters
#         ----------
#         show : bool
#             It it equal to matplotlib.pyplot function show

#         Examples
#         --------
#         FIXME: Add docs.

#         """
#         import matplotlib.pyplot as plt

#         plt.plot(self.strain, self.stress, label=self.name, *args, **kwargs)

#         plt.title(self.name)
#         plt.ylabel(f"Stress [{self.stress_units}]")
#         plt.xlabel(f"Strain [{self.strain_units}]")
#         plt.legend()
#         if show:
#             plt.show()
