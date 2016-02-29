from math import sqrt

def pearson(v1,v2):
    if len(v1)!=len(v2):
        raise ValueError('Vectors are different lengths.')

    # Sums
    sum1=sum(v1)
    sum2=sum(v2)
    
    # Sum of squares
    sum1sq=sum([pow(v,2) for v in v1])
    sum2sq=sum([pow(v,2) for v in v2])
    
    # Sum of products
    psum=sum([v1[i]*v2[i] for i in range(len(v1))])
    
    # Calculate pearson score
    num=psum-(sum1*sum2/len(v1))
    den=sqrt((sum1sq-pow(sum1,2)/len(v1))*(sum2sq-pow(sum2,2)/len(v1)))
    if den==0:
        return 0
        
    return 1.0-num/den

def tanamoto(v1,v2):
    c1,c2,shr=0,0,0
    
    for i in range(len(v1)):
        if v1[i]!=0:
            c1+=1 # in v1
        if v2[i]!=0:
            c2+=1 # in v2
        if v1[i]!=0 and v2[i]!=0:
            shr+=1 # in both
            
    return 1.0-(float(shr)/(c1+c2-shr))