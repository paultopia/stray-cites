import re, sys
citestring = 'Herod., 3.80.5-6. Nardulli, Peyton, Bajjalieh 2013, 139-192. Starr, 1936, 1143-1152.'
def multiAuthor(citestring):
	longcite = r'([\s(][A-Z1][A-Za-z1]*-?[A-Za-z1]*),[\s(][A-Z1][A-Za-z1]*-?[A-Za-z1]*[ ,]?( \(?\d\d\d\d[a-z]?[\s.,)])'
	for x in range(0, 10):
		newstring = re.sub(longcite, '\g<1> \g<2>', citestring)
	return(newstring)
newstring = multiAuthor(citestring)
print('OLD STRING: \n' + citestring + '\n NEW STRING: \n' + newstring)
