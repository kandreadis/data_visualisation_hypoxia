import matplotlib.pyplot as plt
import numpy as np
# from matplotlib import cm
import pandas as pd


def load_data(file_name):
    """
    Load data from .csv log file of MonaLisa
    :param file_name: Name of log file, e.g. "test"
    :return:
    """
    file_loc = "result_data/" + file_name
    dataframe = pd.read_csv(filepath_or_buffer=file_loc, sep="	", dtype=object, header=0)
    data = dataframe.to_numpy()
    data_header = dataframe.columns.to_numpy()[3:-1]
    data_entries = data[3:,3:-1]
    filter_places = ["H+_int_(pH_int)", "CA9", "O2_inverse", "O2"]
    filter_indeces = []
    for i,place in enumerate(data_header):
        if place in filter_places:
            filter_indeces.append(i)
    filter_traces = data_entries[:,filter_indeces].astype(int)
    print("Imported dataframe of shape", filter_traces.shape)
    return filter_places, filter_traces


def plot_save_data(file_name, labels, traces):
    plt.figure(figsize=(10,6))
    for i, label in enumerate(labels):
        plt.plot(traces[:,i], label=label)
    plt.vlines(x=0,ymin=0,ymax=np.max(traces),linestyles="--",colors="0",label="$O_2$ = 2")
    plt.vlines(x=6000,ymin=0,ymax=np.max(traces),linestyles="--",colors="0.4",label="$O_2$ = 0")
    plt.vlines(x=12000,ymin=0,ymax=np.max(traces),linestyles="--",colors="0.7",label="$O_2$ = 2")
    plt.xlabel("Simulation Steps")
    plt.ylabel("Number of Tokens")
    plt.legend()
    file_loc = "figures/" + file_name
    plt.savefig(file_loc, dpi=300)
    plt.show()

file_name = "oxygen_2_0_2_transcription_0.1"
place_names, place_traces = load_data(file_name+".csv")
plot_save_data(file_name=file_name+".png", labels=place_names, traces=place_traces)