
# coding: utf-8

# In[14]:

from mitmproxy import io
from mitmproxy.exceptions import FlowReadException
import sys
from controller import init_logger


# In[18]:

def read_flowfile(flowfile):
    with open(flowfile, 'rb') as logfile:    
        freader = io.FlowReader(logfile)
        try:
            for flow in freader.stream():
                find_search_keyword(str(flow))
                break
        except FlowReadException as e:
            print("flow file corrupted: {}".format(e))


# In[19]:

def find_search_keyword(flow):
    lines = flow.split('\n')
    for line in lines:
        if line.find('request') >= 0:
            print(line)


# In[ ]:



