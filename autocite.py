import sys, re, argparse, string, codecs

# written for python 3

# note that this code cannot handle uncapitalized in last name space, mostly relevant 
# for bell hooks and for van, von, etc.  None of those appear in my refs so I don't care. 

parser = argparse.ArgumentParser()
parser.add_argument("citearg", help="the file containing the citations from footnotes etc.")
parser.add_argument("refarg", help="the file containing reference list")
manuFiles = parser.parse_args()


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
		year = dashfound[1]
		# print(choppedrefs[0])
		name = goFindName(choppedrefs[0])
		ref = name + ' ' + year
		dashedlist.extend(ref)
		sublist = dedash(choppedrefs[1])
		dashedlist.extend(sublist)
		return dashedlist

	

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
		tempstr = refchunk[0:splitIndex]
		realrefpattern = r'(^[A-Z1][A-Za-z1]*-?[A-Za-z1]*[,.])'
		firstreal = re.search(realrefpattern, tempstr, re.MULTILINE)
		# print(firstreal)
		chopIndex = firstreal.start()
		theresults = [chopIndex, year]
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

def refChopper(chopindex, refchunk): 
	# print(chopindex)
	secondpart = refchunk[chopindex:len(refchunk)]
	secondpart = '\n' + secondpart
	firstpart = refchunk[0:chopindex]
	firstpart = firstpart + '\n'
	# print(firstpart)
	# print(secondpart)
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
	print(pgresult)
	rightresult = pgresult[::-1]
	print(rightresult)
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
    newRefsList = cleanup(rawRefslist)
    dashedList = dedash(reffile)
    newRefsList.extend(dashedList)
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
        if matchFound == 1:
            missingList.append(tempcite)
    return(missingList)
        

def checkCites(citefile, reffile):
    corpoi = makeCorpoi(citefile, reffile)
    citecorpus = corpoi[0]
    citecorpus = conv2ASCII(citecorpus)
    refcorpus = corpoi[1]
    # print(refcorpus)
    # print(corpoi[1])
    refcorpus = dumbDash(refcorpus)
    # print(refcorpus)
    refcorpus = conv2ASCII(refcorpus)
    # print(citecorpus)
    # print(refcorpus)
    citelist = makeCiteList(citecorpus)
    # print(citelist)
    # print(refcorpus)
    reflist = makeRefList(refcorpus)
    # print(reflist)
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
