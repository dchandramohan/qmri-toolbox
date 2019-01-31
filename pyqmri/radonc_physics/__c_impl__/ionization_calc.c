
#include <stdio.h>
#include <math.h>

#include "ionization_calc.h"

const ELEMENT _H_ = {"H", 1, 1.0079, 19.2};
const ELEMENT _C_ = {"C", 6, 12.011, 81};
const ELEMENT _N_ = {"N", 7, 14.0067, 82};
const ELEMENT _O_ = {"O", 8, 15.9994, 106};
const ELEMENT _P_ = {"P", 15, 30.9736, 195.5};
const ELEMENT _S_ = {"S", 16, 32.06, 203.4};
const ELEMENT _Ca_ = {"Ca", 20, 40.08, 215.8};
const ELEMENT _Se_ = {"Se", 34, 78.96, 348};

float calc_Im_bragg(__uint8_t n_el,            // number of elemental constituents
		    __uint8_t *q_el,           // array of quantities of each element
		    ELEMENT *el_list)        // array of elements
{
  __uint8_t ii;
  float w_el[MAX_NUM_ELEMENTS];

  // total molecular weight
  printf("Computing total molecular weight... ");
  float total_mol_wt;
  total_mol_wt = 0;
  
  for (ii = 0; ii < n_el; ii++)
    total_mol_wt += (float)q_el[ii] * el_list[ii].A;
  printf("%f grams/mol\n", total_mol_wt);
  
  // relative abundances
  printf("\nComputing relative abundances...\n");
  for (ii = 0; ii < n_el; ii++) {
    w_el[ii] = ((float)q_el[ii] * el_list[ii].A) / total_mol_wt;
    printf("\t[%s] = %f%%\n", el_list[ii].symbol, w_el[ii] * 100.0);
  }

  // Bragg Additivity Rule
  printf("\nComputing mean ionization potential, I_m (eV), by Bragg Additivity Rule ...\n");
  float sum1, sum2, term1, Im;
  sum1 = 0;
  sum2 = 0;
  
  for (ii = 0; ii < n_el; ii++) {
    term1 = (w_el[ii] * el_list[ii].Z) / el_list[ii].A;
    sum1 += term1 * log(el_list[ii].I);
    sum2 += term1;
  }
  
  Im = exp(sum1 / sum2);
  printf("\tI_m (BAR) = %f\n\n", Im);

  return Im;
}

float calc_el_dens(float mass_dens,           // mass density
		   __uint8_t n_el,            // number of elemental constituents
		   __uint8_t *q_el,           // array of quantities of each element
		   ELEMENT *el_list)          // array of elements
{
  __uint8_t ii;
  float w_el[MAX_NUM_ELEMENTS];
  
  // total molecular weight
  printf("Computing total molecular weight... ");
  float total_mol_wt;
  total_mol_wt = 0;
  
  for (ii = 0; ii < n_el; ii++)
    total_mol_wt += (float)q_el[ii] * el_list[ii].A;
  printf("%f grams/mol\n", total_mol_wt);
  
  // relative abundances
  printf("\nComputing relative abundances...\n");
  for (ii = 0; ii < n_el; ii++) {
    w_el[ii] = ((float)q_el[ii] * el_list[ii].A) / total_mol_wt;
    printf("\t[%s] = %f%%\n", el_list[ii].symbol, w_el[ii] * 100.0);
  }

  float sum1;
  sum1 = 0.0;
  for (ii = 0; ii < n_el; ii++) {
    sum1 += w_el[ii] * ((float)el_list[ii].Z / el_list[ii].A);
  }

  float w_H, w_O, sum2;
  w_H = (2.0 * _H_.A)/((2.0 * _H_.A) + (1.0 * _O_.A));
  w_O = (1.0 * _O_.A)/((2.0 * _H_.A) + (1.0 * _O_.A));
  sum2 = ((w_H * (float)_H_.Z / _H_.A) + (w_O * (float)_O_.Z / _O_.A));
  
  return mass_dens * sum1 / sum2;
}

  
