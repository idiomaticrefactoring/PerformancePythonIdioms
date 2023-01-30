import copy
import os,sys,ast
import traceback

import numpy as np
code_dir="/".join(os.path.abspath(__file__).split("/")[:-2])+"/"
sys.path.append(code_dir)
sys.path.append(code_dir+"performance/")
from scipy import stats
import performance_util
class CodeInfo():
  def __init__(self, repo_name,file_html,cl='',me='',code_info=[], test_case_info_list=[],file_content="",compli_code_time_list=dict(),simple_code_time_list=dict(),own_config=0,iterations=10,file_path="",flag_total_test_html=dict(),flag_total_test_html_instances=dict(),flag_total_test_html_pythonic=dict(),flag_total_test_html_instances_pythonic=dict(),num_ele_list=dict()):
    self.code_info=code_info
    self.test_case_info_list = test_case_info_list
    '''
    each ele--corresponding dict of each invocation
                              ---- each key is a test_method, value_list is a two-dimension time list, 
                                    each time list is corresponding to an test case(input instance)
    '''
    self.compli_code_time_dict=compli_code_time_list# key is an element of self.test_case_info_list
    self.simple_code_time_dict = simple_code_time_list  # key is an element of self.test_case_info_list
    self.file_html=file_html
    self.repo_name=repo_name
    self.cl=cl
    self.me=me
    self.own_config=own_config
    self.iterations=iterations
    self.file_content=file_content
    self.flag_total_test_html=flag_total_test_html# 0--unstable 1--stable 2--containing one instance without test cases
    #flag_total_test_html_instances[(test_html, each_rela_path, cl, me)][ind_test_case]+=stable_flag
    self.flag_total_test_html_instances=flag_total_test_html_instances# num means how many invocations are steady
    #flag_total_test_html[(test_html, each_rela_path, cl, me)]=1
    self.flag_total_test_html_pythonic= flag_total_test_html_pythonic  # 0--unstable 1--stable 2--containing one instance without test cases
    self.flag_total_test_html_instances_pythonic = flag_total_test_html_instances_pythonic
    self.num_ele_list=num_ele_list
    self.run_test_res_compli_code=[]
    self.run_test_res_simple_code = []
    self.type_add_list=[]
  def get_chain_compare_complicted_code_pythonic_code(self):
    old_tree, new_tree=self.code_info

    if "and " in ast.unparse(new_tree):
      for e_value in old_tree.values:
        if isinstance(e_value,ast.Compare):
          compare_fuzhu=copy.deepcopy(e_value)
          break
      old_tree.values = []
      values=new_tree.values
      for value in values:
        if len(value.ops)>1:
          new_tree=value
          comparators=[value.left]+[comp for comp in value.comparators]

          for ind_op,op in enumerate(value.ops):
            compare_fuzhu_2=copy.deepcopy(compare_fuzhu)
            compare_fuzhu_2.left=comparators[ind_op]
            compare_fuzhu_2.comparators[-1]=comparators[ind_op+1]
            compare_fuzhu_2.ops[-1]=op
            old_tree.values.append(compare_fuzhu_2)
          self.new_code_info=old_tree,new_tree
          return old_tree,new_tree
    self.new_code_info = old_tree, new_tree
    return old_tree,new_tree
    pass
  def set_run_test_res_compli_code(self,run_test_res_compli_code):
    self.run_test_res_compli_code=run_test_res_compli_code

  def set_run_test_res_simple_code(self, run_test_res_simple_code):
    self.run_test_res_simple_code = run_test_res_simple_code
  def get_stable_time_list_improve(self,warms_up=3,window=4,invocations=10,stable_info_dict=dict()):
    compli_code_time_list = self.compli_code_time_dict
    simple_code_time_list = self.simple_code_time_dict
    print("len: ",len(compli_code_time_list),len(simple_code_time_list))

    num_add_ele_dict = self.num_ele_list
    total_time_list_info_dict = dict()
    if len(compli_code_time_list)<50 or  len(simple_code_time_list)<50:
      print(compli_code_time_list)
      print(simple_code_time_list)
      print(num_add_ele_dict)
      return total_time_list_info_dict
    for ind_invo, each_compli_code_time_dict in enumerate(compli_code_time_list[:invocations]):
      each_simple_compli_code_time_dict=simple_code_time_list[ind_invo]
      for test_me in each_compli_code_time_dict:
        if test_me in each_simple_compli_code_time_dict:
        # if test_me in stable_info_dict:
          for ind_instance, instance_time_list in enumerate(each_compli_code_time_dict[test_me]):
            if ind_instance in each_simple_compli_code_time_dict[test_me]:
            # if ind_instance in stable_info_dict[test_me]:
              if test_me not in total_time_list_info_dict:
                total_time_list_info_dict[test_me] = dict()
              if ind_instance not in total_time_list_info_dict[test_me]:
                total_time_list_info_dict[test_me][ind_instance] = {"time_list": [], "num_ele": None,
                                                                    "pythonic_time_list": []}
              steady_time_list = [float(e) for e in instance_time_list[warms_up:]]
              valid_time_list = performance_util.get_time_list_within_cov(steady_time_list, window)
              if valid_time_list:
                total_time_list_info_dict[test_me][ind_instance]["pythonic_time_list"].append(valid_time_list)
                if total_time_list_info_dict[test_me][ind_instance]["num_ele"] is None:
                  try:
                    total_time_list_info_dict[test_me][ind_instance]["num_ele"] = int(
                      num_add_ele_dict[test_me][ind_instance][0])
                  except:
                    print("steady_time_list: ",steady_time_list)
                    print("num_add_ele_dict[test_me][ind_instance]: ",num_add_ele_dict[test_me][ind_instance])
                    traceback.format_exc()
                    raise
              simple_steady_time_list = [float(e) for e in each_simple_compli_code_time_dict[test_me][ind_instance][warms_up:]]
              simple_valid_time_list = performance_util.get_time_list_within_cov(simple_steady_time_list, window)
              if simple_valid_time_list:
                total_time_list_info_dict[test_me][ind_instance]["time_list"].append(
                  simple_valid_time_list)
    self.total_time_list_info_dict=total_time_list_info_dict
    return total_time_list_info_dict
  # get total_time_list_info_dict[test_me][ind_instance]["pythonic_time_list"] based on Cov strategy
  def get_stable_time_list(self,warms_up=3,window=4,stable_info_dict=dict(),invocations=None):
    compli_code_time_list = self.compli_code_time_dict
    simple_code_time_list = self.simple_code_time_dict
    num_add_ele_dict = self.num_ele_list
    total_time_list_info_dict = dict()
    if not invocations:
      invocations=len(compli_code_time_list)
    for ind_invo, each_compli_code_time_dict in enumerate(compli_code_time_list[:invocations]):
      for test_me in each_compli_code_time_dict:
        if test_me in stable_info_dict:
          for ind_instance, instance_time_list in enumerate(each_compli_code_time_dict[test_me]):
            if ind_instance in stable_info_dict[test_me]:
              if test_me not in total_time_list_info_dict:
                total_time_list_info_dict[test_me] = dict()
              if ind_instance not in total_time_list_info_dict[test_me]:
                total_time_list_info_dict[test_me][ind_instance] = {"time_list": [], "num_ele": None,
                                                                    "pythonic_time_list": []}
              steady_time_list = [float(e) for e in instance_time_list[warms_up:]]
              valid_time_list = performance_util.get_time_list_within_cov(steady_time_list, window)
              if valid_time_list:
                total_time_list_info_dict[test_me][ind_instance]["pythonic_time_list"].append(valid_time_list)
                if total_time_list_info_dict[test_me][ind_instance]["num_ele"] is None:
                  try:
                    total_time_list_info_dict[test_me][ind_instance]["num_ele"] = int(
                      num_add_ele_dict[test_me][ind_instance][0])
                  except:
                    print("steady_time_list: ",steady_time_list)
                    print("num_add_ele_dict[test_me][ind_instance]: ",num_add_ele_dict[test_me][ind_instance])
                    traceback.format_exc()
                    raise

    for ind_invo, each_compli_code_time_dict in enumerate(simple_code_time_list[:invocations]):
      for test_me in each_compli_code_time_dict:
        if test_me in stable_info_dict:
          for ind_instance, instance_time_list in enumerate(each_compli_code_time_dict[test_me]):
            if ind_instance in stable_info_dict[test_me]:
              steady_time_list = [float(e) for e in instance_time_list[warms_up:]]
              valid_time_list = performance_util.get_time_list_within_cov(steady_time_list, window)
              if valid_time_list:
                total_time_list_info_dict[test_me][ind_instance]["time_list"].append(
                  valid_time_list)

    self.total_time_list_info_dict=total_time_list_info_dict
    return total_time_list_info_dict
  # get stable test instance of test method
  def get_stable_info_dict(self,threshold=1):
    stable_info_dict = dict()
    all_instance=0
    stable_instance=0
    for test_me in self.flag_total_test_html_instances:
      instance_list = self.flag_total_test_html_instances[test_me]
      instance_list_pythonic = self.flag_total_test_html_instances_pythonic[test_me]

      for instance in instance_list:
        all_instance+=1
        if instance in instance_list_pythonic and instance_list_pythonic[instance] >= threshold and instance_list[
          instance] >= threshold and test_me in self.num_ele_list and instance in self.num_ele_list[test_me]:
          stable_instance+=1
          if test_me not in stable_info_dict:
            stable_info_dict[test_me]=[instance]
          else:
            stable_info_dict[test_me].append(instance)
        else:
          print(f"the {instance} instance of test method {test_me} is not stable,please check:\n ","instance_list: ",instance_list,"\ninstance_list_pythonic:",instance_list_pythonic)
        # else:
        #   print(f"the {instance} is not stable: ",instance_list_pythonic[instance])
    if all_instance!=stable_instance:
      print(f"{self.file_html} is not stable: ",all_instance,stable_instance)
    else:
      print(f"all instances of {self.file_html} is stable")
    return stable_info_dict
  def get_stable_info_dict_improve(self,threshold=1):
    stable_info_dict = dict()
    all_instance=0
    stable_instance=0
    for test_me in self.flag_total_test_html_instances:
      instance_list = self.flag_total_test_html_instances[test_me]
      instance_list_pythonic = self.flag_total_test_html_instances_pythonic[test_me]

      for instance in instance_list:
        all_instance+=1
        if instance in instance_list_pythonic and instance_list_pythonic[instance] >= threshold and instance_list[
          instance] >= threshold and test_me in self.num_ele_list and instance in self.num_ele_list[test_me]:
          stable_instance+=1
          if test_me not in stable_info_dict:
            stable_info_dict[test_me]=[instance]
          else:
            stable_info_dict[test_me].append(instance)
        else:
          print(f"the {instance} instance of test method {test_me} is not stable,please check:\n ","instance_list: ",instance_list,"\ninstance_list_pythonic:",instance_list_pythonic)
        # else:
        #   print(f"the {instance} is not stable: ",instance_list_pythonic[instance])
    if all_instance!=stable_instance:
      print(f"{self.file_html} is not stable: ",all_instance,stable_instance)
    else:
      print(f"all instances of {self.file_html} is stable")
    return stable_info_dict
  def get_total_instances(self):
    total_instance=0
    for i, e_invo in enumerate(self.compli_code_time_dict):
      for test_me in e_invo:
        for ind_case, test_case_time in enumerate(e_invo[test_me]):
          total_instance+=1
      break
    return  total_instance
      # print(test_case_time)
  # remove the added ele
  def get_performance_improve_info(self, total_time_list_info_dict=dict(),threshold=1,invocations=None,steps=1000,merge=0,remove_outlier=False,factor=3):
    # total_time_list_info_dict=self.total_time_list_info_dict
    perf_info_dict=dict()
    if merge:
      if not hasattr(self, "total_time_list_info_dict_merge"):
        print(">>>>>>>>>it does not have total_time_list_info_dict_merge")
        self.get_stable_time_list_tosem_2020_merge_improve()
      total_time_list_info_dict=self.total_time_list_info_dict_merge
      # print(total_time_list_info_dict)
    else:
      if not hasattr(self, "total_time_list_info_dict"):
        print(">>>>>>>>>it does not have total_time_list_info_dict")
        self.get_stable_time_list_tosem_2020_improve()
      total_time_list_info_dict=self.total_time_list_info_dict
    print("total_time_list_info_dict: ",total_time_list_info_dict.keys(),self.file_html,self.test_case_info_list)
    for test_me in total_time_list_info_dict:

      perf_info_dict[test_me]=dict()
      for ind_instance in total_time_list_info_dict[test_me]:

        if not invocations:
          invocations = len(total_time_list_info_dict[test_me][ind_instance]["time_list"])
        valid_time_list = total_time_list_info_dict[test_me][ind_instance]["time_list"][:invocations]
        valid_idiom_time_list = total_time_list_info_dict[test_me][ind_instance]["pythonic_time_list"][:invocations]
        # print("test_me,ind_instance: ", test_me, ind_instance)
        # print("valid_time_list: ",valid_time_list[0])
        # print("valid_idiom_time_list: ", valid_idiom_time_list[0])
        if remove_outlier:
          filter_time_list=performance_util.filter_outlier_2(valid_time_list,factor)
          filter_time_list_idiom=performance_util.filter_outlier_2(valid_idiom_time_list,factor)

          # filter_time_list=performance_util.filter_outlier(valid_time_list)
          # filter_time_list_idiom=performance_util.filter_outlier(valid_idiom_time_list)

          # flatten_time_list=[ee for e in valid_time_list for ee in e]
          # median=np.median(flatten_time_list)
          # mad=stats.median_abs_deviation(flatten_time_list)
          # filter_time_list=[e for e in flatten_time_list if median+3*mad>e>median-3*mad]
          # flatten_time_list_idiom = [ee for e in valid_idiom_time_list for ee in e]
          # median = np.median(flatten_time_list_idiom)
          # mad = stats.median_abs_deviation(flatten_time_list_idiom)
          # filter_time_list_idiom = [e for e in flatten_time_list_idiom if median + 3 * mad > e > median - 3 * mad]

          real_per_change=sum(filter_time_list)/sum(filter_time_list_idiom)
        else:
          # print("valid_time_list: ", sum([sum(e) for e in valid_time_list]),"valid_idiom_time_list: ", sum(
          #   [sum(e) for e in valid_idiom_time_list]))
          real_per_change = sum([sum(e) for e in valid_time_list]) / sum(
            [sum(e) for e in valid_idiom_time_list])
          # print("the ratio: ",sum([sum(e) for e in valid_time_list]),sum(
          #   [sum(e) for e in valid_idiom_time_list]),real_per_change)

        all_boot_time_list = performance_util.num_bootstrap(valid_time_list, steps=steps)
        all_boot_idiom_time_list = performance_util.num_bootstrap(valid_idiom_time_list, steps=steps)

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
          # print("e_time_list: ",sum(e_time_list))
          # print(e_idiom_time_list)
          # print(np.mean(np.array(e_time_list,dtype=np.float64),None))
          per_change = e_sum / e_idiom_sum
          prf_change_list.append(per_change - real_per_change)
        left, right = np.percentile(prf_change_list, [2.5, 97.5])
        # self.mean_perf_change = real_per_change
        if left + real_per_change < 1 < right + real_per_change:
          # print("1 is in performance confidence interval, the file_name: ", self.file_html)
          print((left + real_per_change, right + real_per_change), real_per_change)
          # self.mean_perf_change = 1.0
        else:
          # print("file_name: ", file_name)
          print(left+real_per_change, right+real_per_change,real_per_change)
          pass
        # self.stable_compli_time_list = valid_time_list
        # self.stable_simp_time = valid_idiom_time_list
        # self.interval = (left, right)
        perf_info_dict[test_me][ind_instance]=[real_per_change,left+ real_per_change,right+ real_per_change,(right-left)/real_per_change]
        print(f"{len(valid_time_list)} and {len(valid_idiom_time_list)} stable num, {ind_instance}th instance of {test_me} test method's  performance change info: ", real_per_change,
              (left+ real_per_change, right+ real_per_change))
    self.perf_info_dict=perf_info_dict
  def get_performance_info(self, total_time_list_info_dict=dict(),threshold=1,invocations=None,steps=1000,remove_outlier=False,factor=1.5):
    # total_time_list_info_dict=self.total_time_list_info_dict

    for test_me in total_time_list_info_dict:
      for ind_instance in total_time_list_info_dict[test_me]:
        if not invocations:
          invocations = len(total_time_list_info_dict[test_me][ind_instance]["time_list"])
        num_ele=total_time_list_info_dict[test_me][ind_instance]["num_ele"]
        valid_time_list = total_time_list_info_dict[test_me][ind_instance]["time_list"][:invocations]
        valid_idiom_time_list = total_time_list_info_dict[test_me][ind_instance]["pythonic_time_list"][:invocations]
        if len(valid_time_list) < threshold or len(valid_idiom_time_list) < threshold:
          print(f"check time list of {ind_instance}th of {test_me} because its stable invocations is less than {threshold} ",
                len(valid_time_list), len(valid_idiom_time_list))
          continue
        if remove_outlier:
          filter_time_list=performance_util.filter_outlier_2(valid_time_list,factor)
          filter_time_list_idiom=performance_util.filter_outlier_2(valid_idiom_time_list,factor)

          # filter_time_list=performance_util.filter_outlier(valid_time_list)
          # filter_time_list_idiom=performance_util.filter_outlier(valid_idiom_time_list)

          # flatten_time_list=[ee for e in valid_time_list for ee in e]
          # median=np.median(flatten_time_list)
          # mad=stats.median_abs_deviation(flatten_time_list)
          # filter_time_list=[e for e in flatten_time_list if median+3*mad>e>median-3*mad]
          # flatten_time_list_idiom = [ee for e in valid_idiom_time_list for ee in e]
          # median = np.median(flatten_time_list_idiom)
          # mad = stats.median_abs_deviation(flatten_time_list_idiom)
          # filter_time_list_idiom = [e for e in flatten_time_list_idiom if median + 3 * mad > e > median - 3 * mad]

          real_per_change=sum(filter_time_list)/sum(filter_time_list_idiom)
        else:
          real_per_change = sum([sum(e) for e in valid_time_list]) / sum(
            [sum(e) for e in valid_idiom_time_list])

        all_boot_time_list = performance_util.num_bootstrap(valid_time_list, steps=steps)
        all_boot_idiom_time_list = performance_util.num_bootstrap(valid_idiom_time_list, steps=steps)

        '''
        get performance change and confidence interval
        '''
        prf_change_list = []
        for ind_step, boot_time_list in enumerate(all_boot_time_list):
          boot_idiom_time_list = all_boot_idiom_time_list[ind_step]
          if remove_outlier:
            filter_time_list = performance_util.filter_outlier_2(boot_time_list,factor)
            filter_time_list_idiom = performance_util.filter_outlier_2(boot_idiom_time_list,factor)
            # filter_time_list = performance_util.filter_outlier(boot_time_list)
            # filter_time_list_idiom = performance_util.filter_outlier(boot_idiom_time_list)
            e_sum=sum(filter_time_list)
            e_idiom_sum=sum(filter_time_list_idiom)
          else:
            e_sum = sum([sum(e) for e in boot_time_list])
            e_idiom_sum = sum([sum(e) for e in boot_idiom_time_list])
          # print("e_time_list: ",sum(e_time_list))
          # print(e_idiom_time_list)
          # print(np.mean(np.array(e_time_list,dtype=np.float64),None))
          per_change = e_sum / e_idiom_sum
          prf_change_list.append(per_change - real_per_change)
        left, right = np.percentile(prf_change_list, [2.5, 97.5])
        # self.mean_perf_change = real_per_change
        if left + real_per_change < 1 < right + real_per_change:
          # print("1 is in performance confidence interval, the file_name: ", self.file_html)
          print((left + real_per_change, right + real_per_change), real_per_change)
          # self.mean_perf_change = 1.0
        else:
          # print("file_name: ", file_name)
          # print(left+real_per_change, right+real_per_change,real_per_change)
          pass
        # self.stable_compli_time_list = valid_time_list
        # self.stable_simp_time = valid_idiom_time_list
        # self.interval = (left, right)
        self.total_time_list_info_dict[test_me][ind_instance]["perf_change"]=[real_per_change,left+ real_per_change,right+ real_per_change]
        print(f"{len(valid_time_list)} and {len(valid_idiom_time_list)} stable num, {ind_instance}th instance of {test_me} test method's  performance change info: ", real_per_change,
              (left+ real_per_change, right+ real_per_change),num_ele)
        # return real_per_change,(left+ real_per_change, right+ real_per_change)
  # a instance (an method invocation in a test method) contain many substance (a method invocation executes a python fragment multiple time)
  def get_stable_time_list_tosem_2020_merge_improve(self, warms_up=3):
    # stable_info_dict=self.get_stable_info_dict(threshold=0)
    compli_code_time_list = self.compli_code_time_dict
    simple_code_time_list = self.simple_code_time_dict
    num_add_ele_dict = self.num_ele_list

    print("************compli_code_time_list****************")
    print(len(compli_code_time_list),compli_code_time_list[0])
    print("***********simple_code_time_list*****************")
    print(len(simple_code_time_list),simple_code_time_list[0])
    total_time_list_info_dict_merge = dict()
    for ind_invo, each_compli_code_time_dict in enumerate(compli_code_time_list):

      for test_me in each_compli_code_time_dict:
        # if ind_invo == 0:
        # print("************compli_code_time_list****************")
        # print(compli_code_time_list[ind_invo][test_me])
        # print("***********simple_code_time_list*****************")
        # print(simple_code_time_list[ind_invo][test_me])
        #   pass
        if test_me in simple_code_time_list[ind_invo]:
          for ind_instance, instance_time_list in enumerate(each_compli_code_time_dict[test_me]):
            if ind_instance< len(simple_code_time_list[ind_invo][test_me]):
              # print(">>>>>come here",self.file_html,test_me,ind_instance,instance_time_list)
              if test_me not in total_time_list_info_dict_merge:
                total_time_list_info_dict_merge[test_me] = dict()
              if ind_instance not in total_time_list_info_dict_merge[test_me]:
                total_time_list_info_dict_merge[test_me][ind_instance] = {"time_list": [],
                                                                    "pythonic_time_list": [],"num_subinstance":None, "num_ele": None}
              valid_time_list = [sum([float(ee) for ee in e]) for e in instance_time_list[warms_up:]]

              if valid_time_list:
                if not ind_invo:
                  total_time_list_info_dict_merge[test_me][ind_instance]["num_subinstance"]=[len(e) for e in instance_time_list[warms_up:]]
                total_time_list_info_dict_merge[test_me][ind_instance]["pythonic_time_list"].append(valid_time_list)
                if total_time_list_info_dict_merge[test_me][ind_instance]["num_ele"] is None:
                  if num_add_ele_dict:
                    try:
                      total_time_list_info_dict_merge[test_me][ind_instance]["num_ele"] = int(
                        num_add_ele_dict[test_me][ind_instance][0][0])
                    except:

                      print("num_add_ele_dict[test_me][ind_instance] is None: ", num_add_ele_dict)
                      traceback.print_exc()
              # for ind_instance, instance_time_list in enumerate(each_compli_code_time_dict[test_me]):
              simp_instance_time_list=simple_code_time_list[ind_invo][test_me][ind_instance]
              valid_time_list = [sum([float(ee) for ee in e]) for e in simp_instance_time_list[warms_up:]]
              if valid_time_list:
                total_time_list_info_dict_merge[test_me][ind_instance]["time_list"].append(
                  valid_time_list)


    # for ind_invo, each_compli_code_time_dict in enumerate(simple_code_time_list):
    #   for test_me in each_compli_code_time_dict:
    #
    #       for ind_instance, instance_time_list in enumerate(each_compli_code_time_dict[test_me]):
    #
    #           valid_time_list = [sum([float(ee) for ee in e]) for e in instance_time_list[warms_up:]]
    #           if valid_time_list:
    #             total_time_list_info_dict_merge[test_me][ind_instance]["time_list"].append(
    #               valid_time_list)

    self.total_time_list_info_dict_merge = total_time_list_info_dict_merge
    return total_time_list_info_dict_merge
  def get_stable_time_list_tosem_2020_improve(self, warms_up=3):
    # stable_info_dict=self.get_stable_info_dict(threshold=0)
    compli_code_time_list = self.compli_code_time_dict
    simple_code_time_list = self.simple_code_time_dict
    num_add_ele_dict=self.num_ele_list
    total_time_list_info_dict_merge = dict()
    for ind_invo, each_compli_code_time_dict in enumerate(compli_code_time_list):
      for test_me in each_compli_code_time_dict:
        if test_me in simple_code_time_list[ind_invo]:
          for ind_instance, instance_time_list in enumerate(each_compli_code_time_dict[test_me]):
            if ind_instance in simple_code_time_list[ind_invo][test_me]:
              if test_me not in total_time_list_info_dict_merge:
                total_time_list_info_dict_merge[test_me] = dict()
              if ind_instance not in total_time_list_info_dict_merge[test_me]:
                total_time_list_info_dict_merge[test_me][ind_instance] = {"time_list": [],
                                                                    "pythonic_time_list": [],"num_subinstance":None, "num_ele": None}
              valid_time_list = [float(ee) for e in instance_time_list[warms_up:] for ee in e]
              if valid_time_list:
                if not ind_invo:
                  total_time_list_info_dict_merge[test_me][ind_instance]["num_subinstance"]=[len(e) for e in instance_time_list[warms_up:]]
                total_time_list_info_dict_merge[test_me][ind_instance]["pythonic_time_list"].append(valid_time_list)
                if total_time_list_info_dict_merge[test_me][ind_instance]["num_ele"] is None:
                  try:
                    total_time_list_info_dict_merge[test_me][ind_instance]["num_ele"] = int(
                      num_add_ele_dict[test_me][ind_instance][0][0])
                  except:

                    print("num_add_ele_dict[test_me][ind_instance] is None: ", num_add_ele_dict)
                    traceback.print_exc()
              simp_instance_time_list = simple_code_time_list[ind_invo][test_me][ind_instance]
              valid_time_list = [float(ee) for e in instance_time_list[warms_up:] for ee in e]
              if valid_time_list:
                total_time_list_info_dict_merge[test_me][ind_instance]["time_list"].append(
                  valid_time_list)

    # for ind_invo, each_compli_code_time_dict in enumerate(simple_code_time_list):
    #   for test_me in each_compli_code_time_dict:
    #     # if test_me in stable_info_dict:
    #       for ind_instance, instance_time_list in enumerate(each_compli_code_time_dict[test_me]):
    #         # if ind_instance in stable_info_dict[test_me]:
    #           valid_time_list = [float(ee) for e in instance_time_list[warms_up:] for ee in e]
    #           if valid_time_list:
    #             total_time_list_info_dict_merge[test_me][ind_instance]["time_list"].append(
    #               valid_time_list)

    self.total_time_list_info_dict = total_time_list_info_dict_merge
    return total_time_list_info_dict_merge
  def get_stable_time_list_tosem_2020(self, warms_up=3):
    stable_info_dict=self.get_stable_info_dict(threshold=0)
    compli_code_time_list = self.compli_code_time_dict
    simple_code_time_list = self.simple_code_time_dict
    num_add_ele_dict = self.num_ele_list
    total_time_list_info_dict = dict()
    for ind_invo, each_compli_code_time_dict in enumerate(compli_code_time_list):
      for test_me in each_compli_code_time_dict:
        if test_me in stable_info_dict:
          for ind_instance, instance_time_list in enumerate(each_compli_code_time_dict[test_me]):
            if ind_instance in stable_info_dict[test_me]:
              if test_me not in total_time_list_info_dict:
                total_time_list_info_dict[test_me] = dict()
              if ind_instance not in total_time_list_info_dict[test_me]:
                total_time_list_info_dict[test_me][ind_instance] = {"time_list": [], "num_ele": None,
                                                                    "pythonic_time_list": []}
              valid_time_list = [float(e) for e in instance_time_list[warms_up:]]
              if valid_time_list:
                total_time_list_info_dict[test_me][ind_instance]["pythonic_time_list"].append(valid_time_list)
                if total_time_list_info_dict[test_me][ind_instance]["num_ele"] is None:
                  try:
                    total_time_list_info_dict[test_me][ind_instance]["num_ele"] = int(
                      num_add_ele_dict[test_me][ind_instance][0])
                  except:
                    print("steady_time_list: ", valid_time_list)
                    print("num_add_ele_dict[test_me][ind_instance]: ", num_add_ele_dict[test_me][ind_instance])
                    traceback.format_exc()
                    raise

    for ind_invo, each_compli_code_time_dict in enumerate(simple_code_time_list):
      for test_me in each_compli_code_time_dict:
        if test_me in stable_info_dict:
          for ind_instance, instance_time_list in enumerate(each_compli_code_time_dict[test_me]):
            if ind_instance in stable_info_dict[test_me]:
              valid_time_list = [float(e) for e in instance_time_list[warms_up:]]
              if valid_time_list:
                total_time_list_info_dict[test_me][ind_instance]["time_list"].append(
                  valid_time_list)

    self.total_time_list_info_dict = total_time_list_info_dict
    return total_time_list_info_dict
  def update_kld_real_max_min(self,remove_outlier=0,warmups=3,steps=1000):
    dict_cov_time_list=self.dict_cov_ci_kld_time_list
    if not hasattr(self,"total_time_list_info_dict"):
      self.get_stable_time_list_tosem_2020(warms_up=warmups)
    if self.total_time_list_info_dict:
      total_time_list_info_dict=self.total_time_list_info_dict
      for test_me in total_time_list_info_dict:
        # dict_cov_time_list[test_me]=dict()
        for ind_instance in total_time_list_info_dict[test_me]:
          # dict_cov_time_list[test_me][ind_instance]=dict()
          cov_instance_list = []
          cov_idiom_instance_list = []
          ci_instance_list = []
          ci_idiom_instance_list = []
          prob_kld_instance_list = []
          prob_kld_idiom_instance_list = []
          pre_valid_time_list=[]
          pre_valid_idiom_time_list=[]
          for invocations in range(1, min(len(total_time_list_info_dict[test_me][ind_instance]["time_list"]), len(
                  total_time_list_info_dict[test_me][ind_instance]["pythonic_time_list"])) + 1):
            valid_time_list = total_time_list_info_dict[test_me][ind_instance]["time_list"][:invocations]
            valid_idiom_time_list = total_time_list_info_dict[test_me][ind_instance]["pythonic_time_list"][:invocations]
            flat_valid_time_list = [e for e_invo_list in valid_time_list for e in e_invo_list]
            flat_valid_idiom_time_list = [e for e_invo_list in valid_idiom_time_list for e in e_invo_list]
            # print("len of valid_time_list: ",len(flat_valid_time_list),len(flat_valid_idiom_time_list))

            if invocations!=1:
              kld_time=performance_util.get_kld_x_y(pre_valid_time_list,flat_valid_time_list,remove_outlier)
              kld_idiom_time=performance_util.get_kld_x_y(pre_valid_idiom_time_list, flat_valid_idiom_time_list,remove_outlier)
              prob_kld_instance_list.append(kld_time)
              prob_kld_idiom_instance_list.append(kld_idiom_time)
            pre_valid_time_list=flat_valid_time_list
            pre_valid_idiom_time_list=flat_valid_idiom_time_list

          dict_cov_time_list[test_me][ind_instance]["kld_time_list"] = prob_kld_instance_list
          dict_cov_time_list[test_me][ind_instance]["kld_pythonic_time_list"] = prob_kld_idiom_instance_list
          # print("self.dict_cov_ci_kld_time_list: ",dict_cov_time_list)
    self.dict_cov_ci_kld_time_list=dict_cov_time_list
  def compute_CI_forks_list(self,warmups=3,steps=1000):
    if hasattr(self, "dict_cov_ci_kld_time_list"):
      dict_cov_time_list=self.dict_cov_ci_kld_time_list
    else:
      dict_cov_time_list = dict()
    if not hasattr(self, "total_time_list_info_dict"):
      self.get_stable_time_list_tosem_2020(warms_up=warmups)
    if self.total_time_list_info_dict:
      total_time_list_info_dict = self.total_time_list_info_dict
      for test_me in total_time_list_info_dict:
        if test_me not in dict_cov_time_list:
          dict_cov_time_list[test_me] = dict()
        for ind_instance in total_time_list_info_dict[test_me]:
          if ind_instance not in dict_cov_time_list[test_me]:
            dict_cov_time_list[test_me][ind_instance] = dict()
          cov_instance_list = []
          cov_idiom_instance_list = []
          ci_instance_list = []
          ci_idiom_instance_list = []
          prob_kld_instance_list = []
          prob_kld_idiom_instance_list = []
          pre_valid_time_list = []
          pre_valid_idiom_time_list = []
          for invocations in range(1, min(len(total_time_list_info_dict[test_me][ind_instance]["time_list"]), len(
                  total_time_list_info_dict[test_me][ind_instance]["pythonic_time_list"])) + 1):
            valid_time_list = total_time_list_info_dict[test_me][ind_instance]["time_list"][:invocations]
            valid_idiom_time_list = total_time_list_info_dict[test_me][ind_instance]["pythonic_time_list"][:invocations]
            flat_valid_time_list = [e for e_invo_list in valid_time_list for e in e_invo_list]
            flat_valid_idiom_time_list = [e for e_invo_list in valid_idiom_time_list for e in e_invo_list]
            # print("len of valid_time_list: ",len(flat_valid_time_list),len(flat_valid_idiom_time_list))
            all_boot_time_list = performance_util.num_bootstrap(valid_time_list, steps=steps)
            all_boot_idiom_time_list = performance_util.num_bootstrap(valid_idiom_time_list, steps=steps)
            left, right = performance_util.compute_ci(all_boot_time_list)
            mean_time = (right - left) / np.mean(valid_time_list)
            ci_instance_list.append(mean_time)
            left, right = performance_util.compute_ci(all_boot_idiom_time_list)
            mean_time = (right - left) / np.mean(valid_idiom_time_list)
            ci_idiom_instance_list.append(mean_time)

          dict_cov_time_list[test_me][ind_instance]["ci_time_list"] = ci_instance_list
          dict_cov_time_list[test_me][ind_instance]["ci_pythonic_time_list"] = ci_idiom_instance_list

    # print("self.dict_cov_ci_kld_time_list: ",dict_cov_time_list)
    self.dict_cov_ci_kld_time_list = dict_cov_time_list
  def compute_cov_CI_forks_list(self,warmups=3,steps=1000):
    dict_cov_time_list=dict()
    if not hasattr(self,"total_time_list_info_dict"):
      self.get_stable_time_list_tosem_2020(warms_up=warmups)
    if self.total_time_list_info_dict:
      total_time_list_info_dict=self.total_time_list_info_dict
      for test_me in total_time_list_info_dict:
        dict_cov_time_list[test_me]=dict()
        for ind_instance in total_time_list_info_dict[test_me]:
          dict_cov_time_list[test_me][ind_instance]=dict()
          cov_instance_list = []
          cov_idiom_instance_list = []
          ci_instance_list = []
          ci_idiom_instance_list = []
          prob_kld_instance_list = []
          prob_kld_idiom_instance_list = []
          pre_valid_time_list=[]
          pre_valid_idiom_time_list=[]
          for invocations in range(1, min(len(total_time_list_info_dict[test_me][ind_instance]["time_list"]), len(
                  total_time_list_info_dict[test_me][ind_instance]["pythonic_time_list"])) + 1):
            valid_time_list = total_time_list_info_dict[test_me][ind_instance]["time_list"][:invocations]
            valid_idiom_time_list = total_time_list_info_dict[test_me][ind_instance]["pythonic_time_list"][:invocations]
            flat_valid_time_list = [e for e_invo_list in valid_time_list for e in e_invo_list]
            flat_valid_idiom_time_list = [e for e_invo_list in valid_idiom_time_list for e in e_invo_list]
            # print("len of valid_time_list: ",len(flat_valid_time_list),len(flat_valid_idiom_time_list))
            all_boot_time_list = performance_util.num_bootstrap(valid_time_list, steps=steps)
            all_boot_idiom_time_list = performance_util.num_bootstrap(valid_idiom_time_list, steps=steps)
            left, right =performance_util.compute_ci(all_boot_time_list)
            mean_time=(right-left)/np.mean(valid_time_list)
            ci_instance_list.append(mean_time)
            left, right = performance_util.compute_ci(all_boot_idiom_time_list)
            mean_time = (right - left) / np.mean(valid_idiom_time_list)
            ci_idiom_instance_list.append(mean_time)

            cov = performance_util.compute_cov(flat_valid_time_list)
            # if cov>5:
            #     print(f"{test_me} of {ind_instance} cov>30: ",cov,invocations)
            cov_instance_list.append(cov)
            cov = performance_util.compute_cov(flat_valid_idiom_time_list)
            if invocations!=1:
              kld_time=performance_util.get_kld_x_y(pre_valid_time_list,flat_valid_time_list)
              kld_idiom_time=performance_util.get_kld_x_y(pre_valid_idiom_time_list, flat_valid_idiom_time_list)
              prob_kld_instance_list.append(kld_time)
              prob_kld_idiom_instance_list.append(kld_idiom_time)
            pre_valid_time_list=flat_valid_time_list
            pre_valid_idiom_time_list=flat_valid_idiom_time_list

            cov_idiom_instance_list.append(cov)
          dict_cov_time_list[test_me][ind_instance]["kld_time_list"] = prob_kld_instance_list
          dict_cov_time_list[test_me][ind_instance]["kld_pythonic_time_list"] = prob_kld_idiom_instance_list
          dict_cov_time_list[test_me][ind_instance]["ci_time_list"] = ci_instance_list
          dict_cov_time_list[test_me][ind_instance]["ci_pythonic_time_list"] = ci_idiom_instance_list
          dict_cov_time_list[test_me][ind_instance]["cov_time_list"]=cov_instance_list
          dict_cov_time_list[test_me][ind_instance]["cov_pythonic_time_list"] = cov_idiom_instance_list
    # print("self.dict_cov_ci_kld_time_list: ",dict_cov_time_list)

    self.dict_cov_ci_kld_time_list=dict_cov_time_list
  def bootstrap_time_list(self,warmups=3,steps=1000):
    dict_cov_time_list=dict()
    if hasattr(self,"total_time_list_info_dict"):
      self.get_stable_time_list_tosem_2020(warms_up=warmups)
    if self.total_time_list_info_dict:
      total_time_list_info_dict=self.total_time_list_info_dict
      for test_me in total_time_list_info_dict:
        dict_cov_time_list[test_me]=dict()
        for ind_instance in total_time_list_info_dict[test_me]:
          dict_cov_time_list[test_me][ind_instance]=dict()
          ci_instance_list = []
          ci_idiom_instance_list = []

          for invocations in range(1, min(len(total_time_list_info_dict[test_me][ind_instance]["time_list"]), len(
                  total_time_list_info_dict[test_me][ind_instance]["pythonic_time_list"])) + 1):
            valid_time_list = total_time_list_info_dict[test_me][ind_instance]["time_list"][:invocations]
            valid_idiom_time_list = total_time_list_info_dict[test_me][ind_instance]["pythonic_time_list"][:invocations]
            # print("len of valid_time_list: ",len(flat_valid_time_list),len(flat_valid_idiom_time_list))
            all_boot_time_list = performance_util.num_bootstrap(valid_time_list, steps=steps)
            all_boot_idiom_time_list = performance_util.num_bootstrap(valid_idiom_time_list, steps=steps)

            ci_idiom_instance_list.append(all_boot_idiom_time_list)
            ci_instance_list.append(all_boot_time_list)

          dict_cov_time_list[test_me][ind_instance]["bootstrap_time_list_pre_k_forks"] = ci_instance_list
          dict_cov_time_list[test_me][ind_instance]["bootstrap_pythonic_time_list_pre_k_forks"] = ci_idiom_instance_list
    # print("self.dict_cov_ci_kld_time_list: ",dict_cov_time_list)
    self.dict_ci_bootstrap_time_list=dict_cov_time_list
  # 计算前k个forks的CI
  # def update_ci_info(self):


  #'''
  # 计算k+1个forks与k个forks的diff/k_mean的CI
  def ci_diff_k_plus_1_forks_k_forks(self,warmups=3,steps=1000,bootstrap_time_remove_flag=0):
    dict_cov_time_list=dict()
    if hasattr(self,"dict_ci_bootstrap_time_list"):
      dict_ci_bootstrap_time_list=self.dict_ci_bootstrap_time_list
      for test_me in dict_ci_bootstrap_time_list:
        dict_cov_time_list[test_me]=dict()
        for ind_instance in dict_ci_bootstrap_time_list[test_me]:
          dict_cov_time_list[test_me][ind_instance] = dict()
          bootstrap_time_list_pre_k_forks=dict_ci_bootstrap_time_list[test_me][ind_instance]["bootstrap_time_list_pre_k_forks"]
          ci_instance_list=performance_util.get_ci_diff_list(bootstrap_time_list_pre_k_forks)

          bootstrap_pythonic_time_list_pre_k_forks=dict_ci_bootstrap_time_list[test_me][ind_instance]["bootstrap_pythonic_time_list_pre_k_forks"]
          ci_idiom_instance_list = performance_util.get_ci_diff_list(bootstrap_pythonic_time_list_pre_k_forks)

          dict_cov_time_list[test_me][ind_instance]["ci_diff_time_list_before_after_forks"] = ci_instance_list
          dict_cov_time_list[test_me][ind_instance]["pythonic_ci_diff_time_before_after_forks"] = ci_idiom_instance_list
      self.dict_ci_diff_before_after_forks=dict_cov_time_list
      print("use dict_ci_bootstrap_time_list to compute self.dict_cov_ci_kld_time_list: ", dict_cov_time_list)

      if bootstrap_time_remove_flag:
        self.__delattr__("dict_ci_bootstrap_time_list")
      return None
    if not hasattr(self,"total_time_list_info_dict"):
      self.get_stable_time_list_tosem_2020(warms_up=warmups)
    if self.total_time_list_info_dict:
      total_time_list_info_dict=self.total_time_list_info_dict
      for test_me in total_time_list_info_dict:
        dict_cov_time_list[test_me]=dict()
        for ind_instance in total_time_list_info_dict[test_me]:
          dict_cov_time_list[test_me][ind_instance]=dict()
          ci_instance_list = []
          ci_idiom_instance_list = []
          pre_valid_time_list = []
          pre_valid_idiom_time_list = []
          for invocations in range(1, min(len(total_time_list_info_dict[test_me][ind_instance]["time_list"]), len(
                  total_time_list_info_dict[test_me][ind_instance]["pythonic_time_list"])) + 1):
            valid_time_list = total_time_list_info_dict[test_me][ind_instance]["time_list"][:invocations]
            valid_idiom_time_list = total_time_list_info_dict[test_me][ind_instance]["pythonic_time_list"][:invocations]
            # print("len of valid_time_list: ",len(flat_valid_time_list),len(flat_valid_idiom_time_list))
            all_boot_time_list = performance_util.num_bootstrap(valid_time_list, steps=steps)
            all_boot_idiom_time_list = performance_util.num_bootstrap(valid_idiom_time_list, steps=steps)
            if invocations != 1:
              diff = performance_util.get_ci_diff(pre_valid_time_list, all_boot_time_list)
              pythonic_diff = performance_util.get_ci_diff(pre_valid_idiom_time_list, all_boot_idiom_time_list)
              ci_idiom_instance_list.append(pythonic_diff)
              ci_instance_list.append(diff)
            pre_valid_time_list = all_boot_time_list
            pre_valid_idiom_time_list = all_boot_idiom_time_list


          dict_cov_time_list[test_me][ind_instance]["ci_diff_time_list_before_after_forks"] = ci_instance_list
          dict_cov_time_list[test_me][ind_instance]["pythonic_ci_diff_time_before_after_forks"] = ci_idiom_instance_list
    print("use time list to compute self.dict_cov_ci_kld_time_list: ",dict_cov_time_list)
    self.dict_ci_diff_before_after_forks=dict_cov_time_list
  #'''
  def save_sizeof_feature(self,feature):
      self.size_obj_dict=feature
  def get_code_str(self):
    code_str_list=[]
    for e in self.code_info:
      if isinstance(e, list):
        continue
      elif isinstance(e,ast.AST):
        code_str_list.append(ast.unparse(e))
      elif isinstance(e,str):
        code_str_list.append(e)
    return "\n".join(code_str_list)

  def get_features(self):

    dict_feature={"num_loop": 0, "num_if": 0, "num_if_else": 0,
                    "num_func_call": 0,"num_param":0,
                 "num_var":0,"num_List":0,"num_Dict":0,"num_Set":0,"num_Tuple":0,"num_Subscript":0,"num_Slice":0,"num_Attr":0,
                 "num_line":0, "num_Keywords":0,"num_constant":0,"num_Operators":0,"num_Delimiters":0}
    new_feature={}
    dict_feature = {"num_for": 0, "num_if": 0, "num_if_else": 0,
                    "num_func_call": 0, "num_ele": int(self.num_add_ele)}
    num_for = 0
    num_if = 0
    num_if_else = 0
    num_func_call = 0
    num_ele = 0
    for_node = self.code_info[0]
    assign_node_node = self.code_info[1]
    ast.Set
    ast.List
    ast.Tuple
    ast.Dict
    for node in ast.walk(for_node):
      if isinstance(node, ast.For):
        dict_feature["num_for"] += 1
      elif isinstance(node, ast.If):
        if node.orelse:
          dict_feature["num_if_else"] += 1
        else:
          dict_feature["num_if"] += 1
      elif isinstance(node, ast.Call):
        dict_feature["num_func_call"] += 1
    self.dict_feature = dict_feature
    return dict_feature






