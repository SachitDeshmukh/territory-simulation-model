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

MAIN_DIR = r"C:\Users\Sachit Deshmukh\Documents\Python Scripts\Territory-model-Ishwari"
INPUT_PARAMS = {
            "num-green-clan": [15, 20, 25, 30],
            "num-blue-clan": [15, 20, 25, 30],
            "green-hostile?": [False],
            "yellow-hostile?": [False],
            "blue-hostile?": [False],
            "red-hostile?": [False]
        }

# Function to introduce a delay
def rest():
    time.sleep(3)

# Generate all possible parameter combinations
def gen_param_combos(all_params):
    return [dict(zip(all_params.keys(), values)) for values in product(*all_params.values())]

# Save simulation data in CSV and Excel formats
def save_data(data, backup_file_name, sheet_prefix):
    data.to_csv(f"{backup_file_name}.csv")

    xlsx_file_name = f"NETLOGO_Territory-12_{datetime.now().strftime('%Y-%m-%d')}.xlsx"

    mode = 'a' if os.path.exists(xlsx_file_name) else 'w'
    with pd.ExcelWriter(xlsx_file_name, mode=mode, engine='openpyxl') as writer:
        data.to_excel(writer, sheet_name=f"{sheet_prefix}_{datetime.now().strftime("%H-%M-%S")}", index=False)

    logging.info(f"RESULTED SAVED TO {xlsx_file_name}")

# NetLogo simulation class handling execution
class NetLogoSim:
    def __init__(self, parameters, runs, ticks):
        self.params = parameters  # Store parameter combinations
        self.runs = runs  # Define the number of simulation runs
        self.max_ticks = ticks
        self.tick_start = 0
        self.tick_step = 50

    # Run simulation for a parameter combination
    def params_stability(self, combo, iter):
        netlogo = NetLogoLink(gui=False, netlogo_home=r"C:\Users\Sachit Deshmukh\AppData\Local\NetLogo")
        netlogo.load_model(r"C:\Users\Sachit Deshmukh\Documents\Python Scripts\Territory-model-Ishwari\12-Territory-model-with-multiple-clans.nlogo")

        combo_serial = self.params.index(combo)
        try:
            for param, value in combo.items():
                netlogo.command(f"set {param} {value}")  # Set model parameters

            netlogo.command("setup")  # Initialize simulation

            results = {
                "Combo": combo_serial,
                "Iteration": iter+1,
                "Blue-Count-start": combo.get("num-green-clan"),
                "Green-Count-start": combo.get("num-blue-clan")
                }

            for tick_target in range(self.tick_start, self.max_ticks, self.tick_step):
                while netlogo.report("ticks") < tick_target and netlogo.report("count turtles") > 0:
                    netlogo.command("go")
                if netlogo.report("count turtles") > 0:
                    results[f"Green-Territory-{tick_target}"] = netlogo.report("count green-patches")
                    results[f"Blue-Territory-{tick_target}"] = netlogo.report("count blue-patches")
                else:
                    # If all turtles are dead before this tick, record NA
                    results[f"Green-Territory-{tick_target}"] = np.nan
                    results[f"Blue-Territory-{tick_target}"] = np.nan
            
            logging.info(f"Combination {combo_serial} iteration {iter+1} complete.")
        
        except Exception as e:
            logging.error(f"Simulation error with params {combo}: {e}")
            return None  # Ensure failed runs don’t corrupt output
        
        finally:
            netlogo.kill_workspace()  # Close NetLogo workspace

        return results

    # Filter valid results and compute averages
    def filter_params(self, results):
        results = [res for res in results if res is not None]
        result_data = pd.DataFrame(results)
        for i in range(self.tick_start, self.max_ticks, self.tick_step):
            green_avg_territory = result_data.groupby("Combo")[f"Green-Territory-{i}"].mean().reset_index()
            green_avg_territory.rename(columns={f"Green-Territory-{i}": f"Green-Avg-Territory-{i}"}, inplace=True)
            blue_avg_territory = result_data.groupby("Combo")[f"Blue-Territory-{i}"].mean().reset_index()
            blue_avg_territory.rename(columns={f"Blue-Territory-{i}": f"Blue-Avg-Territory-{i}"}, inplace=True)
            result_data = result_data.merge(green_avg_territory, on="Combo").merge(blue_avg_territory, on="Combo")         
        return result_data
    
    def clean_data_ratio(self, dataset):
        dataset = pd.DataFrame(dataset)
        dataset = dataset.drop_duplicates(subset=["Combo", "Blue-Count-start", "Green-Count-start"])
        clean_data = dataset[["Combo", "Blue-Count-start", "Green-Count-start"]].copy()
        for i in range(self.tick_start, self.max_ticks, self.tick_step):
            clean_data[f"{i}_avg_ratio"] = (dataset[f"Green-Avg-Territory-{i}"]/dataset[f"Blue-Avg-Territory-{i}"]).fillna(1.0)
        return clean_data

# Main execution function
def simulate():
    os.chdir(MAIN_DIR)  # Change working directory to main directory

    if not jpype.isJVMStarted():
        jpype.startJVM()  # Start Java Virtual Machine

    try:
        logging.info(f"Starting iteration...")
        param_combinations = gen_param_combos(INPUT_PARAMS)
        start_time_temp = datetime.now()
        simulation = NetLogoSim(param_combinations, runs=20, ticks=301)  # Initialize simulation object
        iter_data = Parallel(n_jobs=6, backend="multiprocessing")(
            delayed(simulation.params_stability)(combo, x) for combo in simulation.params for x in range(simulation.runs)
        )  # Run simulations in parallel
        end_time_temp = datetime.now()
        time.sleep(3)
        total_time = (end_time_temp - start_time_temp).total_seconds()
        logging.info(f"Time taken: {total_time}.")

    finally:
        logging.info("CLEANING UP RESOURCES...")
        jpype.shutdownJVM()  # Shut down Java Virtual Machine

    logging.info("ALL SIMULATIONS COMPLETE.")

    territory_results = simulation.filter_params(iter_data)
    save_data(territory_results, backup_file_name="Territory_output_raw", sheet_prefix="RAW")

    clean_results = simulation.clean_data_ratio(territory_results)
    save_data(clean_results, backup_file_name="Territory_output_clean", sheet_prefix="CLEAN")

    return clean_results