# ==============================================================================
#
# 20100403-1411-gpuboo - filum.py
# Filum string methods / Wesley Andres Watters Farfan
# A wide range of useful methods for operating on strings
#
# <type>
# 
# Module </type>
#
# <package>
# 
# Filum Omnigenus </package>
#
# <language>
# 
# Python 2.54 </language>
#
# <dependencies>
# 
# </dependencies>
#
# <updates>
# 
# </updates>
#
# <notes>
# 
# </notes>
#
# ==============================================================================

import re

# ------------------------------------------------------------------------------
#
# 20091114-3832-mpuboo - Remove nonalphanumeric characters from a string
#
# <summary>
# 
# Removes all characters that aren't alphanumeric and replaces with a space.
# </summary>
#
# <syntax>
# 
# out_string = remove_nonalphanumeric(string) </syntax>
#
# <dependencies>
# 
# re </dependencies>
#
# -----------------------------------------------------------------------------

def remove_nonalphanumeric(string) :
    
    # >> re.sub performs a substitution, here, a white-space is substituted.
    # >> The regular expression "[^A-Za-z0-9]" means "match all characters that
    # >> are not (^) alphanumeric: i.e., not A-Z, a-z, or 0-9.
    
    string_out = re.sub(r'[^A-Za-z0-9]',' ',string)
    return string_out

# ------------------------------------------------------------------------------
#
# 20091114-3117-mpuboo - Remove leading and trailing whitespaces
#
# <summary>
# 
# Removes all whitespace characters from beginning and end of string. </summary>
#
# <syntax>
# 
# out_string = remove_bounding_whitespaces(string) </syntax>
#
# <dependencies>
# 
# re </dependencies>
#
# -----------------------------------------------------------------------------

def remove_bounding_whitespaces(string) :

    # >> re.sub performs a substitution, in this case a no-space is substituted.
    # >> '^\s*' means: match all whitespaces (\s*) at the beginning (^) of the
    # >> string.
    
    string_tmp = re.sub(r'^\s*','', string, re.M)

    # >> re.sub performs a substitution, in this case a no-space is substituted.
    # >> '\s*$' means: match all whitespaces (\s*) at the end ($) of string.

    string_out = re.sub(r'\s*$','', string_tmp)
    return string_out
    
# ------------------------------------------------------------------------------
#
# 20091117-2106-mpuboo - Non-alphanumeric and bounding whitespace removal
#
# <summary>
# 
# Removes comment characters and bounding whitespaces. </summary>
#
# <syntax>
# 
# out_string = clean_string(string) </syntax>
#
# <dependencies>
# 
# re </dependencies>
#
# ------------------------------------------------------------------------------
 
def clean_string(string) :

    tmp0 = re.sub(r'[#%]','',string)
    tmp1 = re.sub(r'//','',tmp0)
    string_out = remove_bounding_whitespaces(tmp1)
    return string_out

# ------------------------------------------------------------------------------
#
# 20100403-1419-mpuboo - Escape special characters for matching
#
# <summary>
# 
# Escapes special characters so that string can be matched using re. </summary>
#
# <syntax>
# 
# out_string = fix_str_for_match(string) </syntax>
#
# <dependencies>
# 
# re </dependencies>
#
# 
# ------------------------------------------------------------------------------

def fix_str_for_match(string) :

    new_string = re.sub('\+','\\+',string)      # >> Escape the plus signs
    new_string = re.sub('\^','\\^',new_string)  # >> Escape the carets
    new_string = re.sub('\.','\\.',new_string)  # >> Escape the periods
    new_string = re.sub('\[','\\[',new_string)
    new_string = re.sub('\]','\\]',new_string)
    new_string = re.sub('\?','\\?',new_string)
    new_string = re.sub('\*','\\*',new_string)
    new_string = re.sub('\$','\\$',new_string)
    new_string = re.sub('\(','\\(',new_string)
    new_string = re.sub('\)','\\)',new_string)
    new_string = re.sub('\|','\\|',new_string)
    new_string = re.sub('\{','\\{',new_string)
    new_string = re.sub('\}','\\}',new_string)
    
# !! Currently, we cannot escape "\": i.e., this line triggers an exception:
# !! new_string = re.sub('\\','\\\\',new_string); perhaps try this:
# !! new_string = new_string.replace('\','\\')
        
    return new_string
