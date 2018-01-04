clear  
clc  
%导入数据
X = dlmread('fods.txt'); 
%数据行列计数 
[N,m] = size(X);  
%数据归一化处理  
mm = m-1;
for i=1:mm
X(1:N,i)=X(1:N,i)-mean(X(1:N,i));
X(1:N,i)=X(1:N,i)/std(X(1:N,i));
end
  
%数据最后一列为RTN报酬率
Y=X(1:N,m);

%将RTN划分为两类 大于一记为1，其他记为0. 
YY=zeros(N,1);
for i=1:N
    if Y(i)>=1
        YY(i)= 1;
    else
        YY(i)=0;
    end
end

X=[X(1:N,1:mm),ones(N,1)];   

%十次交叉验证 Xtr Ftr为训练集，Xts fts为测试集5000个
pets=zeros(10,1);
for i=1:10
    ii = randperm(N);
    Xts=X(ii((i-1)*5000+1:i*5000),:);
    Xtr=X(setdiff(ii,ii((i-1)*5000+1:i*5000),'stable'),:);  
    fts = Y(ii((i-1)*5000+1:i*5000));
    ftr = YY(setdiff(ii,ii((i-1)*5000+1:i*5000),'stable'));  
    %神经网络20层训练模型
    [net] = feedforwardnet(20);  
    [net] = train(net, Xtr', ftr');
    [output] = net(Xts');
    %预测的RTN小于0.5为赔钱 大于0.5为赚钱 
    %计算预测为赚钱的股票对 平均的实际报酬率
    
      a=0;
      for j=1:5000
          if output(j) < 0.5
            fts(j)=0;
            a=a+1;
          end 
      end
      %每次循环得到的结果放入1*10矩阵
      pets(i)=sum(fts)/(5000-a);
end

%十次交叉后实际报酬率的平均值
aa=mean(pets)

%aa=1.0053