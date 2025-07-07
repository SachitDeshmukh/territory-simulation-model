import logging  # Logging setup for monitoring execution

# Set logging format and level
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Importing the modules
import territory_simulate
import territory_graphs

def main():
    SIM_DONE = True
    GEN_GRAPH = True

    results = territory_simulate.simulate() if (SIM_DONE == GEN_GRAPH) or SIM_DONE else int(3)
    territory_graphs.test_function(results) if GEN_GRAPH else logging.info("The graphs were not generated.")

if __name__ == "__main__":
    main()