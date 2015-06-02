import sys, re, argparse, string, codecs

# written for python 3

# save it all as ascii first, no need to worry about unicode so long as conversions to ascii are same in each file 
# this means this script need not be written for python 3 after all, but what the hell, it's done now.

# actually needs to be able to handle, but not match, unicode characters for greek text in notes. 
# I think that should be ok... except for foreign authors.  it will break on foreign authors?
# christ I may have to figure out unicode.
# this stackoverflow may have answer: 
# http://stackoverflow.com/questions/6005459/is-there-a-way-to-match-any-unicode-non-alphabetic-character

# ALTERNATIVELY I can just run some damned command-line tool to convert all to ascii first.
# also, bad news, it looks like I don't have consistent use of accents and such between text 
# and refs.  this will produce spurious non-matches.  Still, as long as they are rare, 
# can be fixed by hand.

# converting to ascii seems like clearly best choice.  so long as the things that look like 
# letters in unicode convert to letters in ascii that should work.

# there appears to be a gnu app that can handle this: 
# http://www.gnu.org/savannah-checkouts/gnu/libiconv/documentation/libiconv-1.13/iconv.1.html

# the problem with this solution is that if I just replace non-ascii chars with arbitrary 
# letters, then the stupid MS word dashes will also be replaced by letters, which will 
# break the dedash function. Probably the easiest solution to that little glitch is to 
# manually search and replace the dash strings.  

# actually, why not just search and replace the dash strings in the script??  After all, 
# python can handle unicode, it's only the regex character matching that's an issue. Then 
# the dedash regex can just match on whatever arbitrary string I put in place of the 
# dashes. And then I can convert everything else to ascii before doing the real regex 
# with str.encode.  Ok, that's the plan.  it's dirty but it will work.  Snapshotting a 
# version here with the regex that matches the stupid dashes first. 

parser = argparse.ArgumentParser()
parser.add_argument("citearg", help="the file containing the citations from footnotes etc.")
parser.add_argument("refarg", help="the file containing reference list")
manuFiles = parser.parse_args()

#####################################################################################
#
#
#				### ALL THIS STUFF IS IN PROGRESS CODE TO DEAL WITH DASHED-LINE 
				### REPEATED AUTHORS.  NOT YET COMPLETE
#
#

# totally unnecessary function but useful to keep head straight.
# going to put in the moment I've got a string for refslist.
def dumbDash(bigstring):
	bigstring = bigstring.replace('———', 'DUMBDASHWASHERE')
	bigstring = bigstring.replace('—', 'DUMBDASHWASHERE')
	# just in case
	return bigstring


def conv2ASCII(bigstring): 
	def convHandler(error)
		return ('FOREIGN', error.start + 1)
	codecs.register_error('foreign', convHandler)
	bigstring = bigstring.encode('ascii', 'foreign')

	


# call dedash from makereflist, then define another function down the line to concatenate 
# its results with the results from the ordinary makereflist.
def dedash(reffchunk):
	dashedlist = []
	dashfound = goSearchDashes(refchunk)
	if dashfound == 0:
		return dashedlist
	else:
		choppedrefs = refsChopper(dashfound[0], refchunk)
		year = dashfound[1]
		name = goFindName(choppedrefs[0])
		ref = name + year
		dashedlist.append(ref)
		sublist = dedash(choppedrefs[1])
		dashlist.extend(sublist)

	

# search downward through string to find first reference line starting with non-char.
# needs to return a two item-list, first item is index of line break before char 
# after dashblock, as an integer; second is year.  
# needs to just return integer 0 if nothing is found.
def goSearchDashes(refchunk): 
	dashpattern = r'(^[^A-Za-z.]*\.).*( \(?\d\d\d\d[a-z]?[.)])'
	founddash = re.compile(dashpattern, re.MULTILINE)
	firstmatch = founddash.search()
	if firstmatch == None: 
		return 0
	else: 
		year = firstmatch.group(2)

# needs to return a two-item list, first item being string before index, second item being
# string after index and this second string must start with a newline.  
def refsChopper(index, list):

# this carries out the back search.  needs to reverse string then search for newline 
# followed by char, return the word that char starts.  (remember to reverse that word 
# back again before returning)
def goFindName(refchunk):
	

#
#
#####################################################################################

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
    for i in rawList:
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


def makeCiteList(citefile):
    citepattern = r'[\s(][A-Z][A-Za-z]*-?[A-Za-z]*[ ,]? \(?\d\d\d\d[a-z]?[\s.,)]'
    foundcites = re.compile(citepattern)
    rawCitelist = foundcites.findall()
    cleanCitelist = cleanup(rawCitelist)
    finalCiteList = list(set(cleanCitelist))
    return(finalCiteList)


def makeRefList(reffile):
    namepattern = r'(^[A-Z][A-Za-z]*-?[A-Za-z]*),.*( \(?\d\d\d\d[a-z]?[.)])'
    foundrefs = re.compile(namepattern, re.MULTILINE)
    refsTuplesList = foundrefs.findall()
    rawRefslist = []
    for i in refsTuplesList:
        tupestring = refsTuplesList[i]
        tupestring = ' '.join(tupestring)
        rawRefslist.append(tupestring)
    finalRefsList = cleanup(rawRefslist)
    # no need to de-dupe here: should be no duplicate values in refs list. (though it might be nice to throw a warning if there are)


def getMissing(list1, list2):
    missingList = []
    for i in list1:
        matchFound = 0 
        tempcite = list1[i]
        for j in list2:
            if tempcite == list2[j]:
                matchFound = 1
        if matchFound = 0:
            missingList.append(tempcite)
    return(missingList)
        

def checkCites(citefile, reffile):
    corpoi = makeCorpoi(citefile, reffile)
    citecorpus = corpoi[0]
    refcorpus = corpoi[1]
    refcorpus = dumbDash(refcorpus)
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

checkCites(manuFiles.citearg, manuFiles.refarg)
