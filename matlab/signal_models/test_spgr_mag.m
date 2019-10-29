clear all
close all

%% setup sequence parameters
TR = 5.0 % ms
TE = 0.024 % ms
alph = degtorad(1) % 1 degree tip angle

%% setup sample parameters
PD = [1.0, 0.8, 0.7, 0.6, 0.5, 0.0]; % arbitrary units (scaled)
T1 = [50, 500, 1000, 4000]; % ms
T2str = 2000; % ms (assuming water & identical between samples)

%% calculate theoretical spgr signal magnitude
Signal = zeros(length(T1),length(PD));

for ii=1:length(T1)
  for jj=1:length(PD)
    Signal(ii,jj) = spgr_mag(PD(jj), T1(ii), T2str, TR, TE, alph);
  end
end

%% plot results
figure;
hold on;

plot(PD, Signal/Signal(1,1)); % plot signal normalized to the first value (expected to be max)
title('SPGR signal vs PD');
xlabel('Proton Density (a.u.)');
ylabel('SPGR Signal (a.u.)');
legend(split(num2str(T1)), 'Location', 'best');
