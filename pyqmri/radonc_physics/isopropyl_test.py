import atom_calc

ipa = atom_calc.Compound({'C' : 3, 'H' : 8, 'O' : 1})
water = atom_calc.Compound({'H' : 2, 'O' : 1})

vol_frac_ipa = 0.91
vol_frac_water = 1 - vol_frac_ipa

dens_ref_ipa_pure = 0.786
dens_ref_water_pure = 1.0

dens_meas_ipa_mix = 0.812266

mass_frac_ipa = vol_frac_ipa * dens_ref_ipa_pure / dens_meas_ipa_mix
mass_frac_water = vol_frac_water * dens_ref_water_pure / dens_meas_ipa_mix

ipa_mix = atom_calc.AnalyticMixture({ipa : mass_frac_ipa, water : mass_frac_water})
print('Calculated relative electron density of 91% vol. Isopropyl Alcohol = {:f}'.format(ipa_mix.calc_density_rel_el(dens_meas_ipa_mix)))

