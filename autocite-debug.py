import sys, re, argparse, string, codecs

# THIS IS JUST A COPY OF THE AUTOCITE FOR DEBUGGING, TO ALLOW SOME TESTS.  IGNORE.

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
	return bigstring

	


# searches for repeat author refs beg. w/ dashes, concatenates them w/ name from root ref

def dedash(reffchunk):
	dashedlist = []
	dashfound = goSearchDashes(refchunk)
	if dashfound == 0:
		return dashedlist
	else:
		choppedrefs = refsChopper(dashfound[0], refchunk)
		year = dashfound[1]
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
	founddash = re.compile(dashpattern, re.MULTILINE)
	firstmatch = founddash.search()
	if firstmatch == None: 
		return 0
	else: 
		year = firstmatch.group(2)
		realrefpattern = r'(^[A-Z1][A-Za-z1]*-?[A-Za-z1]*[,.])'
		foundreal = re.compile(realrefpattern, re.MULTILINE)
		firstreal = foundreal.search()
		splitIndex = firstreal.start()
		theresults = [splitIndex, year]
		return theresults

# returns list of two strings, one before index, one after. Adds newlines just to be safe.

def refChopper(chopindex, refchunk): 
	secondpart = refchunk[chopindex:len(refchunk)]
	secondpart = '\n' + secondpart
	firstpart = refchunk[0:chopindex]
	firstpart = firstpart + '\n'
	choppedlist = [firstpart, secondpart]
	return choppedlist



# this carries out the back search.  nreverse string then search for char 
# followed by newline, return the word that ends in char.  (reversing again)
# I suppose I could have just found the last match before index in a grouped list of 
# matches rather than doing it this way, but damn the torpedoes, onward.

def goFindName(refchunk):
	flipchunk = refchunk[::-1]
	# how did anyone ever write code without google and stackoverflow?
	backnamepattern = r'([A-Za-z1]*[A-Z1]$)'
	foundname = re.compile(backnamepattern, re.MULTILINE)
	rightname = foundname.search()
	result = rightname.group
	rightresult = result[::-1]
	return rightresult


def makeCorpoi(citefile, reffile):
    citebox = open(citefile, 'r')
    refbox = open(reffile, 'r')
    citecorpus = citebox.read()
    refcorpus = refbox.read()
    citebox.close()
    refbox.close()
    corpoi = [citecorpus, refcorpus]
    return corpoi


def cleanup(rawList):
    cleanlist = [] 
    for i, c in enumerate(rawList):
        tempvar = rawList[i]
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

# TEST VERSION OF MAKECITELIST TO SEE WHAT'S WRONG
def makeCiteList(citefile):
    citepattern = r'brown cow'
    rawCitelist = re.findall(citepattern, citefile)
    # rawCitelist = re.findall(r'brown cow', citefile)
    cleanCitelist = cleanup(rawCitelist)
    finalCiteList = list(set(cleanCitelist))
    print(finalCiteList)
    # return(finalCiteList)
    # print(rawCitelist)

faketext = "the brown cow goes moo, your mom, your mom is a brown cow"

faketext2 = "brown cow"

makeCiteList(faketext)

# makeCiteList(faketext2)

# def makeCiteList(citefile):
#     citepattern = r'[\s(][A-Z1][A-Za-z1]*-?[A-Za-z1]*[ ,]? \(?\d\d\d\d[a-z]?[\s.,)]'
#     foundcites = re.compile(citepattern)
#     rawCitelist = foundcites.findall()
#     cleanCitelist = cleanup(rawCitelist)
#     finalCiteList = list(set(cleanCitelist))
#     return(finalCiteList)


def makeRefList(reffile):
    namepattern = r'(^[A-Z1][A-Za-z1]*-?[A-Za-z1]*),.*( \(?\d\d\d\d[a-z]?[.)])'
    foundrefs = re.compile(namepattern, re.MULTILINE)
    refsTuplesList = foundrefs.findall()
    rawRefslist = []
    for i in refsTuplesList:
        tupestring = refsTuplesList[i]
        tupestring = ' '.join(tupestring)
        rawRefslist.append(tupestring)
    newRefsList = cleanup(rawRefslist)
    dashedList = dedash(reffile)
    newRefsList.extend(dashedList)
    # no need to de-dupe here: should be no duplicate values in refs list. 
    # (though it might be nice to throw a warning if there are. bugrit)


def getMissing(list1, list2):
    missingList = []
    for i in list1:
        matchFound == 0 
        tempcite = list1[i]
        for j in list2:
            if tempcite == list2[j]:
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
    refcorpus = dumbDash(refcorpus)
    refcorpus = conv2ASCII(refcorpus)
    citelist = makeCiteList(citecorpus)
    reflist = makeRefList(refcorpus)
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

# checkCites(manuFiles.citearg, manuFiles.refarg)

