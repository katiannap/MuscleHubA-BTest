#!/usr/bin/env python
# coding: utf-8

# In[4]:


from codecademySQL import sql_query


# In[ ]:





# In[5]:


sql_query('''
SELECT *
FROM visits
LIMIT 5
''')


# In[6]:


sql_query('''
SELECT *
FROM fitness_tests
LIMIT 5
''')


# In[7]:


sql_query('''
SELECT *
FROM applications
LIMIT 5
''')


# In[9]:


sql_query('''
SELECT *
FROM purchases
LIMIT 5
''')


# In[12]:


df = sql_query('''
SELECT visits.first_name,
       visits.last_name,
       visits.visit_date,
       fitness_tests.fitness_test_date,
       applications.application_date,
       purchases.purchase_date
FROM visits
LEFT JOIN fitness_tests
    ON fitness_tests.first_name = visits.first_name
    AND fitness_tests.last_name = visits.last_name
    AND fitness_tests.email = visits.email
LEFT JOIN applications
    ON applications.first_name = visits.first_name
    AND applications.last_name = visits.last_name
    AND applications.email = visits.email
LEFT JOIN purchases
    ON purchases.first_name = visits.first_name
    AND purchases.last_name = visits.last_name
    AND purchases.email = visits.email
WHERE visits.visit_date >= '7-1-17'
''')


# In[13]:


import pandas as pd
from matplotlib import pyplot as plt


# In[14]:


df['ab_test_group'] = df.fitness_test_date.apply(lambda x:
                                                'A' if pd.notnull(x) else 'B')


# In[15]:


ab_counts = df.groupby('ab_test_group').first_name.count().reset_index()
ab_counts


# In[18]:


plt.pie(ab_counts.first_name.values, labels=['A', 'B'], autopct='%0.2f%%')
plt.axis('equal')
plt.show()
plt.savefig('ab_test_pie_chart.png')


# In[19]:


df['is_application'] = df.application_date.apply(lambda x: 'Application'
                                                  if pd.notnull(x) else 'No Application')


# In[20]:


app_counts = df.groupby(['ab_test_group', 'is_application'])               .first_name.count().reset_index()


# In[21]:


app_pivot = app_counts.pivot(columns='is_application',
                            index='ab_test_group',
                            values='first_name')\
            .reset_index()
app_pivot


# In[22]:


app_pivot['Total'] = app_pivot.Application + app_pivot['No Application']


# In[23]:


app_pivot['Percent with Application'] = app_pivot.Application / app_pivot.Total
app_pivot


# In[24]:


from scipy.stats import chi2_contingency

contingency = [[250, 2254], [325, 2175]]
chi2_contingency(contingency)


# In[ ]:





# In[25]:


df['is_member'] = df.purchase_date.apply(lambda x: 'Member' if pd.notnull(x) else 'Not Member')


# In[26]:


just_apps = df[df.is_application == 'Application']


# In[27]:


member_count = just_apps.groupby(['ab_test_group', 'is_member'])                 .first_name.count().reset_index()
member_pivot = member_count.pivot(columns='is_member',
                                  index='ab_test_group',
                                  values='first_name')\
                           .reset_index()

member_pivot['Total'] = member_pivot.Member + member_pivot['Not Member']
member_pivot['Percent Purchase'] = member_pivot.Member / member_pivot.Total
member_pivot


# In[28]:


contingency = [[200, 50], [250, 75]]
chi2_contingency(contingency)


# In[29]:


final_member_count = df.groupby(['ab_test_group', 'is_member'])                 .first_name.count().reset_index()
final_member_pivot = final_member_count.pivot(columns='is_member',
                                  index='ab_test_group',
                                  values='first_name')\
                           .reset_index()

final_member_pivot['Total'] = final_member_pivot.Member + final_member_pivot['Not Member']
final_member_pivot['Percent Purchase'] = final_member_pivot.Member / final_member_pivot.Total
final_member_pivot


# In[30]:


contingency = [[200, 2304], [250, 2250]]
chi2_contingency(contingency)


# In[31]:


# Percent of Visitors who Apply
ax = plt.subplot()
plt.bar(range(len(app_pivot)),
       app_pivot['Percent with Application'].values)
ax.set_xticks(range(len(app_pivot)))
ax.set_xticklabels(['Fitness Test', 'No Fitness Test'])
ax.set_yticks([0, 0.05, 0.10, 0.15, 0.20])
ax.set_yticklabels(['0%', '5%', '10%', '15%', '20%'])
plt.show()
plt.savefig('percent_visitors_apply.png')


# In[32]:


# Percent of Applicants who Purchase
ax = plt.subplot()
plt.bar(range(len(member_pivot)),
       member_pivot['Percent Purchase'].values)
ax.set_xticks(range(len(app_pivot)))
ax.set_xticklabels(['Fitness Test', 'No Fitness Test'])
ax.set_yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
ax.set_yticklabels(['0%', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'])
plt.show()
plt.savefig('percent_apply_purchase.png')


# In[33]:


# Percent of Visitors who Purchase
ax = plt.subplot()
plt.bar(range(len(final_member_pivot)),
       final_member_pivot['Percent Purchase'].values)
ax.set_xticks(range(len(app_pivot)))
ax.set_xticklabels(['Fitness Test', 'No Fitness Test'])
ax.set_yticks([0, 0.05, 0.10, 0.15, 0.20])
ax.set_yticklabels(['0%', '5%', '10%', '15%', '20%'])
plt.show()
plt.savefig('percent_visitors_purchase.png')


# In[ ]:




