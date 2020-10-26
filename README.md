# Unofficial SIPRI Arms Transfers Database API wrapper
To reiterate, I am not in any way affiliated with the Stockholm International Peace Research Institute, I have just created a Python wrapper for their <a href="https://www.sipri.org/databases/armstransfers">Arms Transfers Database</a> web interface for my own (and ideally others') convenience. 

For any and all questions about the form or content of the data, please refer to SIPRI's <a href="https://www.sipri.org/databases/armstransfers/sources-and-methods">website</a>.

_It should go without saying but please don't abuse this tool in downloading the data very generously gathered and provided by SIPRI. All download requests are ultimately served by SIPRI web resources._ 

## Usage
### Setup
To set this facility up locally, clone this repo and adjust your `PYTHONPATH` to point to wherever you saved it. I have a `git` folder where I keep all my projects locally that is part of that path, so I can refer to any project as if it's its own module, but whatever works for you. 

To download data, simply import the API connection class:

```python
from sipri_arms.api import arms_db
```

### Define a query
Once imported, you can instantiate it very simply with default query parameters.

```python
conn = arms_db()
conn
# Target: https://armstrade.sipri.org/armstrade/html/export_trade_register.php
# Params: {low_year: 1950
#          high_year: 2020
#          seller_country_code: 
#          buyer_country_code: 
#          armament_category_id: any
#          buyers_or_sellers: sellers
#          filetype: csv
#          include_open_deals: on
#          sum_deliveries: 
```

This will by default grab all the data, so if your interests are more specific it's best to update the query parameters as such:
```python
conn.update(low_year=2016, seller_country_code='USA')
conn
# Target: https://armstrade.sipri.org/armstrade/html/export_trade_register.php
# Params: {low_year: 2016
#          high_year: 2020
#          seller_country_code: USA
#          buyer_country_code: 
#          armament_category_id: any
#          buyers_or_sellers: sellers
#          filetype: csv
#          include_open_deals: on
#          sum_deliveries: 
```

### Get the data
Getting the data is then as easy as running the `query()` function. You can optionally specify new parameters any time you run the query. These new settings will remain after running, too. 
```python
result = conn.query()
#       tidn buyercod sellercod  odat  ... status  tivunit tivorder  tivdel
# 0    61421      AFG       USA  2017  ...      N     0.30    16.50   16.50
# 1    60475      AFG       USA  2018  ...      N     0.90     7.20    7.20
# 2    63355      AFG       USA  2019  ...      S     7.20     0.00    0.00
# 3    60033      AFG       USA  2016  ...      N     0.14   234.22  234.22
# 4    60334      AFG       USA  2016  ...      N     0.14    60.62   60.62
# ..     ...      ...       ...   ...  ...    ...      ...      ...     ...
# 928  60396       VN       USA  2016  ...      S    54.00    54.00   54.00
# 929  63183       VN       USA  2019  ...      S    54.00    54.00    0.00
# 930  62530      XSX       USA  2017  ...      N     0.15     0.30    0.30
# 931  60701      XSX       USA  2016  ...      N     0.14     0.70    0.70
# 932  59146      ZAM       USA  2015  ...      N     1.50     6.00    6.00

# [933 rows x 22 columns]

result = conn.query(high_year=2017)
#       tidn buyercod sellercod  odat  ... status  tivunit tivorder  tivdel
# 0    60033      AFG       USA  2016  ...      N     0.14   234.22  234.22
# 1    60334      AFG       USA  2016  ...      N     0.14    60.62   60.62
# 2    61299      AFG       USA  2017  ...      N     0.14   920.64    0.00
# 3    59482      AFG       USA  2015  ...      N     0.70     8.40    8.40
# 4    61920      AFG       USA  2017  ...      N     0.02     5.00    1.00
# ..     ...      ...       ...   ...  ...    ...      ...      ...     ...
# 602  39073       UK       USA  2006  ...      N     0.80    44.80   22.40
# 603  59302      UKR       USA  2015  ...      S     1.20     7.20    4.80
# 604  60396       VN       USA  2016  ...      S    54.00    54.00   54.00
# 605  62530      XSX       USA  2017  ...      N     0.15     0.30    0.30
# 606  60701      XSX       USA  2016  ...      N     0.14     0.70    0.70

# [607 rows x 22 columns]
```

There are actually two potential endpoints for queries, one for the "Trade Registers" with detailed arms trade listings, and one for "trend-indicator value" (TIV) listings. The latter summarizes arms transfers by value. By default, the endpoint is set to the former ("registers") but can be updated to the latter very easily:
```python
conn.endpoint = "tiv"
conn
# Target: https://armstrade.sipri.org/armstrade/html/export_values.php
# Params: {low_year: 2016
#          high_year: 2017
#          country_code: 
#          import_or_export: import
#          filetype: csv
#          summarize: country
```
Note: some query parameters are common to both endpoints, and any common ones will be retained when switching endpoints. 

Additionally, there are multiple formats in which the data may be returned. By default, this is set to CSV and data will be returned as a Pandas `DataFrame` object. Optionally, this can be changed to any of `['rtf','html','json']` as well. Setting `conn.params(filetype='json')` will return a `dict` object, and the other two options will simply pass a `str` representation which can be written to a file or handled in some other way as desired. 
