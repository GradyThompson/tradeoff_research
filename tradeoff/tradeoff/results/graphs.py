from results import result_manager

result_data_folder = "result_data\\"
job_set = "js1"
schedulers = ["FIFO_c100", "KJD1", "KJD2", "UJD1", "UJD2", "rl_rr01_m100", "rl_rr02_m100", "rl_rr03_m100",
              "rl_rr04_m100", "rl_rr06_m100", "rl_rr09_m100", "rl_rr13_m100", "rl_rr19_m100", "rl_rr28_m100",
              "rl_rr41_m100"]
scheduler_data = {}
for scheduler in schedulers:
    scheduler_data[scheduler] = result_data_folder + scheduler + "_" + job_set + ".txt"

result_manager.plot_max_queue_v_cost(scheduler_data)