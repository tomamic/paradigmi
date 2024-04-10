from pyspark import SparkContext
sc = SparkContext.getOrCreate()

import random
num_samples = 1_000_000

def inside(p):
    x, y = random.random(), random.random()
    return x*x + y*y < 1

count = sc.parallelize(range(num_samples)).filter(inside).count()

pi = 4 * count / num_samples
print(pi)

sc.stop()