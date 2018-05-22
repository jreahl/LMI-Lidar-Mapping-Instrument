# ==============================================================================
#
# 20091120-1532-gpuboo - omnigenus.py
# General Python Utilities / Wesley Andres Watters Farfan
# A medley of handy python utilities for a wide range of applications.
#
# <type>
# 
# Module </type>
#
# <package>
# 
# Omnigenus </package>
#
# <language>
# 
# Python 2.54 </language>
#
# <dependencies>
# 
# Python modules: sys </dependencies>
#
# <notes>
#
# Always use "from omnigenus import function", since the location of these 
# utilities may change in the future. </notes>
#
# ==============================================================================

import sys

# >> This method does not merit a header.  It prints w/out EOL carriage return:
   
def prynt(string) :
    sys.stdout.write(string)

# ------------------------------------------------------------------------------
#
# 20100204-1753-mpuboo - Numeric menu
# 
# <summary>
#
# Accepts a list of strings as menu options; displays this & prompts user.
# </summary>
#
# <syntax>
# 
# sel = numeric_menu(menu_title, menu_prompt, menu_options) </syntax>
#
# <inputs>
# 
# Strings "menu_title", "menu_prompt" are the menu title and prompt, 
# respectively (surprise!).  The argument "menu_options" is a list of strings 
# that are the menu options. </inputs>
#
# <products>
# 
# The output "sel" is an integer that the user selected, indicating the 
# choice menu_options[sel-1]. That is, the user is shown a numbered list of the
# items in "menu_options" and prompted to select one, where this selection is 
# returned in "sel". </products>
#
# <type>
# 
# Function </type>
#
# <updates>
#
# 2010.06.22 </updates>
#
# ------------------------------------------------------------------------------

def numeric_menu(menu_title, menu_prompt, menu_options) :

    prynt('\n' + menu_title + '\n\n')  # >> Prints the menu title.

    # >> Prints the menu items:

    for i in range(0,len(menu_options),1):
                
        if len(menu_options) < 10 :        
           prynt('['+ str(i+1) + '] '+ menu_options[i] + '\n')
        elif len(menu_options) >=10 :
           prynt('[' + str(i+1).zfill(2) + '] '+ menu_options[i] + '\n')
            
    # >> Prompts the user for a selection: 

    prynt('\n');

    sel = raw_input(menu_prompt + ' : ')

    # >> If the input is not an integer, or exceeds the number of menu options,
    # >> then return "0".
    
    try: 
        isel = int(sel)
    except : 
        isel = 0

    if isel > len(menu_options) : return 0
    else : return isel

    
# ------------------------------------------------------------------------------
#
# 20100404-1047-mpuboo - Create current date-time-stamp
#
# <summary>
# 
# Creates a date and time-stamp with the broken or long formats. </summary>
#
# <syntax>
# 
# datetimestamp = make_datetime_stamp(whether_broken) </syntax>
#
# <inputs>
#
# Argument whether_broken is a boolean set to "True" if the date and time 
# should be "broken".  That is, written as 2010.04.04+10.47 instead of 
# 20100404+1047. </inputs>
#
# <products>
#
# The date-timestamp is output, composed of current date and time. </products>
# 
# <dependencies>
# 
# time </dependencies>
#
# <notes>
#
# For definitions of the long and broken formats, see {20100123-1918/datedef}.
# </notes>
#
# ------------------------------------------------------------------------------
    
def make_datetime_stamp(whether_broken) :

    import time

    # >> Query and parse the current date and time: 
    
    x = time.localtime()

    if whether_broken :
    
        cdate = str(x.tm_year) + '.' + str(x.tm_mon).zfill(2) + \
            '.' + str(x.tm_mday).zfill(2)
        ctime = str(x.tm_hour).zfill(2) + '.' + str(x.tm_min).zfill(2)
                
    else :

        cdate = str(x.tm_year) + str(x.tm_mon).zfill(2) + \
            str(x.tm_mday).zfill(2)
        ctime = str(x.tm_hour).zfill(2) + str(x.tm_min).zfill(2)

 
    
    datetimestamp = cdate + '+' + ctime  # >> Creates the current datetimestamp

    return datetimestamp    
    
    
# ------------------------------------------------------------------------------
#
# 20100531-1157-mpuboo - Find all matching elements of a list
#
# <summary>
# 
# Given a list and a value, finds indices of all elements that match. </summary>
#
# <syntax>
# 
# matching_values = findall_matches(alist, match_val) </syntax>
#
# <inputs>
#
# Inputs are list "alist" and the value to be matched "match_val".  </inputs>
#
# <products>
#
# The output is the list of indices of all elements that match exactly.
# </products>
# 
# <notes> 
#
# See findall_partial_matches() below, {20100821-2321}, for a means of finding
# all elements that partially match. 
#
# Note that this function is superseded by the "nonzero()" function in numerical
# python and should not be used.  </notes>
#
# ------------------------------------------------------------------------------

def findall_matches(alist, match_val) :
    import numpy as np
    inds = np.nonzero(np.array(alist)==match_val)[0]
    return list(inds)


# def findall_matches(alist, match_val) :
    
#     all_matches = []

#     blist = alist[:]

#     num_matches = alist.count(match_val) # >> Count the number of matches
    
#     for i in range(0,num_matches,1) :

#         # !! .index() returns the first instance; therefore, as we encounter
#         # !! first instances, we replace them with -99999999 and move on until
#         # !! the indices of all matches are added to "all_matches". 

#         ind = blist.index(match_val)
#         all_matches.append(ind)
#         blist[ind] = -99999999

#     return all_matches


# ------------------------------------------------------------------------------
#
# 20100615-6890-gpuboo - Set equal aspect ratio for 3D axes
#
# <summary>
#
# Computes 3D axes ranges so that these, when applied, makes aspect ratio equal.
# </summary>
#
# <syntax>
#
# xlims_exp,ylims_exp,zlims_exp = make_equal_3daxes(xlims,ylims,zlims)
# </syntax>
#
# <inputs>
#
# The tree input arguments are obtained from the axes object (e.g., "ax") as
# follows:
#
# ::
# xlims  = ax.get_xlim3d()  
# ylims  = ax.get_ylim3d()  
# zlims  = ax.get_zlim3d()  </inputs>
# ::
#
# </inputs>
#
# <products>
#
# Outputs are the corrected range for equal aspect ratio display.  These limits
# must be supplied to "set_xlim3d", etc, as follows:
# 
# ::
# ax.set_xlim3d(xlims_exp)
# ax.set_ylim3d(ylims_exp)        
# ax.set_zlim3d(zlims_exp)
# ::
#
# </products>
#
# <type>
#
# Function </type>
#
# <notes>
#
# This method was moved here from {20100615-1528} on 2013.02.02. </notes>
#
# ------------------------------------------------------------------------------

# !! Akin to "axis equal" in Matlab, but *not* the same, since the space
# !! occupied by each axis is *also* equal, and you still need to plug the new
# !! bounds into axis3D.set_xlim(), etc.

def make_equal_3daxes(xlims, ylims, zlims) : 

        hf_rngx = (max(xlims) - min(xlims))/2;
        hf_rngy = (max(ylims) - min(ylims))/2;
        hf_rngz = (max(zlims) - min(zlims))/2;  

        max_hf_rng = max([hf_rngz, hf_rngy, hf_rngx])

        xlim_eq = [ (xlims[0] + hf_rngx - max_hf_rng), \
                         (xlims[0] + hf_rngx + max_hf_rng) ]

        ylim_eq = [ (ylims[0] + hf_rngy - max_hf_rng), \
                         (ylims[0] + hf_rngy + max_hf_rng) ]

        zlim_eq = [ (zlims[0] + hf_rngz - max_hf_rng), \
                         (zlims[0] + hf_rngz + max_hf_rng) ]

        return xlim_eq, ylim_eq, zlim_eq

# ==============================================================================
#
# 20100821-1702-mpuboo - Sort order from list comparison
# 
# <summary>
# 
# Compares two lists to obtain a sort order, which can be applied to others. 
# </summary>
#
# <syntax>
# 
# sort_order = get_list_sort_order(list_sorted, list_original) </syntax>
#
# <inputs>
# 
# First input (list_sorted) is the version of list_original (2nd argument) whose
# sort order is sought. </inputs>
#
# <products>
# 
# Output "sort_order" are the indexes of list_original in the order required to
# produce list_sorted. </products>
#
# <type>
# 
# Function </type>
#
# <notes>
#
# Please note that this method has been superseded by the "argsort()" method in
# numerical python, and should no longer be used. </notes>
#
# ==============================================================================

def get_list_sort_order(list_sorted, list_original) :

    i = 0

    sort_order = []

    # >> Loop over all items in the sorted list:

    for item in list_sorted : 

        # >> Find all matching elements of the original list that match the
        # >> current item of the sorted list:

        all_matches = findall_matches(list_original, item)    

        # >> Count the number of instances of the current item in the sorted
        # >> list that we have already passed:

        num_already_passed = list_sorted[:i].count(item)

        # >> The number already passed is the index of the matched index from
        # >> the sorted list:

        sort_order.append(all_matches[num_already_passed])
        i += 1

    return sort_order

# ------------------------------------------------------------------------------
#
# 20100821-2321-mpuboo - Find all partially matching elements
#
# <summary>
# 
# Given a list and a value, finds indices of elements that contain the value. 
# </summary>
#
# <syntax>
# 
# matching_values = findall_partial_matches(alist, match_val) </syntax>
#
# <inputs>
#
# Inputs are list "alist" and the value to be matched "match_val". </inputs>
#
# <products>
#
# The output is the list of indices of all elements that match partially: i.e.,
# that contain the match_val.  For example, suppose alist = ['hello','hell no']
# and match_val = 'hell'.  Since 'hell' occurs in both elements, the result
# should be matching_values should equal [0, 1]. </products>
#
# ------------------------------------------------------------------------------

def findall_partial_matches(alist, match_val) :
    
    all_matches = []

    for i in range(0,len(alist),1) : 
        if match_val in alist[i] : all_matches.append(i)

    return all_matches

# ------------------------------------------------------------------------------
#
# 20100907-0843-mpuboo - Unpickle a pickled object           
#
# <summary>
# 
# Given a filename that contains a pickled object, this method unpickles it.  
# </summary>
#
# <syntax>
# 
# unpickled_object = unpickle(filename)                                
#
# <inputs>
#
# Sole input is the filename of the file containing the pickled object.</inputs>
#
# <products>
#
# Output is the unpickled object stored in "filename." </products> ially: i.e.,
#
# <dependencies>
#
# pickle </dependencies>
#
# <notes>
#
# A method that simplifies matters ever so slightly. </notes>
#
# ------------------------------------------------------------------------------

def unpickle(filename) : 

    import pickle

    fili = open(filename,'r')  # >> Open file for reading
    obj = pickle.load(fili)    # >> Unpickle 
    fili.close()               # >> Close the open file (object fails otherwise)

    return obj

# ------------------------------------------------------------------------------
#
# 20100907-2048-mpuboo - Initialize Matplotlib display by showing plots w/logo
#
# <summary>
# 
# Opens a figure window so that future plotting commands refresh instantly.
# </summary>
#
# <syntax>
# 
# init_pylab_display() </syntax>
#
# <products>
#
# Without showing a figure window first (which the user must close), Pylab plot
# functions of all kinds will not instantly draw their output.  This method
# provides a convenient way to initialize the display.  </products>
#
# <dependencies>
#
# pylab </dependencies>
#
# <notes>
#
# I fully expect this function to become obsolete in the future, once I (or
# pylab) sort out a sensible way to deal with this annoying problem. </notes>
#
# ------------------------------------------------------------------------------


def init_pylab_display() :

    import pylab as pl

    pl.figure(973,figsize=(3,3))  # >> Create a small figure
    pl.plot([0],[0])            # >> Initialize plot

    # >> Write text to the figure:

    pl.text(-0.055,0.02,'Golemics',fontsize=36)
    pl.text(-0.052,0.006,'DEI EX MACHINIS',fontsize=17)

    pl.text(-0.055,-0.055,\
             'This window initializes the\nMatplotlib drawing functions.\n' + \
             'Please close it to continue.\n\n'
             'All Golemics programs\nare licensed under\nGNU Public License 3.0'
             ,fontsize=10)

    # >> Hide the axes:

    frame1 = pl.gca()
    frame1.axes.get_xaxis().set_visible(False)
    frame1.axes.get_yaxis().set_visible(False)

    # >> Show the figure (prompting the user to close it)

    pl.show()


# ==============================================================================
#
# 20110121-2246-mpuboo - Parse Epdoml date-time string      
#
# <summary>
# 
# Parses a date-time string written using any one of the Epdoml formats.   
# </summary>
#
# <syntax>
# 
# (t_epoch, t_strct, t_strng, dt) = parse_date(date_string) </syntax>
#
# <inputs>
#
# Sole input is a string (date_string) containing the date and or time in an
# Epdoml date-time format, all of which are defined in the body of the code.
# </inputs>
#
# <products>
#
# Returns a tuple consisting of seconds since the epoch (t_epoch), a Python time
# struct (t_strct), a string containing date and time in traditional format, and
# the number of seconds that must be added to t_epoch for UTC if t_epoch refers
# to the current time-zone. </products>
#
# <dependencies>
#
# omnigenus, time, re </dependencies>
#
# <notes> </notes>
#
# ==============================================================================

def parse_date(date_strn) : 

    import time, re  # >> Standard Python libraries

    inis = []

    # -- Patterns for all Epdoml date-time formats -----------------------------

    # >> 90121 (unpadded short (5 digits))
    inis.append({'mtch':'(\d{1})(\d{2})(\d{2})',
                 'flds':['yr','mo','dy']})

    # >> 110121 (padded short (6 digits))
    inis.append({'mtch':'(\d{2})(\d{2})(\d{2})',
                 'flds':['yr','mo','dy']})

    # >> 20110121 (long date)
    inis.append({'mtch':'(\d{4})(\d{2})(\d{2})',
                 'flds':['yr','mo','dy']})

    # >> 2011.01.21 (broken date)
    inis.append({'mtch':'(\d{4})\.(\d{2})\.(\d{2})',
                 'flds':['yr','mo','dy']})

    # >> 20110121-1419 (EDI)
    inis.append({'mtch':'(\d{4})(\d{2})(\d{2})-(\d{2})(\d{2})',
                 'flds':['yr','mo','dy','hr','mn']})

    # >> 201101211419 (unbroken date-time)
    inis.append({'mtch':'(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})',
                 'flds':['yr','mo','dy','hr','mn']})

    # >> 2011.01.21+14.19 (broken date-time)
    inis.append({'mtch':'(\d{4})\.(\d{2})\.(\d{2})\+(\d{2})\.(\d{2})',
                 'flds':['yr','mo','dy','hr','mn']})

    # >> 20110121+1419 (long date-time)
    inis.append({'mtch':'(\d{4})(\d{2})(\d{2})\+(\d{2})(\d{2})',
                 'flds':['yr','mo','dy','hr','mn']})

    # --------------------------------------------------------------------------
    # -- Main loop for matching regular-expressions & extracting date/time info
    # --------------------------------------------------------------------------

    dvals = {} # >> this will 

    for ini in inis : 
        imat = re.search(ini['mtch'],date_strn)

        # >> Loop over all matching strings.  When a match occurs, extract the
        # >> date/time components from corresponding matched groups:

        if imat : 
            for fld in ini['flds'] :
                dvals[fld] = \
                    int(imat.group(ini['flds'].index(fld)+1))

            # >> If the year is less than 1000, assume this is a match to one of
            # >> the short date-time formats, and add 2000 years (since these
            # >> are only used for years peceding 2000):
                
            if dvals['yr'] < 1000 : dvals['yr'] += 2000

            # >> If no time is specified, set this to midnight:

            if 'hr' not in dvals : dvals['hr'] = 0
            if 'mn' not in dvals : dvals['mn'] = 0

    # >> Form the date-time tuple:

    timetup = (dvals['yr'],dvals['mo'],dvals['dy'],\
                   dvals['hr'],dvals['mn'],0,999,999,-1)

    # >> Translate to time since epoch for local time.  Although not returned,
    # >> the time in UTC is noted in comments:

    t_epoch_loc = time.mktime(timetup)
    # t_epoch_utc = time.timezone + t_epoch_loc

    t_strct_loc = time.localtime(t_epoch_loc)
    # t_strct_utc = time.gmtime(t_epoch_utc)

    t_strng = time.strftime("%a, %d %b %Y %H:%M:%S",t_strct_loc)

    return (t_epoch_loc,t_strct_loc, t_strng, 0-time.timezone)
           

