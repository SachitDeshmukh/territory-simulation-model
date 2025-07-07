import os  # Importing OS module for file operations
import pandas as pd  # Import Pandas for data processing
import numpy as np # Import Numpy
import logging  # Logging setup for monitoring execution
import time  # Time module for delays
import jpype  # Interface for Java-Python interactions
from datetime import datetime  # Date/time handling utilities
from itertools import product  # Cartesian product for param combinations
from joblib import Parallel, delayed  # Parallel execution for simulations
from pynetlogo import NetLogoLink  # Interface for NetLogo simulations
import matplotlib.pyplot as plt  # Plotting graphs with Matplotlib
import seaborn as sns  # Enhanced visualization with Seaborn

# Set logging format and level
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Importing the modules
import territory_simulate
import territory_graphs

def main():
    SIM_DONE = True
    GEN_GRAPH = True

    results = territory_simulate.simulate() if (SIM_DONE == GEN_GRAPH) or SIM_DONE else results = 3
    territory_graphs.test_function(results) if GEN_GRAPH else logging.info("The graphs were not generated.")

if __name__ == "__main__":
    main()