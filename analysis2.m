data_year=dlmread('annual return.txt');

[N, p1] = size(data_year);
p = p1-1;
Y = [data_year(:,2:p1) ones(N,1)];
for j=1:p
Y(:,j)=Y(:,j)-mean(Y(:,j));
Y(:,j)=Y(:,j)/std(Y(:,j));
end
f = data_year(:,1);
%f = f - mean(f);
%f = f/std(f);

w = inv(Y'*Y)*Y'*f;
fh = Y*w;
figure(1), clf,
plot(f, fh, 'bx', 'LineWidth', 2),
grid on
xlabel('True return', 'FontSize', 14)
ylabel('Prediction', 'FontSize', 14)
title('Annual return', 'FontSize', 16)



gama = 0.5;
cvx_begin quiet
variable w2( p+1 );
minimize( norm(Y*w2-f) + gama*norm(w2,1) );
cvx_end
fh2 = Y*w2;
figure(2), clf,
plot(f, fh2, 'co', 'LineWidth', 2),
legend('Regression', 'Sparse Regression');


[iNzero] = find(abs(w2) > 1e-5);
disp('Relevant variables');
disp(iNzero);


% %regression again
% Y_update=[Y(:,2) Y(:,4) Y(:,9) ones(N,1)];
% w_update = inv(Y_update'*Y_update)*Y_update'*f;
% fh_update=Y_update*w_update;
% figure(3), clf,
% plot(f, fh_update, 'bx', 'LineWidth', 2),
% legend('Regression', 'Sparse Regression');




