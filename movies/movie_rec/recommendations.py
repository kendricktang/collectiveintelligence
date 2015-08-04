# from movie_rec.recommendations import loadMovieLens as lml, getRecommendations as gr

from movie_rec.sim_metric import sim_pearsons, sim_distance

def loadMovieLens(path = './data/movielens'):
    # Get movie titles
    movies={}
    for line in open(path + '/' + 'u.item'):
        (id,title)=line.split('|')[0:2]
        movies[id] = title
    
    # Load data
    prefs={}
    for line in open(path + '/' + 'u.data'):
        (user,movieid,rating,ts)=line.split('\t')
        prefs.setdefault(user,{})
        prefs[user][movies[movieid]]=float(rating)
    return prefs

def topMatches(prefs,person,n=5,similarity=sim_pearsons):
    scores=[(similarity(prefs,person,other),other) for other in prefs if other!=person]
    scores.sort()
    scores.reverse()
    return scores[0:n]

def getRecommendations(prefs,person,similarity=sim_pearsons):
    totals={}
    simSums={}

    for other in prefs:
        # don't compare to self
        if other==person:
            continue
        sim=similarity(prefs,person,other)
        
        # ignore scores of zero or lower
        if sim<=0:
            continue
        for item in prefs[other]:
            
            #only score movies the person hasn't seen yet
            if item not in prefs[person] or prefs[person][item]==0:
                # Similarity * score
                totals.setdefault(item,0)
                totals[item]+=prefs[other][item]*sim
                # Sum of similarities
                simSums.setdefault(item,0)
                simSums[item]+=sim
                    
    # Create normalized list
    rankings=[(total/simSums[item],item) for item,total in totals.items()]
    
    # Return sorted list
    rankings.sort()
    rankings.reverse()
    return rankings

def calculateSimilarItems(prefs,n=10):
    # Create a dictionary for similar items
    result={}
    
    # Invert the preference matrix to be item-centric
    itemPrefs=transformPrefs(prefs)
    c=0
    for item in itemPrefs:
        # Status update for large datasets
        c+=1
        if c%100==0:
            print "%d / %d" %(c,len(itemPrefs))
        
        # Find the most similar items
        scores=topMatches(itemPrefs,item,n=n,similarity=sim_distance)
        result[item]=scores
    return result

def getRecommendedItems(prefs,itemMatch,user):
    userRatings=prefs[user]
    scores={}
    totalSim={}
    
    # Loop over items rated by this user
    for (item,rating) in userRatings.items():
        
        # Loop over items similar to this one
        for (similarity,item2) in itemMatch[item]:
            
            # Ignore if item2 has been rated by user
            if item2 in userRatings:
                continue
            
            # Weighted sum of rating items similarity
            scores.setdefault(item2,0)
            scores[item2]+=similarity*rating
            
            # Sum of all the similarities
            totalSim.setdefault(item2,0)
            totalSim[item2]+=similarity
    
    # Divide each total score by the similarity for a weighted average
    rankings = [(score/totalSim[item],item) for item,score in scores.items()]
    rankings.sort()
    rankings.reverse()
    return rankings

def transformPrefs(prefs):
    result={}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item,{})
            
            result[item][person] = prefs[person][item]
    return result