#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np


# In[2]:


import pandas as pd


# In[3]:


# Reading instensities template


# In[4]:


intensities_template = pd.read_csv("intensities_template.csv")


# In[5]:


# Reading pixels files to calculte volumes


# In[6]:


header = ["PIXEL_COUNT"]
pixels_count_volume = pd.read_csv("SMM_s1_ABA_histogram_total.csv", names = header)
pixels_count_volume.insert(0, column = 'INTENSITY', value = range(0, len(pixels_count_volume)))  
pixels_count_volume_in_tissue = pd.read_csv("SMM_s1_ABA_histogram_in_tissue_total.csv", names = header)
pixels_count_volume_in_tissue.insert(0, column = 'INTENSITY', value = range(0, len(pixels_count_volume_in_tissue)))  


# In[7]:


# Reading pixels file to count cell activity


# In[8]:


regions_count_activity_fracc = pd.read_csv("SMM_s1_DR_Seg_3Dcount_75slices.csv")
regions_count_activity_fracc = regions_count_activity_fracc[regions_count_activity_fracc.PIXEL_COUNT != "PIXEL_COUNT"] 


# In[9]:


# Adding-up regions' fracctions


# In[20]:


regions_fracc_1 = regions_count_activity_fracc[["INTENSITY_1", "INTENSITY_1_PERC"]]
regions_fracc_2 = regions_count_activity_fracc[["INTENSITY_2", "INTENSITY_2_PERC"]]
regions_fracc_3 = regions_count_activity_fracc[["INTENSITY_3", "INTENSITY_3_PERC"]]
regions_fracc_1 = regions_fracc_1.rename(columns={"INTENSITY_1": "INTENSITY","INTENSITY_1_PERC" : "COUNTS"})
regions_fracc_2 = regions_fracc_2.rename(columns={"INTENSITY_2": "INTENSITY","INTENSITY_2_PERC" : "COUNTS"})
regions_fracc_3 = regions_fracc_3.rename(columns={"INTENSITY_3": "INTENSITY","INTENSITY_3_PERC" : "COUNTS"})
total_region_activity = regions_fracc_1.append(regions_fracc_2, ignore_index=True).append(regions_fracc_3, ignore_index=True)
total_region_activity["COUNTS"] = total_region_activity["COUNTS"].astype(float)
total_region_activity = total_region_activity.groupby(['INTENSITY']).agg('sum').reset_index()
total_region_activity["COUNTS"] = total_region_activity["COUNTS"].round(0)


# In[27]:


# Adding volumes and activity columns to the template table


# In[24]:


output_s1 = intensities_template.merge(pixels_count_volume, how='left', left_on='LabelID', right_on='INTENSITY')
output_s1 = output_s1.drop(columns=['INTENSITY'])
output_s1 = output_s1.rename(columns = {'PIXEL_COUNT':'VOLUME'})
output_s1 = output_s1.merge(pixels_count_volume_in_tissue, how='left', left_on='LabelID', right_on='INTENSITY')
output_s1['VOLUME'] = output_s1['VOLUME'].div(1000000).round(6)
output_s1 = output_s1.drop(columns=['INTENSITY'])
output_s1 = output_s1.rename(columns = {'PIXEL_COUNT':'VOLUME_IN_TISSUE'})
output_s1['VOLUME_IN_TISSUE'] = output_s1['VOLUME_IN_TISSUE'].div(1000000).round(6)
output_s1["LabelID"] = output_s1["LabelID"].astype(int)
total_region_activity["INTENSITY"] = total_region_activity["INTENSITY"].astype(int)
output_s1 = output_s1.merge(total_region_activity, how='left', left_on='LabelID', right_on='INTENSITY')
output_s1 = output_s1.drop(columns=['INTENSITY'])
output_s1 = output_s1.rename(columns = {'COUNTS':'ACTIVITY'})


# In[26]:


output_s1.to_csv(r's1_DR.csv')

