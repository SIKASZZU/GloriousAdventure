# MIT License

# Copyright (c) 2022 Jakub Woś

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

import math

def square_length(vec2d):
    return vec2d[0] * vec2d[0] + vec2d[1] * vec2d[1]


def substract_vec(vec_a, vec_b):
    return (vec_a[0] - vec_b[0], vec_a[1] - vec_b[1])


def add_vec(vec_a, vec_b):
    return (vec_a[0] + vec_b[0], vec_a[1] + vec_b[1])


def lengthten(vec2d, min_x, min_y):
    ''' lengthtens a vector up to one of given dimensions (whichever is closest) '''
    k = 1
    error_pillow = 0.05     # to compensate for possible float calculation errors
    if vec2d[0] == 0:
        if vec2d[1] == 0:
            return (0, 0)
        k = min_y / vec2d[1]
    elif vec2d[1] == 0:
        k = min_y / vec2d[0]
    else:  
        a = min_x / vec2d[0]
        b = min_y / vec2d[1]
        k = max(a, b)
    k += error_pillow
    return (vec2d[0] * k, vec2d[1] * k)


def normalize(vec2d):
    length = math.sqrt(square_length(vec2d))
    if length == 0:
        return (0, 0)
    return (vec2d[0] / length, vec2d[1] / length)


def get_vector(from_where, to_where):
    return (to_where[0] - from_where[0], to_where[1] - from_where[1])