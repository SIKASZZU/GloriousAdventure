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


from variables import UniversalVariables

def is_zero(x):
    return -UniversalVariables.ZERO_TOLERANCE <= x <= UniversalVariables.ZERO_TOLERANCE  


def is_between(value, start, end):
    return start - UniversalVariables.ZERO_TOLERANCE < value < end + UniversalVariables.ZERO_TOLERANCE


def is_bigger(value, min_val):
    return min_val - UniversalVariables.ZERO_TOLERANCE < value


def is_equal(val1, val2):
    return abs(val1 - val2) < UniversalVariables.ZERO_TOLERANCE


def are_points_equal(vec1, vec2):
    return is_equal(vec1[0], vec2[0]) and is_equal(vec1[1], vec2[1])