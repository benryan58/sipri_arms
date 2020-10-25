
from io import StringIO
import json
import pandas as pd
import requests
from .parameters import ENTITIES, ARM_CATEGORIES, FILETYPES
from .parameters import SUMMARIZE_BY, YEARS, PARAMETERS

class arms_db(object):

    entities = ENTITIES
    arm_categories = ARM_CATEGORIES
    summarize_by = SUMMARIZE_BY
    years = YEARS

    def __init__(self, conn=None, endpoint="registers", **kwargs):
        '''
        Initialize SIPRI Arms Transfer Database query object. 

        Inputs:
        * conn (str): https://armstrade.sipri.org/armstrade/html/
        * endpoint (str): One of "tiv" or "registers"
        * **kwargs (dict): optionally specify query parameters at 
        initialization; defaults vary based on the endpoint specified

        Output:
        * sipri_arms() object
        '''

        self._endpoint = ""

        if len(kwargs) > 0:
            self.params = self.set_params(kwargs)
        else:
            self.params = {}

        if conn is None:
            conn = "https://armstrade.sipri.org/armstrade/html/"

        self.conn = conn
        self.endpoint = endpoint
        self.params = self.get_params()

    def __str__(self):
        rep = "Target: {}\n".format(self.query_string)
        params = ["{}: {}".format(k, v) for k, v in self.params.items()][:-1]
        rep += "Params: {" + "\n         ".join(params)

        return rep

    def __repr__(self):
        return str(self)

    @property
    def endpoint(self):
        return self._endpoint

    @endpoint.setter
    def endpoint(self, newendpt):
        if newendpt == 'registers':
            self.query_string = self.conn + "export_trade_register.php"
        elif newendpt == "tiv":
            self.query_string = self.conn + "export_values.php"
        else:
            print("Invalid endpoint specified; defaulting to "
                  "`...export_trade_register.php`")
            self.query_string = self.conn + "export_trade_register.php"
            newendpt = "registers"

        if self._endpoint != newendpt:
            self._endpoint = newendpt
            old_params = {k: v for k, v in self.params.items()
                          if k in PARAMETERS[newendpt]}
            self.params = PARAMETERS[newendpt]
            self.params.update(old_params)

    @endpoint.deleter
    def endpoint(self):
        del self._endpoint
    
    def get_params(self):
        if len(self.params) > 0:
            return self.params
        else:
            return PARAMETERS[self.endpoint]

    def query(self, **kwargs):
        '''
        Execute query against SIPRI Arms database endpoint. If any `kwargs` 
        are supplied, update the stored query parameters first with these

        Return a `str` representation of the content, unless the filetype 
        specified was one of `['csv','json']`. In that case, return either
        a Pandas `DataFrame` or a `dict`, respectively.
        '''
        if len(kwargs) > 0:
            self.params.update(kwargs)

        if self.params['filetype'] == 'json':
            self.params['filetype'] = 'csv'
            JSON = True
        else:
            JSON = False

        r = requests.post(self.query_string, data=self.params)
        r = r.content.decode()

        if self.params['filetype'] == 'csv':
            kw = {}

            if self.endpoint == 'tiv':
                # the TIV endpoint CSV returns some additional rows at the top
                # and bottom that don't parse well into DataFrames, and 
                # the 
                r = "\n".join(r.content.decode().split("\n")[10:-3])
                kw.update({'index_col': 0})

            r = pd.read_csv(StringIO(r), **kw)

            if JSON:
                self.params['filetype'] = 'json'

                if self.endpoint == 'registers':
                    r.set_index('tidn', inplace=True)

                r = r.to_dict('index')

                for key in r:
                    r[key] = {k: v for k, v in r[key].items() 
                              if pd.notnull(v) and v != ''}

        return r

    def update(self, **kwargs):
        '''
        Change the query parameters specified by `kwargs`
        '''
        self.params.update(kwargs)
        return None






