function cp = gsw_cp(SA,t,p)

% gsw_cp                                             isobaric heat capacity
%==========================================================================
% 
% USAGE:  
%  cp = gsw_cp(SA,t,p)
%
% DESCRIPTION:
%  Calculates the isobaric heat capacity of seawater.
%
% INPUT:
%  SA   =   Absolute Salinity                                      [ g/kg ]
%  t    =   in-situ temperature (ITS-90)                          [ deg C ]
%  p    =   sea pressure                                           [ dbar ]
%          ( ie. absolute pressure - 10.1325 dbar )
%
%  SA & t need to have the same dimensions.
%  p may have dimensions 1x1 or Mx1 or 1xN or MxN, where SA & t are MxN.
%
% OUTPUT:
%  cp   =   heat capacity of seawater                          [ J/(kg*K) ]
%
% AUTHOR: 
%  David Jackett, Trevor McDougall and Paul Barker [ help_gsw@csiro.au ]
%
% VERSION NUMBER: 2.0 (23rd July, 2010)
%
% REFERENCES:
%  IOC, SCOR and IAPSO, 2010: The international thermodynamic equation of 
%   seawater - 2010: Calculation and use of thermodynamic properties.  
%   Intergovernmental Oceanographic Commission, Manuals and Guides No. 56,
%   UNESCO (English), 196 pp.  Available from http://www.TEOS-10.org
%
% The software is available from http://www.TEOS-10.org
%
%==========================================================================

%--------------------------------------------------------------------------
% Check variables and resize if necessary
%--------------------------------------------------------------------------

if ~(nargin == 3)
   error('gsw_cp:  Requires three inputs')
end %if

[ms,ns] = size(SA);
[mt,nt] = size(t);
[mp,np] = size(p);

if (mt ~= ms | nt ~= ns)
    error('gsw_cp: SA and t must have same dimensions')
end

if (mp == 1) & (np == 1)              % p scalar - fill to size of SA
    p = p*ones(size(SA));
elseif (ns == np) & (mp == 1)         % p is row vector,
    p = p(ones(1,ms), :);              % copy down each column.
elseif (ms == mp) & (np == 1)         % p is column vector,
    p = p(:,ones(1,ns));               % copy across each row.
elseif (ms == mp) & (ns == np)
    % ok
else
    error('gsw_cp: Inputs array dimensions arguments do not agree')
end %if

if ms == 1
    SA = SA';
    t = t';
    p = p';
    transposed = 1;
else
    transposed = 0;
end

%--------------------------------------------------------------------------
% Start of the calculation
%--------------------------------------------------------------------------

n0 = 0; 
n2 = 2;

cp = -(t+273.15).*gsw_gibbs(n0,n2,n0,SA,t,p);

if transposed
    cp = cp';
end

end