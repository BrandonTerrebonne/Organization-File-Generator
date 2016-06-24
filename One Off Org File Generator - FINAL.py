
# coding: utf-8

# In[2]:

# Import modules into namespace
import pandas as pd
import numpy as np
import datetime

print "Imports Complete. We'll start by reading the file."


# In[3]:

# Read xlsx doc
filepath = r'C:\Users\brandon.terrebonne\Desktop\\Albertsons_WHSpend_Purchase_by_week_2015_dsd.xlsx'
df = pd.read_excel(filepath)

slash = filepath.rfind('\\')
filename = filepath[slash+1:]

print "'%s' is now loaded.\n\nNext, we'll map the data..." % (filename)


# In[4]:

# Add missing columns, which will now have null values
print "Match the following ESLAP feilds with the original file's feild names:\n"
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
    
print "\nColumns are now mapped.\n\nRunning the next cell will rename the columns and prep the data for export."


# In[5]:

# Rename columns
old_names = [choice_company_id, choice_company_name, choice_address_1, choice_address_2,
            choice_city, choice_state, choice_postal_code, choice_country,
            choice_tax_id, choice_reserve_percentage, choice_reserve_amount, 
            choice_reserve_invoice_priority, choice_reserve_before_adjustments]
new_names = ['company_id','company_name','address_1','address_2',
            'city', 'state', 'postal_code','country','tax_id','reserve_percentage',
            'reserve_amount','reserve_invoice_priority','reserve_before_adjustments']

df2.rename(columns=dict(zip(old_names, new_names)), inplace=True)

# DF NAME CHANGE
df3 = df2

### Cleaning company_id ###

# Strip leading/trailing spaces
def strip(text):
    try:
        return text.strip()
    except AttributeError:
        return text

df3['company_id'] = strip(df3['company_id'])

# Replace NaN with blanks, maintain preexisting float
def check_type(x):
    p = x.split('.')
    try:
        if x == '11111111111111111111':
            y = np.nan
        elif float(x) / float(p[0]) > 1.0:
                y = x
        else:
            y = p[0]
    except ValueError:
        y = x
    return y

df3['company_id'] = df3['company_id'].fillna(11111111111111111111)
df3['company_id'] = df3['company_id'].astype(str)
df3['company_id'] = df3['company_id'].map(check_type)
df3['company_id'] = df3['company_id'].replace('11111111111111111111', '')

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

df3['reserve_amount'] = df3['reserve_amount'].fillna(value=22222222222222222222)
df3['reserve_amount'] = df3['reserve_amount'].astype(str)
df3['reserve_amount'] = filling(df3['reserve_amount'])
df3.fillna(value="", inplace=True)

# PRINT
print "Columns renamed and data prepped!\n\nFinally, we'll take care of leading zeros..."


# In[6]:

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

# DF NAME CHANGE
df4 = df3

if choice_company_id_leading != "":
    df4['company_id'] = leading(df4['company_id'], choice_company_id_leading)
else:
    df4['company_id'] = df4['company_id']

# New DF if user does not require reserve info
df5 = pd.DataFrame(df4, columns=['company_id','company_name','address_1','address_2',
            'city', 'state', 'postal_code','country','tax_id'])

# User input 2, Save data to CSV
while True:
    choice_reserve = raw_input('So let\'s talk about this... Do you REALLY want to include reserve information in this file (Yes or No):')
    if choice_reserve.lower() == 'yes':
        df4.to_csv(r'C:\Users\brandon.terrebonne\Desktop\test_organization_1_20160624.csv', sep=',', index=False, encoding='utf-8')
        print "\nYour file includes reserve information and is now ready!\nDisclaimer: This file will override current supplier-level reserves!!!"
        break
    if choice_reserve.lower() == 'no':
        df5.to_csv(r'C:\Users\brandon.terrebonne\Desktop\test_organization_1_20160624.csv', sep=',', index=False, encoding='utf-8')
        print "\nYour file excludes reserve information and is now ready!"
        break
    else:
        print "\nOh goodness... \'%s\' is not a valid response. Please answer with either \'Yes\' or \'No\'." % (choice_reserve)
        continue


# In[8]:

# def clean_text(row):
#     return [r.decode('unicode_escape').encode('ascii', 'ignore') for r in row]

# df5['company_name'] = df5.apply(clean_text)

#This clears out mandarin characters, but also clears out the characters we don't want... without this, we get both
df5['company_name'] = df5.company_name.str.replace('[^\x00-\x7F]','')


# In[ ]:

df5[(df5['company_id'] == 'M101SN026752')]


# In[9]:

df5.to_csv(r'C:\Users\brandon.terrebonne\Desktop\test_organisation_5_20160623.csv', sep=',', index=False, encoding='utf-8')


# In[ ]:

#### Appendix ####

# Leading zero question: Validation Rules and Exceptions 
while True:
    choice_company_id_leading = raw_input('If company_id has leading zeros, input the field length as an integer (otherwise just hit enter): ')
    if choice_company_id_leading == "":
         break
    elif isinstance(choice_company_id_leading, ( int, long ) ):
        break
        choice_company_id_leading = int(raw_input('If company_id has leading zeros, input the field length (otherwise just hit enter): '))
    else:
        print "Yeah, that answer's not gonna work. Let's try again..."
        continue


# In[ ]:

# Rename columns
old_names = [choice_company_id, choice_company_name, choice_address_1, choice_address_2,
            choice_city, choice_state, choice_postal_code, choice_country,
            choice_tax_id, choice_reserve_percentage, choice_reserve_amount, 
            choice_reserve_invoice_priority, choice_reserve_before_adjustments]
new_names = ['company_id','company_name','address_1','address_2',
            'city', 'state', 'postal_code','country','tax_id','reserve_percentage',
            'reserve_amount','reserve_invoice_priority','reserve_before_adjustments']

df2.rename(columns=dict(zip(old_names, new_names)), inplace=True)

# DF NAME CHANGE
df3 = df2

# Strip leading spaces from company_id
def strip(text):
    try:
        return text.strip()
    except AttributeError:
        return text

df3['company_id'] = strip(df3['company_id'])


#df3['reserve_amount'] = df3['reserve_amount'].fillna(value=22222222222222222222)
#df3['reserve_amount'] = df3['reserve_amount'].astype(str)

def filling(column,x):
    new_column = []
    for item in column:
        if item == '22222222222222222222':
            item = np.nan
            new_column.append(item)
        else:
            item = float(item)
            item = ("{0:.xf}".format(round(item, 2)))
            new_column.append(item)
    return new_column



df3['reserve_percentage'] = df3['reserve_percentage'].fillna(value=22222222222222222222)
df3['reserve_percentage'] = df3['reserve_percentage'].astype(str)
df3['reserve_percentage'] = filling(df3['reserve_percentage'], 0)
#df3['reserve_amount'] = df3['reserve_amount'].astype(str)
#df3['reserve_amount'] = df3['reserve_amount'].replace('22222222222222222222','')
df3.fillna(value="", inplace=True)

df3['reserve_percentage']


# In[ ]:

df3.to_csv(r'C:\Users\brandon.terrebonne\Desktop\test_org1.csv', sep=',', index=False, encoding='utf-8')


# In[ ]:

item = 9.55
item = ("{0:.2f}".format(round(item,0)))
print item


# In[ ]:

item2 = ("{0:.0f}".format(round(2.675, 2)))
print item2

