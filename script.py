from algos import linear_pooled, binary_pool, linear
from utilities import BestSampleSizes, produce_population, num_tests_used

import numpy as np
import math

# Constants
infection_rate = 0.01845457792  # number of people infected with COVID19 / total number of people in the area (this infection rate is for NYC as of 4-26)

# The number of people, where we expect 1 person to have COVID-19. This is the roof of our sampling methodology, as any scenario where more than 1 person
# is expected to have COVID 19 slows down the rate of testing. This number is based on the Binomial Model.
starting_sample = math.ceil(1/infection_rate)

# This is the population size for each individual test. Every algorithm will be evaluated on a population size of 5000 people. This remains constant
# when evaluating every algorithm. Each algorithm is tested on an array of length 5000 with 1s representing people with COVID-19 and 0s representing
# people without COVID-19.
population_size = 5000

# The number of samples with the size of the population that are desired to be ran. Changing this number affects the number of samples run for each
# individual sample size. Ex. 500 means that for any given sample size being evaluated, 500 arrays with population size 5000 will be evaluated for
# every possible sample size between 1 and the starting sample.
num_samples = 500


# Initialize the best_sample_sizes class to store the best testing averages for each algorithm
best_sample_sizes = BestSampleSizes(starting_sample)

# Loop through every possible sample size between 1 and our target starting_sample
for sample_size in range(1, starting_sample):
  print("Evaluating ", num_samples, " samples of ", population_size, " people tested in groups of ", sample_size, " for the linear/linear-pool/binary-pool algos")

  # Create the samples that will be used for the given sample size
  samples = np.random.binomial(population_size, infection_rate, num_samples)

  num_tests = len(samples)

  # These store the number of tests used by each algorithm for the given sample created above
  linear_tests = 0
  linear_pooled_tests = 0
  binary_pooled_tests = 0

  # Test each algorithm with every sample created by the binomial model
  for sample in samples:
    # Create the sample array (composed of 0s and 1s)
    patient_samples = produce_population(sample, population_size)
    
    # Increment the number of tests used for each algorithm
    linear_tests += num_tests_used(patient_samples, sample_size, "linear")
    linear_pooled_tests += num_tests_used(patient_samples, sample_size, "linear_pool")
    binary_pooled_tests += num_tests_used(patient_samples, sample_size, "binary_pool")

  # Average the number of tests used by each algorithm for this given sample
  avg_binary_pool_tests = binary_pooled_tests/num_tests
  avg_linear_tests = linear_tests/num_tests
  avg_linear_pooled_tests = linear_pooled_tests/num_tests

  # Update the best cases for each algorithm given the new averages for this sample size
  best_sample_sizes.update_linear(avg_linear_tests, sample_size)
  best_sample_sizes.update_binary_pool(avg_binary_pool_tests, sample_size)
  best_sample_sizes.update_linear_pool(avg_linear_pooled_tests, sample_size)


# The following code evalautes after evaluating each algorithm at a sampling size from
# 1 to the target starting_sample


# Get the best sampling sizes for every algorithm
best_linear_sample_size = best_sample_sizes.get_best_linear()
best_linear_pool_sample_size = best_sample_sizes.get_best_linear_pool()
best_binary_pool_sample_size = best_sample_sizes.get_best_binary_pool()

print("")
print("Linear testing is most effective for testing COVID 19 in populations of ", best_linear_sample_size, " people.")
print("Linear pooling is most effective for testing COVID 19 in pooled populations of ", best_linear_pool_sample_size, " people.")
print("Binary pooling is most effective for testing COVID 19 in pooled populations of ", best_binary_pool_sample_size, " people.")

# Create a random sample the size of the population_size to test each algorithm
random_sample = np.random.binomial(population_size, infection_rate, 1)
population = produce_population(random_sample[0], population_size)

# Test each algorithm on the random sample to see how many tests they use
linear_tests = num_tests_used(population, sample_size, "linear")
linear_pooled_tests = num_tests_used(population, sample_size, "linear_pool")
binary_pooled_tests = num_tests_used(population, sample_size, "binary_pool")

# Print the findings of testing the algorithms on a random algorithm
print("")
print("In a random population of ", population_size, "people with the provided infection rate: ")
print("Testing patients linearly in groups of ", best_linear_sample_size, " takes ", linear_tests, " tests.")
print("Testing patients using linear pooling in groups of ", best_linear_pool_sample_size, " takes ", linear_pooled_tests, " tests.")
print("Testing patients using binary pooling in groups of ", best_binary_pool_sample_size, " takes ", binary_pooled_tests, " tests.")