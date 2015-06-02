import sys, re, argparse, string

# written for python 3

# save it all as ascii first, no need to worry about unicode so long as conversions to ascii are same in each file 
# this means this script need not be written for python 3 after all, but what the hell, it's done now.

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
		dashlist.append(sublist)
		# gonna need another function to take this list of lists and turn it into a list
		# of strings.  or can I just append the contents of the sublist rather than 
		# the list itself??  contents must be arbitrary length.
	

# search downward through string to find line starting with non-char.
# needs to return a two item-list, first item is index of line break before char 
# after dashblock, as an integer; second is year.  
# needs to just return integer 0 if nothing is found.
def goSearchDashes(refchunk): 

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
