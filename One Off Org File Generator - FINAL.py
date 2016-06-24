
# coding: utf-8

# In[59]:

# Import modules into namespace
import pandas as pd
import numpy as np


# In[66]:

# Read xlsx doc
filepath = r'C:\Users\brandon.terrebonne\Desktop\organization_gen\albertsons_dsd_spend_20160624.xlsx'
df = pd.read_excel(filepath)


# In[67]:

# Add missing columns, which will now have null values
choice_company_id = raw_input('company_id = ')
if choice_company_id == "":
    choice_company_id = "company_id"
choice_company_name = raw_input('company_name = ')
if choice_company_name == "":
    choice_company_name = "company_name"
choice_address_1 = raw_input('address_1 = ')
if choice_address_1 == "":
    choice_address_1 = "address_1"
choice_address_2 = raw_input('address_2 = ')
if choice_address_2 == "":
    choice_address_2 = "address_2"
choice_city = raw_input('city = ')
if choice_city == "":
    choice_city = "city"
choice_state = raw_input('state = ')
if choice_state == "":
    choice_state = "state"
choice_postal_code = raw_input('postal_code = ')
if choice_postal_code == "":
    choice_postal_code = "postal_code"
choice_country = raw_input('country = ')
if choice_country == "":
    choice_country = "country"
choice_tax_id = raw_input('tax_id = ')
if choice_tax_id == "":
    choice_tax_id = "tax_id"
choice_reserve_percentage = raw_input('reserve_percentage = ')
if choice_reserve_percentage == "":
    choice_reserve_percentage = "reserve_percentage"
choice_reserve_amount = raw_input('reserve_amount = ')
if choice_reserve_amount == "":
    choice_reserve_amount = "reserve_amount"
choice_reserve_invoice_priority = raw_input('reserve_invoice_priority = ')
if choice_reserve_invoice_priority == "":
    choice_reserve_invoice_priority = "reserve_invoice_priority"
choice_reserve_before_adjustments = raw_input('reserve_before_adjustments = ')
if choice_reserve_before_adjustments == "":
    choice_reserve_before_adjustments = "reserve_before_adjustments"

df2 = pd.DataFrame(df,columns=[choice_company_id, choice_company_name, choice_address_1, choice_address_2,
                               choice_city, choice_state, choice_postal_code, choice_country,
                               choice_tax_id, choice_reserve_percentage, choice_reserve_amount, 
                               choice_reserve_invoice_priority, choice_reserve_before_adjustments])
# Rename columns
old_names = [choice_company_id, choice_company_name, choice_address_1, choice_address_2,
            choice_city, choice_state, choice_postal_code, choice_country,
            choice_tax_id, choice_reserve_percentage, choice_reserve_amount, 
            choice_reserve_invoice_priority, choice_reserve_before_adjustments]
new_names = ['company_id','company_name','address_1','address_2',
            'city', 'state', 'postal_code','country','tax_id','reserve_percentage',
            'reserve_amount','reserve_invoice_priority','reserve_before_adjustments']

df2.rename(columns=dict(zip(old_names, new_names)), inplace=True)


# In[69]:

#This works in resolving issue #2 on Github
def check_type(x):
    p = x.split('.')
    try:
        if x == 'nan':
            y = np.nan
        elif float(x) / float(p[0]) > 1.0:
                y = x
        else:
            y = p[0]
    except ValueError:
        y = x
    return y

df2['company_id'] = df2['company_id'].astype(str)
df2['company_id'] = df2['company_id'].map(check_type)


# TODO - check if this is needed, which it probably is not
# Strip leading/trailing spaces
def strip(text):
    try:
        return text.strip()
    except AttributeError:
        return text

df2['company_id'] = strip(df2['company_id'])


# In[70]:

### Cleaning reserves###
def filling(column):
    new_column = []
    for item in column:
        if item == '22222222222222222222':
            item = np.nan
            new_column.append(item)
        else:
            item = float(item)
            item = ("{0:.2f}".format(round(item,2)))
            new_column.append(item)
    return new_column

df2['reserve_amount'] = df2['reserve_amount'].fillna(value=22222222222222222222)
df2['reserve_amount'] = df2['reserve_amount'].astype(str)
df2['reserve_amount'] = filling(df2['reserve_amount'])
df2.fillna(value="", inplace=True)


# In[71]:

### Add leading zeros ###

def leading(x, y):
    new_id = []
    field_length = int(y)
    for item in x:
        try:
            leng = field_length - len(str(item))
            if len(str(item)) < 1:
                new_id.append(item)
            elif len(str(item)) < field_length:
                item2 = str("00000000000000000000")
                item3 = ""
                item3 = str(item2[0:leng]) + str(item)
                new_id.append(item3)
            else:
                new_id.append(item)
        except:
            new_id.append(item)
    return new_id

# User input 1
choice_company_id_leading = raw_input('If company_id has leading zeros, input the field length (otherwise just hit enter): ')

if choice_company_id_leading != "":
    df2['company_id'] = leading(df2['company_id'], choice_company_id_leading)
else:
    df2['company_id'] = df2['company_id']

# New DF if user does not require reserve info
df3 = pd.DataFrame(df2, columns=['company_id','company_name','address_1','address_2',
            'city', 'state', 'postal_code','country','tax_id'])

# User input 2, Save data to CSV
while True:
    choice_reserve = raw_input('So let\'s talk about this... Do you REALLY want to include reserve information in this file (Yes or No):')
    if choice_reserve.lower() == 'yes':
        df2.to_csv(r'C:\Users\brandon.terrebonne\Desktop\organization_gen\test_organization_4_20160624.csv', sep=',', index=False, encoding='utf-8')
        print "\nYour file includes reserve information and is now ready!\nDisclaimer: This file will override current supplier-level reserves!!!"
        break
    if choice_reserve.lower() == 'no':
        df3.to_csv(r'C:\Users\brandon.terrebonne\Desktop\organization_gen\test_organization_4_20160624.csv', sep=',', index=False, encoding='utf-8')
        print "\nYour file excludes reserve information and is now ready!"
        break
    else:
        print "\nOh goodness... \'%s\' is not a valid response. Please answer with either \'Yes\' or \'No\'." % (choice_reserve)
        continue

