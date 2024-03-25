#
#normal fectorial
def findfect(n):
    mul = 1
    for i in range(1,n+1):
        if i ==0:
            pass
        else:
            mul = mul*i
            
    return mul


#use recursive 
def resfindfect(n):
    if n==0:
        return 1

    return n * resfindfect(n-1)

