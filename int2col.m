%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Convert integer to excel column identifier%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function col = int2col(n)

	if n<=26
		col = char('A'+n-1);
	else
		n1 = floor((n-1)/26);
		n2 = mod(n-1,26);
		col1 = char('A'+n1-1);
		col2 = char('A'+n2);
		col = strcat(col1,col2);
	end

end