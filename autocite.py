import sys, re, argparse, string, codecs



# written for python 3

# note that this code cannot handle uncapitalized in last name space, mostly relevant 
# for bell hooks and for van, von, etc.  None of those appear in my refs so I don't care. 

parser = argparse.ArgumentParser()
parser.add_argument("citearg", help="the file containing the citations from footnotes etc.")
parser.add_argument("refarg", help="the file containing reference list")
manuFiles = parser.parse_args()




def captureAllYears(substring):
	dashYearGroups = r'^0DUMBDASHWASHERE.*( \(?\d\d\d\d[a-z]?[.)])'
	yearlist = re.findall(dashYearGroups, substring, re.MULTILINE)
	if len(yearlist) == 1:
		return(None)
	else:
		return(yearlist)




	
#######################################################
#
#
#           MORE NEW STUFF IN PROGRESS
#
# multiple authors 
# 





def clearcrap(bigstring):
	bigstring = bigstring.replace(' von ', ' ')
	bigstring = bigstring.replace(' v1FOREIGNn ', ' ')
	bigstring = bigstring.replace(' van ', ' ')
	bigstring = bigstring.replace(' de ', ' ')
	bigstring = bigstring.replace(' d1FOREIGN ', ' ')
	bigstring = bigstring.replace(' der ', ' ')
	bigstring = bigstring.replace(' den ', ' ')
	bigstring = bigstring.replace(' d1FOREIGNn ', ' ')
	bigstring = bigstring.replace(' da ', ' ')
	bigstring = bigstring.replace(' la ', ' ')
	bigstring = bigstring.replace(' l1FOREIGN ', ' ')
	bigstring = bigstring.replace(' du ', ' ')
	bigstring = bigstring.replace(' d\'', ' ')
	bigstring = bigstring.replace(' Von ', ' ')
	bigstring = bigstring.replace(' V1FOREIGNn ', ' ')
	bigstring = bigstring.replace(' Van ', ' ')
	bigstring = bigstring.replace(' De ', ' ')
	bigstring = bigstring.replace(' D1FOREIGN ', ' ')
	bigstring = bigstring.replace(' Der ', ' ')
	bigstring = bigstring.replace(' Den ', ' ')
	bigstring = bigstring.replace(' D1FOREIGNn ', ' ')
	bigstring = bigstring.replace(' Da ', ' ')
	bigstring = bigstring.replace(' La ', ' ')
	bigstring = bigstring.replace(' L1FOREIGN ', ' ')
	bigstring = bigstring.replace(' Du ', ' ')
	bigstring = bigstring.replace(' D\'', ' ')
	bigstring = bigstring.replace('Moreover, ', ' ')
	bigstring = bigstring.replace('However, ', ' ')
	bigstring = bigstring.replace('And, ', ' ')
	bigstring = bigstring.replace('But, ', ' ')
	bigstring = bigstring.replace('Thus, ', ' ')
	bigstring = bigstring.replace('Therefore, ', ' ')
	bigstring = bigstring.replace('Consequently, ', ' ')
	bigstring = bigstring.replace('Accordingly, ', ' ')
	bigstring = bigstring.replace('Finally, ', ' ')
	bigstring = bigstring.replace('Next, ', ' ')
	bigstring = bigstring.replace('First, ', ' ')
	bigstring = bigstring.replace('Second, ', ' ')
	bigstring = bigstring.replace('Third, ', ' ')
	bigstring = bigstring.replace('Fourth, ', ' ')
	bigstring = bigstring.replace('Fifth, ', ' ')
	bigstring = bigstring.replace('Indeed, ', ' ')
	return(bigstring)

def deAnd(bigstring):
	bigstring = bigstring.replace(', and ', ', ')
	bigstring = bigstring.replace(' and ', ', ')
	bigstring = bigstring.replace(' & ', ', ')
	bigstring = bigstring.replace(',,', ',')
	bigstring = bigstring.replace(',,', ',')
	return(bigstring)
	# unlike the previous, this one is only applied to citestring.  
	# getting rid of ands to simplify the regex for searching multiple authors below

# I've decided to handle the whole multiple-authors problem in the hackiest possible way. 
# I'm going to simply strip out all authors beyond the first.  

def multiAuthor(citestring):
	longcite = r'([\s(][A-Z1][A-Za-z1]*-?[A-Za-z1]*),[\s(][A-Z1][A-Za-z1]*-?[A-Za-z1]*[ ,]?( \(?\d\d\d\d[a-z]?[\s.,)])'
	# then replace with group1 plus group2 plus space. This will iteratively strip out all but second-to last name
	# until only first name is left.  
	for x in range(0, 10):
		newstring = re.sub(longcite, '\g<1> \g<2>', citestring)
	return(newstring)

		
#
#
#######################################################





# totally unnecessary to define as function but useful to keep head straight.
# this will only be useful for my text, if other people adapt it, should either 
# generalize or replace the dashes with whatever you use for the repeated-author ref

def dumbDash(bigstring):
	bigstring = bigstring.replace('———', '0DUMBDASHWASHERE')
	bigstring = bigstring.replace('—', '0DUMBDASHWASHERE')
	# just in case
	return bigstring


def conv2ASCII(bigstring): 
	def convHandler(error):
		return ('1FOREIGN', error.start + 1)
	codecs.register_error('foreign', convHandler)
	bigstring = bigstring.encode('ascii', 'foreign')
	newstring = bigstring.decode('ascii', 'foreign')
	return newstring

	


# searches for repeat author refs beg. w/ dashes, concatenates them w/ name from root ref

def dedash(refchunk):
	dashedlist = []
	dashfound = goSearchDashes(refchunk)
	if dashfound == None:
		return dashedlist
	else:
		choppedrefs = refChopper(dashfound[0], refchunk)
		name = goFindName(choppedrefs[0])
		if isinstance(dashfound[1], str):			
			year = dashfound[1]
			# print(choppedrefs[0])
			# print('dashname is:' + name)
			# print ('dashyeae is: ' + year)
			ref = str(name + ' ' + year)
			# print('ref is: ' + ref)
			refinlist = [ref]
			dashedlist.extend(refinlist)
			# print('preparing dashlist.  it currently is: ' + str(dashedlist) + '\n\n\n\n')
		else:
			for year in dashfound[1]:
				ref = str(name + ' ' + year)
				refinlist = [ref]
				# print('appending reference: ' + ref)
				dashedlist.extend(refinlist)
		sublist = dedash(choppedrefs[1])
		dashedlist.extend(sublist)
		return dashedlist
	# this should work because if captureAllYears finds anything it'll be passed into GSD as 
	# a list. Otherwise it'll be passed from GSD as a string.
	# also I really fucking hope python doesn't think a list of strings evaluates to a string.
	# that's exactly the sort of garbage python would do.  If it does, I may fly to silicon 
	# valley and slap guido around a little. It is insanely hard to keep track of data types 
	# in this stupid language. 


	

# search downward through string to find first reference line starting with dash.
# returns a two item-list, first item is index of char 
# returns integer 0 if nothing is found.

def goSearchDashes(refchunk): 
	dashpattern = r'(^0DUMBDASHWASHERE).*( \(?\d\d\d\d[a-z]?[.)])'
	# keeping the old dash code around just in case.
	#	dashpattern = r'(^[^A-Za-z.]*\.).*( \(?\d\d\d\d[a-z]?[.)])'
	firstmatch = re.search(dashpattern, refchunk, re.MULTILINE)
	if firstmatch == None: 
		return None
	else: 
		year = firstmatch.group(2)
		splitIndex = firstmatch.start()
		# print('splitting at' + str(splitIndex))
		tempstr = refchunk[splitIndex:len(refchunk)]
		# print('chunk to search for real: ' + tempstr + '\n\n\n')
		realrefpattern = r'(^[A-Z1][A-Za-z1]*-?[A-Za-z1]*[,.])'
		firstreal = re.search(realrefpattern, tempstr, re.MULTILINE)
		# print('real citation found: ' + firstreal.group(0))
		partialChopIndex = firstreal.start()
		chopIndex = partialChopIndex + splitIndex
		theresults = [chopIndex, year]
		moreyears = captureAllYears(refchunk[splitIndex:chopIndex])
		if moreyears != None:
			theresults = [chopIndex, moreyears]
		# print('setting chopindex at' + str(chopIndex) + '\n\n\n')
		# print(theresults)
		return theresults
		
# this new version halfway behaves correctly: it first does a temporary split on the 
# start of the first dash block, and then searches everything after that for the next 
# real item.  It then passes the index of that real item to the chopper function to 
# chop up and give back for recursion in dedash().  So that's good.
#
# BUT: 
#
# what do I do if the last entry is a dash?  It won't find a next real one, and I'll have 
# to return something that gracefully shuts it down without losing the last entry.  
# how about just have it return end of the string -1 for the chopindex in that case, 
# and then it will have something else to iterate over, won't find any more dash blocks, 
# and will end normally.
# 
# HOWEVER: 
#
# looking at my actual text, neither in the real set nor in the test set is my 
# last entry a dash block.  So I don't need to fix this.  Screw it.  Save it for later 
# if this needs to be generalized or adapted to something else.
# 
# ALSO: 
# it finally fucking works, and the recursive search finds what it ought to find.
#
# CORRECTION: ######################################################################
# 
# not quite yet it doesn't.  now it fails to catch multiple dashcites in a single 
# block, because the recursive search drops the whole block.  I can solve this behavior 
# without tinkering too much with the functioning bits
# 
# new code above is attempt to handle this.

def refChopper(chopindex, refchunk): 
	# print("cutting the text on the basis of chopindex: " + str(chopindex))
	secondpart = refchunk[chopindex:len(refchunk)]
	secondpart = '\n' + secondpart
	firstpart = refchunk[0:chopindex]
	firstpart = firstpart + '\n'
	# print(firstpart)
	# print("searching for name in: \n\n\n\n" + firstpart)
	# print("next recursion on: \n\n\n\n" + secondpart)
	choppedlist = [firstpart, secondpart]
	return choppedlist



# this carries out the back search.  nreverse string then search for char 
# followed by newline, return the word that ends in char.  (reversing again)
# I suppose I could have just found the last match before index in a grouped list of 
# matches rather than doing it this way, but damn the torpedoes, onward.

def goFindName(refchunk):
	# print(refchunk)
	flipchunk = refchunk[::-1]
	# print(flipchunk)
	backnamepattern = r'([A-Za-z1]*[A-Z1]$)'
	rightname = re.search(backnamepattern, flipchunk, re.MULTILINE)
	# print(rightname)
	pgresult = rightname.group()
	# print(pgresult)
	rightresult = pgresult[::-1]
	# print("backward search found: " + rightresult)
	return rightresult


def makeCorpoi(citefile, reffile):
    citebox = open(citefile, 'r')
    refbox = open(reffile, 'r')
    citecorpus = citebox.read()
    refcorpus = refbox.read()
    citebox.close()
    refbox.close()
    corpoi = [str(citecorpus), str(refcorpus)]
    return corpoi


def cleanup(rawList):
    # print('rawlist is: ' + str(rawList))
    cleanlist = [] 
    for nameitem in rawList:
        tempvar = nameitem
        tempvar = tempvar.replace(')', '')
        tempvar = tempvar.replace('(', '')
        tempvar = tempvar.replace(',', '')
        tempvar = tempvar.replace('.', '')
        tempvar = tempvar.lstrip()
        tempvar = tempvar.rstrip()
        tempvar = ' '.join(tempvar.split())
        # a little redundant, but who cares?
        cleanlist.append(tempvar)
        # print('cleanlist is now' + str(cleanlist))
    return cleanlist


def makeCiteList(citefile):
    # print(citefile)
    citepattern = r'[\s(][A-Z1][A-Za-z1]*-?[A-Za-z1]*[ ,]? \(?\d\d\d\d[a-z]?[\s.,)]'
    rawCitelist = re.findall(citepattern, citefile)
    cleanCitelist = cleanup(rawCitelist)
    finalCiteList = list(set(cleanCitelist))
    # print(finalCiteList)
    return(finalCiteList)


def makeRefList(reffile):
    # print(reffile)
    namepattern = r'(^[A-Z1][A-Za-z1]*-?[A-Za-z1]*),.*( \(?\d\d\d\d[a-z]?[.)])'
    # namepattern = r'Rawls'
    refsTuplesList = re.findall(namepattern, reffile, re.MULTILINE)
    # print(refsTuplesList)
    rawRefslist = []
    for nameitem in refsTuplesList:
        tupestring = nameitem
        tupestring = ' '.join(tupestring)
        rawRefslist.append(tupestring)
    # print('rawlist pre-dedash is: ' + str(rawRefslist) + '\n\n')
    dashedList = dedash(reffile)
    # print('dashlist is: ' + str(dashedList) + '\n\n')
    rawRefslist.extend(dashedList)
    newRefsList = cleanup(rawRefslist)
    return(newRefsList)
    # no need to de-dupe here: should be no duplicate values in refs list. 
    # (though it might be nice to throw a warning if there are. bugrit)


def getMissing(list1, list2):
    missingList = []
    for nameitem in list1:
        matchFound = 0 
        tempcite = nameitem
        for matcher in list2:
            if tempcite == matcher:
                matchFound = 1
                break
        if matchFound == 0:
            missingList.append(tempcite)
    return(missingList)
        

def checkCites(citefile, reffile):
    corpoi = makeCorpoi(citefile, reffile)
    citecorpus = corpoi[0]
    citecorpus = conv2ASCII(citecorpus)
    citecorpus = clearcrap(citecorpus)
    citecorpus = deAnd(citecorpus)
    refcorpus = corpoi[1]
    # print(refcorpus)
    # print(corpoi[1])
    refcorpus = dumbDash(refcorpus)
    # print(refcorpus)
    refcorpus = conv2ASCII(refcorpus)
    refcorpus = clearcrap(refcorpus)
    print(citecorpus)
    citecorpus = multiAuthor(citecorpus)
    print('\n\n\n\n MULTI AUTHORS STRIPPED \n\n\n\n')
    print(citecorpus)
    # print(refcorpus)
    citelist = makeCiteList(citecorpus)
    # print('citelist is: ' + str(citelist) + '\n\n\n')
    reflist = makeRefList(refcorpus)
    # print('reflist is: ' + str(reflist) + '\n\n\n')
    unrefedcites = getMissing(citelist, reflist)
    uncitedrefs = getMissing(reflist, citelist)
    screwups = [unrefedcites, uncitedrefs]
    print("CITATIONS WITH NO REFERENCES")
    print("\n")
    print(unrefedcites)
    print("\n")
    print("\n")
    print("\n")
    print("REFERENCES WITH NO CITATIONS")
    print(uncitedrefs)
    # if output is verbose consider sending to a file instead.  but it shouldn't be.

checkCites(manuFiles.citearg, manuFiles.refarg)

