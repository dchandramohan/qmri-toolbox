%	function [T2] = t2fit( TE, S  [,plt [,T2est [,Kest ]]])
%
%	Function finds fit for T2using the input vectors
%	TE and S, which contain the TE used and the measured signal
%	for a series of scans, with a flip angle of 90.
%       Estimates T2* for Gradient Echo, T2 for Spin Echo scans
%
%	In theory,
%			S = Mo * [ exp(-TE/T2) ]  *  [ 1 - exp(-TR/T1) ]
%
%	By keeping TR constant, this reduces to
%
%			S = K  *  [ exp(-TE/T2) ]
%
%
%	NOTE:  It is tempting to try to do a quick measurement of T2 using
%		a multi-echo Spin-Echo sequence.  It is generally accepted
%		that using this method will (in some cases grossly)
%		underestimate T2.  Thus using a single spin echo is
%		preferable.
%
%	The fit is a minimization of  SUMi { (Si - K*(exp(-TEi/T2)))^2 }.
%
%	If plt is set to 1, the fit and the data points will be plotted.
%
% From Brian Hargreaves 4/2005
% Fixed for matlab 7 -  PL 12/2005

function [T2, df, phi, Sfit] = t2fit_complex( TE, S, plot_flag, T2est, Kest, dfest, phiest)

if (nargin < 3)
    plot_flag = 1;		end;
if (nargin < 4) || isempty(T2est)
    T2est =  abs((TE(2)-TE(1))/ log(abs(S(1))/abs(S(2)))) ;		end;
if (nargin < 5) || isempty(Kest)
    Kest = max(abs(S))*1.2; 	end;
if (nargin < 6) || isempty(dfest)
    % assume on-resonance
    dfest = 0; % dfest = angle(S(1)*S(2)')/(TE(2)-TE(1));
end
if (nargin < 7)|| isempty(phiest)
    phiest = angle(S(1));
end

%options = optimoptions(@fminunc,'Display','none','Algorithm','quasi-newton');

lsq_opts = optimset('Display','none','MaxIter', 500, 'MaxFunEvals', 500);

params_est_vec = [Kest, T2est, dfest, phiest];
params_lb = []; params_ub = [];

    function res = model_diff(x)
        Sest = T2_model(x, TE);
        res = [real(Sest(:) - S(:)); imag(Sest(:) - S(:))];
    end

[params_fit_vec,objective_val] = lsqnonlin(@model_diff, params_est_vec, params_lb, params_ub, lsq_opts);

T2 = params_fit_vec(2);
df = params_fit_vec(3); phi = params_fit_vec(4);
[Sfit] = T2_model(params_fit_vec, TE);

if plot_flag
    % plot of fit for debugging
    figure(99)
    plot(TE, real(S), 'b',TE, imag(S),'g', TE, real(Sfit),'b--', TE, imag(Sfit),'g--')
    xlabel('TE')
    title(['T_2 = ' num2str(T2) ' df = ' num2str(df)])
    drawnow, pause(0.5)
end

end

function Smodel = T2_model(x, TE)
Smodel = x(1) * exp( -TE(:)/x(2)-i*2*pi*x(3)*TE(:) + i*x(4));

end




