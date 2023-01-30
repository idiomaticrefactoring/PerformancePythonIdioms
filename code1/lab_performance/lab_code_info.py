import os,sys,ast
import numpy as np
code_dir="/".join(os.path.abspath(__file__).split("/")[:-2])+"/"
sys.path.append(code_dir)
sys.path.append(code_dir+"performance/")
import lab_performance_util,performance_util

class LabCodeInfo():
    def __init__(self, dir_path="",file_path="" , code_info=[],idiomatic_path="",non_idiomatic_path="",
                 compli_code_time_list=dict(), simple_code_time_list=dict(),num_add_ele=None, iterations=10,invocations=10,rciw=[]):
        self.code_info = code_info
        self.compli_code_time_dict = compli_code_time_list  # key is an element of self.test_case_info_list
        self.simple_code_time_dict = simple_code_time_list  # key is an element of self.test_case_info_list
        self.file_path = file_path
        self.iterations = iterations
        self.invocations=invocations
        self.dir_path = dir_path
        self.idiomatic_path=idiomatic_path
        self.non_idiomatic_path = non_idiomatic_path
        self.num_add_ele=num_add_ele
        self.rciw=rciw# interval, mean, invocations_number
    def get_performance_improve_info(self,step=100,warms_up=3,window=4,invo_num=50,remove_outlier=False,factor=1.5):
        # print(">>>>>>>compute performance ci")
        perf_ci_info = []
        warms_up = warms_up
        window = window
        time_list = [[float(e) for e in e_list[warms_up:]] for e_list in self.compli_code_time_dict]
        # valid_time_list = lab_performance_util.get_time_list_within_cov(time_list, window)
        idiom_time_list = [[float(e) for e in e_list[warms_up:]] for e_list in self.simple_code_time_dict]
        # valid_idiom_time_list = lab_performance_util.get_time_list_within_cov(idiom_time_list, window)
        # print("simple_code_time_dict: ", len(self.simple_code_time_dict), self.simple_code_time_dict[0])
        # print("time_list: ",len(time_list[0]))
        # print("idiom_time_list: ",len(idiom_time_list),idiom_time_list[0])
        if len(idiom_time_list) < invo_num:
            print(f"the number of invocations of the benchmark  is less than {invo_num}:", len(idiom_time_list))
        else:
            # print("len: ",len(valid_time_list))
            pass
        if len(time_list) < invo_num:
            print(f"the number of invocations of the benchmark  is less than {invo_num}:", len(time_list))
        else:

            # print("len: ", len(valid_time_list))
            pass
        if remove_outlier:
          # print(sum([sum(e) for e in time_list]), sum([sum(e) for e in idiom_time_list]))
          filter_time_list=performance_util.filter_outlier_2(time_list,factor)
          filter_time_list_idiom=performance_util.filter_outlier_2(idiom_time_list,factor)
          # print(sum(filter_time_list),sum(filter_time_list_idiom))
          real_per_change=sum(filter_time_list)/sum(filter_time_list_idiom)
        else:
            real_per_change = sum([sum(e) for e in time_list]) / sum([sum(e) for e in idiom_time_list])
            # print(sum([sum(e) for e in time_list]), sum([sum(e) for e in idiom_time_list]))
        all_boot_time_list = lab_performance_util.num_bootstrap(time_list, steps=step)
        all_boot_idiom_time_list = lab_performance_util.num_bootstrap(idiom_time_list, steps=step)

        '''
        get performance change and confidence interval
        '''
        prf_change_list = []
        for ind_step, boot_time_list in enumerate(all_boot_time_list):
            boot_idiom_time_list = all_boot_idiom_time_list[ind_step]
            if remove_outlier:
                filter_time_list = performance_util.filter_outlier_2(boot_time_list, factor)
                filter_time_list_idiom = performance_util.filter_outlier_2(boot_idiom_time_list, factor)
                e_sum = sum(filter_time_list)
                e_idiom_sum = sum(filter_time_list_idiom)
            else:
                e_sum = sum([sum(e) for e in boot_time_list])
                e_idiom_sum = sum([sum(e) for e in boot_idiom_time_list])
            # print("e_time_list: ",filter_time_list_idiom,e_idiom_sum,e_sum)
            # print(e_idiom_time_list)
            # print(np.mean(np.array(e_time_list,dtype=np.float64),None))
            try:
                per_change = e_sum / e_idiom_sum
                prf_change_list.append(per_change - real_per_change)
            except:
                continue
        left, right = np.percentile(prf_change_list, [2.5, 97.5])
        self.mean_perf_change = real_per_change
        if left + real_per_change < 1 < right + real_per_change:
            print("file_name: ", self.file_path.split("/")[-1])
            print(left + real_per_change, right + real_per_change, real_per_change)
            # self.mean_perf_change = 1.0
        else:
            # print("file_name: ", file_name)
            # print(left+real_per_change, right+real_per_change,real_per_change)
            pass
        perf_ci_info=[real_per_change,left+ real_per_change,right+ real_per_change,(right-left)/real_per_change]
        self.perf_ci_info = perf_ci_info
        return real_per_change,left+real_per_change, right+real_per_change
    def get_performance_info(self,step=100,warms_up=3,window=4,invo_num=50):
        perf_ci_info = []
        warms_up = warms_up
        window = window
        time_list = [[float(e) for e in e_list[warms_up:]] for e_list in self.compli_code_time_dict]
        valid_time_list = lab_performance_util.get_time_list_within_cov(time_list, window)
        idiom_time_list = [[float(e) for e in e_list[warms_up:]] for e_list in self.simple_code_time_dict]
        valid_idiom_time_list = lab_performance_util.get_time_list_within_cov(idiom_time_list, window)
        if len(valid_idiom_time_list) < invo_num:
            print(f"the number of invocations of the benchmark  is less than {invo_num}:", len(valid_time_list))
        else:
            # print("len: ",len(valid_time_list))
            pass
        if len(valid_time_list) < invo_num:
            print(f"the number of invocations of the benchmark  is less than {invo_num}:", len(valid_time_list))
        else:

            # print("len: ", len(valid_time_list))
            pass
        real_per_change = sum([sum(e) for e in valid_time_list]) / sum([sum(e) for e in valid_idiom_time_list])

        all_boot_time_list = lab_performance_util.num_bootstrap(valid_time_list, steps=step)
        all_boot_idiom_time_list = lab_performance_util.num_bootstrap(valid_idiom_time_list, steps=step)

        '''
        get performance change and confidence interval
        '''
        prf_change_list = []
        for ind_step, boot_time_list in enumerate(all_boot_time_list):
            boot_idiom_time_list = all_boot_idiom_time_list[ind_step]
            e_sum = sum([sum(e) for e in boot_time_list])
            e_idiom_sum = sum([sum(e) for e in boot_idiom_time_list])
            # print("e_time_list: ",sum(e_time_list))
            # print(e_idiom_time_list)
            # print(np.mean(np.array(e_time_list,dtype=np.float64),None))
            per_change = e_sum / e_idiom_sum
            prf_change_list.append(per_change - real_per_change)
        left, right = np.percentile(prf_change_list, [2.5, 97.5])
        self.mean_perf_change = real_per_change
        if left + real_per_change < 1 < right + real_per_change:
            print("file_name: ", self.file_path.split("/")[-1])
            print(left + real_per_change, right + real_per_change, real_per_change)
            # self.mean_perf_change = 1.0
        else:
            # print("file_name: ", file_name)
            # print(left+real_per_change, right+real_per_change,real_per_change)
            pass
        self.stable_compli_time_list = valid_time_list
        self.stable_simp_time = valid_idiom_time_list
        self.interval = (left+real_per_change, right+real_per_change)
        perf_ci_info=[real_per_change,left+ real_per_change,right+ real_per_change,(right-left)/real_per_change]
        self.perf_ci_info = perf_ci_info
        return real_per_change,left+real_per_change, right+real_per_change
    # def set_prf_change_confi_inter(self,stable_compli_time,stable_simp_time,left,right):
    #     self.stable_compli_time_list=stable_compli_time
    #     self.stable_simp_time = stable_simp_time
    #     self.mean=self.mean
    #     self.interval=(left,right)
    def get_performance_stable_iter_invo_info(self,warms_up=3,window=4):
        warms_up = warms_up
        window = window
        time_list = [[float(e) for e in e_list[warms_up:]] for e_list in self.compli_code_time_dict]
        valid_time_list,valid_index_list = lab_performance_util.get_time_list_within_cov_contain_index(time_list, window)
        idiom_time_list = [[float(e) for e in e_list[warms_up:]] for e_list in self.simple_code_time_dict]
        valid_idiom_time_list,valid_idiom_index_list = lab_performance_util.get_time_list_within_cov_contain_index(idiom_time_list, window)
        if len(valid_time_list) < 10:
            print("the number of invocations of the non-idiomatic benchmark  is less than 10:", len(valid_time_list))
        else:

            # print("len: ", len(valid_time_list))
            pass
        print("number of iterations of all invocations of valid_time_list if stable: ",valid_index_list)
        if len(valid_idiom_time_list) < 10:
            print("the number of invocations of the idiomatic benchmark  is less than 10:", len(valid_time_list))
        else:
            # print("len: ",len(valid_time_list))
            pass
        print("number of iterations of all invocations of valid_idiom_time_list if stable: ",valid_idiom_index_list)

    def get_stable_time_list_tosem_2020(self, warms_up=3):
        compli_code_time_list = self.compli_code_time_dict
        simple_code_time_list = self.simple_code_time_dict
        num_add_ele = self.num_add_ele
        total_time_list_info_dict = {"time_list": [], "num_ele": None,
                                     "pythonic_time_list": []}
        for ind_invo, each_compli_code_time_dict in enumerate(compli_code_time_list):


                            valid_time_list = [float(e) for e in each_compli_code_time_dict[warms_up:]]

                            total_time_list_info_dict["time_list"].append(
                                    valid_time_list)
                            total_time_list_info_dict["num_ele"] = int(
                                    num_add_ele)

        for ind_invo, each_compli_code_time_dict in enumerate(simple_code_time_list):
            valid_time_list = [float(e) for e in each_compli_code_time_dict[warms_up:]]

            total_time_list_info_dict["pythonic_time_list"].append(
                valid_time_list)


        self.total_time_list_info_dict = total_time_list_info_dict
        return total_time_list_info_dict

    # def compute_CI_forks_list(self, warmups=3, steps=1000):
    #     if hasattr(self, "dict_cov_ci_kld_time_list"):
    #         dict_cov_time_list = self.dict_cov_ci_kld_time_list
    #     else:
    #         dict_cov_time_list = dict()
    #     if not hasattr(self, "total_time_list_info_dict"):
    #         self.get_stable_time_list_tosem_2020(warms_up=warmups)
    #     if self.total_time_list_info_dict:
    #         total_time_list_info_dict = self.total_time_list_info_dict
    #         for test_me in total_time_list_info_dict:
    #             if test_me not in dict_cov_time_list:
    #                 dict_cov_time_list[test_me] = dict()
    #             for ind_instance in total_time_list_info_dict[test_me]:
    #                 if ind_instance not in dict_cov_time_list[test_me]:
    #                     dict_cov_time_list[test_me][ind_instance] = dict()
    #                 cov_instance_list = []
    #                 cov_idiom_instance_list = []
    #                 ci_instance_list = []
    #                 ci_idiom_instance_list = []
    #                 prob_kld_instance_list = []
    #                 prob_kld_idiom_instance_list = []
    #                 pre_valid_time_list = []
    #                 pre_valid_idiom_time_list = []
    #                 for invocations in range(1, min(len(total_time_list_info_dict[test_me][ind_instance]["time_list"]),
    #                                                 len(
    #                                                         total_time_list_info_dict[test_me][ind_instance][
    #                                                             "pythonic_time_list"])) + 1):
    #                     valid_time_list = total_time_list_info_dict[test_me][ind_instance]["time_list"][:invocations]
    #                     valid_idiom_time_list = total_time_list_info_dict[test_me][ind_instance]["pythonic_time_list"][
    #                                             :invocations]
    #                     flat_valid_time_list = [e for e_invo_list in valid_time_list for e in e_invo_list]
    #                     flat_valid_idiom_time_list = [e for e_invo_list in valid_idiom_time_list for e in e_invo_list]
    #                     # print("len of valid_time_list: ",len(flat_valid_time_list),len(flat_valid_idiom_time_list))
    #                     all_boot_time_list = performance_util.num_bootstrap(valid_time_list, steps=steps)
    #                     all_boot_idiom_time_list = performance_util.num_bootstrap(valid_idiom_time_list, steps=steps)
    #                     left, right = performance_util.compute_ci(all_boot_time_list)
    #                     mean_time = (right - left) / np.mean(valid_time_list)
    #                     ci_instance_list.append(mean_time)
    #                     left, right = performance_util.compute_ci(all_boot_idiom_time_list)
    #                     mean_time = (right - left) / np.mean(valid_idiom_time_list)
    #                     ci_idiom_instance_list.append(mean_time)
    #
    #                 dict_cov_time_list[test_me][ind_instance]["ci_time_list"] = ci_instance_list
    #                 dict_cov_time_list[test_me][ind_instance]["ci_pythonic_time_list"] = ci_idiom_instance_list
    #
    #     # print("self.dict_cov_ci_kld_time_list: ",dict_cov_time_list)
    #     self.dict_cov_ci_kld_time_list = dict_cov_time_list
    def compute_cov_CI_forks_list(self, warmups=3, steps=1000):
        dict_ci_diff_before_after_forks=dict()

        dict_cov_time_list = dict()
        if not hasattr(self, "total_time_list_info_dict"):
            self.get_stable_time_list_tosem_2020(warms_up=warmups)
        if self.total_time_list_info_dict:
            total_time_list_info_dict = self.total_time_list_info_dict
            if 1:
            # for test_me in total_time_list_info_dict:
            #     dict_cov_time_list[test_me] = dict()
            #     for ind_instance in total_time_list_info_dict[test_me]:
            #         dict_cov_time_list[test_me][ind_instance] = dict()
                    cov_instance_list = []
                    cov_idiom_instance_list = []
                    ci_instance_list = []
                    ci_idiom_instance_list = []
                    ci_diff_instance_list = []
                    ci_diff_idiom_instance_list = []
                    prob_kld_instance_list = []
                    prob_kld_idiom_instance_list = []
                    pre_valid_time_list = []
                    pre_valid_idiom_time_list = []
                    pre_boot_valid_time_list=[]
                    pre_boot_valid_idiom_time_list=[]
                    # print("total_time_list_info_dict len: ",len(total_time_list_info_dict["time_list"]),len(total_time_list_info_dict["pythonic_time_list"]))
                    for invocations in range(1, min(len(total_time_list_info_dict["time_list"]),
                                                    len(total_time_list_info_dict["pythonic_time_list"])) + 1):
                        valid_time_list = total_time_list_info_dict["time_list"][:invocations]
                        valid_idiom_time_list = total_time_list_info_dict["pythonic_time_list"][
                                                :invocations]
                        # print("shape of valid_time_list and valid_idiom_time_list: ",
                        #       np.array(valid_time_list).shape,np.array(valid_idiom_time_list).shape
                        #       )
                        flat_valid_time_list = [e for e_invo_list in valid_time_list for e in e_invo_list]
                        flat_valid_idiom_time_list = [e for e_invo_list in valid_idiom_time_list for e in e_invo_list]
                        # print("len of valid_time_list: ",len(flat_valid_time_list),len(flat_valid_idiom_time_list))
                        all_boot_time_list = performance_util.num_bootstrap(valid_time_list, steps=steps)
                        all_boot_idiom_time_list = performance_util.num_bootstrap(valid_idiom_time_list, steps=steps)
                        # print("shape of all_boot_time_list and all_boot_idiom_time_list: ",
                        #       np.array(all_boot_time_list).shape, np.array(all_boot_idiom_time_list).shape
                        #       )
                        left, right = performance_util.compute_ci(all_boot_time_list)
                        mean_time = (right - left) / np.mean(valid_time_list)
                        ci_instance_list.append(mean_time)
                        left, right = performance_util.compute_ci(all_boot_idiom_time_list)
                        mean_time = (right - left) / np.mean(valid_idiom_time_list)
                        ci_idiom_instance_list.append(mean_time)

                        cov = performance_util.compute_cov(flat_valid_time_list)
                        # if cov>5:
                        #     print(f"{test_me} of {ind_instance} cov>30: ",cov,invocations)
                        cov_instance_list.append(cov)
                        cov = performance_util.compute_cov(flat_valid_idiom_time_list)
                        if invocations != 1:
                            kld_time = performance_util.get_kld_x_y(pre_valid_time_list, flat_valid_time_list)
                            kld_idiom_time = performance_util.get_kld_x_y(pre_valid_idiom_time_list,
                                                                          flat_valid_idiom_time_list)
                            prob_kld_instance_list.append(kld_time)
                            prob_kld_idiom_instance_list.append(kld_idiom_time)

                            diff = performance_util.get_ci_diff(pre_boot_valid_time_list, all_boot_time_list)
                            pythonic_diff = performance_util.get_ci_diff(pre_boot_valid_idiom_time_list,
                                                                         all_boot_idiom_time_list)
                            ci_diff_idiom_instance_list.append(pythonic_diff)
                            ci_diff_instance_list.append(diff)
                        pre_boot_valid_time_list = all_boot_time_list
                        pre_boot_valid_idiom_time_list = all_boot_idiom_time_list
                        pre_valid_time_list = flat_valid_time_list
                        pre_valid_idiom_time_list = flat_valid_idiom_time_list

                        cov_idiom_instance_list.append(cov)
                    dict_cov_time_list["kld_time_list"] = prob_kld_instance_list
                    dict_cov_time_list["kld_pythonic_time_list"] = prob_kld_idiom_instance_list
                    dict_cov_time_list["ci_time_list"] = ci_instance_list
                    dict_cov_time_list["ci_pythonic_time_list"] = ci_idiom_instance_list
                    dict_cov_time_list["cov_time_list"] = cov_instance_list
                    dict_cov_time_list["cov_pythonic_time_list"] = cov_idiom_instance_list
                    dict_ci_diff_before_after_forks["ci_diff_time_list_before_after_forks"] = ci_diff_instance_list
                    dict_ci_diff_before_after_forks["pythonic_ci_diff_time_before_after_forks"] = ci_diff_idiom_instance_list
        # print("self.dict_cov_ci_kld_time_list: ",dict_cov_time_list)
        self.dict_cov_ci_kld_time_list = dict_cov_time_list
        self.dict_ci_diff_before_after_forks=dict_ci_diff_before_after_forks

    def get_code_str(self):
        code_str_list = []
        for e in self.code_info:
            if isinstance(e, list):
                continue
            elif isinstance(e, ast.AST):
                code_str_list.append(ast.unparse(e))
            elif isinstance(e, str):
                code_str_list.append(e)
        return "\n".join(code_str_list)
    def get_features(self):
        dict_feature={"num_for":0,"num_if":0,"num_if_else":0,
                     "num_func_call":0,"num_ele":int(self.num_add_ele) }
        num_for=0
        num_if=0
        num_if_else=0
        num_func_call=0
        num_ele=0
        for_node=self.code_info[0]
        assign_node_node=self.code_info[1]
        for node in ast.walk(for_node):
            if isinstance(node,ast.For):
                dict_feature["num_for"]+=1
            elif isinstance(node,ast.If):
                if node.orelse:
                    dict_feature["num_if_else"] += 1
                else:
                    dict_feature["num_if"] += 1
            elif isinstance(node,ast.Call):
                dict_feature["num_func_call"]+=1
        self.dict_feature=dict_feature
        return dict_feature









