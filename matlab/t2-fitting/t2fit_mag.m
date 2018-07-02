%	function [T2] = t2fit_mag( TE, S  http://www.sciencedirect.com/science/article/pii/0730725X93902253?via%3Dihub[,plt [,T2est [,Kest [,Nest ]]]])
%
%	Function finds fit for T2 using the input vectors
%	TE and S, which contain the TE used and the measured signal
%	magnitude for a series of scans.
%   Since signal magnitude is used, an offset for the noise is included.
%       Estimates T2* for Gradient Echo, T2 for Spin Echo scans
%
%			S = K  *  [ exp(-TE/T2) ] + N
%
%	If plt is set to 1, the fit and the data points will be plotted.
%
% SHOULD FIT TO POWER IMAGES BASED ON http://www.sciencedirect.com/science/article/pii/0730725X93902253
%
% PEZL 1/17/2008

function [T2, K, N] = t2fit_mag( TE, S, plt, T2est, Kest, Nest)

if (nargin < 3)
	plt = 1;		end;
if (nargin < 4)
	T2est = (TE(2)-TE(1))/ log(S(1)/S(2));		end;
if (nargin < 5)
	Kest = max(S)*1.2; 	end;
if (nargin < 6)
    [temp, Imax] = max(TE);
    Nest = S(Imax); 	end;

    function Sest = model_decay(x)
        Sest = x(2) .* exp( -TE(:) ./ x(1) ) + x(3);
    end

    function res = model_diff(x)
        res = model_decay(x) - S(:);
    end

X0 = [T2est, Kest, Nest];
lb = [0, 0, 0];
ub = [inf, inf, inf];

opts = optimset('MaxFunEvals', 1e4, 'Display', 'none');

X = lsqnonlin(@model_diff, X0, lb, ub, opts);

%X = fminsearch(eq,[T2est,Kest], [0,1e-8,1e-8,1e-10]);

T2 = X(1);
K = X(2);
N = X(3);


if (plt==1)
    figure(99)
	plot(TE,S,'k+', sort(TE), K * exp(-sort(TE) / T2) + N, 'b--');
    
    tt = sprintf('Fit of T2 from data:  T2=%8.2f ',T2);
	title(tt);
	xlabel('TE');
	ylabel('Signal');
	grid on;
                drawnow, pause(0.5)
end;

end


