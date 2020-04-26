"""
Given an array of 1s and 0s representing COVID-19 patient samples (1 being a positive sample, 0 being negative),
outputs the number of tests needed to test the patients when evaluating them individually. This is simply the
length of the array, as every person is tested individually.

@params arr the array to test
@return the number of tests needed to test the array
"""
def linear(arr):
  return len(arr)

"""
Given an array of 1s and 0s representing COVID-19 patient samples, returns the
number of tests needed to find COVID-19 positive samples when evaluating the tests
in a linear-pooled fashion. By pooling the data, if it tests negative we can move
on with the whole sample and not run any more tests. If it tests positive, we
linearly test every sample in the pool.

@params arr the array to be pooled tested
@return the number of tests needed to test the array in a linearly pooled fashion
"""
def linear_pooled(arr):
  # Check if the sample tests positive for COVID-19
  if (tests_positive(arr)):
    # 1 accounts for the test needed to check the whole array, and len(arr) accounts
    # for the linear tests needed to find positive samples
    return 1 + len(arr)
  else:
    # Return 1 since no sample in the array has COVID-19
    return 1

  return 0


"""
Given an array of 1s and 0s representing COVID-19 patient samples, returns the
number of tests needed to find COVID-19 postive samples when evaluating the tests
in a binary-pooled fashion. By pooling the data, if any selected pool tests negative,
we can simply move on with that sample. If the pool tests positive, we can binary
search for samples that have COVID-19 with less tests overall.

@params arr the array to be pooled tested
@return the number of tests needed to test the array in a binary-pooled fashion
"""
def binary_pool(arr):
  # If the array is only length 1, return as we test it individually
  if (len(arr) == 1):
      return 1
  
  # Stores the number of tests needed to test the pool
  total_tests = 1

  # Check if the given array tests positive for COVID-19 (this is why we start total_tests at 1)
  if (tests_positive(arr)):

    # Find the midpoint and the right/left partitions of the sample
    mid = len(arr)//2
    left_side = arr[0:mid]
    right_side = arr[mid:]


    # Test left side for COVID-19, and find individuals with COVID-19
    if (tests_positive(left_side)):
      total_tests += binary_pool(left_side)

    # Test right side for COVID-19 and find individuals with COVID-19
    if (tests_positive(right_side)):
      total_tests += binary_pool(right_side)

    # Still increment the number of tests used, despite if either side did not
    # test positive for COVID-19
    if (not tests_positive(right_side)):
        total_tests += 1
    
    if (not tests_positive(left_side)):
      total_tests += 1
  
  return total_tests


"""
This method mimics testing a sample in a pooled fashion. It returns True
if any sample in the array as COVID-19 (i.e. there is a 1 in the array). It returns
false otherwise.
"""
def tests_positive(arr):
  for i in arr:
    if (i > 0):
      return True
  return False