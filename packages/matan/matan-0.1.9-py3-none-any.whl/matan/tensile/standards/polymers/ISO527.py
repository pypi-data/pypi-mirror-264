import numpy as np
from .... import misc

"""
According to ISO 527-1: https://cdn.standards.iteh.ai/samples/75824/61c480ef4bf0494aa6966bd4c2244c2e/ISO-527-1-2019.pdf
"""


class tensile_modulus:
    def __init__(
        self,
        stress,
        stress_unit=None,
        strain=None,
        strain_unit=None,
        lower_limit=0.05,
        upper_limit=0.25,
    ):
        """
        Tensile, or Young's modulus is the slope of strain/stress curve, between strains equals to 0.05 and 0.25 percent
        """

        if lower_limit is None:
            lower_limit = 0.05
        if upper_limit is None:
            upper_limit = 0.25
        if strain_unit != "%":
            lower_limit *= 1e-2
            upper_limit *= 1e-2
        stress = np.array(stress)
        strain = np.array(strain)
        # if not percent_strain:
        #     upper_limit = upper_limit / 100
        #     lower_limit = lower_limit / 100
        # TODO: Add percent strain

        module_strain = strain[(strain > lower_limit) & (strain < upper_limit)]
        try:
            low_idx = np.where(strain == min(module_strain))[0][0]
            upp_idx = np.where(strain == max(module_strain))[0][0]
        except ValueError as er:
            print(er)
            raise ValueError("Strain array does not include  values in limit range")
        module_stress = stress[low_idx : upp_idx + 1]
        array = np.vstack([module_strain, np.ones(len(module_strain))]).T

        E, c = np.linalg.lstsq(array, module_stress, rcond=-1)[0]

        r2 = 1 - c / (module_stress.size * module_stress.var())
        self.r2 = round(r2, 4)
        self.value = misc.round_significant(E, significant=3)
        self.module_strain, self.module_stress = module_strain, module_stress


class at_break:
    def __init__(self, stress, strain):
        self.stress = misc.round_significant(stress[len(stress) - 1], significant=3)
        self.strain = misc.round_significant(strain[len(strain) - 1])


class strength:
    def __init__(self, stress, strain):
        self.stress = misc.round_significant(
            self.find_local_maximum(stress), significant=3
        )
        self.strain = misc.round_significant(strain[self.idx])

    def find_local_maximum(self, stress):
        for i in range(1, len(stress) - 1):
            if stress[i - 1] < stress[i] > stress[i + 1] and stress[i] > 1:
                self.idx = i
                return stress[i]

        print("Strength: Local maximum not found, gives max value")
        self.idx = np.where(stress == np.max(stress))[0][0]
        val = np.max(stress)
        return val


class yield_strength:
    def __init__(self, stress, strain):
        try:
            self.stress = misc.round_significant(
                stress[self.find_idx(stress, strain)], significant=3
            )
            self.strain = misc.round_significant(strain[self.find_idx(stress, strain)])
        except IndexError:
            self.stress, self.strain = None, None

    def find_idx(self, stress, strain):
        for i in range(1, len(strain)):
            if strain[i] > strain[i - 1] and stress[i] <= stress[i - 1]:
                if stress[i] > 1:
                    return i
                else:
                    continue
                    # exit()
        return len(strain) - 1
