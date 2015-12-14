#!/usr/bin/env python

from math import sqrt
from csv import reader

def normalization_divisor(set_a, set_b):
    """ Given two sets, returns the divisor that should be used to 
        normalize the cross-correlation value """
    a_squared_sum = 0
    b_squared_sum = 0

    for i in range(0, len(set_a)):
        a_squared_sum += set_a[i]**2
        b_squared_sum += set_b[i]**2

    return sqrt(a_squared_sum*b_squared_sum)

def cross_correlate(set_a, set_b, normalize=False, unbaised=False):
    """ Given two equally-sized sets, returns the correlation set computed
    by taking a sliding "lag" window that is used to offset the second set.
    
    Takes an optional "normalize" flag that will normalize each item in the 
    correlation set (off by default). Also takes an "unbaised" flag that will
    weigh each computation of the correlation of the two sets for a given lag, 
    giving greater lags greater weight. Since the sets have the same length,
    lag can bias the correlation to lower values because there are fewer data
    to iterate over, and this technique can help avoid that. It's off by default.
    """
    correlation_set = {}
    if normalize:
        n_divisor = normalization_divisor(set_a, set_b)

    if len(set_a) == len(set_b):
        for lag in range(-1*(len(set_a)-1), len(set_a)):
            print lag,
            c_sum = 0
            for i in range(0, len(set_a)):
                if i - lag < 0 or i - lag >= len(set_a):
                    print ".", # "miss" - the lag prevents a hit for i in both sets a and b
                else:
                    print "!", # "hit" - there's a corresponding set_b[i] for this set_a[i]
                    c_sum += set_a[i]*set_b[i-lag]
            print ", = %.2f" % c_sum
        
            if unbaised:
                c_sum /= len(set_a) - abs(lag) # greater lag, greater c_sum
            
            if normalize:
                correlation_set[lag] = c_sum/n_divisor # FIXME unbaised flag probably makes this normalization invalid
            else:
                correlation_set[lag] = c_sum

        return correlation_set
    else:
        print "Sets must have the same length"
        return -1

def best_correlation(set_a, set_b, normalize=True, unbaised=False):
    """ Returns the best correlation found by cross_correlate(), and the lag required to find it. """
    correlation_set = cross_correlate(set_a, set_b, normalize=normalize, unbaised=unbaised)
    maximum_correlation_position = max(correlation_set.iterkeys(), key=(lambda key: correlation_set[key]))

    print "Best correlation when set_b lags by %d positions, with a correlation of %f" % (maximum_correlation_position, correlation_set[maximum_correlation_position])


if __name__ == "__main__":
    indexes = []
    set_a = []
    set_b = []

    with open('input.csv', 'rb') as csvfile:
        inputreader = reader(csvfile) # header\nindex,set_a,set_b\nindex,set_a,set_b\n...

        # skip header
        next(inputreader)

        for row in inputreader:
            if row[0] == '':
                continue
            indexes.append(row[0])
            set_a.append(float(row[1]))
            set_b.append(float(row[2]))

    best_correlation(set_a, set_b, normalize=True, unbaised=True)
