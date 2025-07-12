import os  # Importing OS module for file operations
import pandas as pd  # Import Pandas for data processing
import numpy as np # Import Numpy
import matplotlib.pyplot as plt  # Plotting graphs with Matplotlib
import logging  # Logging setup for monitoring execution
import territory_config # Importing the simulation module
from datetime import datetime  # Date/time handling utilities

def load_data():
    while True:
        file_input = input("Please enter the name of Excel file with the data: ")
        if os.path.exists(os.path.join(territory_config.main_dir, file_input)) == False:
            print("This file name is incorrect.")
            continue
        else:    
            source_file = pd.ExcelFile(file_input)
            break

    while True:
        source_sheet = input("Please enter the name of Excel sheet with the data: ")
        if not source_sheet in source_file.sheet_names:
            print("This sheet name is incorrect.")
            continue
        else:
            results = pd.read_excel(source_file, sheet_name=source_sheet)
            logging.info("Successfully loaded data.")
            break
    return results

def reshape_data(data):
    data = pd.DataFrame(data)

    id_vars = territory_config.id_cols
    melt_cols = [col for col in data.columns if col.endswith(territory_config.column_suffix)]
    var_name = territory_config.var_col
    value_name = territory_config.value_col

    reshape_data = pd.melt(data, id_vars=id_vars, value_vars=melt_cols, var_name=var_name, value_name=value_name, ignore_index=False)
    reshape_data[var_name] = reshape_data[var_name].str.replace(territory_config.column_suffix, "", regex=False)
    return reshape_data

def prep_graph(data):
    data = pd.DataFrame(data)
    y_values = {}

    for combo in sorted(data["Combo"].unique()):
        values = data.loc[data["Combo"] == combo, territory_config.value_col]
        y_values[f"Combination {combo+1}"] = list(values)

    return y_values

def gen_graphs(raw_data):
    clean_data = reshape_data(raw_data)   
    y_data = prep_graph(clean_data)
    x_data = territory_config.X_data

    plt.figure(figsize=(12, 6))
    for label, y_combo in y_data.items():
        plt.plot(x_data, y_combo, label=label)
    plt.xlabel(territory_config.X_label)
    plt.ylabel(territory_config.Y_label)
    plt.legend()
    plt.title(territory_config.graph_title)

    png_file = f"{territory_config.file_name}_{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.png"
    plt.savefig(png_file, dpi=300, bbox_inches='tight')

    logging.info(f"Graph generated. File saved to {png_file}")