import logging  # Logging setup for monitoring execution
import msvcrt # To work with keyboard input

# Set logging format and level
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Importing the modules
import territory_simulate
import territory_graphs

def ask_yes_no_keypress(prompt):
    print(prompt, end='', flush=True)
    while True:
        key = msvcrt.getch().decode('utf-8').lower()
        if key == 'y':
            print('Y')
            return True
        elif key == 'n':
            print('N')
            return False

def main():
    SIM_DONE = ask_yes_no_keypress("Is the simulation already complete? [Y/N]: ") # user to define before each simulation
    GEN_GRAPH = ask_yes_no_keypress("Do you want to generate the graphs? [Y/N]: ") # user to define before each simulation

    while GEN_GRAPH:
        if not SIM_DONE:
            results = territory_simulate.simulate() # simulate the NETLOGO model if not simulated before
        else:
            results = territory_graphs.load_data() # load pre-existing data from Excel sheet
        territory_graphs.gen_graphs(results)
        GEN_GRAPH = False
    else:
        if not SIM_DONE:
            territory_simulate.simulate()
        logging.info("The graphs were not generated.")

if __name__ == "__main__":
    main()