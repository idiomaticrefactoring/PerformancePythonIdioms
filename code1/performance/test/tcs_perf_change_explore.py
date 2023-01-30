import sys,ast,os,csv,time,traceback
code_dir="/".join(os.path.abspath(__file__).split("/")[:-3])+"/"
sys.path.append(code_dir)
# sys.path.append(code_dir+"lab_performance/")
sys.path.append(code_dir+"test_case/")
import util,get_test_case_acc_util,performance_util,configure_pro_envir_util
from code_info import CodeInfo
from extract_simp_cmpl_data import ast_util
import ast_performance_util
# import replace_content_by_ast_time_percounter
import performance_replace_content_by_ast_time_percounter
if __name__ == '__main__':
    bench_time_info_dir = util.data_root + "performance/list_compre_benchmarks_perf_change/"
    for file_name in os.listdir(bench_time_info_dir):

        file_name_no_suffix=file_name[:-4]
        lab_code_info = util.load_pkl(bench_time_info_dir, file_name_no_suffix)
        lab_code_info: CodeInfo
        cl, me, repo_name = lab_code_info.cl, lab_code_info.me, lab_code_info.repo_name
        # print(lab_code_info.compli_code_time_dict)
        #lab_code_info.simple_code_time_dict
        file_html=lab_code_info.file_html
        #"https://github.com/kylejusticemagnuson/pyti/tree/master/pyti/directional_indicators.py":
        # reader---"https://github.com/kellyjonbrazil/jc/tree/master/jc/parsers/systemctl_luf.py":
        #"https://github.com/tanghaibao/goatools/tree/master/goatools/nt_utils.py":
        # csv_obj---"https://github.com/TabViewer/tabview/tree/master/tabview/tabview.py"
        #"https://github.com/vinta/fuck-coding-interviews/tree/master/data_structures/graphs/adjacency_map_directed_weighted_graph.py"
        #"https://github.com/rasbt/mlxtend/tree/master/mlxtend/evaluate/confusion_matrix.py"
        '''
        ele 多的时候
        #https://github.com/kellyjonbrazil/jc/tree/master/jc/parsers/systemctl_ls.py 26 下降
        #https://github.com/kellyjonbrazil/jc/tree/master/jc/parsers/systemctl_luf.py 246 轻微上升
        #https://github.com/kylejusticemagnuson/pyti/tree/master/pyti/directional_indicators.py 127 下降
        #https://github.com/TabViewer/tabview/tree/master/tabview/tabview.py 31 下降
        #https://github.com/tanghaibao/goatools/tree/master/goatools/nt_utils.py 119 下降
        https://github.com/vinta/fuck-coding-interviews/tree/master/data_structures/graphs/adjacency_map_directed_weighted_graph.py
        30 18 8 ele 下降
        #
        
        #"https://github.com/in-toto/in-toto/tree/master/in_toto/rulelib.py" 
        这个重点check 10 ele 有1个提升，下降； 8 个ele 3个有提升，下降； 6 个ele 有提升，下降
        #https://github.com/rlabbe/filterpy/tree/master/filterpy/kalman/UKF.py
        这个重点check 5 ele 有下降和上升
        #https://github.com/Axelrod-Python/Axelrod/tree/master/axelrod/graph.py
        这个重点check 6 ele 下降, 2 ele 上升
        #https://github.com/maqp/tfc/tree/master/src/common/reed_solomon.py
        ele 1 有上升1.1和轻微下降
        #https://github.com/more-itertools/more-itertools/tree/master/more_itertools/more.py
        ele 3 有上升1.5和下降轻微
        #https://github.com/salesforce/policy_sentry/tree/master/policy_sentry/util/arns.py
        ele 2 有上升和下降, 3 上升, 4 下降
        #https://github.com/TomasTomecek/sen/tree/master/sen/tui/widgets/table.py
        ele 2 有上升和下降
        
        #https://github.com/berkerpeksag/astor/tree/master/tests/support.py
        这个重点check 0 ele 竟然速度improve
        #https://github.com/dulwich/dulwich/tree/master/dulwich/pack.py
        这个重点check 1,2 ele 竟然速度improve >2x
        #https://github.com/gnebbia/kb/tree/master/kb/db.py
        0 ele 竟然速度improve >1.5x 1 ele improve <1.5x
        #https://github.com/google/pinject/tree/master/pinject/bindings.py
        0, 1 速度improve
        #https://github.com/gugarosa/opytimizer/tree/master/opytimizer/optimizers/swarm/kh.py
        0 ele improve
        #https://github.com/indigo-dc/udocker/tree/master/udocker/cmdparser.py
        0 ele improve
        #https://github.com/indigo-dc/udocker/tree/master/udocker/container/structure.py
        2 ele improve
        #https://github.com/indigo-dc/udocker/tree/master/udocker/engine/fakechroot.py
        0, 2 ele improve
        #https://github.com/simpleai-team/simpleai/tree/master/simpleai/search/csp.py
        2 ele 1.5
        #https://github.com/soxoj/maigret/tree/master/maigret/report.py
        2 ele 1.2
        
        #https://github.com/in-toto/in-toto/tree/master/in_toto/verifylib.py
        随着元素增多 performance change 减少，当到6的时候,反而在1的左右了。1 ele的时候perf change最大
        #https://github.com/kellyjonbrazil/jc/tree/master/jc/parsers/csv_s.py
        0 ele improve, 2 ele 在1.0x左右, 11766/128/87 下降, 18 ele 上升
        #https://github.com/nccgroup/ScoutSuite/tree/master/ScoutSuite/core/fs.py 
        ele 2的时候上升 1.3
                     ｜
                     ｜
        https://github.com/google/capirca/tree/master/tools/cgrep.py 
        2 ele 下降
        https://github.com/idealo/imagededup/tree/master/imagededup/utils/general_utils.py
        2,1 ele 下降
        https://github.com/pydicom/pydicom/tree/master/pydicom/fileset.py
        0,1,3 ele 轻微下降/上升
        https://github.com/rasbt/mlxtend/tree/master/mlxtend/evaluate/confusion_matrix.py
        4 ele 轻微下降 16 上升1.2
        
        
        https://github.com/readbeyond/aeneas/tree/master/aeneas/globalfunctions.py
        0 improve 1,2 ele 下降
        
        
        #https://github.com/cantools/cantools/tree/master/cantools/subparsers/dump/formatting.py
        这个 8 ele 有上升和下降  3 ele 有上升和下降 0,1,2 ele都上升了
        #https://github.com/cloud-custodian/cloud-custodian/tree/master/c7n/filters/iamaccess.py
        0 ele 有上升和下降
        #https://github.com/HunterMcGushion/hyperparameter_hunter/tree/master/hyperparameter_hunter/space/space_core.py
        1 ele 有上升和下降
        #https://github.com/networkx/networkx/tree/master/networkx/algorithms/coloring/equitable_coloring.py
        0 ele 有上升 1.3和下降 0.8
        #https://github.com/networkx/networkx/tree/master/networkx/readwrite/json_graph/adjacency.py
        2 ele 有上升和下降，1 ele 下降
        #https://github.com/PyTorchLightning/lightning-flash/tree/master/flash/core/classification.py
        2 ele 有上升和下降
        #https://github.com/quantumlib/OpenFermion/tree/master/src/openfermion/chem/molecular_data.py
        2 ele 有上升和下降
        #https://github.com/quantumlib/OpenFermion/tree/master/src/openfermion/transforms/repconversions/qubit_tapering_from_stabilizer.py
        2 ele 上升和下降 1 ele 有上升和下降
        2 ele 下降
        '''
        if file_html!="https://github.com/kellyjonbrazil/jc/tree/master/jc/parsers/systemctl_ls.py":#"https://github.com/kellyjonbrazil/jc/tree/master/jc/parsers/systemctl_luf.py":#"https://github.com/Axelrod-Python/Axelrod/tree/master/axelrod/graph.py":#"https://github.com/in-toto/in-toto/tree/master/in_toto/rulelib.py":#"https://github.com/vinta/fuck-coding-interviews/tree/master/data_structures/graphs/adjacency_map_directed_weighted_graph.py":#"https://github.com/kylejusticemagnuson/pyti/tree/master/pyti/directional_indicators.py":#"https://github.com/kellyjonbrazil/jc/tree/master/jc/parsers/systemctl_luf.py":
            continue

        total_time_list_info_dict=lab_code_info.total_time_list_info_dict
        for key in total_time_list_info_dict:
            test_html,test_total, test_cl, test_me=key
            # if test_html!="https://github.com/kellyjonbrazil/jc/tree/master/tests/test_csv.py":
            #     continue
            print(repo_name, cl, me, file_html, lab_code_info.get_code_str())
            print("test_html,test_total, test_cl, test_me: ",file_name,test_html,test_total, test_cl, test_me)
            for instance in total_time_list_info_dict[key]:
                print('>>>>>>>>>>>>>instance-',instance)
                time_list=total_time_list_info_dict[key][instance]['time_list']
                pythonic_time_list=total_time_list_info_dict[key][instance]['pythonic_time_list']
                print("time_list: ",time_list)
                print("pythonic_time_list: ", pythonic_time_list)
                print("num_ele: ", total_time_list_info_dict[key][instance]['num_ele'])
                print("perf_change: ",lab_code_info.total_time_list_info_dict[key][instance]["perf_change"])

        # break
    pass
