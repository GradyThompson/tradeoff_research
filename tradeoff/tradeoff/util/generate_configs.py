models = ["KJD1", "KJD2", "UJD1", "UJD2"]
params = [0.1*x for x in range(1, 10)]

for model in models:
    for param in params:
        s_param = str(round(param, 3))
        config_file = "model_config\\" + model + "_e" + s_param + ".txt"
        file_line = "schedulers." + model + "," + model + "," + s_param
        with open(config_file, "w") as file:
            file.write(file_line)