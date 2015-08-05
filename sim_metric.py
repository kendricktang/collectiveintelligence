from math import sqrt


# pearson correlation coefficient for p1 and p2
def sim_pearsons(prefs, p1, p2):
    """Pearson correlation coefficient metric"""
    # Get list of mutually rated items
    si = {}
    for item in prefs[p1]:
        if item in prefs[p2]:
            si[item] = 1

    # Find number of mutually rated items
    n = len(si)

    # If no ratings in common, return 0
    if n == 0:
        return 0

    # Add up preferences
    sum1 = sum([prefs[p1][item] for item in si])
    sum2 = sum([prefs[p2][item] for item in si])

    # Sum up squares
    sum1sq = sum([pow(prefs[p1][item], 2) for item in si])
    sum2sq = sum([pow(prefs[p2][item], 2) for item in si])

    # Sum up products
    pSum = sum([prefs[p1][item]*prefs[p2][item] for item in si])

    # Calculate pearson score
    num = pSum-(sum1*sum2/n)
    den = sqrt((sum1sq-pow(sum1, 2)/n)*(sum2sq-pow(sum2, 2)/n))
    if den == 0:
        return 0

    r = num/den
    return r


def sim_distance(prefs, p1, p2):
    """Euclidean distance metric"""
    # Get list of mutually rated items
    si = {}
    for item in prefs[p1]:
        if item in prefs[p2]:
            si[item] = 1

    # if no ratings in common, return 0
    if len(si) == 0:
        return 0

    # Add up squares of differences
    sum_of_squares = sum(
        [pow(prefs[p1][item]-prefs[p2][item], 2) for item in si])

    return 1/(1+sqrt(sum_of_squares))
