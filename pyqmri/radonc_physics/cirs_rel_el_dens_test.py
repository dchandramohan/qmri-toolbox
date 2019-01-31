import atom_calc

CIRS_materials = {
    'Water (Diagnostic)' : {
        'Measured Density' : 1.016,
        'Composition' : {
            'C' : 0.6872,
            'O' : 0.1769,
            'H' : 0.0955,
            'N' : 0.0166,
            'Ca' : 0.0218,
            'Cl' : 0.0015
        },
        'Reference El. Dens.' : 1.002
    },
    'Lung (Inhale)' : {
        'Measured Density' : 0.197,
        'Composition' : {
            'C' : 0.6750,
            'O' : 0.1860,
            'H' : 0.0880,
            'N' : 0.0350,
            'Cl' : 0.0160,
        },
        'Reference El. Dens.' : 0.190,
    },
    'Lung (Exhale)' : {
        'Measured Density' : 0.494,
        'Composition' : {
            'C' : 0.7020,
            'O' : 0.1510,
            'H' : 0.0980,
            'N' : 0.0230,
            'Ca' : 0.0160,
            'Cl' : 0.0100,
        },
        'Reference El. Dens.' : 0.489,
    },
    'Breast Tissue (50% Gland/50% Adipose)' : {
        'Measured Density' : 0.989,
        'Composition' : {
            'C' : 0.7030,
            'O' : 0.1700,
            'H' : 0.0960,
            'N' : 0.0190,
            'Ca' : 0.0090,
            'Cl' : 0.0020,
        },
        'Reference El. Dens.' : 0.976,
    },
    'Liver' : {
        'Measured Density' : 1.069,
        'Composition' : {
            'C' : 0.7010,
            'O' : 0.1636,
            'H' : 0.0922,
            'N' : 0.0199,
            'Ca' : 0.0222,
            'Cl' : 0.0011,
        },
        'Reference El. Dens.' : 1.052,
    },
    'Muscle' : {
        'Measured Density' : 1.067,
        'Composition' : {
            'C' : 0.6970,
            'O' : 0.1680,
            'H' : 0.0910,
            'N' : 0.0210,
            'Ca' : 0.0220,
            'Cl' : 0.0010,
        },
        'Reference El. Dens.' : 1.043,
    },
    'Adipose' : {
        'Measured Density' : 0.966,
        'Composition' : {
            'C' : 0.7130,
            'O' : 0.1640,
            'H' : 0.1000,
            'N' : 0.0180,
            'Ca' : 0.0030,
            'Cl' : 0.0020,
        },
        'Reference El. Dens.' : 0.949,
    },
    'Ref. Bone 200 mg/cc HA' : {
        'Measured Density' : 1.167,
        'Composition' : {
            'C' : 0.5630,
            'O' : 0.2270,
            'H' : 0.0700,
            'N' : 0.0200,
            'Ca' : 0.0850,
            'P' : 0.0330,
            'Cl' : 0.0020,
        },
        'Reference El. Dens.' : 1.117,
    },
    'Ref. Bone 800 mg/cc HA' : {
        'Measured Density' : 1.613,
        'Composition' : {
            'C' : 0.3911,
            'O' : 0.3372,
            'H' : 0.0445,
            'N' : 0.0087,
            'Ca' : 0.2177,
            'Cl' : 0.0005,
        },
        'Reference El. Dens.' : 1.456
    },
}

for plug in CIRS_materials:
    print('{:s} | {:f} | {:f}'.format(
        plug,
        atom_calc.EmpiricalSubstance(CIRS_materials[plug]['Composition']).calc_density_rel_el(
            CIRS_materials[plug]['Measured Density']
        ),
        CIRS_materials[plug]['Reference El. Dens.']
    ))

