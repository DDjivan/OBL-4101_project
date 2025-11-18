function y = TFCT_Interp(X,t,Nov)

% y = TFCT_Interp(X, t, hop)
% Interpolation du vecteur issu de la TFCT
%
% X : matrice issue de la TFCT
% t : vecteur des temps (valeurs réelles) sur lesquels on interpole
% Pour chaque valeur de t (et chaque colonne), on interpole le module du spectre
% et on détermine la différence de phase entre 2 colonnes successives de X
%
% y : la sortie est une matrice où chaque colonne correspond à l'interpolation de la colonne correspondante de X
% en préservant le saut de phase d'une colonne à l'autre
%
% programme largement inspiré d'un programme fait à l'université de Columbia


[nl,nc] = size(X);

% calcul de N = Nfft
N = 2*(nl-1);

% if nargin <3
%   % default value
%   Nov = N/2;
% end

% Initialisations
%-------------------
% Le spectre interpolé
y = zeros(nl, length(t));

% Phase initiale
ph = angle(X(:,1));

% Déphasage entre chaque échantillon de la TF
dphi = zeros(nl,1);
dphi(2:nl) = (2*pi*Nov)./(N./(1:(N/2)));

% Premier indice de la colonne interpolée à calculer
% (première colonne de Y). Cet indice sera incrémenté
% dans la boucle
ind_col = 1;

% On ajoute à X une colonne de zéros pour éviter le problème de
% X(col+1) en fin de boucle
X = [X,zeros(nl,1)];


% Boucle pour l'interpolation
%----------------------------
%Pour chaque valeur de t, on calcul la nouvelle colonne de Y à partir de 2
%colonnes successives de X

%% Votre programme commence ici

