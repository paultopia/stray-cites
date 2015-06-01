import sys, re, argparse, string

# written for python 3

# save it all as ascii first, no need to worry about unicode so long as conversions to ascii are same in each file 
# this means this script need not be written for python 3 after all, but what the hell, it's done now.

parser = argparse.ArgumentParser()
parser.add_argument("citearg", help="the file containing the citations from footnotes etc.")
parser.add_argument("refarg", help="the file containing reference list")
manuFiles = parser.parse_args()



def makeCorpoi(citefile, reffile)
    citebox = open(citefile, 'r')
    refbox = open(reffile, 'r')
    citecorpus = citebox.read()
    refcorpus = refbox.read()
    citebox.close()
    refbox.close()
    corpoi = [citecorpus, refcorpus]
    return corpoi


def cleanup(rawList)
    cleanlist = [] 
    for i in rawList:
        tempvar = rawList[i]
        tempvar = tempvar.replace(')', '')
        tempvar = tempvar.replace('(', '')
        tempvar = tempvar.replace(',', '')
        tempvar = tempvar.replace('.', '')
        tempvar = tempvar.lstrip()
        tempvar = tempvar.rstrip()
        ' '.join(tempvar.split())
        # a little redundant, but who cares?
        cleanlist.append(tempvar)
    return cleanlist


def makeCiteList(citefile)
    citepattern = r'\s[A-Z][A-Za-z]*-?[A-Za-z]* \(?\d\d\d\d[a-z]?[\s.,)]'
    foundcites = re.compile(citepattern)
    rawCitelist = foundcites.findall()
    cleanCitelist = cleanup(rawCitelist)
    finalCiteList = list(set(cleanCitelist))
    return(finalCiteList)


def makeRefList(reffile) 
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


def getMissing(list1, list2)
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
        

def checkCites(citefile, reffile)
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
