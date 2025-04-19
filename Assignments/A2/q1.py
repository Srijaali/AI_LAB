# You're designing an autonomous drone for a hiking mission. This drone is equipped with a sensor that can
# measure the elevation (height) at its current position, but it cannot see the entire terrain at once. You aim
# to program the drone to find the highest peak in a given one-dimensional mountain range. The elevation
# increases up to a peak and then decreases; this forms an unimodal pattern. To simulate this task, you're
# given access to a black-box function query(x) that returns the elevation at position x, where x is an integer
# between 0 and N. You are given:
# A function
# def query(x: int) -> int
# returns the elevation at index x.
# An integer N represents the maximum value of x. You need to implement the function
# def find_peak(N: int) -> int
# that uses a Hill Climbing algorithm to find the index p (0 ≤ p ≤ N) at which the elevation is maximum.
# The function query(x) follows the unimodal rule:
# There exists a peak index p such that:
# query(x) < query(x + 1) for all x < p
# query(x) > query(x + 1) for all x ≥ p
# SUPPOSE a query function is this can be replaceable with any function.

# def query(x):
# return -1 * (x - 7)**2 + 49
# Simulated elevation query function (you can replace this with your real sensor logic)
def query(x):
    return -1 * (x - 7)**2 + 49  # This is a parabola with a peak at x = 7

def peak(N: int) -> int:
    low, high = 0, N
    while low < high:
        mid = (low + high) // 2
        if query(mid) < query(mid + 1):
            low = mid + 1  # Move right
        else:
            high = mid  # Move left (or stay)
    return low  # low == high at peak


N = 15  # Maximum index to search
peak_index = peak(N)
print("Peak found at index:", peak_index)
print("Elevation at peak:", query(peak_index))
