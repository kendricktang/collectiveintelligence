import random
from algs.sim_metric import pearson


def readfile(filename):
    lines = [line for line in file(filename)]

    # First line is column titles
    colnames = lines[0].strip().split('\t')[1:]
    rownames = []
    data = []
    for line in lines[1:]:
        word_count = line.strip().split('\t')
        rownames.append(word_count[0])
        data.append([float(x) for x in word_count[1:]])

    return rownames, colnames, data


class Bicluster(object):
    def __init__(self, vec, left=None, right=None, distance=0.0, id=None):
        self.vec = vec
        self.left = left
        self.right = right
        self.distance = distance
        self.id = id


def hcluster(rows, distance=pearson):
    distances = {}    # cache of distance calculations
    currentclustid = -1

    # Clusters are initially just the rows
    clust = [Bicluster(rows[i], id=i) for i in range(len(rows))]

    # Join two closest clusters!
    while len(clust) > 1:
        lowestpair = (0, 1)
        closest = distance(clust[0].vec, clust[1].vec)

        # Check every pair and look for new closest pair
        for i in range(len(clust)):
            for j in range(i+1, len(clust)):
                if (clust[i].id, clust[j].id) not in distances:
                    distances[(clust[i].id, clust[j].id)] = (
                        distance(clust[i].vec, clust[j].vec))

                d = distances[(clust[i].id, clust[j].id)]

                if d < closest:
                    closest = d
                    lowestpair = (i, j)

        # Calculate the average of the two clusters:
        mergevec = [
            (clust[lowestpair[0]].vec[i]+clust[lowestpair[1]].vec[i])/2.0
            for i in range(len(clust[0].vec))]

        # Create the new cluster
        newcluster = Bicluster(
            mergevec,
            left=clust[lowestpair[0]],
            right=clust[lowestpair[1]],
            distance=closest,
            id=currentclustid
        )

        # Remake clusters
        currentclustid -= 1
        del(clust[lowestpair[1]])
        del(clust[lowestpair[0]])
        clust.append(newcluster)

    return clust[0]


def kcluster(rows, distance=pearson, k=4):
    # Determine the max and min values for each attribute
    ranges = [
        (min(row[i] for row in rows), max(row[i]for row in rows))
        for i in range(len(rows[0]))]

    # Create k randomly placed centroids
    clusters = [
        [
            random.random()*(ranges[i][1]-ranges[i][0])
            for i in range(len(rows[0]))]
        for j in range(k)]

    lastmatches = None
    for t in range(100):
        print 'Iteration %d' % t
        bestmatches = [[] for i in range(k)]

        # Find which centroid is closest for each row
        for j in range(len(rows)):
            row = rows[j]
            bestmatch = 0
            for i in range(k):
                d = distance(clusters[i], row)
                if d < distance(clusters[bestmatch], row):
                    bestmatch = i
            bestmatches[bestmatch].append(j)

        if bestmatches == lastmatches:
            break
        else:
            lastmatches = bestmatches

        # Move the centroids to the averages of their members
        for i in range(k):
            avgs = [0.0]*len(rows[0])
            if len(bestmatches[i]) > 0:
                for rowid in bestmatches[i]:
                    for m in range(len(rows[rowid])):
                        avgs[m] += rows[rowid][m]
                for j in range(len(avgs)):
                    avgs[j] /= len(bestmatches[i])
                clusters[i] = avgs

    return bestmatches
