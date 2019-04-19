

###### Imports ######

from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd
import sys
import csv
import glob
import os
from pandas import ExcelWriter
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

#######  Webscraping  ########

# global variables
domain    = "https://reports.########.com"
checkListURI = "/hq/restaurants/########/reports/checks"
startDate = "01-01-2014"
endDate   = "01-31-2019"

## Using Selenium grab the check listing page contents
# from selenium import webdriver
driver = webdriver.Chrome()

checkListUrl = domain + checkListURI +"?startDate=" + startDate + "&endDate=" + endDate

print("Loading check lists from: " + checkListUrl)
    
# Get the page from the server
driver.get(checkListUrl)
time.sleep(30)

# login if necessary
try:
    print("Logging in")
    username = driver.find_element_by_name('email')
    password = driver.find_element_by_name('password')
    username.send_keys('#######')
    password.send_keys('########')
    driver.find_element_by_name("commit").click()
    time.sleep(4)
except NoSuchElementException:
    print("Already Logged in")
    
time.sleep(240)


## select all the rows of the check table in the check page listing
# using selenium select all the day rows from the check listing table
checkrows=driver.find_elements_by_css_selector("tr.day")

nrows = len(checkrows)
print("day rows = " + str(nrows))


# Loop over day rows and expand out each day, to expose the check rows
for x in range(nrows):
    driver.execute_script("document.getElementsByClassName('day')[" + str(x) + "].click()")
    time.sleep(.5)
    
#Select the table body rows that represent checks
html=BeautifulSoup(driver.page_source,'html.parser')
time.sleep(1)
#grab the table body
table = html.find("table", { "data-test-id" : "checks-list" })
tbody = table.tbody
    
checkrows = tbody.findAll("tr", class_="check")

print(len(checkrows))


# loop over the check rows and display the url
listofchecks=[]
for row in checkrows:
    tdList = row.findAll('td')
    url = domain+tdList[1].a['href']
    listofchecks.append(url)
    
#save list to txt file
with open('S_list_2018_2j.txt','w') as filehandle:
    for item in listofchecks:
        filehandle.write('%s\n' % item)
        
#load list from txt file
list2015=[]
with open('S_list_2018_2j.txt','r') as filehandle:
    for line in filehandle:
        currentplace=line[:-1]
        list2015.append(currentplace)
        
        
it_0=""
Price=""
Quantity=""
Subtotal=""
Total_Tax=""
Gross=""
Course=""
Ordered=""
VC=""
VC_Total=""
VC_Reason=""
VC_Note=""
divs = ""
d=""
l=""
Check_Number=""
Check_Type=""
Name=""
Server=""
Seated=""
Guests=""
Status=""
Tax=""
girlhasnoname = ""
cash_payment = ""
credit_payment = ""
cash_tip = ""
credit_tip = ""
chk_ex_tax=""
tax=""
check_total=""

check_recs = []


count=0
try:
    for check in list2015:
        try:
            driver.get(check)
        except:
            print("check error")
            pass
        time.sleep(3)
        html=BeautifulSoup(driver.page_source,'html.parser')
        count=count+1
        print(str(count)+" of "+str(len(checkrows))+" checks processed...")

        divs = html.find("div", {"id": "checks-attributes"})
        d    = divs.find("ul",{"class":"property-list left"})

        # check information list
        check_info_list = d.findAll("span",{"class":"li-data"})

        # make sure list is not None
        if check_info_list != None:
            # get the list length
            checkinfolilstlen = len(check_info_list)
            #check number
            if checkinfolilstlen > 0 and check_info_list[0] != None:
                Check_Number = check_info_list[0].getText()
            else:
                Check_Number = ""
            #check type
            if checkinfolilstlen > 1 and check_info_list[1] != None:
                Check_Type = check_info_list[1].getText()
            else:
                Check_Type = ""
            #check name
            if checkinfolilstlen > 2 and check_info_list[2] != None:
                Name = check_info_list[2].getText()
            else:
                Name = ""
            #check server
            if check_info_list[3] != None:
                Server = check_info_list[3].getText()
            else:
                Server = ""
            #seated
            if check_info_list[4] != None:
                Seated = check_info_list[4].getText()
            else:
                Seated = ""
            #Guests
            if check_info_list[5] != None:
                Guests = check_info_list[5].getText()
            else:
                Guests = ""
            #status
            if check_info_list[6] != None:
                Status = check_info_list[6].getText()
            else:
                Status= ""
            #Tax
            if check_info_list[7] != None:
                Tax = check_info_list[7].getText()
            else:
                Tax= ""

    ##########################
        # check totals
        checkTotalsBlock = html.find("div", {"id":"check-totals"})

        if checkTotalsBlock != None:
            # check totals
            totalSpan = checkTotalsBlock.find("span", {"data-test-id", "total"})
            if totalSpan != None:
                check_total = totalSpan.getText
            else:
                check_total = ""
            # ex check
            ExtotalSpan = checkTotalsBlock.find("span", {"data-test-id", "total-excl-tax"})
            if totalSpan != None:
                 chk_ex_tax = ExtotalSpan.getText()
            else:
                 chk_ex_tax =  ""
            # tax
            RXtotalSpan = checkTotalsBlock.find("span", {"data-test-id", "total-tax"})
            if totalSpan != None:
                tax = TXtotalSpan.getText()
            else:
                tax = ""

            # data elements without a data-test-id
            data_tiles = checkTotalsBlock.findAll("span",{"class":"tile-data"})

            if data_tiles != None:
                data_tile_len = len(data_tiles)

                if data_tile_len > 7 and data_tiles[7] != None:
                    cash_payment = data_tiles[7].getText()
                else:
                    cash_payment = ""
                if data_tile_len > 8 and data_tiles[8] != None:
                    credit_payment = data_tiles[8].getText()
                else:
                    credit_payment = ""
                if data_tile_len > 9 and data_tiles[9] != None:
                    credit_tip  = data_tiles[9].getText()
                else:
                    credit_tip  = ""

     ################


        try:
            check_items_table = html.find("table", { "class" : "table data-table sortable" })
        except:
            pass
        try:
            check_item_list=check_items_table.findAll("tr")
        except:
            pass
        

        for check_item_row in check_item_list:
            check_item_fields = check_item_row.findAll('td')

            if check_item_fields != None:
                # get check_item_fields len
                check_item_fields_len = len(check_item_fields)
                # item number
                if check_item_fields_len > 0 and check_item_fields[0] != None:
                    it_0 = check_item_fields[0].getText()
                else:
                    it_0 = ""
                # price
                if check_item_fields_len > 1 and check_item_fields[1] != None:
                    Price = check_item_fields[1].getText()
                else:
                    Price = ""
                # quantity
                if check_item_fields_len > 2 and check_item_fields[2] != None:
                    Quantity= check_item_fields[2].getText()
                else:
                    Quantity = ""
                # subtotal
                if check_item_fields_len > 3 and check_item_fields[3] != None:
                    Subtotal= check_item_fields[3].getText()
                else:
                    Subtotal = ""
                # Total Tax
                if check_item_fields_len > 4 and check_item_fields[4] != None:
                    Total_Tax = check_item_fields[4].getText()
                else:
                    Total_Tax = ""            
                # Gross
                if check_item_fields_len > 5 and check_item_fields[5] != None:
                    Gross= check_item_fields[5].getText()
                else:
                    Gross = ""            
                # Course
                if check_item_fields_len > 6 and check_item_fields[6] != None:
                    Course = check_item_fields[6].getText()
                else:
                    Course = ""
                # Ordered
                if check_item_fields_len > 7 and check_item_fields[7] != None:
                    Ordered = check_item_fields[7].getText()
                else:
                    Ordered = ""
                # VC
                if check_item_fields_len > 8 and check_item_fields[8] != None:
                    VC = check_item_fields[8].getText()
                else:
                    VC = ""            
                # Ordered
                if check_item_fields_len > 9 and check_item_fields[9] != None:
                    VC_Total = check_item_fields[9].getText()
                else:
                    VC_Total = ""            
                # Ordered
                if check_item_fields_len > 10 and check_item_fields[10] != None:
                    VC_Reason = check_item_fields[10].getText()
                else:
                    VC_Reason = ""            
                # Ordered
                if check_item_fields_len > 11 and check_item_fields[11] != None:
                    VC_Note= check_item_fields[11].getText()
                else:
                    VC_Note = ""

            check_recs.append({"Item":it_0, "Price":Price,"Quantity":Quantity,"Subtotal":Subtotal, 
                       "Item Tax":Total_Tax,"Gross":Gross,"Course":Course,
                       "Ordered": Ordered,"VC":VC,"VC_Total":VC_Total,"VC_Reason":VC_Reason,
                      "VC_Note":VC_Note,"Check_Number":Check_Number,"Check_Type":Check_Type,
                       "Name":Name,"Server":Server,"Seated":Seated,"Guests":Guests,
                       "Status":Status,"Tax Type":Tax,"Total(minus Tax)":chk_ex_tax,"check_total":check_total,
                       "credit_tip":credit_tip,"cash_tip":cash_tip,"cash_payment":cash_payment,
                       "credit_payment":credit_payment,"tax":tax})
except:
    print("Error with url: "+ check)
    pass

    
check_recs=pd.DataFrame(check_recs)

check_recs["Item"] = check_recs["Item"].str.replace("\n", "")


writer = pd.ExcelWriter('##########.xlsx')
check_recs.to_excel(writer,'Sheet1')
writer.save()



####### Data Wrangling  ########

data1a = pd.read_excel('##########.xlsx')




#####Replace any 0 values in quantity with 1
data1a=data1a.dropna(subset=['Subtotal','Item'], how='all')
data1a.Quantity.replace(np.NaN, 1, inplace=True)
#print("Sum of Items:  "+ str(data1a.Quantity.sum()))

#convert Quantity feature from float to integer
data1a.Quantity=data1a.Quantity.astype(int)


#strip $ and ,; convert type to float
data1a['Price'] = data1a['Price'].str.replace(',', '')
data1a['Price'] = data1a['Price'].str.replace('$', '')
data1a['Price'] = data1a['Price'].astype(float)
data1a['Subtotal'] = data1a['Subtotal'].str.replace('$', '')
data1a['Subtotal'] = data1a['Subtotal'].str.replace(',', '')
data1a['Subtotal'] = data1a['Subtotal'].astype(float)

#Make Unique Identifier based off check date and number
data1a['UI'] =data1a['Seated'].astype(str)+'_'+data1a['Check_Number'].astype(str)


# for each row append guests, items, & subtotals in new columns;  subtotals is at the item level 
i_t=[]
s_t=[]
for i,r in data1a.iterrows():
    i_t.append(data1a.loc[data1a['UI'] == r.UI, 'Quantity'].sum())
    s_t.append(data1a.loc[data1a['UI'] == r.UI, 'Subtotal'].sum())
    
#append lists as columns to data frames
data1a['CkT_Item']=i_t
data1a['CkT_Sbt']=s_t

#only drop rows with null values in  Subtotal and Item - 
#this will ensure only the rows with NAsubtotals and items are dropped
data1a=data1a.dropna(subset=['Subtotal','Item'], how='all')

#Replacenull items(which will have an associated price with "Misc Charge")
data1a['Item']=data1a['Item'].fillna('Misc_Charge')

## Create average price 
# drop duplicate rows based on the unique identifier
temp_df=data1a.drop_duplicates(['UI'], keep='last')
temp_df = temp_df[(temp_df['CkT_Sbt']>0) & (temp_df['Guests']>0)]
avg_iorder=temp_df['CkT_Item'].suam()/temp_df['Guests'].sum()
print(avg_iorder)


##Go through primary data and apply avg_iorder where guests are 0

for i, r in data1a.iterrows():
#If guests count equals 0
    if r.Guests:
        if r.Guests==0:
#If subtotal and quantity checks total  equal 0, divide items by avg_iorder
            if r.CkT_Sbt:
                if r.CkT_Sbt != 0 and r.CkT_Item != 0:
                    data1a.set_value(i, 'Guests', np.rint(r.CkT_Item/avg_iorder))

data1a.Guests.replace(0, 1, inplace=True)


#clone rows based on Quantity
data1a=pd.DataFrame(data1a.values.repeat(data1a.Quantity, axis=0), columns=data1a.columns)

#update quantity to reflect totals
data1a.Quantity = np.where(data1a.Quantity > 1, 1, data1a.Quantity)

print("Sum of Items after cloning rows based on quantity:  "+ str(data1a.Quantity.sum()))


#drop rows where the item is null
data1a=data1a[data1a.Item != np.nan]
data1a=data1a[data1a.Item.notnull()]

#replace null course values with "Misc"
data1a["Course"].replace(np.nan,"Misc",inplace=True)
#replace 0 guest entries with 1(which are a apart of checks with charges)
data1a['Guests'].replace(0, 1 ,inplace=True)

#date/time formatting
data1a['Seated'] = pd.to_datetime(data1a['Seated'])
data1a['Day of the Week']= pd.to_datetime(data1a['Seated']).dt.date
data1a['Day of the Week']= pd.to_datetime(data1a['Day of the Week']).dt.dayofweek
data1a['Day']= data1a['Day of the Week']
data1a['Day'].replace(0, "Mon" ,inplace=True)
data1a['Day'].replace(1,"Tues" ,inplace=True)
data1a['Day'].replace(2, "Wed" ,inplace=True)
data1a['Day'].replace(3, "Thu" ,inplace=True)
data1a['Day'].replace(4, "Fri" ,inplace=True)
data1a['Day'].replace(5, "Sat" ,inplace=True)
data1a['Day'].replace(6, "Sun" ,inplace=True)

#Create Year and Month ColumnsColumn
data1a["Year"]=data1a['Seated'].dt.year
data1a["Month"]=data1a['Seated'].dt.month

table = data1a.pivot_table(values=['Price'], columns=['Year','Month'],  aggfunc=np.sum)
print(table)


###Correct Course Names
course_list=["1st Course","2nd Course","3rd Course","4th Course","5th Course","Amuse","Last Course"]

data1a["Course"].replace(course_list,"Food",inplace=True)


##Correct Check Names for Mobile Orders
sms_list=[
"Seamless",
"Seamless Togo",
"Seamless/1",
"Seamless/2",
"Seamless/3",
"Seamless/4",
"Seamless/take Away"
"To Go Seamless",
"To Go-seamless", "Seamless 1"
"To-Go",
"To Go",
"To Go- Cierra",
"To Go- Brett",
"Adam- To Go",
"Deborah To Go",
"To Go- Adam",
"To Go 1",
"Togo",
"22 To Go/1",
"To Go For Kristen",
"To Go Logan",
"To Go-Dean",
"To Go- Logan",
"To Go - Crystal",
"To Go- Sally",
"Logan To Go 2034703418",
"To Go Roberto",
"Noel- To Go"]

gh_list=[
"Grub",
"Grub Hub",
"Grub Hub To Go",
"Grub Hub-to Go",
"Grubhub",
"Grubhub 2",
"Grubhub 2816271/1",
"Grubhub/1",
"Grubhub/2",
"Grubhub2",
"Grubhub3",
"Grubhubb",
"Grub Hub 4",
"Grub Hub 3",
"Grub Hub 2",
"Grub Hub 1",
"Grub Hub",
"Grub Hub 5",
"Grub Hub- 3",
"Grub Hub- 2",
"Grub Hub -1",
"Grub-Hub 6",
"Grub-Hub 5",
"Grub-Hub 4",
"Grub-Hub 3",
"Grub-hub 2",
"Grub-Hub",
"Grub Hub Sales",
"Grub",
"Grub",
"Grub Hub",
"Grub Hub To Go",
"Grub Hub-to Go",
"Grubhub",
"Grubhub 2",
"Grubhub 2816271/1",
"Grubhub/1",
"Grubhub/2",
"Grubhub2",
"Grubhub3",
"Grubhubb",
"To Go Grub Hub",
"Grub Hub 4",
"Grub Hub 3",
"Grub Hub 2",
"Grub Hub 1",
"Grub Hub",
"Grub Hub 5",
"Grub Hub- 3",
"Grub Hub- 2",
"Grub Hub -1",
"Grub-Hub 6",
"Grub-Hub 5",
"Grub-Hub 4",
"Grub-Hub 3",
"Grub-hub 2",
"Grub-Hub",
"Grub Hub Sales",
"Grub",
"Grub Hub 6",
"Grub Hb 5",
"Grub Hub 9",
"Grub Hub 8",
"Grub Hub 7",
]


pm_list=[ 
"Post Mates",
"Postmates",
"Postmates To Go"]
data1a["Name"].replace(sms_list,"Seamless",inplace=True)
data1a["Name"].replace(gh_list,"Grubhub",inplace=True)
data1a["Name"].replace(pm_list,"Postmates",inplace=True)



## Correct Check Type Categories

incorrect_checktypes=[
"Seamless",
"Grubhub",
"Postmates"
"104 To Go",
"Bar To Go",
"Caviar - To Go",
"Caviar To - Go",
"Caviar To Fo",
"Caviar To Go",
"Caviar To Go 2 ",
"Caviar To Go!",
"Caviar To-go",
"Caviar Togo",
"Gita To Go",
"Grub",
"Grub Hub",
"Grub Hub To Go",
"Grub Hub-to Go",
"Grubhub",
"Grubhub 2",
"Grubhub 2816271/1",
"Grubhub/1",
"Grubhub/2",
"Grubhub2",
"Grubhub3",
"Grubhubb",
"Grub Hub 4",
"Grub Hub 3",
"Grub Hub 2",
"Grub Hub 1",
"Grub Hub",
"Grub Hub 5",
"Grub Hub- 3",
"Grub Hub- 2",
"Grub Hub -1",
"Grub-Hub 6",
"Grub-Hub 5",
"Grub-Hub 4",
"Grub-Hub 3",
"Grub-hub 2",
"Grub-Hub",
"Grub Hub Sales",
"Grub",
"To-Go",
"To Go",
"Marcia Togo",
"To Go- Brett",
"Adam- To Go",
"22 To Go/1",
"To Go For Kristen",
"To Go Logan",
"To Go-Dean",
"To Go- Logan",
"To Go - Crystal",
"To Go- Sally",
"Logan To Go 2034703418",
"To Go Roberto",
"Noel- To Go",
"Jesse To Go",
"Lauren To Go",
"Post Mates",
"Postmates",
"Postmates To Go",
"Relay To Go",
"Seamless",
"Seamless Togo",
"Seamless/1",
"Seamless/2",
"Seamless/3",
"Seamless/4",
"Seamless/take Away",
"Take Away",
"Take Out",
"Take Out Window",
"To",
"To G",
"To Go",
"To Go - Jesse",
"To Go - Julie",
"To Go 101",
"To Go 3",
"To Go Caviar",
"To Go Grub Hub",
"To Go POST MATES",
"To Go Puto!",
"To Go Seamless",
"To Go Window",
"To Go-seamless",
"To Go....",
"To-go #1759 CAVIAR",
"Togo",
"Togo At Bar",
"Togo Caviar",
"Togooo",
"To-Go",
"To Go",
"To Go- Cierra",
"To Go- Brett",
"Adam- To Go",
"Deborah To Go",
"To Go- Adam",
"To Go 1",
"Togo",
"22 To Go/1",
"To Go For Kristen",
"To Go Logan",
"To Go-Dean",
"To Go- Logan",
"To Go - Crystal",
"To Go- Sally",
"Logan To Go 2034703418",
"To Go Roberto",
"Noel- To Go"]


#Use pandas to overwrite any GrubHub, Seamless, or To Go orders check names as "To Go"
data1a.loc[data1a['Name'].isin(incorrect_checktypes), 'Check_Type'] = "To Go"
data2=data1a

# Zero out any void or comp amounts; these should not be included 
data2['Price']=np.where(data2.VC == 'V', 0.00, data2.Price)
data2['Price']=np.where(data2.VC == 'C', 0.00, data2.Price)

#Print Total Sales by Month & Year
table2 = data2.pivot_table(values=['Price'], columns=['Year','Month'],  aggfunc=np.sum)
print(table2)

#Print Total Guest Count by Month & Year
data3=data2
data3['UI'] =data3['Seated'].astype(str)+'_'+data3['Check_Number'].astype(str)
data3=data3.drop_duplicates(subset='UI', keep="first")
table3 = data3.pivot_table(values=['Guests'], columns=['Year','Month'],  aggfunc=np.sum)
table3

#Print Top 20 Beverages & Food Items (count)
bev_pt=pd.pivot_table(data2[data2.Course=="Beverages"],index=["Item"],values=["Quantity"],aggfunc='count').sort_values(by='Quantity', ascending=False)
food_pt=pd.pivot_table(data2[data2.Course!="Beverages"],index=["Item"],values=["Quantity"],aggfunc='count').sort_values(by='Quantity', ascending=False)
print(food_pt.head(20))
print(bev_pt.head(20))

#Print Top 5 Food Items Sold
ax = sns.barplot(x="Item", y="Quantity", data=food_pt.reset_index().head(5)).set_title("Top Food Items Sold")
plt.xticks(rotation='vertical') 
plt.show()

#Print Top 5 Beverage Items Sold
ax = sns.barplot(x="Item", y="Quantity", data=bev_pt.reset_index().head(5)).set_title("Top Beverages Sold")
plt.xticks(rotation='vertical') 
plt.show()

#Print Total Sales by Day of the Week
data2 = data2.sort_values(['Day of the Week'])
sns.barplot(x=data2['Day'], y=data2['Price'] , color="green", estimator=sum).set_title("Total Revenue by Day of the Week")
plt.show()

#Print Total Guest Count by Day of the Week
data4 = data3.sort_values(['Day of the Week'])
sns.barplot(x=data4['Day'], y=data4['Guests'] , color="skyblue", estimator=sum).set_title("Total Number of Guests by Day of the Week")
plt.show()

##store merged df to .xlsx file and json
writer = ExcelWriter('############.xlsx')
data2.to_excel(writer,'Raw_Data')
writer.save()

data2.to_json('############..json', orient='records', lines=True)