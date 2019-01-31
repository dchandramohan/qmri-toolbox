__author__ = 'Dharshan Chandramohan'
'''
Calculates Im via the Bragg Additivity Rule and Relative 
Electron Density for pure compounds, analytical mixtures 
of pure compounds, and experimentally determined mixtures...
'''

import numpy as np

_periodic_table = { # maybe eventually expand this to contain more elements... implement as ordereddict sorted by atomic number, etc.
    'H' : { 'Z' : 1, 'A' : 1.0079, 'I_m' : 19.2 },
    'C' : { 'Z' : 6, 'A' : 12.011, 'I_m' : 81 },
    'N' : { 'Z' : 7, 'A' : 14.0067, 'I_m' : 82 },
    'O' : { 'Z' : 8, 'A' : 15.9994, 'I_m' : 106 },
    'P' : { 'Z' : 15, 'A' : 30.9736, 'I_m' : 195.5 },
    'S' : { 'Z' : 16, 'A' : 32.06, 'I_m' : 203.4 },
    'Cl' : { 'Z' : 17, 'A' : 35.45 },
    'Ca' : { 'Z' : 20, 'A' : 40.08, 'I_m' : 215.8 },
    'Se' : { 'Z' : 34, 'A' : 78.96, 'I_m' : 348 },
}

class Compound(object):
    
    def __init__(self, formula_dict):
        self.formula = [(_periodic_table[symbol], formula_dict[symbol]) for symbol in formula_dict]
        return

    def calc_mol_wt(self):
        return sum(nn * el['A'] for el, nn in self.formula)

    def calc_density_rel_el(self, physical_dens):
        w_total = self.calc_mol_wt()

        water = [(_periodic_table['H'], 2), (_periodic_table['O'], 1)]
        water_w_tot = sum(nn * el['A'] for el, nn in water)
        water_ref = sum(((nn * el['A'])/water_w_tot) * (el['Z']/el['A']) for el, nn in water)

        return physical_dens * sum(((nn * el['A'])/w_total) * (el['Z']/el['A']) for el, nn in self.formula) / water_ref

    def calc_Im_bragg(self):
        w_total = self.calc_mol_wt()

        w_el = [nn * el['A'] / w_total for el, nn in self.formula] # relative abundance (by mass) of each element
        numerator = sum(((w_el[ii] * el['Z'] / el['A']) * np.log(el['I_m'])) for ii, el, nn in enumerate(self.formula))
        denominator = sum((w_el[ii] * el['Z'] / el['A']) for ii, el, nn in enumerate(self.formula))

        return np.exp(numerator / denominator)


class AnalyticMixture(object):

    def __init__(self, composition_dict):
        self.mass_composition = composition_dict
        return

    def calc_density_rel_el(self, physical_dens):
        w_total = sum(self.mass_composition[cmpd] * cmpd.calc_mol_wt() for cmpd in self.mass_composition)
        
        water = [(_periodic_table['H'], 2), (_periodic_table['O'], 1)]
        water_w_tot = sum(nn * el['A'] for el, nn in water)
        water_ref = sum(((nn * el['A'])/water_w_tot) * (el['Z']/el['A']) for el, nn in water)

        sum1 = 0
        for cmpd in self.mass_composition:
            for el, nn in cmpd.formula:
                sum1 += ((nn * el['A'])/w_total) * (el['Z']/el['A'])

        return physical_dens * sum1 / water_ref

    def calc_Im_bragg(self):
        pass


class EmpiricalSubstance(object):

    def __init__(self, composition_dict):
        self.elemental_composition = [(_periodic_table[el], composition_dict[el]) for el in composition_dict]
        return

    def calc_density_rel_el(self, physical_dens):
        water = [(_periodic_table['H'], 2), (_periodic_table['O'], 1)]
        water_w_tot = sum(nn * el['A'] for el, nn in water)
        water_ref = sum(((nn * el['A'])/water_w_tot) * (el['Z']/el['A']) for el, nn in water)

        return physical_dens * sum(w_el * el['Z'] / el['A'] for el, w_el in self.elemental_composition) / water_ref


