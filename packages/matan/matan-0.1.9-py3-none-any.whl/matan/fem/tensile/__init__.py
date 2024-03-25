def elastic_strain(stress, tensile_modulus):
    return [stress_val / tensile_modulus for stress_val in stress]


def plastic_strain(strain, elastic_strain):
    return [
        strain_val - elastic_strain_val
        for strain_val, in strain
        for elastic_strain_val in elastic_strain
    ]
