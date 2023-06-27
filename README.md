# Packet Monitor Drop Counter Plotter

This is a Python script that uses the [Packet Monitor](https://docs.microsoft.com/en-us/windows-server/networking/technologies/pktmon/pktmon) tool to collect and plot the drop counters on a Windows system. It requires Python 3 and matplotlib.

## How it works

The script does the following steps:

- It starts the Packet Monitor tool in capture mode with the `-c` and `-o` options to enable drop counters and output to stdout.
- It creates a multiprocessing queue and a process to plot the data using matplotlib.
- It runs a loop that calls the `get_drop_counters` function every second. This function uses subprocess to run the `pktmon counters --type drop --json` command and parses the output as JSON. It returns a dictionary of counter names and values.
- It puts the dictionary of counters into the queue for the plotting process to consume.
- It updates the plot with the new data every second, using datetime objects for the x-axis and summing up all the counter values for the y-axis.
- It stops the Packet Monitor tool when the script is interrupted or terminated.

## How to use it

To run the script, you need to have Python 3 and matplotlib installed. You can install matplotlib using pip:

```bash
pip install matplotlib
```

You also need to have administrator privileges to run the Packet Monitor tool.

To run the script, simply execute it from the command line:

```bash
python pktmon_drop_counter_plotter.py
```

You should see a plot window showing the total number of dropped packets over time. You can close the window or press Ctrl-C to stop the script.