#ifndef __DCM_IONIZATION_CALC_H__
#define __DCM_IONIZATION_CALC_H__

#define MAX_NUM_ELEMENTS __UINT8_MAX__

typedef struct {
  char symbol[3];
  __uint8_t Z;             // Atomic number
  float A;           // Atomic weight
  float I;           // Mean ionization potential
} ELEMENT;

const ELEMENT _H_; // = {"H", 1, 1.0079, 19.2};
const ELEMENT _C_; //  = {"C", 6, 12.011, 81};
const ELEMENT _N_; // = {"N", 7, 14.0067, 82};
const ELEMENT _O_; // = {"O", 8, 15.9994, 106};
const ELEMENT _P_; // = {"P", 15, 30.9736, 195.5};
const ELEMENT _S_; // = {"S", 16, 32.06, 203.4};
const ELEMENT _Ca_; // = {"Ca", 20, 40.08, 215.8};
const ELEMENT _Se_; // = {"Se", 34, 78.96, 348};

float calc_Im_bragg(__uint8_t n_el, __uint8_t *q_el, ELEMENT *el_list);
float calc_el_dens(float mass_dens, __uint8_t n_el, __uint8_t *q_el, ELEMENT *el_list);

#endif
