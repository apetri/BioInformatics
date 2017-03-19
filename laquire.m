numFiles = 10;
%range = 'L2:L601';
sheet = 1;

myData = cell(1,numFiles);
myF = cell(1,numFiles);
mydF = cell(1,numFiles);
t1= [.1:.1:60]
t=transpose(t1)

for fileNum = 1:numFiles
    fileName = 'data/a2.xlsx';
    myData{fileNum} = soma(fileName,sheet,'B'+fileNum,2,601);
end

for fileNum = 1:numFiles
    dump= myData{fileNum}
    dumpy=dump(100:200)
    F=mean(dumpy)
    myF{fileNum} = F;
end

for fileNum = 1:numFiles
    dump = myData{fileNum}
    dumpy = myF{fileNum}
    deltaF = dump-dumpy
    mydF{fileNum} = deltaF/F
end

%range = 'B102:B501';
%sheet = 1;
myBackground = cell(1,numFiles);

for fileNum = 1:numFiles
    fileName = 'data/a2.xlsx';
    myBackground{fileNum} = background(fileName,sheet,'B2:B601');
end

for fileNum = 1:numFiles
    dump = myData{fileNum}
    dumpy = myBackground{fileNum}
    myclean{fileNum} = dump-dumpy
    end

for fileNum = 1:numFiles
    dump= myclean{fileNum}
    dumpy=dump(100:200)
    F=mean(dumpy)
    myF{fileNum} = F
end
for fileNum = 1:numFiles
    dump = myclean{fileNum}
    dumpy = myF{fileNum}
    deltaF = dump-dumpy
    mydF{fileNum} = deltaF/dumpy
end

dfof = cell2mat(mydF);
average = mean(dfof,2);
plot(t,dfof);
