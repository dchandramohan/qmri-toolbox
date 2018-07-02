#include <stdio.h>
#include "ionization_calc.h"

int main() {
  printf("[[[*** Testing my mean ionization potential calculator! ... ***]]]\n\n");

  // define materials: Hydroxyapatite
  __uint8_t n_el_HA = 4;
  ELEMENT el_list_HA[MAX_NUM_ELEMENTS] = { _H_, _O_, _P_, _Ca_ };
  __uint8_t q_el_HA[MAX_NUM_ELEMENTS] = { 1, 13, 3, 5 };

  // define materials: Gypsum
  __uint8_t n_el_Gpsm = 4;
  ELEMENT el_list_Gpsm[MAX_NUM_ELEMENTS] = { _H_, _O_, _S_, _Ca_ };
  __uint8_t q_el_Gpsm[MAX_NUM_ELEMENTS] = { 4, 6, 1, 1 };
  
  float Im_HA, Im_Gpsm;
  printf("*@*@*@* Hydroxyapatite (Ca5(PO4)3(OH)) *@*@*@*\n");
  Im_HA = calc_Im_bragg(n_el_HA, q_el_HA, el_list_HA);

  printf("\n*@*@*@* Gypsum (CaSO4 * 2 H2O) *@*@*@*\n");
  Im_Gpsm = calc_Im_bragg(n_el_Gpsm, q_el_Gpsm, el_list_Gpsm);

  printf("Gypsum differs from Hydroxyapatite by %f%% ...\n", 100.0 * (Im_Gpsm - Im_HA) / Im_HA);
  printf("DONE!\n");
  return 0;
}
  
  
