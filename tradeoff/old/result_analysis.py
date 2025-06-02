import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from scipy.optimize import curve_fit
import math

results_folder = "./results/"

def fit_funct(x, p1, p2, p3, p4):
    return p1 + p2/x + p3*x + p4*x**2

def cost_vs_max_time(file):
    df = pd.read_csv(file)

    fifo_xs = []
    fifo_ys = []
    bounded_xs = []
    bounded_ys = []
    deterministic_xs = []
    deterministic_ys = []

    for index, row in df.iterrows():
        if "deterministic" in row["algorithm"].lower():
            qt = row["queue_times"]
            y = row["cost"]
            x = max([float(t) for t in qt[1:-1].split(",")])
            deterministic_xs.append(x)
            deterministic_ys.append(y)
        if "bounded" in row["algorithm"].lower():
            qt = row["queue_times"]
            y = row["cost"]
            x = max([float(t) for t in qt[1:-1].split(",")])
            bounded_xs.append(x)
            bounded_ys.append(y)
        if "edf" in row["algorithm"].lower():
            qt = row["queue_times"]
            y = row["cost"]
            x = max([float(t) for t in qt[1:-1].split(",")])
            fifo_xs.append(x)
            fifo_ys.append(y)

    plt.scatter(bounded_xs, bounded_ys, color="r", label="bounded")
    plt.scatter(deterministic_xs, deterministic_ys, color="b", label="deterministic")
    plt.scatter(fifo_xs, fifo_ys, color="g", label="fifo")

    plt.ylim(5900, 7000)
    plt.legend()
    plt.ylabel("Cost")
    plt.xlabel("Maximum buffer time (q*)")
    plt.show()

def cost_vs_max_time_optimal(file):
    df = pd.read_csv(file)

    fifo_xs = []
    fifo_ys = []
    bounded_xs = []
    bounded_ys = []
    deterministic_xs = []
    deterministic_ys = []
    optimal_xs = []
    optimal_ys = []
    double_xs = []
    double_ys = []

    for index, row in df.iterrows():
        if "deterministic" in row["algorithm"].lower():
            qt = row["queue_times"]
            y = row["cost"]
            x = np.max([float(t) for t in qt[1:-1].split(",")])*100
            deterministic_xs.append(x)
            deterministic_ys.append(y)
        if "bounded" in row["algorithm"].lower():
            qt = row["queue_times"]
            y = row["cost"]
            x = np.max([float(t) for t in qt[1:-1].split(",")])*100
            bounded_xs.append(x)
            bounded_ys.append(y)
        if "double" in row["algorithm"].lower():
            qt = row["queue_times"]
            y = row["cost"]
            x = np.max([float(t) for t in qt[1:-1].split(",")])*100
            double_xs.append(x)
            double_ys.append(y)
        if "edf" in row["algorithm"].lower():
            qt = row["queue_times"]
            y = row["cost"]
            x = np.max([float(t) for t in qt[1:-1].split(",")])*100
            fifo_xs.append(x)
            fifo_ys.append(y)
        if "optimal" in row["algorithm"].lower():
            y = row["cost"]
            x = float(row["queue_times"][1:-1])*100
            optimal_xs.append(x)
            optimal_ys.append(y)

    plt.scatter(optimal_xs, optimal_ys, color="tab:olive", label="Optimal")
    plt.scatter(bounded_xs, bounded_ys, color="r", label="UJD2")
    plt.scatter(deterministic_xs, deterministic_ys, color="b", label="KJD2")
    plt.scatter(fifo_xs, fifo_ys, color="g", label="FIFO Fixed")
    plt.scatter(double_xs, double_ys, color="tab:grey", label="UJD1")

    plt.xlim(0, 180000)
    plt.ylim(5900, 7000)
    plt.legend()
    plt.xlabel("Maximum buffer time (q*)")
    plt.ylabel("Cost")
    plt.show()

def cost_vs_max_time_optimal_line(file):
    df = pd.read_csv(file)

    fifo_xs = []
    fifo_ys = []
    bounded_xs = []
    bounded_ys = []
    deterministic_xs = []
    deterministic_ys = []
    optimal_xs = []
    optimal_ys = []
    double_xs = []
    double_ys = []

    for index, row in df.iterrows():
        if "deterministic" in row["algorithm"].lower():
            qt = row["queue_times"]
            y = row["cost"]
            x = np.max([float(t) for t in qt[1:-1].split(",")])*100
            deterministic_xs.append(x)
            deterministic_ys.append(y)
        if "bounded" in row["algorithm"].lower():
            qt = row["queue_times"]
            y = row["cost"]
            x = np.max([float(t) for t in qt[1:-1].split(",")])*100
            bounded_xs.append(x)
            bounded_ys.append(y)
        if "double" in row["algorithm"].lower():
            qt = row["queue_times"]
            y = row["cost"]
            x = np.max([float(t) for t in qt[1:-1].split(",")])*100
            double_xs.append(x)
            double_ys.append(y)
        if "edf" in row["algorithm"].lower():
            qt = row["queue_times"]
            y = row["cost"]
            x = np.max([float(t) for t in qt[1:-1].split(",")])*100
            fifo_xs.append(x)
            fifo_ys.append(y)
        if "optimal" in row["algorithm"].lower():
            y = row["cost"]
            x = float(row["queue_times"][1:-1])*100
            optimal_xs.append(x)
            optimal_ys.append(y)

    plt.plot(optimal_xs, optimal_ys, color="tab:olive", label="Optimal")
    plt.plot(bounded_xs, bounded_ys, color="r", label="UJD2")
    plt.plot(deterministic_xs, deterministic_ys, color="b", label="KJD2")
    #plt.plot(fifo_xs, fifo_ys, color="g", label="FIFO Fixed")
    #plt.plot(double_xs, double_ys, color="tab:grey", label="UJD1")

    plt.xlim(0, 10000)
    plt.ylim(5900, 7000)
    plt.legend()
    plt.xlabel("Maximum buffer time (q*)")
    plt.ylabel("Cost")
    plt.show()

def cost_vs_avg_time(file):
    df = pd.read_csv(file)

    fifo_xs = []
    fifo_ys = []
    bounded_xs = []
    bounded_ys = []
    deterministic_xs = []
    deterministic_ys = []
    double_xs = []
    double_ys = []

    for index, row in df.iterrows():
        if "deterministic" in row["algorithm"].lower():
            qt = row["queue_times"]
            y = row["cost"]
            x = np.average([float(t) for t in qt[1:-1].split(",")])*100
            deterministic_xs.append(x)
            deterministic_ys.append(y)
        if "bounded" in row["algorithm"].lower():
            qt = row["queue_times"]
            y = row["cost"]
            x = np.average([float(t) for t in qt[1:-1].split(",")])*100
            bounded_xs.append(x)
            bounded_ys.append(y)
        if "edf" in row["algorithm"].lower():
            qt = row["queue_times"]
            y = row["cost"]
            x = np.average([float(t) for t in qt[1:-1].split(",")])*100
            fifo_xs.append(x)
            fifo_ys.append(y)
        if "double" in row["algorithm"].lower():
            qt = row["queue_times"]
            y = row["cost"]
            x = np.max([float(t) for t in qt[1:-1].split(",")])*100
            double_xs.append(x)
            double_ys.append(y)

    plt.scatter(bounded_xs, bounded_ys, color="r", label="UJD2")
    plt.scatter(deterministic_xs, deterministic_ys, color="b", label="KJD2")
    plt.scatter(fifo_xs, fifo_ys, color="g", label="FIFO Fixed")
    plt.scatter(double_xs, double_ys, color="tab:grey", label="UJD1")

    plt.xlim(0, 180000)
    plt.ylim(5900, 7000)
    plt.legend()
    plt.ylabel("Cost")
    plt.xlabel("Average queue time")
    plt.show()

def cost_vs_avg_time_line(file):
    df = pd.read_csv(file)

    fifo_xs = []
    fifo_ys = []
    bounded_xs = []
    bounded_ys = []
    deterministic_xs = []
    deterministic_ys = []
    double_xs = []
    double_ys = []

    for index, row in df.iterrows():
        if "deterministic" in row["algorithm"].lower():
            qt = row["queue_times"]
            y = row["cost"]
            x = np.average([float(t) for t in qt[1:-1].split(",")])*100
            deterministic_xs.append(x)
            deterministic_ys.append(y)
        if "bounded" in row["algorithm"].lower():
            qt = row["queue_times"]
            y = row["cost"]
            x = np.average([float(t) for t in qt[1:-1].split(",")])*100
            bounded_xs.append(x)
            bounded_ys.append(y)
        if "edf" in row["algorithm"].lower():
            qt = row["queue_times"]
            y = row["cost"]
            x = np.average([float(t) for t in qt[1:-1].split(",")])*100
            fifo_xs.append(x)
            fifo_ys.append(y)
        if "double" in row["algorithm"].lower():
            qt = row["queue_times"]
            y = row["cost"]
            x = np.average([float(t) for t in qt[1:-1].split(",")])*100
            double_xs.append(x)
            double_ys.append(y)

    plt.plot(bounded_xs, bounded_ys, color="r", label="UJD2")
    plt.plot(deterministic_xs, deterministic_ys, color="b", label="KJD2")
    plt.plot(fifo_xs, fifo_ys, color="g", label="FIFO Fixed")
    plt.plot(double_xs, double_ys, color="tab:grey", label="UJD1")

    plt.xlim(0, 180000)
    plt.ylim(5900, 7000)
    plt.legend()
    plt.ylabel("Cost")
    plt.xlabel("Average queue time")
    plt.show()

def normalized_cost_vs_max_time(file):
    df = pd.read_csv(file)

    fifo_xs = []
    fifo_ys = []
    bounded_xs = []
    bounded_ys = []
    deterministic_xs = []
    deterministic_ys = []
    optimal_xs = []
    optimal_ys = []
    double_xs = []
    double_ys = []

    for index, row in df.iterrows():
        if "deterministic" in row["algorithm"].lower():
            qt = row["queue_times"]
            y = row["cost_ratio"]
            x = np.max([float(t) for t in qt[1:-1].split(",")])*100
            deterministic_xs.append(x)
            deterministic_ys.append(y)
        if "bounded" in row["algorithm"].lower():
            qt = row["queue_times"]
            y = row["cost_ratio"]
            x = np.max([float(t) for t in qt[1:-1].split(",")])*100
            bounded_xs.append(x)
            bounded_ys.append(y)
        if "edf" in row["algorithm"].lower():
            qt = row["queue_times"]
            y = row["cost_ratio"]
            x = np.max([float(t) for t in qt[1:-1].split(",")])*100
            fifo_xs.append(x)
            fifo_ys.append(y)
        if "double" in row["algorithm"].lower():
            qt = row["queue_times"]
            y = row["cost_ratio"]
            x = np.max([float(t) for t in qt[1:-1].split(",")])*100
            double_xs.append(x)
            double_ys.append(y)
        if "optimal" in row["algorithm"].lower():
            y = row["cost_ratio"]
            x = float(row["queue_times"][1:-1])
            optimal_xs.append(x)
            optimal_ys.append(y)

    plt.plot(optimal_xs, optimal_ys, color="tab:olive", label="Optimal")
    plt.plot(bounded_xs, bounded_ys, color="r", label="UJD2")
    plt.plot(deterministic_xs, deterministic_ys, color="b", label="KJD2")
    plt.plot(fifo_xs, fifo_ys, color="g", label="FIFO Fixed")
    plt.plot(double_xs, double_ys, color="tab:grey", label="UJD1")

    plt.xlim(0, 20000)
    plt.legend()
    plt.ylabel("Cost ratio")
    plt.xlabel("Maximum buffer time (q*)")
    plt.show()

def queue_time_cdf(file):
    df = pd.read_csv(file)

    epsilon = "0.01923"

    for index, row in df.iterrows():
        if "deterministic" in row["algorithm"].lower() and epsilon in row["algorithm"].lower():
            qt = row["queue_times"]
            xs = [float(t) for t in qt[1:-1].split(",")]
            plt.hist(xs, len(xs)//4, density=True, cumulative=True, histtype='step', alpha=0.8, color='r', label="KJD2")
        if "bounded" in row["algorithm"].lower() and epsilon in row["algorithm"].lower():
            qt = row["queue_times"]
            xs = [float(t) for t in qt[1:-1].split(",")]
            plt.hist(xs, len(xs)//4, density=True, cumulative=True, histtype='step', alpha=0.8, color='b', label="UJD2")

    plt.legend()
    plt.xlabel("Queue time")
    plt.ylabel("CDF")
    plt.show()


test1 = results_folder + "test1.csv"
FIFO_test = results_folder + "FIFO.csv"
bounded_test = results_folder + "bounded.csv"
determinsitic_test = results_folder + "deterministic.csv"
det_bound_test = results_folder + "det_bound.csv"
test = results_folder + "test.csv"
final = results_folder + "final.csv"
final_zoomed = results_folder + "final_zoomed.csv"

# queue_time_cdf(final_zoomed)
# cost_vs_avg_time(final_zoomed)
# cost_vs_avg_time_line(final_zoomed)
# cost_vs_max_time_optimal(final_zoomed)
cost_vs_max_time_optimal_line(final_zoomed)
# normalized_cost_vs_max_time(final)
# normalized_cost_vs_max_time(final_zoomed)
#cost_vs_avg_time(test2)