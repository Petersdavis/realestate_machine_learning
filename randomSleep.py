from random import seed
from random import random
import time

def sleep(scalar):
    seed(time.time())
    irregularTimeout = random() * scalar
    time.sleep(irregularTimeout)