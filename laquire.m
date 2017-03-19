%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%Options%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

numRealizations = 10;
sheet = 1;

%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%Data%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%

myData = cell(1,numRealizations);
myF = cell(1,numRealizations);
mydF = cell(1,numRealizations);
myClean = cell(1,numRealizations);

for r = 1:numRealizations
    fileName = 'data/a2.xlsx';
    myData{r} = soma(fileName,sheet,'B'+r,2,601);
    myF{r} = mean(myData{r}(100:200));
    myDf{r} = myData{r}/myF{r} - 1.0
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%Background%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

myBackground = cell(1,numRealizations);

for r = 1:numRealizations
    fileName = 'data/a2.xlsx';
    myBackground{r} = soma(fileName,sheet,'B',2,601);
    myClean{r} = myData{r} - myBackground{r};
    myF{r} = mean(myClean{r}(100:200))
    mydF{r} = myClean{r}/myF{r} - 1.0
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%Plotting%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

dfof = cell2mat(mydF);
average = mean(dfof,2);
plot(t,dfof);
