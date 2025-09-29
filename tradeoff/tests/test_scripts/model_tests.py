from tests.test_scripts.end_to_end import end_to_end_model_test

"""
FIFO Test 1

Runs the FIFO scheduling model on a job set stored in the file FIFO_t1.txt and compares the output schedule to the 
expected

container number = 10
"""
def fifo_test_1():
    print("FIFO test 1")
    startup_duration: int = 1
    model_config_file:str = "model_config/FIFO_c10.txt"
    expected_file:str = "tests/expected/FIFO_t1.txt"
    jobs_file:str = "tests/job_sets/FIFO_t1.txt"
    results_file:str = "tests/results/FIFO_t1.txt"
    end_to_end_model_test(startup_duration=startup_duration,
                          model_config_file=model_config_file,
                          results_file=results_file,
                          jobs_file=jobs_file,
                          expected_file_name=expected_file)
    print()

"""
KJD1 Test 1

Runs the KJD1 scheduling model on a job set stored in the file KJD1_t1.txt and compares the output schedule to the 
expected

epsilon = 0.5
"""
def kjd1_test_1():
    print("KJD1 test 1")
    startup_duration: int = 1
    model_config_file:str = "model_config/KJD1_e0.5.txt"
    expected_file:str = "tests/expected/KJD1_t1.txt"
    jobs_file:str = "tests/job_sets/KJD1_t1.txt"
    results_file:str = "tests/results/KJD1_t1.txt"
    end_to_end_model_test(startup_duration=startup_duration,
                          model_config_file=model_config_file,
                          results_file=results_file,
                          jobs_file=jobs_file,
                          expected_file_name=expected_file)
    print()

"""
KJD2 Test 1

Runs the KJD2 scheduling model on a job set stored in the file KJD2_t1.txt and compares the output schedule to the 
expected

epsilon = 0.5
"""
def kjd2_test_1():
    print("KJD2 test 1")
    startup_duration: int = 1
    model_config_file:str = "model_config/KJD2_e0.5.txt"
    expected_file:str = "tests/expected/KJD2_t1.txt"
    jobs_file:str = "tests/job_sets/KJD2_t1.txt"
    results_file:str = "tests/results/KJD2_t1.txt"
    end_to_end_model_test(startup_duration=startup_duration,
                          model_config_file=model_config_file,
                          results_file=results_file,
                          jobs_file=jobs_file,
                          expected_file_name=expected_file)
    print()

"""
UJD1 Test 1

Runs the UJD1 scheduling model on a job set stored in the file UJD1_t1.txt and compares the output schedule to the 
expected

epsilon = 0.5
"""
def ujd1_test_1():
    print("UJD1 test 1")
    startup_duration: int = 1
    model_config_file:str = "model_config/UJD1_e0.5.txt"
    expected_file:str = "tests/expected/UJD1_t1.txt"
    jobs_file:str = "tests/job_sets/UJD1_t1.txt"
    results_file:str = "tests/results/UJD1_t1.txt"
    end_to_end_model_test(startup_duration=startup_duration,
                          model_config_file=model_config_file,
                          results_file=results_file,
                          jobs_file=jobs_file,
                          expected_file_name=expected_file)
    print()

"""
UJD2 Test 1

Runs the UJD2 scheduling model on a job set stored in the file UJD2_t1.txt and compares the output schedule to the 
expected

epsilon = 0.5
"""
def ujd2_test_1():
    print("UJD2 test 1")
    startup_duration: int = 1
    model_config_file:str = "model_config/UJD2_e0.5.txt"
    expected_file:str = "tests/expected/UJD2_t1.txt"
    jobs_file:str = "tests/job_sets/UJD2_t1.txt"
    results_file:str = "tests/results/UJD2_t1.txt"
    end_to_end_model_test(startup_duration=startup_duration,
                          model_config_file=model_config_file,
                          results_file=results_file,
                          jobs_file=jobs_file,
                          expected_file_name=expected_file)
    print()

"""
Performs the end to end tests for all models
"""
def end_to_end_tests():
    fifo_test_1()
    kjd1_test_1()
    kjd2_test_1()
    ujd1_test_1()
    ujd2_test_1()

end_to_end_tests()