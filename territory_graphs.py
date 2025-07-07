# Generate scatter plot for results visualization
"""def gen_graph(X_data, Y_data_1, Y_data_2):
    png_file_name = f"NETLOGO_Territory-12_{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.png"
    plt.figure(figsize=(12, 6))
    sns.scatterplot(x=X_data, y=Y_data_1, hue=Y_data_1, marker="o")
    sns.scatterplot(x=X_data, y=Y_data_2, color="black", marker="X")
    plt.xticks(X_data)
    plt.xlabel("DENSITY OF TREES")
    plt.ylabel("PERCENTAGE OF TREES BURNED")
    plt.title("FUNCTION OF DENSITY OVER TREES BURNED - VERSION 2")
    plt.legend(title="Percentage Burned")
    plt.savefig(png_file_name, dpi=300, bbox_inches='tight')
    plt.show()
    plt.pause(5)
    plt.close()
    logging.info(f"Scatter Plot generated. Graph file saved to {png_file_name}")"""

# density_data = territory_results["Density"]
    # percentage_data = territory_results["Output"]
    # avg_perc_data = territory_results["Avg_Perc_Burned"]
    # gen_graph(density_data, percentage_data, avg_perc_data)  # Generate result graph

def test_function(test_data):
    test_data += 1
    print(f"This is a test function to obtain the data points {test_data}.")