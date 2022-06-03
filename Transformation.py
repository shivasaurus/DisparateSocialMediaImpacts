#!/usr/bin/env python
# coding: utf-8

# In[6]:


import numpy as np
import pandas as pd


# https://zerobone.net/blog/cs/gram-schmidt-orthogonalization/
def gram_schmidt(A):
    
    (n, m) = A.shape
    
    for i in range(m):
        
        q = A[:, i] # i-th column of A
        
        for j in range(i):
            q = q - np.dot(A[:, j], A[:, i]) * A[:, j]
        if np.array_equal(q, np.zeros(q.shape)):
            raise np.linalg.LinAlgError("The column vectors are not linearly independent")
        
        # normalize q
        q = q / np.sqrt(np.dot(q, q))
        
        # write the vector back in the matrix
        A[:, i] = q
    return A


def repeated_gs_removal(cols_x, names_remove, df):
    transformDF = pd.DataFrame()
    for col in cols_x:
        extension = []
        extension.extend(names_remove)
        extension.append(col)
        transformDF[col] = pd.Series(gram_schmidt(np.array(df[extension]))[:,-1])
    return transformDF


# In[ ]:




