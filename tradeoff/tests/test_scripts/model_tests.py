from end_to_end import end_to_end_model_test

"""
FIFO Test 1

Runs the FIFO scheduling model on a job set stored in the file FIFO_t1.txt and compares the output schedule to the 
expected

container number = 10
"""
def fifo_test_1():
    config_file_name:str = "tests\\config\\FIFO_t1.txt"
    expected_file_name:str = "tests\\expected\\FIFO_t1.txt"
    print("FIFO test 1")
    end_to_end_model_test(config_file_name=config_file_name, expected_file_name=expected_file_name)
    print()

"""
KJD1 Test 1

Runs the KJD1 scheduling model on a job set stored in the file KJD1_t1.txt and compares the output schedule to the 
expected

epsilon = 0.5
"""
def kjd1_test_1():
    config_file_name:str = "tests\\config\\KJD1_t1.txt"
    expected_file_name:str = "tests\\expected\\KJD1_t1.txt"
    print("KJD1 test 1")
    end_to_end_model_test(config_file_name=config_file_name, expected_file_name=expected_file_name)
    print()

"""
KJD2 Test 1

Runs the KJD2 scheduling model on a job set stored in the file KJD2_t1.txt and compares the output schedule to the 
expected

epsilon = 0.5
"""
def kjd2_test_1():
    config_file_name:str = "tests\\config\\KJD2_t1.txt"
    expected_file_name:str = "tests\\expected\\KJD2_t1.txt"
    print("KJD2 test 1")
    end_to_end_model_test(config_file_name=config_file_name, expected_file_name=expected_file_name)
    print()

"""
UJD1 Test 1

Runs the UJD1 scheduling model on a job set stored in the file UJD1_t1.txt and compares the output schedule to the 
expected

epsilon = 0.5
"""
def ujd1_test_1():
    config_file_name:str = "tests\\config\\UJD1_t1.txt"
    expected_file_name:str = "tests\\expected\\UJD1_t1.txt"
    print("UJD1 test 1")
    end_to_end_model_test(config_file_name=config_file_name, expected_file_name=expected_file_name)
    print()

"""
UJD2 Test 1

Runs the UJD2 scheduling model on a job set stored in the file UJD2_t1.txt and compares the output schedule to the 
expected

epsilon = 0.5
"""
def ujd2_test_1():
    config_file_name:str = "tests\\config\\UJD2_t1.txt"
    expected_file_name:str = "tests\\expected\\UJD2_t1.txt"
    print("UJD2 test 1")
    end_to_end_model_test(config_file_name=config_file_name, expected_file_name=expected_file_name)
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

ujd2_test_1()
# end_to_end_tests()