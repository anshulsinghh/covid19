import numpy as np
from algos import linear_pooled, binary_pool, linear
import sys

"""
This method takes in the number of people infected by COVID-19, and the overall
population size. It then produces of randomly indexed 1s and 0s corresponding to
to infected and non-infected people respectively.

@params num_infected the number of people infected in the population
@params population_size the number of people in the population

@return an array composing of randomly indexed 1s and 0s (the 1s represent
people with COVID-19 and the 0s represent people who do not have COVID-19)
"""
def produce_population(num_infected, population_size):
  population = [1]*num_infected+[0]*(population_size - num_infected)
  np.random.shuffle(population)
  return population


"""
This method takes in an array of patient samples, given as an array of 1s and 0s.
(1s represent positive tests, 0s represent negative tests). It then takes in the
sample size being used to iterate through the samples, and the test type. It then
tests the sample using the given sample spacings, and the specified test type.

@params patient_samples an array of 1s and 0s which represent positive and negative
COVID-19 test results.
@params sample_size the sample size at which samples are grouped to be tested from
teh patient_samples array
@params test_type the type of test that will be used

@return the number of tests used, given the samples array, the test type, and the
sampling size
"""
def num_tests_used(patient_samples, sample_size, test_type):
  tests_used = 0
  for i in range(0, len(patient_samples), sample_size):
    sample = patient_samples[i:i+sample_size]

    if test_type == "linear_pool":
      tests_used += linear_pooled(sample)
    
    if test_type == "binary_pool":
      tests_used += binary_pool(sample)
    
    if test_type == "linear":
      tests_used += linear(sample)
  
  return tests_used


"""
This class keeps track of the best averages for each algorithm, and the best
sampling size based on teh best averages for each algorithm. This class particularly
simplifies the code in the script.py file, where we need to keep track of the best
sampling size for each algorithm, and the lowest number of samples used by each algorithm.
"""
class BestSampleSizes:
  def __init__(self, starting_sample):
    self.best_binary_pool_avg = sys.maxsize
    self.best_linear_pool_avg = sys.maxsize
    self.best_linear_avg = sys.maxsize

    self.best_binary_pool_sample_size = starting_sample
    self.best_linear_pool_sample_size = starting_sample
    self.best_linear_sample_size = starting_sample

  def get_best_linear_pool(self):
    return self.best_linear_pool_sample_size

  def get_best_binary_pool(self):
    return self.best_binary_pool_sample_size

  def get_best_linear(self):
    return self.best_linear_sample_size
  
  def update_linear_pool(self, new_avg, sample_size):
    if new_avg < self.best_linear_pool_avg:
      self.best_linear_pool_sample_size = sample_size
      self.best_linear_pool_avg = new_avg

  def update_binary_pool(self, new_avg, sample_size):
    if new_avg < self.best_binary_pool_avg:
      self.best_binary_pool_avg = new_avg
      self.best_binary_pool_sample_size = sample_size

  def update_linear(self, new_avg, sample_size):
    if new_avg < self.best_linear_avg:
      self.best_linear_avg = new_avg
      self.best_linear_sample_size = sample_size