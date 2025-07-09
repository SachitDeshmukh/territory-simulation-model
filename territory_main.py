import logging  # Logging setup for monitoring execution

# Set logging format and level
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Importing the modules
import territory_simulate
import territory_graphs

def main():
    SIM_DONE = True # user to define before each simulation
    GEN_GRAPH = True # user to define before each simulation

    while GEN_GRAPH:
        if not SIM_DONE:
            results = territory_simulate.simulate() # simulate the NETLOGO model if not simulated before
        else:
            results = territory_graphs.load_data() # load pre-existing data from Excel sheet
        territory_graphs.test_function(results)
        GEN_GRAPH = False
    else:
        if not SIM_DONE:
            territory_simulate.simulate()
        logging.info("The graphs were not generated.")

if __name__ == "__main__":
    main()