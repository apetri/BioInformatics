%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%Options%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%Each input row must be in the format: <fileName> <sheet> <background column> <first data column> <last data column> <first row> <last row>

inputs = {
    
    'data/a2.xlsx' 1 'B' 'C' 'D' 2 601 ;
    'data/a2.xlsx' 1 'B' 'E' 'G' 2 601 ;

} 

%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%Data%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%

%Time: watch out that with this choice length(t)=600. lastRow - firtRow in the data must match this 
t = transpose([.1:.1:60]);

%Counter start
r = 1;

%Cycle over files
for f = 1:size(inputs,1)

    [ fileName sheet bCol firstCol lastCol firstRow lastRow ] = inputs{f,:} ;
    
    %Load background
    myBackground = excelRead(fileName,sheet,bCol,firstRow,lastRow) ;

    %Load data, subtract background
    for col = firstCol:lastCol
        myData{r} = excelRead(fileName,sheet,col,firstRow,lastRow) ;
        myClean{r} = myData{r} - myBackground ;
        myF{r} = mean(myClean{r}(100:200)) ;
        mydF{r} = myClean{r}/myF{r} - 1.0 ;
        r = r+1 ;
    end 

end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%Plotting%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

dfof = cell2mat(mydF);
average = mean(dfof,2);
plot(t,dfof); hold;
plot(t,average,'k--');
