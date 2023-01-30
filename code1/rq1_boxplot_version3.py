import sys,ast,os,csv,time,copy
import numpy as np
import matplotlib.pyplot as plt
code_dir="/".join(os.path.abspath(__file__).split("/")[:-2])+"/"
sys.path.append(code_dir)
sys.path.append(code_dir+"performance/")
sys.path.append(code_dir+"lab_performance/")
sys.path.append(code_dir+"wrap_refactoring/")
import util
import lab_performance_util
import lab_performance_util
import pandas as pd
import matplotlib.scale as mscale
import matplotlib.ticker as ticker
def boxplot_feature(input_list):
    percentile = np.percentile(input_list, (25, 50, 75), interpolation='linear')

    Q1 = percentile[0]
    Q2 = percentile[1]
    Q3 = percentile[2]
    IQR = Q3 - Q1
    ulim = Q3 + 1.5 * IQR
    llim = Q1 - 1.5 * IQR
    print("boxplot_feature: ",Q1,Q3,ulim,llim)
import matplotlib.transforms as mtransforms

def read_df(path_list,key="perf_change",rciw="RCIW",dict_info_sum=dict()):
    perf_lab_list = []
    for ind_p, path in enumerate(path_list[:num_idioms]):

        list_comp_data = pd.read_csv(path)


        perf=list_comp_data[key]
        print("**********************path: ", path)
        # boxplot_feature(perf)
        print(perf.describe())
        rciw_list=list_comp_data[rciw]
        max_perf,min_perf,mean_perf,median_perf=np.max(perf),np.min(perf),np.mean(perf),np.median(perf)
        dict_info_sum["max_perf"].append(max_perf)
        dict_info_sum["min_perf"].append(min_perf)
        dict_info_sum["mean_perf"].append(mean_perf)
        dict_info_sum["median_perf"].append(median_perf)
        dict_info_sum["mean_rciw"].append(np.mean(rciw_list))
        for ind_perf,each_perf in enumerate(perf):
            if each_perf < 1:
                # if each_perf < 0.5:
                    perf[ind_perf] = (2 - 1 / (each_perf ** RATIO_scale))  # 2-(1/(each_perf+0.1**10)**0.3)
                # else:
                #     perf[ind_perf] = (2 - 1 / (each_perf))  # 2-(1/(each_perf+0.1**10)**0.3)
            else:
                # if each_perf < 2:
                #     perf[ind_perf] = each_perf
                # else:
                    perf[ind_perf] = each_perf **RATIO_scale
            # if each_perf<1:
            #     if each_perf<0.5:
            #         perf[ind_perf]=(2-1/(each_perf**0.3))#2-(1/(each_perf+0.1**10)**0.3)
            #     else:
            #         perf[ind_perf] = (2 - 1 / (each_perf ))  # 2-(1/(each_perf+0.1**10)**0.3)
            # else:
            #     if each_perf<2:
            #         perf[ind_perf] =each_perf
            #     else:
            #         perf[ind_perf] = each_perf ** 0.3
        perf_lab_list.append(perf)
    print(path,len(perf_lab_list))
    return perf_lab_list


class SquareRootScale(mscale.ScaleBase):
    """
    ScaleBase class for generating square root scale.
    """

    name = 'squareroot'

    def __init__(self, axis, **kwargs):
        # note in older versions of matplotlib (<3.1), this worked fine.
        # mscale.ScaleBase.__init__(self)

        # In newer versions (>=3.1), you also need to pass in `axis` as an arg
        mscale.ScaleBase.__init__(self, axis)

    def set_default_locators_and_formatters(self, axis):
        axis.set_major_locator(ticker.AutoLocator())
        axis.set_major_formatter(ticker.ScalarFormatter())
        axis.set_minor_locator(ticker.NullLocator())
        axis.set_minor_formatter(ticker.NullFormatter())

    def limit_range_for_scale(self, vmin, vmax, minpos):
        return max(0., vmin), vmax

    class SquareRootTransform(mtransforms.Transform):
        input_dims = 1
        output_dims = 1
        is_separable = True

        def transform_non_affine(self, a):
            b=[]
            for e in a:
                # if e==0:
                #     print("yes zero: ",e)
                #     b.append(0)
                #     continue
                if e>1:
                    b.append(e**0.3)
                else:
                    b.append(e)
            return np.array(b)
            # return (np.array(a)10) ** 0.2

        def inverted(self):
            return SquareRootScale.InvertedSquareRootTransform()

    class InvertedSquareRootTransform(mtransforms.Transform):
        input_dims = 1
        output_dims = 1
        is_separable = True

        def transform(self, a):
            return np.array(a)# ** 10

        def inverted(self):
            return SquareRootScale.SquareRootTransform()

    def get_transform(self):
        return self.SquareRootTransform()


#https://stackoverflow.com/questions/42277989/square-root-scale-using-matplotlib-python
if __name__ == '__main__':
    RATIO_scale=0.3
    list_comp_path = util.data_root_mv + "lab_performance/list_compre_benchmarks_fun_and_Nfunc_once_again/csv/train_data_list_compre.csv"

    set_comp_path = util.data_root_mv + "lab_performance/set_compre_benchmarks_once_again/csv/train_data_set_compre_2.csv"
    set_comp_path = util.data_root_mv + "lab_performance/set_compre_benchmarks_once_again_2/csv/" + "train_data_set_compre_2.csv"

    dict_comp_path = util.data_root_mv + "lab_performance/dict_compre_benchmarks/csv/train_data_dict_compre.csv"

    chain_compare_path = util.data_root_mv + "lab_performance/chain_compare_benchmarks_new/csv/train_data_chain_compare.csv"
    chain_compare_path= util.data_root_mv + "lab_performance/chain_compare_benchmarks_new_3/csv/"+"train_data_chain_compare_new_3.csv"

    truth_test_path = util.data_root_mv + "lab_performance/truth_value_test_benchmarks/csv/train_data_truth_value_test.csv"

    loop_else_path = util.data_root_mv + "lab_performance/for_else_benchmarks/csv/train_data_loop_else.csv"
    assign_multi_path = util.data_root + "lab_performance/multi_ass_benchmarks/csv/train_data_multi_ass.csv"
    star_in_call_path = util.data_root_mv + "lab_performance/call_star_benchmarks/csv/train_data_call_star.csv"
    for_multi_tar_path = util.data_root + "lab_performance/for_multi_targets_benchmarks/csv/train_data_for_multi_targets.csv"
    for_multi_tar_path= util.data_root + "lab_performance/for_multi_targets_benchmarks/csv/train_data_for_multi_targets_new.csv"

    path_list = [list_comp_path, set_comp_path, dict_comp_path, chain_compare_path, truth_test_path,
                 loop_else_path, assign_multi_path, star_in_call_path, for_multi_tar_path]
    num_idioms=9
    dict_info_list= {"path":copy.deepcopy(path_list),"max_perf":[], "min_perf":[], "mean_perf":[], "median_perf":[],"mean_rciw":[]}

    perf_lab_list=read_df(path_list,dict_info_sum=dict_info_list)
    list_comp_path = util.data_root + "performance/a_list_comprehension/list_comprehension_perf_two_result.csv"
    set_comp_path = util.data_root_mv + "performance/a_set_comprehension/csv/perf_two_result_add_num_set_compreh.csv"
    set_comp_path=util.data_root_mv + "performance/a_set_comprehension_2/csv/perf_two_result_add_num_set_compreh.csv"

    dict_comp_path = util.data_root_mv + "performance/a_dict_comprehension/csv/perf_two_result_2_add_ele.csv"
    chain_compare_path = util.data_root + "performance/chain_compare/csv/perf_two_result_chain_compare.csv"
    truth_test_path = util.data_root_mv + "performance/a_truth_value_test/csv/perf_two_result.csv"
    loop_else_path = util.data_root_mv + "performance/a_for_else/csv/perf_two_result_2.csv"
    loop_else_path = util.data_root_mv + "performance/a_for_else/csv/perf_two_result_2_for_else.csv"
    loop_else_path = util.data_root_mv + "performance/a_for_else/csv/train_data_a_for_else_add_size.csv"

    assign_multi_path = util.data_root + "performance/a_multi_assign/csv/remove_outlier_3factor_perf_two_result_merge.csv"
    assign_multi_path = util.data_root + "performance/a_multi_assign/csv/perf_two_result_merge_multi_ass.csv"

    star_in_call_path = util.data_root_mv + "performance/a_call_star_single/csv/perf_two_result_2.csv"
    star_in_call_path = util.data_root_mv + "performance/a_call_star_single/csv/perf_two_result_2_call_star.csv"
    star_in_call_path = util.data_root_mv + "performance/a_call_star_single_2/csv/train_data_call_star.csv"

    for_multi_tar_path = util.data_root_mv + "performance/a_for_multi_tar_single_2/csv/a_for_multi_tar_single_perf_two_result_total.csv"

    path_list_2 = [list_comp_path, set_comp_path, dict_comp_path, chain_compare_path, truth_test_path,
                 loop_else_path, assign_multi_path, star_in_call_path, for_multi_tar_path]
    for key in dict_info_list:
        print("len: ",key, len(dict_info_list[key]))
    # print(dict_info_list)
    dict_info_list["path"].extend(path_list)
    perf_real_list = read_df(path_list_2,key="perf_change_zonghe",rciw="RCIW_zonghe",dict_info_sum=dict_info_list)
    for key in dict_info_list:
        print("len: ",key, len(dict_info_list[key]))
    # print(dict_info_list)
    # data_a = [[1, 2, 5], [5, 7, 2, 2, 5], [7, 2, 5]]
    # data_b = [[6, 4, 2], [1, 2, 5, 3, 2], [2, 3, 5, 1]]
    dataMain = pd.DataFrame(data=dict_info_list)
    dataMain.to_csv(util.data_root_mv + "rq_1_total_statis.csv", index=False)
    ticks = ["list-\ncmpre", "set-\ncmpre", "dict-\ncmpre", "chain-\ncmp",
             "truth-\ntest", "loop-\nelse", "ass-\nmulti-tar", "star-\nin-call", "for-mul\nti-tar"]

    # ticks = ["list-comp\nrehension", "set-comp\nrehension", "dict-comp\nrehension", "chain-\ncompare",
    #           "truth-\ntest", "loop-\nelse", "ass-\nmulti-tar", "star-\nin-call", "for-mul\nti-tar"]

    #https://stackoverflow.com/questions/16592222/matplotlib-group-boxplots
    def set_box_color(bp, color):
        # bp['boxes'].set(facecolor=color)
        # bp['boxes'].set_facecolor(color)
        plt.setp(bp['fliers'], color='#f0f0f0')
        # plt.setp(bp['whiskers'], color=color)
        # plt.setp(bp['caps'], color=color)
        plt.setp(bp['boxes'], facecolor=color)
        # for patch in bp['boxes']:
        #     # for patch in e:
        #         patch.set_facecolor(color)#set(facecolor=color)
            # plt.setp(bp['medians'], color=color)

    step=3.3
    plt.figure()
    fig, ax = plt.subplots()
    flierprops = {'marker': 'o', 'markersize': 2,'markeredgecolor':'#7f7f7f'}
    bpl = ax.boxplot(perf_lab_list, positions=np.array(range(len(path_list))) * step - 0.4, widths=0.6, patch_artist=True,flierprops=flierprops)
    bpr = ax.boxplot(perf_real_list, positions=np.array(range(len(path_list_2))) * step + 0.4, widths=0.6, patch_artist=True,flierprops=flierprops)
    # color_1='#d62728'#'#e5f5e0'#'#a50f15'#'#31a354'#e5f5e0'
    # color_2='b'#'#fff7bc'#'#2C7BB6'#'#084081'#'#3182bd'#'#2C7BB6'#'#fff7bc'
   #https://matplotlib.org/stable/users/prev_whats_new/dflt_style_changes.html
    color_1='#238b45'#'#9467bd'#'#e5f5e0'#'#a50f15'#'#31a354'#e5f5e0'
    color_2='#1f77b4'#'#08519c'#'#fff7bc'#'#2C7BB6'#'#084081'#'#3182bd'#'#2C7BB6'#'#fff7bc'

    set_box_color(bpl, color_1)  #'#D7191C' colors are from http://colorbrewer2.org/
    for ind in range(0,len(bpl["whiskers"]),2):
        e=bpl["whiskers"][ind]
        e_r = bpr["whiskers"][ind]
        e_upper = bpl["whiskers"][ind+1]
        e_r_upper = bpr["whiskers"][ind+1]
        print("lab Whiskers: ", ticks[ind // 2], min(e.get_ydata()),max(e_upper.get_ydata()),max(e_upper.get_ydata())-min(e.get_ydata()))
        print("real Whiskers: ", ticks[ind // 2], min(e_r.get_ydata()),max(e_r_upper.get_ydata()),max(e_r_upper.get_ydata())-min(e_r.get_ydata()))
    # for ind,e in enumerate(bpl["whiskers"]):
    #     e_r=bpr["whiskers"][ind]
    #     print("lab Whiskers: ",ticks[ind//2],e.get_ydata())
    #     print("real Whiskers: ", ticks[ind // 2], e_r.get_ydata())
    set_box_color(bpr, color_2)#'#2C7BB6'
    # print("Whiskers: ", bpr["whiskers"], bpr["whiskers"])
    # bpl['boxes'].
    # draw temporary red and blue lines and use them to create a legend
    plt.plot([], c=color_1, label='synthetic data')
    plt.plot([], c=color_2, label='real-project data')
    plt.legend()
    # plt.xticks(fontsize=20)
    # plt.yticks(fontsize=20)
    def func_1(x,):
        for e in x:
            x**5
    # mscale.register_scale(SquareRootScale)
    # ax.set_yscale('squareroot')
    # ax.yaxis.grid(color='gray', linestyle='dashed')

    # ax.set_yscale('function',functions=(lambda x: x**5, lambda x: x**(0.2)))
    # 'function', functions = (lambda x: x ** 5, lambda x: x ** (0.2))
    # plt.yscale('log',basey=2)
    # plt.xticks(rotation=15)
    plt.xticks(np.array(range(len(path_list))) * step,ticks)#range(0, len(ticks) * 2, 2), ticks)
    plt.axhline(y=2**RATIO_scale,color='g',lw=1,linestyle="--")
    plt.axhline(y=1, color='b', lw=1, linestyle="--")
    plt.axhline(y=(2-1/(0.5**RATIO_scale)), color='r', lw=1,linestyle="--")
    plt.xlim(-2, len(ticks) * step)
    # plt.yticks([0.1,0.5]+[i for i in range(11)]+[13],['1/10','1/2']+[i for i in range(11)]+[13])
    # plt.yticks([0.1,0.5]+[i for i in range(11)]+[13],['10','2']+[i for i in range(11)]+[13])
    # plt.yticks([0.1,0.5]+[i for i in range(11)]+[13],['1/10','1/2']+[i for i in range(11)]+[13])
    # plt.yticks([0.05,0.5]+[i for i in range(11)]+[13],['1/20','1/2']+[i for i in range(11)]+[13])
    # plt.yticks([0.05,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]+[i for i in range(11)]+[13],['20','1/10','1/5','']+[i for i in range(11)]+[13])
    # plt.yticks([0,1/20,1/10,1/2,6/10,7/10,8/10,9/10]+[i for i in range(11)]+[13],['','1/20','1/10','5/10','6/10','7/10','8/10','9/10']+[i for i in range(11)]+[13])
    # plt.yticks([1/10,2/10,3/10,4/10,5/10,6/10,7/10,8/10,9/10]+[i for i in range(11)]+[13],['1/10','2/10','3/10','4/10','5/10','6/10','7/10','8/10','9/10']+[i for i in range(11)]+[13])
    plt.yticks([2-1/(1/i)**0.3 for i in [20,10,8,6,4,3,2]]+[i**0.3 for i in [1,2,3,4,6,8,10]]+[13**0.3],['20','10','8','6','4','3','2']+[i for i in [1,2,3,4,6,8,10]]+[13])

    # plt.ylim(0,14)
    # plt.yticks([0.05,0.1, 0.5]+[i for i in range(11)]+[13],['1/20','1/10','1/2']+[i for i in range(11)]+[13])

    # plt.ylim(0, 14)
    # plt.ylabel("performance change")

    plt.ylabel("<---------------slowdown--------------|--------speedup------------>")

    plt.tight_layout()

    # plt.savefig('boxcompare.png')
    plt.savefig("performance_rq1_compare_boxplot_new.pdf", format="pdf", bbox_inches="tight")
plt.show()