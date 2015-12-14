#!/usr/bin/env python

from math import sqrt
from csv import reader

def normalization_divisor(set_a, set_b):
    a_squared_sum = 0
    b_squared_sum = 0

    for i in range(0, len(set_a)):
        a_squared_sum = a_squared_sum + set_a[i]**2
        b_squared_sum = b_squared_sum + set_b[i]**2

    return sqrt(a_squared_sum*b_squared_sum)

def cross_correlate(set_a, set_b, normalize=False, unbaised=False):
    correlation_set = {}
    if normalize:
        n_divisor = normalization_divisor(set_a, set_b)

    if len(set_a) == len(set_b):
        for lag in range(-1*(len(set_a)-1), len(set_a)):
            print lag,
            c_sum = 0
            for i in range(0, len(set_a)):
                if i - lag < 0 or i - lag >= len(set_a):
                    print ".",
                else:
                    print "!",
                    c_sum += set_a[i]*set_b[i-lag]
            print ", = %.2f" % c_sum
        
            if unbaised:
                c_sum /= len(set_a) - abs(lag)
            
            if normalize:
                correlation_set[lag] = c_sum/n_divisor
            else:
                correlation_set[lag] = c_sum

        return correlation_set
    else:
        print "Sets must have the same length"
        return -1

def best_correlation(set_a, set_b, normalize=True, unbaised=False):
    correlation_set = cross_correlate(set_a, set_b, normalize=normalize, unbaised=unbaised)
    maximum_correlation_position = max(correlation_set.iterkeys(), key=(lambda key: correlation_set[key]))

    print "Best correlation when set_b lags by %d positions, with a correlation of %f" % (maximum_correlation_position, correlation_set[maximum_correlation_position])


if __name__ == "__main__":
    indexes = []
    set_a = []
    set_b = []

    with open('input.csv', 'rb') as csvfile:
        inputreader = reader(csvfile)

        # skip header
        next(inputreader)

        for row in inputreader:
            if row[0] == '':
                continue
            indexes.append(row[0])
            set_a.append(float(row[1]))
            set_b.append(float(row[2]))

    best_correlation(set_a, set_b, normalize=True, unbaised=True)
