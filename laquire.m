%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%Options%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%First and last data rows
firstRow = 2
lastRow = 300

%Each input row must be in the format: <fileName> <sheet> <background column> <first data column> <last data column>
inputs = {
    
    'data/a2.xlsx' 1 'B' 'C' 'D' ;
    'data/a2.xlsx' 1 'B' 'E' 'G' ;

} 

%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%Data%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%

%Time: firstRow, lastRow set the extremes. Each row is 1/10 of second
t = (transpose([firstRow:lastRow])-1)/10;

%Counter start
r = 1;

%Cycle over files
for f = 1:size(inputs,1)

    [ fileName sheet bCol firstCol lastCol ] = inputs{f,:} ;
    
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
plot(t,dfof); hold on;
plot(t,average,'k--');
