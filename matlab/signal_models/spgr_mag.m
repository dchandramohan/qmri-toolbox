function [S] = spgr_mag(PD, T1, T2str, TR, TE, alph, k)

  if ~exist('k','var')
    k = 1.0; % scale factor (catch all, can be used for coil sensitivity, etc, etc.)
  end

  S = k * PD * exp(-TE/T2str) * ((sin(alph) * (1 - exp(-TR/T1)))/(1 - (cos(alph) * exp(-TR/T1))))
  return S

end

