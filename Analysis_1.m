data = dlmread('C:\Users\ydl1y17\Desktop\FoDS\pairs_Fin_x.csv'); 

[N, p1] = size(data);
data = data(data(:, p1) ~= 1, :) ;
[N, p1] = size(data);
p = p1 - 1 ;
X = data(:, 2:p) ;
X = X - mean(X) ;
X = X ./ (ones(N, 1) * std(X)) ;

y = 1 * (data(:, p1) > 1) + -1 * (data(:, p1) < 1) ;
yv = data(:, p1) ;

g = unique(data(:, 1)) ;

%   Neural Network - feedforward - 20 layer
nH_layers = 20 ;

% The top N values
top_N = 5 ;

currect_percentage = zeros(length(g)-1, 1) ;
prediction_return = zeros(length(g)-1, 2) ;

for i = 1:length(g)-1
    %   Test set
    Xtr = X(data(:, 1) == g(i), :);
    ytr = y(data(:, 1) == g(i), :);
    %   Training set
    Xts = X(data(:, 1) == g(i+1), :);
    yts = y(data(:, 1) == g(i+1), :);
    ytvs = yv(data(:, 1) == g(i+1), :);
    
    %   Neural Network - feedforward - 2 layer
    [net] = feedforwardnet(nH_layers);
    [net, tr] = train(net, Xtr', ytr');
    [output] = net(Xts');
    
    prediction = (output >= 0) * 1 + (output < 0) * -1 ;
    
    currect_percentage(i, 1) = sum(prediction' == yts) / length(prediction) ;
    prediction_return(i, 1) = sum((output >= 0) * ytvs) / sum(output >= 0) ;
    rtn = 0 ;
    for j = 1: top_N
        [val, ind1] = max(output);
        rtn = rtn + val ;
        output(ind1) = -Inf;
    end
    prediction_return(i, 2) = rtn /top_N ;
    
end