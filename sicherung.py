import numpy as np

storage_list = array([0,0,0,0])
profile_list = array([-2,3,5,2])


a = profile_list

b = int(profile_list[np.where(a==a.min())] + profile_list[np.where(a==a.max())])
c = int(profile_list[np.where(a==a.max())] - profile_list[np.where(a==a.max())])
print(b, c)
#addiert maximum und Minimum und setzt maximum auf 0

profile_list[np.where(a==a.min())] = b
profile_list[np.where(a==a.max())] = c 

#ersetzt maximum und minimum mit den berechneten Werten in der Liste
print(profile_list)


p = min(storage_list) + max(storage_list)
print(p)

a = storage_list
np.where(a==a.min())
#print(np.where(a==a.min()))
np.where(a==a.max())
#print(np.where(a==a.max()))
#Indexnummern der Maxima und Minima


















import numpy as np

storage_list = array([-20,-15,30,30])
a = storage_list

#print(storage_list[np.where(a==a.max())])

if len(storage_list[np.where(a==a.max())]) > 1:
    maximum_list = storage_list[np.where(a==a.max())]
    minimum_list = storage_list[np.where(a==a.min())]
    print(maximum_list)
    print(minimum_list)
    b = int(minimum_list[0] + maximum_list[0])
    c = int(maximum_list[0] - maximum_list[0])


    storage_list[np.where(a==a.min())] = b
    storage_list[np.where(a==a.max())] = c 
    print(storage_list)
    
    
    
    
        if min(storage_list) < 0 and max(storage_list) > 0:
        b = int(storage_list[np.where(a==a.min())] + storage_list[np.where(a==a.max())])
        c = int(storage_list[np.where(a==a.max())] - storage_list[np.where(a==a.max())])
        storage_list[np.where(a==a.min())] = b
        storage_list[np.where(a==a.max())] = c 
        print(storage_list)
        #setzt das Maximum und Minimum auf die neuen Werte in der Speicher Liste
        



