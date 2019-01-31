#include <stdio.h>
#include "ionization_calc.h"

int main() {
  printf("[[[*** Testing my electron density calculator! ... ***]]]\n\n");

  // define materials: Acetone
  __uint8_t n_el_Ace = 3;
  ELEMENT el_list_Ace[MAX_NUM_ELEMENTS] = { _H_, _O_, _C_ };
  __uint8_t q_el_Ace[MAX_NUM_ELEMENTS] = { 6, 1, 3 };
  
  float mass_dens_Ace[2];
  mass_dens_Ace[0] = 0.784623;
  mass_dens_Ace[1] = 0.787411;

  __uint8_t ii;
  float tmp;
  for (ii = 0; ii < 2; ii++) {
    printf("\n=> Acetone container #%d <=\n", ii);
    tmp = calc_el_dens(mass_dens_Ace[ii], n_el_Ace, q_el_Ace, el_list_Ace);
    printf("  => Electron Density = %f\n", tmp);
  }

    // define materials: Hydroxyapatite
  __uint8_t n_el_HA = 4;
  ELEMENT el_list_HA[MAX_NUM_ELEMENTS] = { _H_, _O_, _P_, _Ca_ };
  __uint8_t q_el_HA[MAX_NUM_ELEMENTS] = { 1, 13, 3, 5 };

  printf("\n=> Bone container <=\n");
  tmp = calc_el_dens(0.784824, n_el_HA, q_el_HA, el_list_HA);
  printf("  => Electron Density = %f\n", tmp);
  
  printf("\nDONE!\n");
  return 0;
}
  
  
