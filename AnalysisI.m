clear  
clc  
%��������
X = dlmread('fods.txt'); 
%�������м��� 
[N,m] = size(X);  
%���ݹ�һ������  
mm = m-1;
for i=1:mm
X(1:N,i)=X(1:N,i)-mean(X(1:N,i));
X(1:N,i)=X(1:N,i)/std(X(1:N,i));
end
  
%�������һ��ΪRTN������
Y=X(1:N,m);

%��RTN����Ϊ���� ����һ��Ϊ1��������Ϊ0. 
YY=zeros(N,1);
for i=1:N
    if Y(i)>=1
        YY(i)= 1;
    else
        YY(i)=0;
    end
end

X=[X(1:N,1:mm),ones(N,1)];   

%ʮ�ν�����֤ Xtr FtrΪѵ������Xts ftsΪ���Լ�5000��
pets=zeros(10,1);
for i=1:10
    ii = randperm(N);
    Xts=X(ii((i-1)*5000+1:i*5000),:);
    Xtr=X(setdiff(ii,ii((i-1)*5000+1:i*5000),'stable'),:);  
    fts = Y(ii((i-1)*5000+1:i*5000));
    ftr = YY(setdiff(ii,ii((i-1)*5000+1:i*5000),'stable'));  
    %������20��ѵ��ģ��
    [net] = feedforwardnet(20);  
    [net] = train(net, Xtr', ftr');
    [output] = net(Xts');
    %Ԥ���RTNС��0.5Ϊ��Ǯ ����0.5Ϊ׬Ǯ 
    %����Ԥ��Ϊ׬Ǯ�Ĺ�Ʊ�� ƽ����ʵ�ʱ�����
    
      a=0;
      for j=1:5000
          if output(j) < 0.5
            fts(j)=0;
            a=a+1;
          end 
      end
      %ÿ��ѭ���õ��Ľ������1*10����
      pets(i)=sum(fts)/(5000-a);
end

%ʮ�ν����ʵ�ʱ����ʵ�ƽ��ֵ
aa=mean(pets)

%aa=1.0053