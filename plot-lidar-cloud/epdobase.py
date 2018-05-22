# ==============================================================================
#
# 20100526-1500-gpuboo - epdobase.py
# Epdobase : Epdomonus Database Module / Wesley Andres Watters Farfan
# Definition of the Epdomonus Database class (Epdobase) and associated methods
#
# <type>
# 
# Module </type>
#
# <package>
# 
# Database PyEpdox </package>
#
# <language>
# 
# Python 2.x </language>
#
# <os>
# 
# GNU/Linux </os>
#
# <dependencies>
# 
# See dependencies for individual methods. (Grep this file for the word
# "import".) </dependencies>
#
# <updates>
# 
# 2010.08.21; 2010.08.22; 2010.08.29; 2010.09.04; 2010.09.26; 2010.10.03; 
# 2010.10.25; 2010.10.26; 2010.10.27; 2010.10.28; 2011.04.27; 2011.05.30;
# 2012.01.06; 2013.07.10; 2014.01.02; 2014.01.09; 2015.08.09; 2015.11.28; 
# </updates>
#
# <notes> 
#
# Most of the utilities in this model relate in some way to supporting
# operations that involve Epdobase objects.  Epdobase is a class of objects that
# hold database information (defined in {20100527-1045}, below).  A database is
# made up of a set of fields (columns) that have individual names, as well as
# records (rows) that contain values for each or some of the fields.  An
# Epdobase object can also have meta-data: a set of fields and their values
# which refer to the database as a whole (or which contain information about the
# database as a whole). Each record of the database, in addition to having
# field-assigned values, may also contain "unassigned matter".  In that case,
# the field values may function as meta-data for the unassigned matter.  (Note
# that the unassigned matter may itself contain a database.)
#
# What follows is a list of input and output formats that can be written-to from
# an Epdobase object or read-from into an Epdobase object:
#
# * Epdex   (*.dex) = Epdex-formatted text file ("Epdomonus index")
# * Epdata  (*.dat) = Epdata-formatted text file ("Epdomonous database") 
# * Epdadex (*.ddx) = Epdata-formatted text w/Epdex-formatted unassigned matter
# * Epdobin (*.dob) = Text header w/field definitions + numeric matrix as binary
# * CSV     (*.csv) = Comma-separated values 
# * Latex   (*.tex) = Latex table (write support only)
# 
# Epdata and Epdex formatting are defined in {20100123-1918}.  Epdobin is used
# for storing large, multi-dimensional arrays of numbers. 
#
# Please note that this module was called "PyEpdict" until 2010.10.26, when the
# name was changed to "Epdobase".  Before this date, the primary class was
# called "Epdict" for "Epdomonus Dictionary". </notes>
#
# <tasklist>
#
# ~ Add method for checking that an epdobase is well-formed
# o Add method for pickling epdobases
# x Add method for sorting an epdobase by one field
# x Add method for "numerizing" fields (in numeric version called ndct)
# x Add method for converting ndct to dcty
# x Add method for adding new fields of correct length, filled with nulls
# x Add method that returns records w/specified values in multiple fields
# x Add method that returns the number of records
# - Add method for writing to an HTML table
# x Add method for writing to a LaTex table
# x Add method for writing to a csv table (spreadsheet)
# x Add method for reading from a csv table (spreadsheet)
# - Add method for writing to an xml-formatted table [101111]
# - Add method for reading from an xml-formatted table [101111]
# - Add method for writing to a MySQL table or database
# - Add method for reading from a MySQL table or database
# - Add method that returns the numeric dictionary as a Numpy array
# x Add method that finds all empty strings, replaces them with "null".
# - Add method that reads Epdadex, using same code as get_epdices() on umat.
# - Add method for writing Epdadex from list of epdobases ("epdices").
# x Add meta-data variable and assignment in Epdadex. 
# - Add method for reading & removing meta-data (insert into major I/O methods) 
# - Add class-level method that reads epdobase object from string ("fromstring")
# - Add method that extracts Epdex and Epdata embedded in an Epdoml document. 
# x Update get_matching_records to include partial matches (searches)
# x Update the epdata reader so that it reads unassigned matter
# x Update all methods to handle unassigned matter separately as "umat".
# - Update epdata parser and writer to handle angular reference tags 
# x Pound-sign at ends of lines in Epdex should be optional (maybe already is)
# x Pound-sign at ends of lines should not be written.
# - Implement means of escaping pound-signs in Epdex. 
# x Add binary format called "Epdobin" for direct ep.ndct I/O. 
# x Store ndct columns as arrays instead of lists.
# x Vectorize epdobase.numerize() to avoid looping over records.
# x Vectorize epdobase.characterize() to avoid looping over records.
# x Fix Epdata parser so it works even if square-ref tags are indented.
# - Add handling of tags for embedding Epdata in Epdoml. [110122]
# - Add handling of multiple embedded Epdata documents. [110122]
# x Add forced-read as one format or the other (e.g., fmat='dat' or fmat='auto')
# x Add handling of pgh blocks (double ampersands). [110122]
# - Use numpy.genfromtxt() to add function for ingesting any table. [120111]
# - Add means of specifying precision of output. [140102]
# </tasklist>
#
# ==============================================================================

import pdb          # >> Python debugger
import numpy as np  # >> Numerical python
 
# ==============================================================================
#
# 20100527-1045-mpuboo - Epdobase Class
#
# <summary>
#
# Epdomonus dictionary super class: database class for Epdex and Epdata files
# </summary>
#
# <syntax>
# 
# epdobase_name = cl_epdobase() </syntax>
#
# <methods>
# 
# * add_fields(fields, fields_defs)     = add fields and field definitions
# * as_string(epdoc_type)               = write epdobase to string as epdoc_type
# * characterize()                      = copy ndct to dcty records as strings
# * get_epdices()                       = parse individual records as epdex/data
# * init_fields(fields)                 = initialize all fields in "fields"
# * len()                               = count the number of records
# * load(filepath, format='auto')       = load file "filepath" w/format "format"
# * make_empty_records(N)               = add/append N empty records [130710]
# * matching_records(valdict)           = find indices of all matching records
# * nullify()                           = replace all empty strings with "null"
# * numerize()                          = create ndct = dcty, but w/number types
# * pickle()                            = pickle the epdobase
# * unnullify()                         = replace all "nulls" with empty strings
# * save(format, filepath)              = save epdobase as epdex/epdata/epdobin
# * save_part(format, fields, filename) = save a part of the epdobase 
# * search_records(valdict)             = search records (partial matching)
# * shrink(inds)                        = keep subset of all records 
# * sort_records(field, whether_reverse)= sort records by field "field"
# </methods>
# 
# <variables>
#
# * dcty = dictionary whose keys are field names; each has list of equal length
# * defs = definitions of each field name (describing contents of its records)
# * flds = the field names: the list of keys to dcty
# * meta = dictionary containing meta-data with arbitrary keys and values
# * ndct = a numerized version of dcty: non-alpha records converted to int/float
# * umat = unassigned matter; must at least be an empty list. 
# * pres = precision: dict formated like defs, but w/# desired digits after zero
# </variables>
# 
# <products>
# 
# See comments for individual methods of the class. </products>
#
# <type>
# 
# Class </type>
#
# <dependencies>
# 
# copy </dependencies>
#
# <updates> 
# 
# - Epdices added (for ingesting Epdadex) [101003]
# - Meta-data variable (.meta) added [101025] 
# - Added explicit file-format specification in load(). [110530] 
# - Added CSV load support. [110530] 
# - Added the shrink method. [151128] </updates> 
#
# ==============================================================================

class cl_epdobase : 

    #---------------------------------------------------------------------------
    # -- Initializing variables ------------------------------------------------
    #---------------------------------------------------------------------------

    def __init__(self): 

        self.dcty = {}    # >> Dictionary
        self.defs = {}    # >> Field definitions 
        self.flds = []    # >> Field names
        self.ndct = {}    # >> Numeric dictionary (numerized version of dcty)
        self.umat = []    # >> Unassigned matter (content not assoc. w/fields)
        self.meta = {}    # >> Meta data for entire dictionary (1-level deep)
        self.pres = {}    # >> Precision: num digits after zero (for printing)

    #---------------------------------------------------------------------------
    # -- Loading Epdobase from Epdex, Epdata/Epdadex, or Epdobin ---------------
    #---------------------------------------------------------------------------

    # >> Loads Epdomonously-formatted data into the Epdobase object:            
        
    def load(self, filepath, format='auto'):

        fili = open(filepath,'r')

        strn = fili.read() # >> Reads entire file into a string

        if format == 'auto':

            # >> Determine whether format is Epdex, Epdata, or Epdobin, and
            # >> launch the parser accordingly.  Note that the file type may be
            # >> ambiguous, in which case we parse as Epdex if '++' occurs
            # >> first, and as Epdata if '[' occurs first.  e.g., the unassigned
            # >> matter may be formatted as Epdata in an Epdex file, or as Epdex
            # >> in an Epdata file.  The ability to discriminate between these
            # >> latter possibilities (although not in a very sophisticated
            # >> manner) was added on 2010.10.03.

            contains_pp    = '++' in strn      # >> true if file has '++' in it
            contains_sqbrk = '[' in strn       # >> true if file has '[' in it

            contains_dob   = '[file_type] Epdobin' in strn # >> true for Epdobin

            if contains_dob : file_format = 'dob'      # >> Epdobin file

            elif contains_pp and not contains_sqbrk :  # >> has '++' and not '['
                file_format = 'dex'

            elif not contains_pp and contains_sqbrk :  # >> has '[' and not '++'
                file_format = 'dat'

            elif contains_pp and contains_sqbrk :      # >> has both (Epdadex?)

                warning_msg = 'Epdobase: Warning: file format is not obvious...'

                spbrk_index = strn.find('[')           # >> first index of '['
                pp_index    = strn.find('++')          # >> first index of '++' 

                if spbrk_index < pp_index:             # >> '[' occurs first

                    warning_msg += ' reading as Epdata (i.e., Epdadex).'
                    file_format = 'dat'

                else :                                 # >> '++' occurs first 

                    warning_msg += ' reading as Epdex.'
                    file_format = 'dex'

                print(warning_msg)

        # ! I've added the option of explicitly specifying the format in the
        # ! epdobase call: [110530]

        else: file_format = format     # >> format was defined in epdobase call


        # >> Finally, parse the files according to type:

        if   file_format == 'dat' : prsd = parse_epdata(strn,'first_tag')
        elif file_format == 'dex' : prsd = parse_epdex(strn)
        elif file_format == 'dob' : prsd = parse_epdobin(strn) 
        elif file_format == 'ddx' : prsd = parse_epdata(strn) 
        elif file_format == 'csv' : prsd = parse_csv(strn) 

        # >> Assign parsed elements accoringly:

        if file_format == 'dob' : 
            self.ndct = prsd[0]        # >> epdobin loads to numeric dict
        else: self.dcty = prsd[0]      # >> all others load to main dict

        self.flds = prsd[1]  # >> fields
        self.defs = prsd[2]  # >> field definitions

        # >> There is no handling of unassigned matter in epdobin:

        if file_format != 'dob': self.umat = prsd[3] 

        fili.close() # >> Close the input file

    #---------------------------------------------------------------------------
    # -- Save as Epdex, Epdata, Epdobin, CSV, or LaTex, or pickle it -----------
    #---------------------------------------------------------------------------

    # :: Save to file ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    # >> Saves the Epdobase object in Epdex, Epdata, Epdobin or CSV file.  
    # >>
    # >> Inputs are:
    # >>
    # >> format   = 'dex','epdex','epdata','dat','epdobin','epdob','dob','csv',
    # >>            'tex', or 'latex'
    # >>
    # >> fields   = list of field names
    # >> filename = file name   

    def save_part(self, format, fields, filepath) :

        import copy

        strn = ''
        filo = open(filepath,'w')
        field_defs = {}

        # >> If the number of fields is not equal to the number of field
        # >> definitions, then pear it down to the requested subset: 

        if len(self.defs) != len(fields) :

            if len(self.defs) != 0 : 
                
                for field in fields:
                    field_defs[field] = self.defs[field]
        else:

            field_defs = copy.deepcopy(self.defs)

        # >> Save as epdex, epdata, epdobin, csv, as requested...            

        # !! I would like to eliminate the calls to "copy.deepcopy", used here
        # !! because it is easiest to deal with unassigned matter by simply
        # !! adding a field called "umat" to the dictionary (see
        # !! {20100526-1511}). The call to "copy.deepcopy" creates a complete
        # !! copy of the dictionary, which makes this method a memory hog:

        if format == 'epdex' or format == 'dex':

            strn = write_epdex(copy.deepcopy(self.dcty), fields, \
                                   field_defs, self.umat[:])

        # !! Writing epdata does not modify the dictionary:

        elif format == 'epdata' or format == 'epdat' or format == 'dat':
            strn = write_epdata(self.dcty, fields, field_defs, self.umat)

        # !! Note that Epdobin does not handle unassigned matter, and that the
        # !! numerical dictionary (.ndct) is the output:

        elif format == 'epdobin' or format == 'epdob' or format == 'dob':
            strn = write_epdobin(self.ndct, fields, field_defs) 

        elif format == 'csv' : 
            strn = write_csv(self.dcty, fields, field_defs, self.umat, 
                             pres=self.pres)

        elif format == 'tex' or format == 'latex': 
            strn = write_latex(self.dcty, fields, field_defs, self.umat,
                               pres=self.pres)
                   
        filo.write(strn)
        filo.close()

    def save(self, format, filepath) : 

            self.save_part(format, self.flds[:], filepath)

    # :: Pickle the epdobase :::::::::::::::::::::::::::::::::::::::::::::::::::

    # !! I'm amazed it's taken this long to add a pickler. [140109]

    # >> Sole input is a flag for use of a timestamp (yrmody+hrmn), which by
    # >> default is false.  

    # >> To unpickle, simply use :: grim = om.unpickle(filename.pkl ::.

    def pickle(self, filepath, useTimeStamp = False) :

        import os
        import omnigenus as om
        import pickle

        # !! N.B. this will fail if there is more than one period in filename:

        fwoutext = filepath.split('.')[0]

        if useTimeStamp : 

            timestamp = om.make_datetime_stamp(False)
            fname = fwoutext + '_' + timestamp + '.pkl'

        else :
            
            fname = filepath

        filo = open(fname,'w')
        pickle.dump(self,filo)
        filo.close()

    # :: Write contents of Epdobase to string ::::::::::::::::::::::::::::::::::

    # >> Sole input is epdoc_type, which can have the values 'dex' (for Epdex)
    # >> and 'dat" (for Epdata) or 'dob' (for Epdobin), 'csv' (for CSV), 'tex'
    # >> (for LaTex) and other variants of these, listed below. [101003]
    
    def as_string(self, epdoc_type) :

        import copy  # >> [101028]

        if epdoc_type == 'dex' or epdoc_type == 'epdex': 
            strn = write_epdex(copy.deepcopy(self.dcty), \
                                   self.flds,self.defs,self.umat)

        elif epdoc_type == 'dat' or epdoc_type == 'epdata' \
                or epdoc_type == 'epdat': 
            strn = write_epdata(self.dcty,self.flds,self.defs,self.umat)

        elif epdoc_type == 'dob' or epdoc_type == 'epdob' \
                or epdoc_type == 'epdobin': 
            strn = write_epdata(self.dcty,self.flds,self.defs,self.umat,
                                pres=self.pres)

        elif epdoc_type == 'csv': 
            strn = write_csv(self.dcty,self.flds,self.defs,self.umat,
                             pres=self.pres)

        elif epdoc_type == 'tex' or epdoc_type == 'latex': 
            strn = write_latex(self.dcty,self.flds,self.defs,self.umat,
                               pres=self.pres)

        return strn

    # --------------------------------------------------------------------------
    # -- Handling Epdadex and Epdo-formatted records ---------------------------
    # --------------------------------------------------------------------------
    
    # :: Parsing records as Epdex or Epdata ::::::::::::::::::::::::::::::::::::
    
    # >> If it is known that the contents of a field are formatted as Epdex or
    # >> Epdata, this method will translate each record of that field to an
    # >> epdobase object and return a list of these objects with the same number
    # >> of elements as there are records in the global epdobase object.  Here,
    # >> the input "field_name" is a kwarg, set by default to "umat" or
    # >> "unassigned matter".  The second keyword argument "epdoc_type" is set
    # >> to "dex" for Epdex and "dat" for Epdata (default is "dex").  Note that
    # >> this is primarily used for Epdata documents whose unassigned matter is
    # >> formatted as Epdex (hence the default settings).
    
    # !! This method was added on 2010.10.03, mainly in support of "Epdadex":
    # !! i.e., Epdata whose unassigned matter is formatted as Epdex.  

    def get_epdices(self, field_name='umat', epdoc_type='dex') : 

        if field_name == 'umat' : col = self.umat
        else : col = self.dcty[field_name]

        epdices = []
        
        for i in range(0,self.len(),1) : 

            ep = cl_epdobase()            # >> create an Epdobase object

            # >> Parse the record:

            if   epdoc_type == 'dex' : parsed = parse_epdex(self.umat[i])
            elif epdoc_type == 'dat' : parsed = parse_epdat(self.umat[i])

            # >> Populate the corresponding Epdobase:

            ep.dcty = parsed[0]; ep.flds = parsed[1] 
            ep.defs = parsed[2]; ep.umat = parsed[3]

            # >> Add the field values for the currect record as meta-data for
            # >> this Epdobase object... (N.B. This was added on 2010.10.25 and
            # >> not immediately tested.  The for-loop was also changed.)
            
            ep.meta = {}
            
            for field in self.flds : ep.meta[field] = self.dcty[field][i]

            epdices.append(ep)  # >> Finally, append the epdobase

        return epdices

    #---------------------------------------------------------------------------
    # -- Computing attributes --------------------------------------------------
    #---------------------------------------------------------------------------

    # >> Computes and returns the number of records in the Epdobase:

    def len (self) : return num_dict_records(self.dcty)

    #---------------------------------------------------------------------------
    # -- Shrink current epdobase to a subset of records ------------------------
    #---------------------------------------------------------------------------

    # Inds is a list or array of indices of records that should be kept; all the
    # rest are discarded. [151128]

    def shrink(self, inds) :

        inds_arr = np.array(inds)
        inds_lst = list(inds)

        for fld in self.flds:

            self.ndct[fld] = self.ndct[fld][inds_arr]
            tmp_dcty       = np.array(self.dcty[fld])
            self.dcty[fld] = list(tmp_dcty[inds_arr])
            
    #---------------------------------------------------------------------------
    # -- Initializing fields & adding new ones ---------------------------------
    #---------------------------------------------------------------------------

    # :: Initializing fields :::::::::::::::::::::::::::::::::::::::::::::::::::

    # >> Creates empty lists for each field name in the list "fields", storing
    # >> these in the dictionary "dcty" and numeric dictionary "ndct".  This
    # >> should be used when creating an epdobase from scratch that has no
    # >> records.

    def init_fields(self, fields) :

        self.flds = fields

        for field in fields : 
            self.dcty[field] = []
            self.ndct[field] = []
            self.defs[field] = ''

    # :: Adding new fields :::::::::::::::::::::::::::::::::::::::::::::::::::::

    # >> Adds the field names in "fields" and their definitions/descriptions in
    # >> "field_defs" to the Epdobase.  Of course there should be a one-to-one
    # >> correspondence between the elements of fields and field-defs, which are
    # >> both lists of strings.  This should be used to add new fields to an
    # >> Epdobase object that already has some fields and records.  Inputs are:

    # >> * fields     = list of field names to add
    # >> * field_defs = definitions/descriptions of the fields in "fields"

    # !! Note that you can pass '' for "field_defs" if you don't want any. 

    def add_fields(self, fields, field_defs) :

        num_records = self.len() 
        
        for field in fields : 

            self.flds.append(field)
            self.dcty[field] = []

            # >> Fill all the new records with 'null's:
            
            for i in range(0,num_records,1): self.dcty[field].append('null')
            
            # >> If field_defs are supplied, store them.
            
            if len(field_defs) > 0 : self.defs[field] = field_defs[field]

    # --------------------------------------------------------------------------
    # -- Finding & sorting records ---------------------------------------------
    # --------------------------------------------------------------------------

    # :: Return matching records :::::::::::::::::::::::::::::::::::::::::::::::

    # >> Returns the indices of any records that match any of the fields and
    # >> record values in valdict exactly, or any records that match all of them
    # >> exactly.  The sole input "valdict" is a dictionary whose keys are the
    # >> fields to be matched, and whose values are lists of all the values to
    # >> be matched. For details, see {20100704-2216}.

    def matching_records(self, valdict) :

        any_matched, all_matched = \
            get_matching_records(self.dcty, valdict, 'exact')
        
        return all_matched

    # :: Searching records :::::::::::::::::::::::::::::::::::::::::::::::::::::

    # >> Returns the indices of any records that contain any of the record
    # >> values in valdict for any of the fields indicated in that dictionary
    # >> variable, or any records that match all of them.  The sole input
    # >> "valdict" is a dictionary whose keys are the fields to be searched, and
    # >> whose values are lists of all the values to be searched for. For
    # >> details, see {20100704-2216}.

    def search_records(self, valdict) :

        any_matched, all_matched = \
            get_matching_records(self.dcty, valdict, 'partial')

        return any_matched

    # :: Sorting records :::::::::::::::::::::::::::::::::::::::::::::::::::::::
    
    # >> Sort the records in the epdobase by the field "field".  Input
    # >> "whether_reverse" should be True for reverse order, False otherwise.

    def sort_records(self, field, whether_reverse) :

        sort_epdobase_simple(self, field, whether_reverse)

    # --------------------------------------------------------------------------
    # -- Handling dictionary types, empty records, & nulls ---------------------
    # --------------------------------------------------------------------------

    # :: Numerizing records ::::::::::::::::::::::::::::::::::::::::::::::::::::

    # >> This just refers to converting the data types of whole columns (fields)
    # >> to numbers if possible (int or float), and storing the result in ndct.
    # >> See the header of the function that is wrapped here:

    def numerize(self) : numerize_epdobase(self)
    
    # :: "Characterizing" records ::::::::::::::::::::::::::::::::::::::::::::::

    # >> This just refers to converting the data types of the numeric dictionary
    # >> (ndct) to strings and overwriting the string dictionary dcty.  This
    # >> way, the user can use numerize() to create numeric lists and then
    # >> arrays, perform some operations on these numbers, and then convert them
    # >> back in to the string-dictionary form that allows access to e.g., file
    # >> I/O. See the header of the function that is wrapped here for more info:

    def characterize(self) : characterize_epdobase(self)

    # :: Creating, "Nullifying", "Unnullifying" empty records ::::::::::::::::::

    # >> This just refers to converting empty strings to "null"

    def nullify(self) : nullify_epdobase(self)

    # >> This just refers to converting "null"s to empty strings:

    def unnullify(self) : unnullify_epdobase(self)

    # >> Create new/additional empty records [130710]

    def make_empty_records(self,N) : 

        for i in range(N) :
            for fld in self.flds : 
                self.dcty[fld].append('null')

        self.numerize()
                
# ==============================================================================
#
# 20100526-1508-mpuboo - merge_epdobase.py
#
# <summary>
#
# Smart merging and consolidation of two Epdomonus dictionary (epdobase) objects
# </summary>
#
# <syntax>
# 
# ep3 = merge_epdobase(ep1, ep2, match_fields) </syntax>
#
# <inputs>
# 
# Inputs "ep1" and "ep2" are the Epdobase objects to be merged.  Argument
# "match_fields" is a list of names of fields to be used for matching records in
# each epdobase.
#
# There is now also a kwarg "add_nonmatching_records" which should be set to
# False if the user prefers to merge into a database that is the intersection
# rather than union of the two input databases. </inputs>
#
# <products>
# 
# Result is the merged database, also an Epdobase object.  The script will loop
# over all the records in ep1, finding all records in ep2 that match each record
# in ep1 for the fields listed in "match_fields".  If there is no match, a new
# record is created.  Fields in ep2 but not in ep1 are added to ep3; the empty
# fields of non-matching records in ep2 will inherit "null" values in ep3.
# Likewise for fields in ep1 and not in ep2.  Note that matching records having
# the same non-matching fields with different values for ep1 and ep2 will
# inherit the values of ep2 (i.e., ep1's values will be "over-written" by ep2's
# values wherever the values in matching records disagree). </products>
#
# <type>
# 
# Function </type>
#
# <dependencies>
# 
# omnigenus </dependencies>
#
# <updates>
#
# - In some cases, you may not wish to add nonmatching records; I have added
#   a kwarg whose default argument is "True" for backward compatibility. </updates>
#
# <notes> 
#
# As currently implemented, records with empty fields in ep2 that match records
# in ep1 that are not empty will *not* overwrite the ep1 values.  Same behavior
# applies to the unassigned matter.  That is, as currently implemented, the
# merger preserves information, never overwriting information with empty record
# values.  See {saftey1} and {safety2} in the code. </notes>
#
# ==============================================================================

def merge_epdobase(ep1, ep2, match_fields, add_nonmatching_records = True) :

    # >> First nullify both epdobases:

    ep1.nullify()
    ep2.nullify()

    # >> If their fields are undefined (empty), get them from the dict keys:

    if len(ep1.flds) == 0 : ep1.flds = ep1.dcty.keys()
    if len(ep2.flds) == 0 : ep2.flds = ep2.dcty.keys()

    # >> Then create the new dict ep3, w/all the fields of both prior structs:

    ep3 = cl_epdobase()

    ep3.flds = ep1.flds[:]

    for field in ep2.flds:
        if field not in ep3.flds :
            ep3.flds.append(field)

    # >> Copy the field definitions, overwriting ones from ep2 occurring in ep1:

    if len(ep1.defs) > 0 : 
        for field in ep1.flds: ep3.defs[field] = ep1.defs[field][:]

    if len(ep2.defs) > 0 : 
        for field in ep2.flds: ep3.defs[field] = ep2.defs[field][:]

    # >> The length of ep1 and ep2:

    len_ep1 = ep1.len()    
    len_ep2 = ep2.len()

    # >> Create arrays for all the ep2 fields:

    for field in ep2.flds : 
        ep3.dcty[field] = []
        for i in range(0,len_ep1,1) :
            ep3.dcty[field].append('null') 

    # >> Fill the ep3 dictionary with the dictionary records of ep1:

    for field in ep1.flds : ep3.dcty[field] = ep1.dcty[field][:]

    # >> Fill unassigned matter in ep3 with the unassigned matter of ep1:

    ep3.umat = ep1.umat[:] # >> Note that ep1.umat might be empty!

    # >> If ep2 has unassigned matter and ep1 does not, fill ep3's unassigned
    # >> matter with as many nulls as there are records in ep1:

    if len(ep2.umat) > 0 and len(ep3.umat) == 0 :
        for i in range(0, len_ep1, 1 ) : ep3.umat.append("null")

# -- Find all records in ep2 that match a record -------------------------------
     
    # >> For each "record" of ep2, find the record of ep3 with matching values
    # >> in the match_fields, 

    matches = []

    for i in range(0, len_ep2, 1) : # >> For each record in ep2 ...

        valdict = {}

        for field in match_fields : valdict[field] = ep2.dcty[field][i]
        tmp1,tmp2 = get_matching_records(ep3.dcty,valdict,'exact')
        matches.append(tmp2)

# -- Overwrite existing records, add the new ones ------------------------------

    # >> Now update the matching records with the values in ep2.  If a record
    # >> had no match, then add the entire record.

    for i in range (0, len_ep2, 1) :  # >> For each record in ep2...

        # >> if there were no matches to this reccord, add it to ep3:

        if len(matches[i]) == 0 and add_nonmatching_records:

            # >> Fields in ep1 not in ep2 are assigned "null"s for all records:

            for field in ep1.flds :
                if field not in ep2.flds:
                    ep3.dcty[field].append('null')

            for field in ep2.flds :

                # >> add the record provided field is neither empty nor "null".
                
                # !! This looks like a mistake as originally written, and
                # !! creates columns of uneven length. [160623]

                #if len(ep2.dcty[field][i]) != 0 and ep2.dcty[field][i] !='null':
                ep3.dcty[field].append(ep2.dcty[field][i])

            # >> Also add the corresponding unassigned matter:        

            if len(ep2.umat) > 0 : ep3.umat.append(ep2.umat[i])
            elif len(ep3.umat) > 0 : ep3.umat.append("null")

        # >> If there was one match to this record, overwrite nonempty fields
        # >> that occur in ep2 and ep3, and add the rest:

        elif len(matches[i]) == 1 :

            # >> For the record in ep1 matching the current record in ep2 ...

            for matching_record in matches[i] :   

                # >> loop over fields and update the values of ep1 into ep3:

                for field in ep2.flds :

                    # >> As long as the field of the current record in ep2 is
                    # >> not null or empty, update its value in the matching
                    # >> record in ep3. [safety1]

                    if len(ep2.dcty[field][i]) != 0 and \
                            ep2.dcty[field][i] !='null':            
                        ep3.dcty[field][matching_record] = ep2.dcty[field][i][:]

                # >> Also update the unassigned matter:
                    
                if len(ep2.umat) > 0 : 

                    # >> As long as the current record's unassigned matter
                    # >> in ep2 is not null or empty, update its value in
                    # >> the matching record in ep3. [safety2]

                    if len(ep2.umat[i]) != 0 and \
                            ep2.umat[i] != 'null' : 
                        ep3.umat[matching_record] = ep2.umat[i]

                # >> If ep2 has no unassigned matter and there is nothing in the
                # >> ep3 recored, add a null (after adding calls to nullify() at
                # >> the start of this method, I think this line is redundant):

                elif len(ep3.umat) > 0 : 
                    if len(ep3.umat[matching_record]) == 0:
                           ep3.umat[matching_record] = 'null'

        # >> If there was more than one matching record, the matching fields are
        # >> non-unique.  Warn the user and exit:

        elif len(matches[i]) > 1 :

            print('merge_epdobase.py: matching fields are nonunique.') 
            print('These records have nonunique identifiers in ep1:')
            for j in matches[i] : print matches[i][j]
            print('Exiting...')
            exit()

    return ep3

# ==============================================================================
#
# 20100526-1510-mpuboo - Parse Epdex
#
# <summary> 
#
# Parse epdex format into an epdobase (N.B. all arrays will be m x 1) </summary>
#
# <syntax>
# 
# epdobase_elements = parse_epdex(string) </syntax>
#
# <inputs>
# 
# The input is a string that contains the contents of a text file, where each
# line is separated by a newline character.  This can be read from a file object
# using the read() method. </inputs>
#
# <products>
# 
# The output is a list with four elements: a dictionary containing the database,
# a list of field-names, a list of field descriptions or definitions, and a list
# of unassigned matter.  This definitions list is of course empty if there was
# no field-definitions line in the Epdex file. The unassigned matter is likewise
# empty if there was no unassigned matter in the document. </products>
#
# <type>
# 
# Function </type>
#
# <dependencies>
# 
# None </dependencies>
#
# <updates> </updates>
#
# <notes> </notes>
#
# ==============================================================================

def parse_epdex(strn) :

    fili = strn.splitlines() # >> Splits string into list of strings at newlines

    field_line = 0  # >> Keeps track of whether we are reading the field-line
    epdex_open = 0  # >> Keeps track of whether we are reading epdex matter

    s = {}          # >> This dictionary will store the database
    field_defs = {} # >> This will store the field definitions

    # >> Keeps track of whether the epdex has unassigned matter:

    has_umatter = False 

    # >> Unassigned matter (if any) is stored in this list:

    umat = []

# -- Main loop over lines in file ----------------------------------------------

    for tline in fili : 

        sline = tline.strip() # >> Remove leading and trailing whitespace

        if sline[0:2] != ';;' :  # >> Ignore commented lines

            # >> Quit if you find "++" on a line by itself (otherwise, the
            # >> program will stop reading at the EOF).

            if len(sline) >= 2 and sline == '++' : break

            # >> On finding this, we're inside epdex matter :

            if len(sline) > 2 and sline[0:2] == '++' :
                field_line = 1
                epdex_open = 1
    
            # >> Populate the epdex database :

            if epdex_open == 1 and field_line == 0 and sline[0:2] != '**':
                strs = tline.split('#') # >> Split the string at the '#'s

                for field in field_list : 
                    stmp = strs[field_list.index(field)].strip()

                    # >> Replace newline characters:

                    s[field].append(stmp.replace('|NL|','\n')) 

            # >> Populate the list of fields : 

            if field_line == 1 :

                field_line = 0
                field_list_tmp = sline[2:].split('#')

                field_list = []

                # >> Eliminate whitespace from field names, initialize the
                # >> dictionary that will hold the database:

                for strn in field_list_tmp : 

                    # >> First determine whether the field refers to unassigned
                    # >> matter:

                    if strn.strip() == 'umat' or strn.strip() == 'Umat' \
                                       or strn.strip() == 'UMAT':

                       has_umatter = True
                       umat_key = strn.strip()

                    if len(strn.strip()) > 0 : 

                        field_list.append(strn.strip())
                        s[strn.strip()] = []
                        field_defs[strn.strip()] = []


            # >> Store the field definitions :

            if epdex_open == 1 and field_line == 0 and sline[0:2] == '**':

                strs = sline[2:].split('#')

                for field in field_list : 
                    field_defs[field] = strs[field_list.index(field)].strip()

    # >> Now, separate the unassigned matter, if any, into the "umat" list:

    if has_umatter :

        umat = s[umat_key]

        del s[umat_key]
        del field_defs[umat_key]
        field_list.remove(umat_key)

    # >> Finally, if there are no field definitions, return these as an empty
    # >> dictionary:

    total_def_len = 0

    for field in field_list: total_def_len += len(field_defs[field])
    if total_def_len == 0 : field_defs = {}

    return [s, field_list, field_defs, umat]
    
# ==============================================================================
#
# 20100526-1511-mpuboo - Write Epdex
#
# </summary>
#
# Writes an epdobase's elements to epdex format (N.B. all arrays must be m x 1)
# </summary>
#
# <syntax>
# 
# strn = write_epdex(dcty, fields, field_defs, umat) </syntax>
#
# <inputs>
# 
# The argument "dcty" is a dictionary having the same format as an epdobase dcty
# variable (see {20100527-1045}). The argument "fields" is equivalent to an
# epdobase flds variable (a list of field names), and field_defs corresponds to
# the "defs" variable of an epdobase object (a list of field definitions).  Note
# that "fields" can be set to an empty string or an empty list, in which case it
# will be filled using the keys() method.  If "field_defs" is empty, then the
# fields will not be defined in the epdata file. </inputs>
#
# <products>
# 
# This method writes the contents of the injested epdobase elements to an
# epdex-formatted string "strn" which can, in turn, be written to a
# file. </products>
#
# <type>
# 
# Function </type>
#
# <updates> </updates>
#
# <notes>
# 
# Note that all new-line characters are replaced with |NL| in the epdex file,
# where each record is allowed to occupy exactly one line. </notes>
#
# ==============================================================================

def write_epdex(s, fields, field_defs, umat) :

    strn = '';

    strn += '++ '  # >> The obligatory opening "++" on the line of field names

    # >> Use the given field names, or derive them from the dictionary keys if
    # >> "fields" is empty:

    if len(fields) == 0 : list_fields = s.keys()  
    else : list_fields = fields

    # >> If there is umatter, simply add this to the list of field names.

    if len(umat) != 0 : 
        list_fields.append('umat')
        s['umat'] = umat       # !! This passes the object, not the reference.

    # >> Build the field-names line, using pound-signs as separators:

    for field in list_fields : strn += field + ' # '

    strn = strn[0:-3]  # >> strike the last ' # '
    strn += '\n'

    # >> Now print the field definitions (if field_defs is not empty)
    # >> (replace any newline characters with "|NL|")

    if len(field_defs) > 0 : # >> this conditional was added circa 101000
        strn += '** '

        # >> Add a definition for unassigned matter, if any:

        if len(umat) != 0 : field_defs['umat'] = 'Unassigned matter'

        # >> Now print all the field definitions:

        for field in list_fields : 
            strn += field_defs[field].replace('\n','|NL|') + ' # ' 

        strn = strn[0:-3]  # >> strike the last ' # '
        strn += '\n'

    # >> Determine the number of records, and add this many lines to the string,
    # >> printing the whole contents of the epdobase dcty.  All newline
    # >> characters are replaced with "|NL|" because all contents of each record
    # >> must lie on the same line.
    
    array_len = num_dict_records(s)  

    for i in range(0,array_len,1) :

        for field in list_fields : 
            strn += str(s[field][i]).replace('\n','|NL|') + ' # '

        strn = strn[0:-3]  # >> strike the last '#'
        strn += '\n'   
            
    # >> Add the closing "++":

    strn += '++\n'  
    return strn

# ==============================================================================
#
# 20100316-3521-mpuboo - Epdata parser
#
# <summary>
# 
# Parses an Epdata file: i.e., an Epdox database, with square-ref-tag entries.
# </summary>
#
# <syntax>
# 
# db_dict = parse_epdata(file_path, start_tag) </syntax>
#
# <inputs>
#
# Input "file_path" is the path to the epdata file, including the filename.  
# (For the definition of the Epdata format, see {20100123-1918}).  The argument
# "start_tag" is the value of the tag (the text enclosed in square brackets) 
# that begins each entry of the database. If this is given as 'first_tag', then 
# parse_epdata will simply use the first tag that it finds. </inputs>
#
# <products>
#
# The output is a dictionary, whose keys correspond to the tags in each entry
# of the database.  The first entry the epdata file *must* contain *all* 
# possible tags.  If any of these are omitted in later entries, then the parser 
# will assign "null" to those values.  If there is no unassigned matter, the
# "gathered" unassigned matter will be an empty list. </products>
# 
# <dependencies>
# 
# re, filum </dependencies>
#
# <updated>
#
# - Previous updates: 2010.04.06; 2010.05.26; 2010.08.15; 
# - Added support for double-ampersand brackets. [110530] </updated>
#
# <notes>
#
# Note that the string next to a square reference tag can continue onto the next 
# line, as in true Epdata files. </notes>
#
# ==============================================================================
        
def parse_epdata(strn, start_tag) :

    import re, filum

    fili = strn.splitlines()  # >> Split string into a list of lines

    # >> Initially, previous line can't be unassigned matter:

    prev_line_was_umatter = False 

    # >> The pattern of the starting tag (from the beginning of a line):

    if start_tag == 'first_tag':

        # startag_pat = '^\[(.*?)\](.*)' # >> Match the first tag 
        # !! This line was modified to accommodate leading whitespace [101027]
        # !! Other matching expressions were modified similarly. [101027]

        startag_pat = '^\s*\[(.*?)\](.*)' # >> Match the first tag

    else :     

        # >> Escape special characters :

        start_tag = filum.fix_str_for_match(start_tag) 

        startag_pat = '^\s*\[(' + start_tag + ')\](.*)'

    # >> The pattern of any other tag (from the beginning of a line):
    
    normtag_pat = '^\s*\[(.*?)\](.*)' # >> Note: "?" means nongreedy matching.

    # >> The pattern of a tag definition:

    defntag_pat = '^\* \[(.*?)\](.*)'

# -- Counting the number of database entries ----------------------------------- 
    
    tot_entries = 0
    
    for line in fili :

        line  = line.strip() # >> wipes leading/trailing whitespace [100926]

        patmatch = re.search(startag_pat,line) 

        if patmatch : 

            tot_entries += 1 

            if tot_entries == 1 :

                start_tag   = patmatch.group(1)
                startag_pat = '^\s*\[(' + start_tag + ')\](.*)'

# -- Parsing the file ----------------------------------------------------------
        
    item_num    = -1    # >> This will be used for counting the database entries
    dubamp_mode = False # >> Keep track of whether in a double-ampersand bracket
    
    # These switches are (like dubamp_mode) used to keep track of state:

    prev_line_had_content = False
    prev_line_was_umatter = False
    
    db = {} # >> This will store the database

    tag_list = [] # >> Will be used to keep order of tags (in order of apprnce)
    tag_defs = {} # >> Will be used to hold tag definitions (if any are found)

    # >> Will be used to store the "unassigned matter": data not associated with
    # >> a specific field:

    umat = [] 

    # >> Main loop

    for line in fili :

        wline = line        # >> keeps leading/trailing whitespace [101028]           
        line = line.strip() # >> Ignore leading and trailing whitespace [100926]

        patmatch = re.search(startag_pat,line,re.M)  # >> Try the start tag
       
        if patmatch : 
            item_num += 1 # >> Count up when you match the start_tag 

        patmatch = re.search(defntag_pat,line,re.M) # >> Try matching a tag def

        if patmatch : # >> If we've matched the pattern of a tag defintion

            strn = patmatch.group(2)
            tag_defs[patmatch.group(1)] = strn.strip()
           
        # >> Now try matching *any* tag, and act on the match only if we're not
        # >> inside of an ampersand bracket.

        patmatch = re.search(normtag_pat,line,re.M) # >> Try matching any tag  
                     
        if patmatch and not dubamp_mode: 
            # >> ... tag is matched and we're not in dubamp brackets...
                    
            # >> First remove the bounding whitespaces from the tag value:

            strn = patmatch.group(1)
            tag_name = strn.strip()
            
            # >> Note it in the running list that maintains the tag order:

            if tag_name not in tag_list : tag_list.append(tag_name)

            # >> If this is the very first tag, create a list for the corres-
            # >> ponding dictionary key with the total number of entries counted
            # >> earlier.  Fill the entries with numbers.  Later, we will 
            # >> replace all integer values with the string "null" (i.e., the 
            # >> entry was not filled).  

            if item_num == 0 : db[tag_name] = range(0,tot_entries,1)
        
            # >> Search the string next to the tag for a double-ampersand, and
            # >> toggle the double-ampersand mode accordingly (i.e., if there is
            # >> one, then we're in a double-ampersand bracket):

            strn = str(patmatch.group(2))
            strn,dubamp_mode = dubamp(strn,dubamp_mode)
    
            # >> Now store the string next to the tag in the dictionary:
            
            db[tag_name][item_num] = strn.strip()
                
            prevtag = tag_name
            
            # >> This will tell the next iteration that there was
            # >> field-associated content on this line (assigned matter):
            
            prev_line_had_content = True  
        
            # >> This will tell the next iteration that the this line was not
            # >> made up of unassigned matter:

            prev_line_was_umatter = False

        elif item_num > -1: 
            
            # >> If no match, content is maybe continued from previous line.
            # >> But we won't even try this until the first match.
                
            # >> See if there's anything on the current line: 
                     
            length_of_current_line = len(line)

            # >> Determine whether current line is a partition / divider:
                        
            if length_of_current_line > 10 :
                if line[0:5] == '-----' or line[0:5] == ':::::' or \
                   line[0:5] == '.....' or line[0:5] == '=====' :
                   
                   is_partition = True
                     
                else : is_partition = False
                
            else : is_partition = False     

            # >> Create a list for the unassigned matter with the total number
            # >> of entries counted earlier.  Fill the entries with numbers.
            # >> Later, we will replace all integer values with the string
            # >> "null" (i.e., the entry was not filled).
            
            if len(umat) == 0: umat = range(0,tot_entries,1)
                                                          
            # >> If the previous line had content and the current one isn't
            # >> empty and not a partition, then append it to the same
            # >> dictionary entry as we did the previous line:
        
            if prev_line_had_content and length_of_current_line > 0 and \
                not is_partition and not prev_line_was_umatter:

                # >> Clean the line of double-ampersands and toggle the
                # >> double-ampersand mode (i.e., double-ampersand bracket)
                # >> accordingly: 

                line,dubamp_mode = dubamp(line, dubamp_mode) 

                # >> Add it to the database

                db[prevtag][item_num] += '\n' + line

            # >> If the previous line had no content and the current one isn't
            # >> empty and not a partition but we are inside of a
            # >> double-ampersand bracket, then append it to the same dictionary
            # >> entry as we did the previous line:

            elif not prev_line_had_content and length_of_current_line > 0 \
                    and not is_partition and not prev_line_was_umatter and \
                    dubamp_mode :

                # >> Clean the line of double-ampersands and toggle the
                # >> double-ampersand mode (i.e., double-ampersand bracket)
                # >> accordingly: 

                line,dubamp_mode = dubamp(line, dubamp_mode) 

                # >> Add it to the database:

                db[prevtag][item_num] += '\n\n' + line
                        
            # >> If the previous line had no content and the current one isn't
            # >> empty and not a partition and we are not in a double ampersand
            # >> bracket, then add this to the generic "unassigned matter"
            # >> (umat) of the current record: matter not associated with any
            # >> specific field.  Also tell next loop that we had no
            # >> field-associated content on this iteration:
        
            elif not prev_line_had_content and length_of_current_line > 0 \
                    and not is_partition and not dubamp_mode and not \
                    prev_line_was_umatter:

                # >> Recall that by default, unfilled unassigned matter is an
                # >> integer, and so we have to set it equal to an empty
                # >> string to get started.

                if isinstance(umat[item_num], type(1)) : umat[item_num] = ''

                umat[item_num] += '\n' + wline # >> w/leading & trailing wspace
                prev_line_had_content = False

                # >> This will tell the next loop that we're reading unassigned
                # >> matter:

                prev_line_was_umatter = True   

            # >> Previous line was unassigned matter and current line is not a
            # >> partition, and so we add it to the unassigned matter:    

            elif not is_partition and prev_line_was_umatter : 

                umat[item_num] += '\n' + wline # >> w/leading & trailing wspace

            # >> Otherwise, tell next iteration we had no field-associated
            # >> content this time:

            else: prev_line_had_content = False                                
                                
    # >> This loop assigns to "null" all the fields that were not filled in:
    # >> i.e., all fields that are still integers, or made up entirely of 
    # >> whitespace characters, or empty strings.  This is used to fill up the
    # >> database (the dictionary) as well as the unassigned matter (umat).
    # >> But if umat has *only* nulls, it is set equal to an empty list.
    
    for tag in db :         
            
        for i in range(0,tot_entries,1) :
            
            str_ver = str(db[tag][i])
            
            if isinstance(db[tag][i],int) or str_ver.isspace() or \
                (len(str_ver) == 0) :
                
                db[tag][i] = 'null'


    # >> Repeat for the unassigned matter & strip leading/trailing whitespace:

    if len(umat) > 0 : 

        for i in range(0,tot_entries,1) : 

            if isinstance(umat[i],int) or umat[i].strip().isspace() or \
                    len(umat[i]) == 0 : umat[i] = 'null'

            umat[i] = umat[i].strip()  # >> wipe leading/trailing whitespace

    # >> If umat has only null values, set it equal to an empty list:

        if umat.count('null') == len(umat) : umat = []

    return [db, tag_list, tag_defs, umat]

# ..............................................................................

# >> Simple method for striking double-ampersands and indicating to the
# >> interpreter that we are currently reading a double-ampersand bracket.

def dubamp(line, dubamp_mode) : 

    if '&&' in line:

        line = line.replace('&&','').strip()
        dubamp_mode = True - dubamp_mode

    return line,dubamp_mode
                        
# ==============================================================================
#
# 20100526-1824-mpuboo - Write Epdata
# 
# <summary>
#
# Writes an epdobase to epdata format (N.B. all arrays must be m x 1) </summary>
#
# <syntax>
# 
# strn = write_epdata(dcty, fields, field_defs, umat) </syntax>
#
# <inputs>
# 
# The argument "dcty" is a dictionary having the same format as an epdobase dcty
# variable (see {20100527-1045}). The argument "fields" is equivalent to an
# epdobase flds variable (a list of field names), and field_defs corresponds to
# the "defs" variable of an epdobase object (a list of field definitions).  Note
# that "fields" can be set to an empty string or an empty list, in which case it
# will be filled using the keys() method.  If "field_defs" is empty, then the
# fields will not be defined in the epdata file. </inputs>
#
# <products>
# 
# This method writes the contents of the injested epdobase elements to an
# epdata-formatted string "strn" which can, in turn, be written to a
# file. </products>
#
# <type>
# 
# Function </type>
#
# <updates> 
# 
# - Added support for double-ampersand brackets. [110530] 
# - Added support for continguous-text blocks. [110530] </updates>
#
# <notes> </notes>
#
# ==============================================================================

def write_epdata(s, fields, field_defs, umat) :

    strn = ''

    # >> Grab fields from dictionary keys if necessary:
    
    if len(fields) == 0 : list_fields = s.keys()
    else : list_fields = fields

    array_len = num_dict_records(s)    

    # >> If there are field definitions, print them first:

    if len(field_defs) == len(fields) :
        for field in fields:
            strn += '* [' + field + '] ' + field_defs[field] + '\n'

        # >> Then add a partition:

        strn += '\n'
        for i in range(0,80,1) : strn += '-'
        strn += '\n'

    # >> Main loop for printing dictionary contents:

    for i in range(0, array_len, 1) :

        strn += '\n'

        for field in list_fields : 

            # >> Print field and its value having double-ampersand brackets
            # >> (indicated by two newline characters in a row): [110530]

            if '\n\n' in str(s[field][i]) :
                strn += '\n[' + str(field) + '] && '+str(s[field][i]) +' &&\n\n'

            # >> Print field and its value if has line continuation (i.e., a
            # >> contiguous text block, indicated any newline characters):
            # >> [110530]

            elif '\n' in str(s[field][i]) :
                strn += '\n[' + str(field) + '] ' + str(s[field][i]) + '\n\n'

            # >> Print the normal, single-line field and its value:
                
            else :
                strn += '[' + str(field) + '] ' + str(s[field][i]) + '\n'

        # >> ... an ampersand-bracket field or continuing field already got two
        # >> newline characters appended to the end:

        if '\n' not in str(s[field][i]) : strn += '\n' 

        # >> Also print unassigned matter:

        if len(umat) > 0 :
            if umat[i] != 'null' : 
                strn += umat[i]

                if umat[i][-2:] == '\n\n' : pass
                elif umat[i][-1] == '\n' : strn += '\n'
                else: strn += '\n\n'

        for i in range(0,80,1) : strn += '-'
        strn += '\n'

    return strn

    
# ==============================================================================
#
# 20100526-1826-mpuboo - Get number of records
#
# <summary>
#
# Returns length of epdobase dictionary or -1 if field lengths differ.</summary>
#
# <syntax>
# 
# array_len = num_dict_records(dictry) </syntax>
#
# <inputs>
# 
# Sole input, dictry, has the format of an epdobase dictionary (i.e., the "dcty"
# variable in an epdobase object). </inputs>
#
# <products>
# 
# Output is just an integer equal to the number of records in the dictionary
# field: i.e., the number of elements in the single list assigned to each
# dictionary key. </products>
#
# <type>
# 
# Function </type>
#
# <updates> </updates>
#
# <notes> </notes>
#
# ==============================================================================

def num_dict_records(s) :

    unequal_lengths = False
    list_fields = s.keys()  # >> Get all dictionary keys

    if len(list_fields) == 0 : array_len = 0 
    else: array_len = len(s[list_fields[0]]) # >> Number of records of 1st field

    # >> Confirm that all fields have same length (otherwise return -1)

    for field in list_fields : 
        if len(s[field]) != array_len :
             unequal_lengths = True
             print('! Warning: the epdobase columns have ' + \
                       'an unequal number of records.\n\n')
             print(field,len(s[field]))
             
    if unequal_lengths: return -1
    else: return array_len

# ==============================================================================
#
# 20100704-2216-mpuboo - Get matching records
# 
# <summary>
# 
# Returns index of any & all records matching input values for specific fields
# </summary>
#
# <syntax>
# 
# any_matched,all_matched = get_matching_records(dcty, valdict) </syntax>
#
# <inputs>
# 
# The input "dcty" is the dictionary on which the matching is performed.  The
# input "valdict" is a dictionary whose fields are the fields in "dcty" to be
# matched, whose values are the values of the records in "dcty" to be matched.
# For example, suppose "dcty" has the fields "height_in_meters" and
# "weight_in_lbs" and "color" and you wish to find all items weighing "50" lbs
# or "40" lbs that are "blue" (or that are blue). Then,
#
# : valdict = {'weight_in_lbs': [40, 50], 'color' : 'blue'} 
#
# The argument "match_type" is a string equal to "partial" (for partial
# matching: i.e., a match occurs if the sought value is contained in a record)
# or "exact" (for exact matching: i.e., a match occurs if the sought value is
# exactly matched. </inputs>
# 
# <products>
# 
# The first product "any_matched" will return the indices of all records that
# match any of the values in valdict for the keys specified in valdict.  In the
# above example, this means all items that are 40 lbs or 50 lbs or that are
# blue.  The second product "all_matched" will return all records that match at
# least one value in each key.  This will return all objects that are 40 lbs and
# blue or 50 lbs and blue, but not any objects that are not blue, and that do
# not weigh 40 lbs or 50 lbs.  </products>
#
# <type>
# 
# Function </type>
#
# <updated>
#
# - "match_type" added for partial matching ("searching") option. [100821]
#
# <dependencies>
# 
# omnigenus </dependencies>
#
# ==============================================================================

def get_matching_records(dcty, valdict, match_type) :

    from omnigenus import findall_matches
    from omnigenus import findall_partial_matches

    # >> Dictionary that will store the matching records for each key: 

    matches_per_key = {}  
    
    # >> This will store the fields that are being matched: 

    match_keys = valdict.keys()

    # >> Fill matches_per_key with empty lists for now:

    for key in match_keys : matches_per_key[key] = []

    # >> For each key...
    
    for key in match_keys :

        vals = valdict[key] # >> Store the matching values...

        # >> ... if there's only one, store it as a list...

        if not isinstance(vals,type([1,2,3])) : vals = [vals];

        # >> ... find all records under the current key in dict that match each
        # >> of the stipulated values; note also that each val is converted to a
        # >> string in case that is not already so:

        for val in vals :
            
            if match_type == "exact" : 
              matches_per_key[key] += findall_matches(dcty[key],str(val))
            elif match_type == "partial" : 
              matches_per_key[key]+=findall_partial_matches(dcty[key],str(val))
    
    # >> Now just make a list of all the records that had at least one match in
    # >> at least one key:        

    any_matched_unreduced = []        

    for key in match_keys : any_matched_unreduced += matches_per_key[key]

    # >> Now make sure there is just once mention of each record in this list:

    any_matched = []

    for item in any_matched_unreduced : 
        if item not in any_matched : any_matched += [item]

    # >> Now we turn to finding records that have at least one match in each
    # >> key.    

    all_matched = []

    for item in any_matched : 

        # >> The idea is just to count the number of keys for which each record
        # >> in any_matched had a match, and check to see if this is equal to
        # >> the total number of keys.  If it is, then the record's index is
        # >> added to all_matched.

        cnt = 0

        for key in match_keys : 
            if item in matches_per_key[key] : cnt += 1

        if cnt == len(match_keys): all_matched += [item]
    
    return any_matched, all_matched


# ==============================================================================
#
# 20100821-1803-mpuboo - Simple sorting of an Epdobase
# 
# <summary>
# 
# Sorts all records in an epdobase (all columns) according to the values in one
# column, in forward or reverse order.  </summary>
#
# <syntax>
# 
# simple_epdobase_simple(ep, field, whether_reverse) </syntax>
#
# <inputs>
# 
# Input "ep" is an Epdobase object.  Input "field" is the field name or column
# that will determine the sort order.  Final input "whether_reverse" should be
# True if the sort order is to be reverse, and False otherwise.  See Python docs
# for a discussion of the sort order for characters of different classes (e.g.,
# numeric versus alphabet characters). </inputs>
#
# <products>
# 
# The input ep has been been resorted.  </products>
#
# <type>
# 
# Function </type>
#
# <dependencies>
# 
# copy, omnigenus </dependencies>
#
# ==============================================================================

def sort_epdobase_simple(ep, field, whether_reverse) :

    from omnigenus import get_list_sort_order
    import copy

    # >> First sort the column indicated by "field", and determine the sort
    # >> order so that this can be applied to all the other fields:

    sort_order = get_list_sort_order(\
                        sorted(ep.dcty[field], reverse = whether_reverse),
                        ep.dcty[field])

    # >> Make a reference copy of the dictionary (the one we consult while
    # >> modifying the original):

    old_dcty = copy.deepcopy(ep.dcty)

    # >> Now sort all columns using the same sort-order:

    for field in ep.flds : 

        for i in range(0,len(sort_order),1) : 

            ep.dcty[field][i] = old_dcty[field][sort_order[i]]
        
# ==============================================================================
#
# 20100821-2045-mpuboo - Numerize Epdobase
# 
# <summary>
# 
# Converts all numeric strings to numeric types, stores them in "ndct"</summary>
#
# <syntax>
# 
# numerize_epdobase(ep, precision = 'double') </syntax>
#
# <inputs>
# 
# Input "ep" is an Epdobase object.  Keyword argument "precision" specifies the
# number of bits of precision, which may be 'single' (32-bit) or 'double'
# (64-bit), where 'double' precision is the default. </inputs>
#
# <products>
# 
# Input "ep" is modified so all columns in the dictionary .dcty are converted to
# numpy arrays.  Lists of pure integers are converted to numpy arrays of single
# or double precision integers.  Lists of floats and integers are converted to
# numpy arrays of single or double precision floats.  Lists of floats and
# integers and strings or floats and strings or integers and strings are
# converted to numpy arrays of strings.  Note that "null" values are not counted
# as strings, and are converted to numpy NaNs at the outset.  If the input
# epdobase ep already has a numerized version of dcty stored in ndct, then it is
# overwritten. </products>
#
# <type>
# 
# Function </type>
#
# <dependencies>
# 
# copy, numpy </dependencies>
#
# <updates>
#
# - ndict columns are now numpy arrays instead of lists [101027]
# - vectorized conversion to numpy arrays (was looping over records) [101027]
# - given empty cells (''), numerize often failed to convert numbers [150809]
# - precision is now always 64 bit; left bogus kwarg for compatibility [150810]
#
# </updates> 
#
# <notes>
#
# Unassigned matter is ignored. 
#
# Also note that since there are no integer nans, any column that has null
# values and integers will be converted to a floating point array! (with nans in
# the nulls). [150810] </notes>
#
# ==============================================================================

def numerize_epdobase(ep, precision = None):

    import copy             # >> Standard Python library
    import numpy as np      # >> Numerical Python 

    # >> Copy the string-format dictionary (dcty) into the numerized one (ndct):

    ep.ndct = copy.deepcopy(ep.dcty)
    
# -- Loop over fields ----------------------------------------------------------

    for field in ep.flds : 

        column     = ep.ndct[field]
        column_arr = np.array(column)

        # >> First replace all "nulls" with "NaN":
        # !! I already tried with ::column_arr[inds_nulls] = np.nan::
        
        flag_nulls = column_arr == 'null' 
        flag_empty = column_arr == ''

        inds_not_empty   = np.nonzero(1 - (flag_nulls + flag_empty))[0]

        if len(inds_not_empty) == len(column) : 
            no_empty_records = True
        else:
            no_empty_records = False

        column_arr_short = column_arr[inds_not_empty] 

        # >> Prior to 2010.10.27, this method looped over individual records to
        # >> determine the appropriate type conversion.  Now, all records of a
        # >> field are converted to float or integer arrays, all at once.  First
        # >> we try converting all values to ints.  If this fails, we try
        # >> converting all values to floats.  If this fails, the column is
        # >> converted to a numpy array of strings:

        try : tmp = np.int64(column_arr_short)
        except: 
            try: tmp = np.float64(column_arr_short)
            except:
                try: tmp = np.array(column_arr_short)
                except: print('Epdobase: error: numerize() choked on ndct.')
            

        if (tmp.dtype == np.array([1.,2.]).dtype or \
                tmp.dtype == np.array([1,2]).dtype) and not no_empty_records:

            # column had empty records, and the rest were numbers

            if precision == 'double': tmp = np.float64(tmp)
            elif precision == 'single': tmp = np.float32(tmp)

            column_nan = np.nan + np.zeros(column_arr.shape)
            column_nan[inds_not_empty] = tmp
            ep.ndct[field] = column_nan

        elif not no_empty_records: # column had empty records, but no numbers

            ep.ndct[field] = column_arr

        else: # column had no empty records

            ep.ndct[field] = tmp
        
# ==============================================================================
#
# 20100821-2100-mpuboo - Characterize Epdobase
# 
# <summary>
# 
# Converts the numeric dictionary (ndct) to strings, overwriting dcty </summary>
#
# <syntax>
# 
# characterize_epdobase(ep) </syntax>
#
# <inputs>
# 
# Input "ep" is an Epdobase object. </inputs>
#
# <products>
# 
# The input "ep" is modified so that dcty has been overwritten by a version of
# ndct in which all records have been converted to strings.  All numpy "nan"s in
# the ndct (the "numeric dictionary") are converted to strings with value
# "null".  </products>
#
# <type>
# 
# Function </type>
#
# <dependencies>
# 
# copy </dependencies>
#
# <updates>
#
# - vectorized conversion to strings; no longer looping over records [101027]
# </updates>
#
# <notes>
#
# Unassigned matter is ignored. </notes>
#
# ==============================================================================
 
def characterize_epdobase(ep):

    import copy
    import numpy as np

    # >> Copy the numeric dictionary (ndct) into the string dictionary (dcty) 

    ep.dcty = copy.deepcopy(ep.ndct)
    
# -- Loop over fields ----------------------------------------------------------

    for field in ep.flds : 

        # >> Function "map" applies the function supplied as the first argument
        # >> to all elements in the sequence (supplied as the second argument).
        # >> I learned this from an 

        ep.dcty[field] = map(str,ep.ndct[field])

# ==============================================================================
#
# 20100822-2100-mpuboo - Nullify Epdobase
# 
# <summary>
# 
# Converts all empty strings to "null" in dcty and umat.
#
# <syntax>
# 
# ep_out = nullify_epdobase(ep) </syntax>
#
# <inputs>
# 
# Input "ep" is an Epdobase object. </inputs>
#
# <products>
# 
# The input "ep" is modified so that all empty strings in dcty and umat have
# been replaced with "null". </products>
#
# <type>
# 
# Function </type>
#
# <dependencies>
# 
# copy </dependencies>
#
# <notes> </notes>
#
# ==============================================================================

def nullify_epdobase(ep) :

    # >> Replacing all empty strings in the dcty with "null":
    
    for field in ep.flds:
        for i in range(0,ep.len(),1) : 
            if ep.dcty[field][i].strip() == '' : ep.dcty[field][i] = "null"

    # >> Doing likewise in the unassigned matter:
    
    if len(ep.umat) != 0 :

        for i in range(0,ep.len(),1) : 
            if ep.umat[i].strip() == '' : ep.umat[i] = "null"

# ==============================================================================
#
# 20100910-1424-mpuboo - Unnullify Epdobase
# 
# <summary>
# 
# Converts all "null"s and "nans" to empty strings in dcty and umat. </summary>
#
# <syntax>
# 
# ep_out = unnullify_epdobase(ep) </syntax>
#
# <inputs>
# 
# Input "ep" is an Epdobase object. </inputs>
#
# <products>
# 
# The input "ep" is modified so that all records with "null" values in dcty are
# changed to empty strings. </products>
#
# <type>
# 
# Function </type>
#
# <dependencies>
# 
# copy </dependencies>
#
# <notes> </notes>
#
# ==============================================================================

def unnullify_epdobase(ep) :

    # >> Replacing all nulls or nans with empty strings:
    
    for field in ep.flds:
        for i in range(0,ep.len(),1) : 
            if ep.dcty[field][i].strip() == 'null' : ep.dcty[field][i] = ''
            if ep.dcty[field][i].strip() == 'nan' : ep.dcty[field][i] = ''

    # >> Doing likewise in the unassigned matter:
    
    if len(ep.umat) != 0 :

        for i in range(0,ep.len(),1) : 
            if ep.umat[i].strip() == 'null' : ep.umat[i] = ''
            if ep.umat[i].strip() == 'nan' : ep.umat[i] = ''

# ==============================================================================
#
# 20101025-1615-mpuboo - Write numeric dictionary to Epdobin-formatted string 
# 
# <summary>
# 
# Writes a numeric dictionary to an Epdobin-formatted file (binary). </summary>
#
# <syntax>
# 
# write_epdobin(ndct, fields, field_defs) </syntax>
#
# <inputs>
# 
# The argument "ndct" is a dictionary having the same format as an epdobase ndct
# variable (see {20100527-1045}). The argument "fields" is equivalent to an
# epdobase flds variable (a list of field names), and field_defs corresponds to
# the "defs" variable of an epdobase object (a list of field definitions).  Note
# that "fields" can be set to an empty string or an empty list, in which case it
# will be filled using the keys() method.  If "field_defs" is empty, then the
# fields will not be defined in the epdobin file. </inputs>
#
# <products>
# 
# This method writes the contents of the ingested epdobase elements to an
# epdata-formatted string "strn" which can, in turn, be written to a file.  
#  
# Epdobin is comprised of a text header that identifies the file as Epdobin, and
# supplies the data type of all numbers in the binary data, as well as its shape
# in rows and columns.  This information is used by parse_epdobin (see
# {20101026-1536}) to parse the binary part. An example header is shown here:
#
# : [file_type] Epdobin
# : [data_type] double
# : [nmbr_rows] 98
# : [nmbr_cols] 4
# : 
# : * x = x position
# : * y = y position
# : * z = z position
# : * c = pixel intensity
#
# Note that the order of the file-properties information is not important,
# whereas the order of field-definitions is critical: this order corresponds to
# the order of columns in the binary data.  The first line "[file_type] Epdobin"
# is used by the Epdobase "load" function to recognize the file as Epdobin.
# </products>
#
# <type>
# 
# Function </type>
#
# <dependencies>
# 
# numpy </dependencies>
#
# <notes> 
#
# At present we do not write numeric dictionary columns as distinct data types.
# For example, if one column is made up of integers and another is made up of
# floats, the whole lot will be written as floats. 
#
# Unassigned matter is ignored. </notes>
#
# ==============================================================================

def write_epdobin(ndct, fields, field_defs) : 

    import numpy as np   # >> Numerical Python

    # >> Create a column-array of the same length as ndct, filled w/zeros:

    matx = np.zeros((num_dict_records(ndct), len(fields)))  

    # >> Fill the array with the values of all records for each field:

    for i in range(0,len(fields),1) : matx[:,i] = ndct[fields[i]]

    dtype = type(matx[0,0]) # >> determine the data type of array elements

    # >> The bytes occupied by each numpy type:

    byte_sizes = {np.int64: 8, np.int32: 4, np.float64: 8, np.double: 8}

    # >> Names used to represent each nympy type:

    type_names = {np.int64: 'int64', np.int32: 'int32', np.float64: 'float64', \
                      np.double: 'double'}

    nrows = matx.shape[0]  # >> note the number of rows
    ncols = matx.shape[1]  # >> note the number of columns

    matx = matx.reshape(nrows*ncols,)  # >> reshape into one-dimensional array

    # >> Assemble the header string:
  
    hdrstring =  ''
    hdrstring += '[file_type] Epdobin\n'
    hdrstring += '[data_type] ' + type_names[dtype] + '\n'
    hdrstring += '[nmbr_rows] ' + str(nrows) + '\n'
    hdrstring += '[nmbr_cols] ' + str(ncols) + '\n\n'

    # >> Now add the definitions of all fields:

    for field in fields : 
        hdrstring += '* ' + field + ' = ' 
        if len(field_defs) > 0 : hdrstring += field_defs[field]
        hdrstring += '\n'

    outstring = matx.tostring()       # >> write the array to a strings
    totstring = hdrstring + outstring # >> combine header and data strings

    return totstring                
            
# ==============================================================================
#
# 20101026-1536-mpuboo - Parse Epdobin-formatted string into Epdobase components
# 
# <summary>
# 
# Parses a numeric dictionary from an Epdobin string. </summary>
#
# <syntax>
# 
# parse_epdobin(strn) </syntax>
#
# <inputs>
# 
# Sole argument "strn" is an Epdobin-formatted string.
# </inputs>
#
# <products>
# 
# The output is a list with three elements: a Epdobase numeric dictionary
# containing the database, a list of field-names, and a list of field
# descriptions or definitions.  This definitions list is of course empty if
# there was no field-definitions line in the Epdex file. </products>
#
# <type>
# 
# Function </type>
#
# <dependencies>
# 
# re, os, numpy </dependencies>
#
# <updates>
#
# - Applied size limit for "fields" in case regexp is matched in binary
#   data. [101112] </updates>
#
# <notes> 
#
# Unassigned matter is ignored.  A description of the Epdobin format can be
# found in {20101025-1615}. </notes>
#
# ==============================================================================

def parse_epdobin(strn) : 

    import numpy as np               # >> Numerical Python
    import re, os                    # >> Standard Python libraries

    lines = strn.splitlines()        # >> Split string at newlines to make list
 
    fields     = []                  # >> Epdobase fields will be stored here
    field_defs = {}                  # >> Epdobase definitions to be stored here

    dtype_name = 'float64'           # >> Default type assumed for parsing data

    # -- Parsing the header data -----------------------------------------------

    for line in lines :         

        format_string = '^\s*\[(.*)\](.*)' # >> reg exp for file properties
        define_string = '^\s*\* (.*)=(.*)' # >> reg exp for field definitions

        fmatch = re.search(format_string,line) # >> attempt matching property
        dmatch = re.search(define_string,line) # >> attempt matching definition

        if dmatch :   # >> populate the field definitions

            fields.append(dmatch.group(1).strip())
            field_defs[dmatch.group(1).strip()] = dmatch.group(2).strip()

        elif fmatch:  # >> populate the file properties

            if fmatch.group(1) == 'nmbr_rows' : 
                nrows = int(fmatch.group(2).strip())

            elif fmatch.group(1) == 'nmbr_cols' : 
                ncols = int(fmatch.group(2).strip())

            elif fmatch.group(1) == 'data_type' : 
                dtype_name = fmatch.group(2).strip() 

    # !! This is required in the event that the regular expression pattern for
    # !! field name definitions was matched somewhere in the binary data:

    fields = fields[0:ncols]

    # >> Look-up tables for byte-size of data types and data type labels:

    byte_sizes = {'int64': 8, 'int32': 4, 'float64': 8, 'double': 8}

    type_names = {'int64': np.int64, 'int32': np.int32, 'float64': np.float64, \
                      'double': np.double}

    # -- Parsing the binary data ---------------------------------------------- 

    bsize = nrows * ncols * byte_sizes[dtype_name] # >> total size in bytes

    # >> Ingest binary data into 1-D numpy array:

    # !! This illustrates how to do this from a file object (former method):
    # fili.seek(0 - bsize, os.SEEK_END) # >> move seek to start of binary data
    # matx = np.fromstring(fili.read(bsize), dtype = type_names[dtype_name])

    matx = np.fromstring(strn[-bsize:], dtype = type_names[dtype_name])  

    matx = matx.reshape(nrows, ncols)  # >> reshape the array 

    ndct = {}

    # >> Populate columns of the numeric dictionary:

    for i in range(0,len(fields),1) : ndct[fields[i]] = matx[:,i]

    return [ndct, fields, field_defs]  # >> return epobase components

# ==============================================================================
#
# 20110427-1844-mpuboo - Write comma-separated values (CSV) file 
#
# </summary>
#
# Writes an epdobase's elements to csv format (N.B. all arrays must be m x 1)
# </summary>
#
# <syntax>
# 
# strn = write_csv(dcty, fields, field_defs, umat, pres=) </syntax>
#
# <inputs>
# 
# The argument "dcty" is a dictionary having the same format as an epdobase dcty
# variable (see {20100527-1045}). The argument "fields" is equivalent to an
# epdobase flds variable (a list of field names), and field_defs corresponds to
# the "defs" variable of an epdobase object (a list of field definitions).  Note
# that "fields" can be set to an empty string or an empty list, in which case it
# will be filled using the keys() method.  If "field_defs" is empty, then the
# fields will not be defined in the epdata file. Finally, "pres" is a
# dictionary, formated like the defs dictionary in the epdobase class, which
# prescribes the number of zeros that should follow a decimal place for each
# quantity. </inputs>
#
# <products>
# 
# This method writes the contents of the injested epdobase elements to an
# csv-formatted string "strn" which can, in turn, be written to a
# file. </products>
#
# <type>
# 
# Function </type>
#
# <updates> </updates>
#
# <notes>
# 
# Note that all new-line characters are replaced with |NL| in the csv file,
# where each record is allowed to occupy exactly one line. </notes>
#
# ==============================================================================

def write_csv(s, fields, field_defs, umat, pres=None) :

    strn = '';

    # >> Use the given field names, or derive them from the dictionary keys if
    # >> "fields" is empty:

    if len(fields) == 0 : list_fields = s.keys()  
    else : list_fields = fields

    # >> If there is umatter, simply add this to the list of field names.

    if len(umat) != 0 : 
        list_fields.append('umat')
        s['umat'] = umat       # !! This passes the object, not the reference.

    # >> Build the field-names line, using commas as separators:

    for field in list_fields : strn += '\"' + field + '\",'

    strn = strn[0:-1]  # >> strike the last ','
    strn += '\n'

    # >> Determine the number of records, and add this many lines to the string,
    # >> printing the whole contents of the epdobase dcty.  All newline
    # >> characters are replaced with "|NL|" because all contents of each record
    # >> must lie on the same line.
    
    array_len = num_dict_records(s)  

    for i in range(0,array_len,1) :
        
        for field in list_fields : 

            orgval = s[field][i]

            # >> Print each value (if that's what it is) with the prescribed
            # >> precision: [140102]

            if pres is not None and orgval != 'nan' and orgval != 'null':
                if len(pres.keys()) != 0 :

                    if field in pres.keys():

                        try : 
                            tmpval = np.float64(orgval)

                            if np.int(pres[field]) != 0:
                                datval = '%.' + str(np.int(pres[field])) + 'f' 
                                datval = datval % tmpval
                            else:
                                datval = str(np.int64(np.round(tmpval)))

                        except: datval = orgval
                    else: datval = orgval
                else: datval = orgval
            else: datval = orgval

            strn += '\"' + datval.replace('\n','|NL|') + '\",'

        strn = strn[0:-1]  # >> strike the last ','
        strn += '\n'   
            
    return strn

# ==============================================================================
#
# 20110530-1335-mpuboo - Parse comma-separated values (CSV) file 
#
# <summary> 
#
# Parse csv format into an epdobase (N.B. all arrays will be m x 1) </summary>
#
# <syntax>
# 
# epdobase_elements = parse_csv(string) </syntax>
#
# <inputs>
# 
# The input is a string that contains the contents of a text file, where each
# line is separated by a newline character.  This can be read from a file object
# using the read() method. </inputs>
#
# <products>
# 
# The output is a list with four elements: a dictionary containing the database,
# a list of field-names, a list of field descriptions or definitions, and a list
# of unassigned matter.  This definitions list is of course empty if there was
# no field-definitions line in the Epdex file. The unassigned matter is likewise
# empty if there was no unassigned matter in the document. </products>
#
# <type>
# 
# Function </type>
#
# <dependencies>
# 
# None </dependencies>
#
# <updates> 
#
# - Fixed a bug that was cutting off last digit. [120808] 
# - Added pound-sign commenting. [150809] </updates>
#
# <notes> </notes>
#
# ==============================================================================

def parse_csv(strn) :

    fili = strn.splitlines() # >> Splits string into list of strings at newlines

    field_line = 0  # >> Keeps track of whether we are reading the field-line

    s = {}          # >> This dictionary will store the database
    field_defs ={}  # >> We'll return field definitions as equal to field names

    # >> Keeps track of whether the file has unassigned matter:

    has_umatter = False 

    # >> Unassigned matter (if any) is stored in this list:

    umat = []

# -- Main loop over lines in file ----------------------------------------------

    field_line = 1 # >> First line of the file indicates field names

    for tline in fili : 

        # >> Skip lines that begin with a pound sign:
        if tline[0] == '#' : continue
        
        sline = tline.strip() # >> Remove leading and trailing whitespace

        # >> Populate the database :

        if field_line == 0 :
            strs = csv_line_splitter(sline) # >> Split at commas not in quotes

            for field in field_list : 
                
                stmp = strs[field_list.index(field)].strip()

                # >> Replace newline characters:

                s[field].append(stmp.replace('|NL|','\n'))                 

        # >> Populate the list of fields : 

        if field_line == 1 :

            field_line = 0
            field_list_tmp = csv_line_splitter(sline)

            field_list = []

            # >> Eliminate whitespace from field names, initialize the
            # >> dictionary that will hold the database:

            for strn in field_list_tmp : 

                # >> First determine whether the field refers to unassigned
                # >> matter:

                if strn.strip() == 'umat' or strn.strip() == 'Umat' \
                                   or strn.strip() == 'UMAT':

                   has_umatter = True
                   umat_key = strn.strip()

                if len(strn.strip()) > 0 : 

                    field_list.append(strn.strip())
                    s[strn.strip()] = []
                    field_defs[strn.strip()] = strn.strip()
            
    # >> Now, separate the unassigned matter, if any, into the "umat" list:

    if has_umatter :

        umat = s[umat_key]

        del s[umat_key]
        del field_defs[umat_key]
        field_list.remove(umat_key)

    # >> Finally, if there are no field definitions, return these as an empty
    # >> dictionary:

    total_def_len = 0

    for field in field_list: total_def_len += len(field_defs[field])
    if total_def_len == 0 : field_defs = {}
    
    return [s, field_list, field_defs, umat]

# ..............................................................................

# >> This simple function parses a line of CSV by scanning
# >> character-by-character for quotation marks and commas:

def csv_line_splitter(line) :
    
    in_quotes = False
    strn = ''
    field_vals = []

    for i in range(0,len(line),1) :
        
        if line[i] == '\"' : in_quotes = True - in_quotes

        # !! Before 120808, this line read... [120808]
        # !! :: elif (line[i] == ',' or line[i] == '\n' or i == len(line)-1)

        elif (line[i] == ',' or line[i] == '\n' or i == len(line)) \
                and not in_quotes : 

            field_vals.append(strn)
            strn = ''

        else: strn += line[i]

    field_vals.append(strn) # >> don't fail to keep the last field value       

    return field_vals
            
# ==============================================================================
#
# 20120106-1229-mpuboo - Write epdobase as a Latex table            
#
# </summary>
#
# Writes an epdobase's elements to a latex table (N.B. all arrays must be m x 1)
# </summary>
#
# <syntax>
# 
# strn = write_latex(dcty, fields, field_defs, umat, justify_char=, caption=,
# pres=) </syntax>
#
# <inputs>
# 
# The argument "dcty" is a dictionary having the same format as an epdobase dcty
# variable (see {20100527-1045}). The argument "fields" is equivalent to an
# epdobase flds variable (a list of field names), and field_defs corresponds to
# the "defs" variable of an epdobase object (a list of field definitions).  Note
# that "fields" can be set to an empty string or an empty list, in which case it
# will be filled using the keys() method.  If "field_defs" is empty, then the
# fields will not be defined in the epdata file. 
#
# Kwarg arguments are justify_char (text justification is l = left (default), r
# = right, c = center), and caption (table caption).  
#
# See {20110427-1844} for the definition of the "pres" variable.
#</inputs>
#
# <products>
# 
# This method writes the contents of the injested epdobase elements to a string
# containing a latex-formatted table. </products>
#
# <type>
# 
# Function </type>
#
# <updates> </updates>
#
# <notes>
# 
# Note that all new-line characters are replaced with a space in the latex
# table, where each record is allowed to occupy exactly one line. 
#
# Also note that, as with all write functions in the epdobase library, simply
# pass an empty list ("[]") to the umat argument if you don't wish
# unassignmatter to appear in the output.  </notes>
#
# ==============================================================================

def write_latex(s, fields, field_defs, umat, justify_char = 'l',
                caption = 'Epdobase table', pres=None) :

    strn = '';
    
    # Write the document preamble text

    strn += '\\documentclass[11pt]{article}\n'
    strn += '\\usepackage{fullpage}\n'
    strn += '\\usepackage[dvips]{graphicx}\n'
    strn += '\\begin{document}\n\n'
    
    # >> Write the preamble text
    
    strn += '\\begin{table}\n'
    strn += '\\begin{center}\n'
    strn += '\\caption{' + caption + '}'
    strn += '\\vspace{3mm}\n'

    # >> Use the given field names, or derive them from the dictionary keys if
    # >> "fields" is empty:

    if len(fields) == 0 : list_fields = s.keys()  
    else : list_fields = fields

    # >> If there is umatter, simply add this to the list of field names.

    if len(umat) != 0 : 
        list_fields.append('notes')
        s['notes'] = umat       # !! This passes the object, not the reference.

    # >> Write the string that determines how text is justified:

    justify_string = '\\begin{tabular}{'

    for i in range(0,len(list_fields),1) : 
        justify_string += justify_char
        
    justify_string += '}\n'

    strn += justify_string

    # >> Build the column names line, using &s as separators:

    for field in list_fields : strn += field + ' & '

    strn = strn[0:-2]  # >> strike the last '&'
    strn += ' \\\\\n\hline\n'

    # >> Determine the number of records, and add this many lines to the string,
    # >> printing the whole contents of the epdobase dcty.  All newline
    # >> characters are replaced with " " because all contents of each record
    # >> must lie on the same line.
    
    array_len = num_dict_records(s)  

    for i in range(0,array_len,1) :

        for field in list_fields : 

            orgval = s[field][i]

            # >> Print each value (if that's what it is) with the prescribed
            # >> precision: [140102]

            if pres is not None and orgval != 'nan' and orgval != 'null':
                if len(pres.keys()) != 0 :

                    if field in pres.keys() :
                        try : 
                            tmpval = np.float64(orgval)
                            
                            if np.int(pres[field]) != 0:
                                datval = '%.' + str(np.int(pres[field])) + 'f' 
                                datval = datval % tmpval
                            else:
                                datval = str(np.int64(np.round(tmpval)))

                        except: datval = orgval
                    else: datval = orgval
                else: datval = orgval
            else: datval = orgval

            strn += datval.replace('\n',' ') + ' & '

        strn = strn[0:-2]  # >> strike the last '&'
        strn += '\\\\\n'   

    # >> Closing the table environment:

    strn += '\hline\n'
    strn += '\end{tabular}\n'
    strn += '\end{center}\n'
    strn += '\end{table}\n\n'

    strn += '\end{document}\n'
    
            
    return strn


