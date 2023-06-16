import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def load_data(file_name, filter_places):
    """
    Load data from .csv log file of MonaLisa.
    :param filter_places:
    :param file_name: Name of log file, e.g. "test"
    :return: Filtered place names and tokens over time
    """
    file_loc = "result_data/" + file_name
    dataframe = pd.read_csv(filepath_or_buffer=file_loc, sep="	", dtype=object, header=0)
    data = dataframe.to_numpy()
    data_header = dataframe.columns.to_numpy()[3:-1]
    data_entries = data[3:, 3:-1]
    filter_places.append("normoxia")
    filter_places.append("hypoxia")
    filter_places = np.asarray(filter_places)
    filter_indeces = np.empty((len(filter_places)))
    for i, place in enumerate(data_header):
        if place in filter_places:
            filter_indeces[int(np.where(filter_places == place)[0])] = i
    filter_indeces = filter_indeces.tolist()
    filter_indeces = [int(filter_indeces) for filter_indeces in filter_indeces]
    filter_traces = data_entries[:, filter_indeces].astype(int)
    print("Imported dataframe of shape", filter_traces.shape)
    return filter_places, filter_traces


def plot_save_data(file_name, labels, traces, oxygen_phases, oxygen_vals):
    """
    Visualise place token traces.
    :param oxygen_vals:
    :param oxygen_phases:
    :param file_name: Name of log file, e.g. "test
    :param labels: Place names (filtered)
    :param traces: Place token traces (filtered)
    :return:
    """
    plt.figure(figsize=(14, 6))
    plt.fill_between(range(traces.shape[0]), 0, np.max(traces), where=traces[:, -1], color="red", alpha=0.1)
    plt.fill_between(range(traces.shape[0]), 0, np.max(traces), where=traces[:, -2], color="green", alpha=0.1)
    for i, trace_label in enumerate(labels[:-2]):
        if trace_label == "H+_int_(pH_int)":
            trace_label = "$H^{+}_{int}$ (inverse pH$_{int}$)"
        if trace_label == "CA9":
            trace_label = "CA$_9$ expression"
        if trace_label == "O2":
            trace_label = "O$_2$ level"

        plt.plot(traces[:, i], label=trace_label, alpha=0.8)

    if oxygen_phases == True:
        for i, o_val in enumerate(oxygen_vals):
            if i == 0:
                phase_label = "O$_2$ supply multiplier = {}".format(str(o_val))
            else:
                phase_label = "{}".format(str(o_val))
            plt.vlines(x=(i / len(oxygen_vals)) * traces.shape[0], ymin=0, ymax=np.max(traces), linestyles="--",
                       label=phase_label, colors=str(i / len(oxygen_vals)))
    if oxygen_phases == "anaerobic":
        for i, o_val in enumerate(oxygen_vals):
            if i == 0:
                phase_label = "anaerobic $H^{+}_{int}$ " + "buildup multiplier = {}".format(str(o_val))
            else:
                phase_label = "{}".format(str(o_val))
            plt.vlines(x=(i / len(oxygen_vals)) * traces.shape[0], ymin=0, ymax=np.max(traces), linestyles="--",
                       label=phase_label, colors=str(i / len(oxygen_vals)))
    plt.xlabel("Simulation Steps")
    plt.ylabel("Number of Tokens")
    plt.legend()
    file_loc = "figures/" + file_name
    plt.savefig(file_loc, dpi=300)
    plt.show()


oxygen_phases = True
oxygen_vals = np.flip(np.arange(0, 2.5, 0.5))
hypox_normox_hypox = np.array([0, 2, 0])

data_dict = {
    "normal_sweep": [True, oxygen_vals, ["H+_int_(pH_int)", "CA9", "O2"]],
    "anaerobic": ["anaerobic", np.array([1, 0.9, 0.8, 0.7, 0.6]), ["H+_int_(pH_int)", "CA9"]],
    "inhibited_CA9_translation_sweep": [True, oxygen_vals, ["H+_int_(pH_int)", "CA9", "O2"]],
    "memory_effect": [True, hypox_normox_hypox, ["H+_int_(pH_int)", "CA9", "O2"]],
    "intermediate": [False, None, ["H+_int_(pH_int)", "CA9", "O2"]]
}

for data in data_dict:
    place_names, place_traces = load_data(data + ".csv", filter_places=data_dict[data][2])
    plot_save_data(file_name=data + ".png", labels=place_names, traces=place_traces, oxygen_phases=data_dict[data][0],
                   oxygen_vals=data_dict[data][1])
