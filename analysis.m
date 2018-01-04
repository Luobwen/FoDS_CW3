data_mon=dlmread('monthly return.txt');

[N, p1] = size(data_mon);
p = p1-1;
Y = [data_mon(:,1:p) ones(N,1)];
for j=1:p
Y(:,j)=Y(:,j)-mean(Y(:,j));
Y(:,j)=Y(:,j)/std(Y(:,j));
end
f = data_mon(:,p1);
%f = f - mean(f);
%f = f/std(f);

w = inv(Y'*Y)*Y'*f;
fh = Y*w;
figure(1), clf,
plot(f, fh, 'bx', 'LineWidth', 2),
grid on
xlabel('True return', 'FontSize', 14)
ylabel('Prediction', 'FontSize', 14)
title('Monthly return', 'FontSize', 16)


