
from validate_email import validate_email

from datetime import timedelta

import datetime
import re

#-----------------------------------------------------------------
def is_alpha_only(value):
      """
      Si l'entrée est une chaine (alpahabetique uniquement)
      """
      return re.match(r'[a-zA-Z]', value)

#-----------------------------------------------------------------
def is_number_only(value):
      """
      Validaiton si l'entrée en nombre uniquement
      """
      return re.match("^[0-9 -]+$", value)

#-----------------------------------------------------------------
def is_alphanumeric_only(value):
      """
      Validaiton si l'entrée en alpha-numérique
      """
      return re.match(r'[a-zA-Z0-9_]', value)

#-----------------------------------------------------------------
def is_phone_valid(value):
      """
      Validation du numero de telephone
      """
      phonePattern = re.compile(r'''
            # don't match beginning of string, number can start anywhere
            (\d{3})     # area code is 3 digits (e.g. '800')
            \D*         # optional separator isvalidate-email any number of non-digits
            (\d{3})     # trunk is 3 digits (e.g. '555')
            \D*         # optional separator
            (\d{4})     # rest of number is 4 digits (e.g. '1212')
            \D*         # optional separator
            (\d*)       # extension is optional and can be any number of digits
            $           # end of string
            ''', re.VERBOSE)

      return phonePattern.search(value)

#-----------------------------------------------------------------
def is_email_valid(value):
      """
      Renvoyer si mail est valide
      Pip validate-email 1.3 (A installer dans le projet)
      """
      return validate_email(value)

#-----------------------------------------------------------------
def is_date_valid(value):
      """
      Teste si la date donnée est valide
      """
      isValidDate = True

      if value is None:
            isValidDate = False
      else:
            try :
                  d = '/'.join(str(x) for x in (value.day, value.month, value.year))
                  day,month,year = d.split('/')
                  datetime.datetime(int(year),int(month),int(day))
            except ValueError :
                  isValidDate = False

      return isValidDate

#-----------------------------------------------------------------
def isNullOrEmpty(value):
    if value and value.strip():
        return False
    return True

#-----------------------------------------------------------------
def is_date_fr_valid(value):
      """
      Teste la validité d'une date fr au format d/m/y
      """
      isValidDate = True
      try :
            day,month,year = value.split('/')
            datetime.datetime(int(year),int(month),int(day))
      except ValueError :
            isValidDate = False

      return isValidDate

#-----------------------------------------------------------------
def date_picker_to_date_string(d_picker, option=False):
      """
      Transform a datetime to a simple date
      @d_picker : datepicker de jquery
      @option : True, on ajoute une journée 
      """
      if is_date_fr_valid(d_picker):
            dfr = d_picker.split('/')
            if option:
                  # ajouter une journée
                  dnew = datetime.datetime(int(dfr[2]), int(dfr[1]), int(dfr[0]), 0, 0) + timedelta(days=1)
                  dnew = '/'.join(str(x) for x in (dnew.day, dnew.month, dnew.year))
                  dfr = dnew.split('/')
                  dfr = dfr[2]+'-'+dfr[1]+'-'+dfr[0] 
                  return dfr
            else:
                  dfr = dfr[2]+'-'+dfr[1]+'-'+dfr[0]
                  return dfr

      return None