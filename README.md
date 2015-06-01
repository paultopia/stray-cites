# stray-cites
personal tool to catch missing references cited in book manuscript or stray citations with no reference in text
work in progress.  to be written in python.  mostly a learning project, plus research 
assistants tend to make errors when you ask them to check references in large manuscripts.

Pseudo-code/design: 

1.  take two files (MS word format, or plain text, or whatever seems most convenient).  
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
  stored as word-year tuples in a list
3.  comparisons
  a.  iterate over text corpus, store any tuple not also found in reflist corpus in missing_ref_list
  b.  iterate over reflist corpus, store any tuple not also found in text corpus in uncited_list 
4.  print missing_ref_list and uncited_list 
5.  define a function([t or r], tuple=ALL, crazy=FALSE) such that first argument picks text or reference list, 
second argument picks a tuple, and 
  a.  if firstarg = t, searches text corpus and prints the entirety of each paragraph/footnote 
  (i.e. separated by carriage returns) containing tuple argument (from missing_ref_list, default is all tuples in that list)
  b.  if firstarg = r, and crazy=FALSE, returns the citation for tuple argument/all tuples in uncited_list
    i. if crazy=TRUE, just flat-out deletes the citation in the word document.  (possibly hard to implement, definitely
    stupid to do, probably will not even try, but it's an expression of frustration with the 10k+ words of references 
    in this book manuscript which have been broken by no fewer than 4 research assistants of various kinds that I'm even 
    considering this kind of drastic step)
6.  get a cup of spiked tea.  
  

questions: 
1.  how to handle non-ascii characters, e.g., in foreign names?  probably best to do this in python 3 for unicode support.
  a.  if based on MS word text, what encoding does word use?  does it depend on fonts?  need to learn how this stuff works 
2.  how to handle footnotes if based on MS word text?  does word represent footnotes as having carriage return at end 
or how else is it encoded?  want to return entire footnotes in the reporting step. 
3.  not robust to refs list with more than 26 cites in one author-year pair, but who publishes 26 things in one year, 
all of which are worth citing in a single book?  nobody, that's who.
4.  how to get the text out of word files into python anyway?  there must be a library for this. 
Or could just copy-paste all the footnotes into a plain text file like a rational person. with any luck that will 
generate carriage returns.  one can hope. 
