import numpy as np
import math

# Goal is to find the number of people it takes to scan for covid 19 fastest

time_for_test = 24 # In hours

def linear(arr):
  # Returns the number of vials needed when testing each patient individually
  return len(arr)


def linear_pooled(arr):
  if (tests_positive(arr)):
    return 1 + len(arr)
  else:
    return 1
  return 0


def binary_pool(arr):
  # Returns the number of vials needed when testing each patient in a specific pool
  if (len(arr) == 1):
      return 1
  
  total_tests = 1
  if (tests_positive(arr)):
    mid = len(arr)//2
    left_side = arr[0:mid]
    right_side = arr[mid:]


    # Test left side
    if (tests_positive(left_side)):
      total_tests += binary_pool(left_side)

    # Test right side
    if (tests_positive(right_side)):
      total_tests += binary_pool(right_side)

    if (not tests_positive(right_side)):
        total_tests += 1
    
    if (not tests_positive(left_side)):
      total_tests += 1

  return total_tests

def tests_positive(arr):
  for i in arr:
    if (i > 0):
      return True
  return False


pooled_size = 10  # sample size
infection_rate = 0.01845457792  # number of trials, probability of each trial


# Number of people sampled (where we expect 1 person to have it)
starting_sample = math.ceil(1/infection_rate)



best_sample_size = starting_sample
best_avg_tests = 10000000000000000

for sample_size in range(1, starting_sample):
  cases = np.random.binomial(sample_size, infection_rate, 100000)

  total_tests = 0
  num_tests = len(cases)
  for num_positive in cases:
    tests = [1]*num_positive+[0]*(sample_size-num_positive)
    np.random.shuffle(tests)

    total_tests += binary_pool(tests)

  avg_tests = total_tests/num_tests

  if avg_tests < best_avg_tests:
    best_avg_tests = avg_tests
    best_sample_size = sample_size

print(best_sample_size)

  # [0, 1, 2, 1, 3, 1, 1, 2, 3, 1, 1, 1]
  # 55 people


# result of flipping a coin 10 times, tested 10000 times.

# print(s)

# print("Hello World")




arr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1]
print(binary_pool(arr))
print(linear(arr))
print(linear_pooled(arr))

