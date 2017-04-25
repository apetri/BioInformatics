%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Convert excel column identifier to integer%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function n = col2int(col)
	
	n = 0;
	
	for c = 1:length(col)
		n = n + (int8(col(c))-int8('A')+1)*(26^(length(col)-c));
	end

end