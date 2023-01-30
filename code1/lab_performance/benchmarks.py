class Benchmark:
    def __init__(self, iterations=10, time_list=[],code_complica="",code_sim="",compli_code_time_list=[],simple_code_time_dict=[]):
        self.iterations=iterations
        self.time_list=time_list
        self.code_complica=code_complica
        self.code_sim=code_sim
        self.compli_code_time_list=compli_code_time_list# key is an element of self.test_case_info_list
        self.simple_code_time_dict=simple_code_time_dict# key is an element of self.test_case_info_list
