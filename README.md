# stray-cites
personal tool to catch missing references cited in book manuscript or stray citations with no reference in text.
rough draft/ work in progress.  written for python 3.  mostly a learning project, plus research 
assistants tend to make errors when you ask them to check references in large manuscripts.  
usage: python autocite.py [citationfile.txt] [referencesfile.txt]

Pseudo-code/design: 

1.  take two files converted to ascii (from the same original format, by the same application, to ensure consistent ascii conversions).  
  a.  file 1: text containing references in author-date format (e.g. "Gowder 2015" or "(Gowder 2015)", 
  with single letters after years for multiple refs per author per year)
  b.  file 2: reference list in some consistent format.  for present purposes, all that matters is that 
  last name of author appears first, year appears somewhere else in a given reference, references are separated 
  by hard returns, and no hard returns appear w/in a reference 
2.  create corpus based on each file 
  a.  text corpus: each unique instance of [capitalized word] + [space] + ([4 digit numeric string] or 
  [4 digit numeric string plus one lowercase letter]), stored as word-year tuples in a list. 
  b.  reflist corpus: first word of each reference (as denoted by carriage returns) + any four-digit numeric 
  string or five-digit numeric + one lowercase letter string meeting any of the following conditions 
  (to distinguish years from page numbers): 
    i. spaces on both sides
    ii. left paren on left
    iii. right paren on right
    iv. space on left, period on right.
  stored as "word year" strings  in a list
3.  comparisons
  a.  iterate over text corpus, store any tuple not also found in reflist corpus in missing_ref_list
  b.  iterate over reflist corpus, store any tuple not also found in text corpus in uncited_list 
4.  print missing_ref_list and uncited_list 
5.  human goes to hunt down the missing citations.  (other automation was planned but is pointless.)

other people: use this if you want, but you'll have to change the regex for however your citations are formatted.

[update: added functionality to handle dashed lines leading repeated authors.  a bit heavy-handed and not general at all, but it should get the job done.  Still untested...]


note to self: everything now works except it can't handle multiple dash-starting refs.  that's a tomorrow project

strategy: just match all dash-starting refs in a block, count the matches, and then generate N 
instances of a concatenator that combines year for each match w/ the name.  

will require a little bit of change in structure.  line searcher will have to return a number 
and a list of years (or just a list of years?), dedash will have to pull out the years and 
repeatedly match them to the name (probably in an external function).  not so bad. 
Probably achievable by making another substring, this one between the index of the first 
dash dash found and the index of the first realname found, and then searching for dash-year 
pairs in there based on existing regex

ALSO: test references do not contain any multi-author cites.  this will probably break. 
to do: 1) just get rid of ", et al" and ", et. al." in preprocessing.  
2) implement some way to look backward in the cite matches (just take index -2?) to see 
if there is a '&' or 'and' or ',', if so, look backward still further and grab previous name.
do this recursively in a lookback function until it stops finding something formatted like a name.
--Note however that this strategy will break on the following format: "Real word [and,%] Ref", 
but that's such bad grammar that I like to think I haven't done it.  