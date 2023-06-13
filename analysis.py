import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

step_block_size = 15000


def load_data(file_name):
    """
    Load data from .csv log file of MonaLisa.
    :param file_name: Name of log file, e.g. "test"
    :return: Filtered place names and tokens over time
    """
    file_loc = "result_data/" + file_name
    dataframe = pd.read_csv(filepath_or_buffer=file_loc, sep="	", dtype=object, header=0)
    data = dataframe.to_numpy()
    data_header = dataframe.columns.to_numpy()[3:-1]
    data_entries = data[3:, 3:-1]
    # filter_places = ["H+_int_(pH_int)", "CA9", "O2_inverse", "O2", "H+_ext_(pH_ext)"]
    # filter_places = ["H+_int_(pH_int)", "CA9", "O2", "H+_ext_(pH_ext)"]
    filter_places = ["H+_int_(pH_int)", "CA9", "O2"]
    filter_indeces = []
    for i, place in enumerate(data_header):
        if place in filter_places:
            filter_indeces.append(i)
    filter_traces = data_entries[:, filter_indeces].astype(int)
    print("Imported dataframe of shape", filter_traces.shape)
    return filter_places, filter_traces


def plot_save_data(file_name, labels, traces):
    """
    Visualise place token traces.
    :param file_name: Name of log file, e.g. "test
    :param labels: Place names (filtered)
    :param traces: Place token traces (filtered)
    :return:
    """
    plt.figure(figsize=(10, 6))
    for i, trace_label in enumerate(labels):
        print(trace_label)
        plt.plot(traces[:, i], label=trace_label)

    oxygen_vals = np.flip(np.arange(0, 2.5, 0.5))
    for i, o_val in enumerate(oxygen_vals):
        plt.vlines(x=(i / len(oxygen_vals)) * traces.shape[0], ymin=0, ymax=np.max(traces), linestyles="--",
                   label=str(o_val), colors=str(i / len(oxygen_vals)))
    plt.xlabel("Simulation Steps")
    plt.ylabel("Number of Tokens")
    plt.legend()
    file_loc = "figures/" + file_name
    plt.savefig(file_loc, dpi=300)
    plt.show()


file_name = "oxygen_sweep"
place_names, place_traces = load_data(file_name + ".csv")
plot_save_data(file_name=file_name + ".png", labels=place_names, traces=place_traces)
