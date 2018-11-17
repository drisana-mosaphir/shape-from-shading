import numpy as np
import math
from collections import OrderedDict

n = 11 # test value to be deleted
h = 1/n
x = np.linspace(0,1,n)

def f(x): # just a test to see whether fast marching is working
    '''The function appearing in the eikonal equation
    |u'(x)| = f(x).'''
    return 1

def ff(n): # applies f to the grid space
    x = np.linspace(0,1,n)
    ff = map(f, x)
    return list(ff)

def fastmarch(n):
    f = ff(n) 
    h = 1/(n-1)
    #Initialization
    t0 = 0
    Z = np.linspace(0,1,n) # grid points
    A = [0, 1] #initial accepted set is just the boundary {0,1} where we know the values
    u = np.repeat(math.inf, n)
    u[0] = 0
    u[-1] = 0
    # update until there are n elements in A, meaning that all the nodes have been incorporated
    while len(A) < n:
        F = neighbors(A) # define the front to be the neighbors of the accepted set, minus the ones that are already in A
        print(F)
        schemeF = map(scheme, F)
        heapsort(list(schemeF))
        #A.append(np.argmin(schemeF))# record the index (i) that minimizes scheme value
        print(A)
        #F.remove(np.argmin(schemeF))#then remove that minimizing element from the front
    return A

def neighbors(A):
    '''Finds the collection of neighbors of all elements in the accepted set'''
    x = np.linspace(0,1,n)
    ind = np.nonzero(np.in1d(x, A))[0] # indices of accepted elements within x
    u = np.repeat(math.inf, n) # test delete later
    u[0] = 0 # test delete later
    u[-1] = 0 # test delete later
    nb = [] # initialize neighbors as empty list
    nb1 = [] #indices of neighbors
    nb2 = [] # u-values
    sch = [] # scheme values
    for i in ind:
        if (i != 0) and (i != len(x)-1):
            nb.append(x[i-1], x[i+1]) # when there are left and right neighbors
            nb1.append(i-1, i+1)
            nb2.append(u[i-1], u[i+1])
            sch.append(scheme(i-1), scheme(i+1))
        elif i == 0: # only have the right neighbor
            nb.append(x[i+1])
            nb1.append(i+1)
            nb2.append(u[i+1])
            sch.append(scheme(i+1))
        else: # only have the left neighbor
            nb.append(x[i-1])
            nb1.append(i-1)
            nb2.append(u[i-1])
            sch.append(scheme(i-1))
        nb = list(OrderedDict.fromkeys(nb)) # lists the union of all neighbors of points in the accepted set
        nb1 = list(OrderedDict.fromkeys(nb1))
    return nb1

def scheme(i): # might need to fix notation to be consistent with f, ff
    s = np.empty()
    u = np.repeat(math.inf, n)
    u[0] = 0
    u[-1] = 0
    if (i != 0) and (i != n-1):
        s.append(h*(ff(n))[i] + min(u[i-1], u[i+1])) # fix this to include the bdry
    elif i == 0:
        s.append(h*(ff(n))[i] + u[i+1])
    else:
       s.append(h*(ff(n))[i] + u[i-1])
    return s

# ----- heapsort ----    

def heapsort(lst):
  # referenced Rosetta Code but updated for Python 3.6
  for start in range(int(round((len(lst)-2)/2)), -1, -1):
    sd(lst, start, len(lst)-1)
 
  for end in range(len(lst)-1, 0, -1):
    lst[end], lst[0] = lst[0], lst[end]
    sd(lst, 0, end - 1)
  return lst
 
def sd(lst, start, end):
  rt = start
  while True:
    child = rt * 2 + 1
    if child > end: break
    if child + 1 <= end and lst[child] < lst[child + 1]:
      child += 1
    if lst[rt] < lst[child]:
      lst[rt], lst[child] = lst[child], lst[rt]
      rt = child
    else:
      break    

# -------------------------------------------------- 
