#!/usr/bin/env python
# coding: utf-8

# In[3]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import time
import re
from datetime import date
import datetime
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import warnings
warnings.filterwarnings("ignore")
from pylab import rcParams
import matplotlib as mpl
from selenium.common.exceptions import TimeoutException 


# In[ ]:


driver = webdriver.Chrome('D:\Web Driver\chromedriver')
driver.get('https://www.instagram.com/')


# In[ ]:


#Login
def login(id, password):
    
    wait = WebDriverWait(driver, 10)
    text_box = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//input[@class = "_2hvTZ pexuQ zyHYP"]')))
    
    text_box[0].send_keys(id)
    text_box[1].send_keys(password)  
    
    login_button = driver.find_element_by_xpath('//button[@class = "sqdOP  L3NKy   y3zKF     "]')
    login_button.submit()
    
login('username','password')

def search_and_open(profile):
    driver.refresh()
    wait = WebDriverWait(driver, 10)
    search_box = wait.until(EC.presence_of_element_located((By.XPATH, '//input[contains(@class, "XTCLo x3qfX")]')))

    search_box.clear()
    search_box.send_keys(profile)
    
    pro = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[contains(@class, "yCE8d")]')))
    pro.click()


# In[4]:


'''1.1 From the list of instagram handles you obtained when you searched ‘food’ in previous project. Open the first 10 handles and find the top 5 which have the highest number of followers
def get_handles_list(word)'''

    driver.refresh()
    wait = WebDriverWait(driver, 10)
    search_box = wait.until(EC.presence_of_element_located((By.XPATH, '//input[contains(@class, "XTCLo x3qfX")]')))

    search_box.clear()
    search_box.send_keys(word)
    
    _list = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//a[contains(@class, "yCE8d")]')))
    
    data = driver.page_source
    html_data = BeautifulSoup(data, 'html.parser')
    
    hlist = html_data.find_all(class_ = 'Ap253')
    
    insta_handle_list=[]
    i=1
    
    for handle in hlist:
        name = handle.string
        if name[0] != '#':
            insta_handle_list.append(name)
        if i==10:
            break
        i = i+1
    return insta_handle_list


# In[5]:


def get_followers(handle):
    
    wait = WebDriverWait(driver, 10)
    search_and_open(handle)
    time.sleep(3)
    fol = wait.until(EC.presence_of_element_located((By.XPATH, '//span[contains(@class, "-nal3")]')))
    
    data = driver.page_source
    html_data = BeautifulSoup(data, 'html.parser')
    
    flist = html_data.find_all(class_ = '-nal3')
    f = flist[1].span['title']
    f = int(f.replace(',',''))
    return f


# In[6]:


def get_followers_for_top10(word):

    handles = get_handles_list('food')
    d = {}
    for h in handles:
        d[h] = get_followers(h)

    print('First 10 handles are:')
    for k,v in d.items():
        print(k,':',v)

    keys = np.array(list(d.keys()))
    values = np.array(list(d.values()))

    ind = values.argsort()[::-1]
    ind = ind[:5]

    keys_5 = keys[ind]
    values_5 = values[ind]
    
    print()
    print('Top 5 handles which have the highest number of followers are:')
    for i in range(5):
        print(keys_5[i],':', values_5[i])
        
    return [keys, values, keys_5, values_5]

ans = get_followers_for_top10('food')


# In[ ]:


#1.2 Now Find the number of posts these handles have done in the previous 3 days
def get_days(d):
    
    year = int(d[0:4])
    month = int(d[5:7])
    day = int(d[8:10])

    from datetime import date

    current_time = datetime.datetime.now() 
    f_date = date(year, month, day)
    l_date = date(current_time.year, current_time.month, current_time.day)
    delta = l_date - f_date
    
    return delta.days


# In[7]:


def get_last_three_days_post():

    no_of_days = 0
    count = 0

    while True:
        
        wait = WebDriverWait(driver, 10)
        dt = wait.until(EC.presence_of_element_located((By.XPATH, '//a[contains(@class, "c-Yi7")]')))

        data = driver.page_source
        html_data = BeautifulSoup(data, 'html.parser')

        date = html_data.find(class_ = '_1o9PC')
        d = date['datetime']
        no_of_days = get_days(d)

        if no_of_days < 4:
            count = count + 1
        else:
            break

        next_ = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[contains(@class, "_65Bje  coreSpriteRightPaginationArrow")]')))
        next_.click()

        dt = wait.until(EC.presence_of_element_located((By.XPATH, '//a[contains(@class, "c-Yi7")]')))

    return count


# In[8]:


def get_last_three_days_post_for_handles(handles):
    #handles = get_handles_list('food')
    
    print("Number of posts posted by Top 5 handles which have the highest number of followers in the previous 3 days are:")
    
    num = []
    for h in handles:

        search_and_open(h)
        time.sleep(2)

        wait = WebDriverWait(driver, 10)
        post = wait.until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "_9AhH0")]')))
        post.click()
        
        n = get_last_three_days_post()
        print(h,':', n)
        num.append(n)
        
    return [handles, num]
ans_12 = get_last_three_days_post_for_handles(ans[2])


# In[9]:


#1.3 Depict this information using a suitable graph
#Using ans form 1.1

rcParams['figure.figsize'] = 7,7
plt.bar(ans[2],ans[3])
plt.ylabel('Number of Followers',fontsize=15)
plt.title('Top 5 handles which have the highest number of followers among the first 10 handles when searched "food"',fontsize=15)
plt.yticks(fontsize=15)
plt.xticks(rotation='vertical',fontsize=15)
plt.show()


# In[ ]:


#USING ans_12 from 1.2
ans_12 = get_last_three_days_post_for_handles(ans[2])


# In[10]:


rcParams['figure.figsize'] = 6,6
plt.bar(ans_12[0],ans_12[1])
plt.ylabel('Number of Posts',fontsize=15)
plt.title('Number of posts posted by Top 5 handles which have the highest number of followers in the previous 3 days',fontsize=15)
plt.yticks(fontsize=15)
plt.xticks(rotation='vertical',fontsize=15)
plt.show()


# In[ ]:


#2.1 Open the 5 handles you obtained in the last question, and scrape the content of the first 10 posts of each handle.
def get_content():

    wait = WebDriverWait(driver, 10)
    post = wait.until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "_9AhH0")]')))
    post.click()
    
    count = 0
    content_list = []
    
    while count < 10:

        content = wait.until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "C4VMK")]')))

        data = driver.page_source
        html_data = BeautifulSoup(data, 'html.parser')

        content_data = html_data.find(class_ = 'C4VMK')
        c = content_data.contents[1]
        content_list.append(list(c.stripped_strings))
        count = count + 1
        
        next_ = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[contains(@class, "_65Bje  coreSpriteRightPaginationArrow")]')))
        next_.click()
        

    return content_list


# In[11]:


def get_content_handles(handles):
    
    content_list = []
    
    for h in handles:
        search_and_open(h)
        time.sleep(2)
        content = get_content()
        
        print('The content of the first 10 posts of', h, 'are:')
        print()
        for l in content:
            for c in l:
                print(c)
            print("------------------------------------------------")
        print("****************************************************")
        print()
        content_list.append(content)
    return content_list
    
#handles = ['buzzfeedfood','dilsefoodie','foodtalkindia','foodiesdelhite','baebornfoodie']
#Using ans[2] from 1.1
ans_21 = get_content_handles(ans[2])


# In[12]:


2.2 Prepare a list of all words used in all the scraped posts and calculate the frequency of each word
def remove_emoji(text):
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  
        u"\U0001F300-\U0001F5FF"  
        u"\U0001F680-\U0001F6FF"  
        u"\U0001F1E0-\U0001F1FF"  
        u"\U00002500-\U00002BEF"  
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642"
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  
        u"\u3030"                       
        "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'',text)
    


# In[13]:


def get_word_freq(content_list):
    d = {}
    d_h = {}

    for h in content_list:
        for l in h:
            for s in l:
                s = remove_emoji(s)
                s = s.replace('-',' ')
                s = s.replace('.',' ')
                s = s.replace(',',' ')
                s = s.replace('!','')
                s = s.replace('?','')
                s = s.replace(':','')
                s = s.replace('(','')
                s = s.replace(')','')
                s = s.replace('/','')
                s = s.replace("'",'')
                s = s.replace('"','')
                s = s.replace('•','')
                s = re.sub(" \d+", " ", s)
                for w in s.split(" "):
                    if w != " " and w != "":
                        d[w] = d.get(w,0) + 1
                        if w[0] == '#':
                            d_h[w] = d_h.get(w,0) + 1
    return [d, d_h]
    


# In[14]:


#Using ans_21 from 2.1
ans_22 = get_word_freq(ans_21)

# Result description:
# ans_22[0] is a dictinary with all words (including hastags) as keys and their frequency as values
# ans_22[1] is a dictinary with only all hastags as keys and their frequency as values


print('List of all words used in all the scraped posts along with the frequency of each word are:')
for k,v in ans_22[0].items():
    if k.isnumeric():
        continue
    else:
        print(k,':', v)


# In[ ]:


#2.3 Create a csv file with two columns : the word and its frequency
def create_csv(d):
    l = []
    for k, v in d.items():
        l.append([k,v])
    
    df = pd.DataFrame(l, columns=['Word','Frequency'])
    df.to_csv('word_freq.csv', index=False)
    return
#Using ans_22 from 2.2
create_csv(ans_22[0])


# In[15]:


#2.4 Now, find the hashtags that were most popular among these bloggers
def get_popular_hastags(d):
    
    keys = np.array(list(d.keys()))
    values = np.array(list(d.values()))

    ind = values.argsort()[::-1]
    ind = ind[:10]

    keys_10 = keys[ind]
    values_10 = values[ind]
    
    print()
    print('Top 10 hashtags that were most popular among these bloggers are:')
    for i in range(10):
        print(keys_10[i],':', values_10[i])
        
    return [keys_10, values_10]
    
#Using ans_22 from 2.2
ans_24 = get_popular_hastags(ans_22[1])


# In[16]:


#2.5 Plot a Pie Chart of the top 5 hashtags obtained and the number of times they were used by these bloggers in the scraped posts
#Using ans_24 from 2.4
for i in range(5):
    print('Hashtag', ans_24[0][i], 'was used', ans_24[1][i], 'times')
rcParams['figure.figsize'] = 6,6
plt.pie(ans_24[1][:5], labels = ans_24[0][:5], autopct = '%.2f%%', labeldistance=1.1)
plt.title(' Pie Chart of the top 5 hashtags obtained',fontsize=17)
plt.axis('equal')
mpl.rcParams['font.size'] = 15
plt.show()


# In[17]:


#3.1 Find out the likes of the top 10 posts of the 5 handles obtained earlier

def get_likes():

    wait = WebDriverWait(driver, 10)
    post = wait.until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "_9AhH0")]')))
    post.click()

    l = []
    count = 0

    while True:

        try:
            wait = WebDriverWait(driver, 3)
            #like = wait.until(EC.presence_of_element_located((By.XPATH, '//span[contains(@class, "qBUYS _7CSz9 FGFB7 videoSpritePlayButton")]')))

            view = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[contains(@class, "vcOH2")]')))
            view.click() 

            data = driver.page_source
            html_data = BeautifulSoup(data, 'html.parser')

            likes = html_data.find(class_ = 'vJRqr')
            like = likes.span.string 
            like = int(like.replace(",",""))

            back = wait.until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "QhbhU")]')))
            back.click()
            
        except TimeoutException:
            
            wait = WebDriverWait(driver, 5)
            ll = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "sqdOP")]')))
            
            data = driver.page_source
            html_data = BeautifulSoup(data, 'html.parser')

            likes = html_data.find_all(class_ = 'sqdOP')
            like = likes[2].span.string 
            if like is None:
                like = likes[3].span.string
            like = int(like.replace(",",""))

        l.append(like)
        count = count + 1

        if count == 10:
            break

        next_ = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[contains(@class, "_65Bje  coreSpriteRightPaginationArrow")]')))
        next_.click()

    return l

def get_likes_handle(handles):
    d = {}
    for h in handles:
        search_and_open(h)
        time.sleep(2)
        l = get_likes()
        d[h] = l
        print('Number of likes of the top 10 posts of', h, 'are:')
        for i in l:
            print(i)
        print()   
    return d

# Using ans[2] from 1.1
ans_31 = get_likes_handle(ans[2])
#ans_31 = get_likes_handle(['foodtalkindia'])


# In[ ]:


#3.2 Calculate the average likes for a handle
def get_average_likes(d):
    d_avg = {}
    for k,v in d.items():
            avg = sum(v) // 10
            d_avg[k] = avg
    return d_avg
#Using ans_31 from 3.1
ans_32 = get_average_likes(ans_31)

print('Average likes for each handle are:')
for k,v in ans_32.items():
    print(k, ":", v)


# In[ ]:


#3.3 Divide the average likes obtained from the number of followers of the handle to get the average followers:like ratio of each handle

def get_average_followers_like_ratio(k_5, f_5, d):
    d_ratio={}
    for i in range(5):
        d_ratio[k_5[i]] = (f_5[i])//(d[k_5[i]])
    return d_ratio
#Using ans from 1.1 and ans_32 from 3.2

ans_33 = get_average_followers_like_ratio(ans[2], ans[3], ans_32)

print('Average followers:like ratio of each handle are:')
for k,v in ans_33.items():
    print(k, ":", v)


# In[18]:


#3.4 Create a bar graph to depict the above obtained information
## Using ans_32 and ans_33 from 3.2 and 3.3 respectively
keys_32 = np.array(list(ans_32.keys()))
values_32 = np.array(list(ans_32.values()))

rcParams['figure.figsize'] = 6,6
plt.bar(keys_32,values_32)
plt.ylabel('Average likes',fontsize=15)
plt.title('Average likes for each handle',fontsize=15)
plt.yticks(fontsize=15)
plt.xticks(rotation='vertical',fontsize=15)
plt.show()

keys_33 = np.array(list(ans_33.keys()))
values_33 = np.array(list(ans_33.values()))

plt.bar(keys_33,values_33)
plt.ylabel('Average followers:like ratio',fontsize=15)
plt.title('Average followers:like ratio of each handle',fontsize=15)
plt.yticks(fontsize=15)
plt.xticks(rotation='vertical',fontsize=15)
plt.show()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




