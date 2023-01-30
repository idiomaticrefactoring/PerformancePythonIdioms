import csv,os,json
import time,dis

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

def parse(data, raw=False, quiet=False):
    """
    Main text parsing function
    Parameters:
        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True
    Returns:
        List of Dictionaries. Raw or processed structured data.
    """
    x=2
    if x>7 and x<10:
        pass
    raw_output = []
    cleandata = data.splitlines()

    # Clear any blank lines
    cleandata = list(filter(None, cleandata))

    if 1:

        dialect = 'excel'  # default in csv module
        try:
            dialect = csv.Sniffer().sniff(data[:1024])
            if '""' in data:
                dialect.doublequote = True
        except Exception:
            pass

        reader = csv.DictReader(cleandata*1000, dialect=dialect)
        list_reader = reader#list(reader)
        start=time.perf_counter()
        for i in range(1):
            for row in list_reader:
                raw_output.append(row)
        end=time.perf_counter()
        print(">>>>time: ",end-start)

        print(len(raw_output))
        return end-start
def code_range():
    end_i=2
    repeat=10**6
    total_time=0
    for i in range(repeat):
        start = time.perf_counter()
        links = dict()
        for i in range(1,end_i):
            links[i]=[]
        end = time.perf_counter()
        total_time+=end - start

    total_time_python = 0
    for i in range(repeat):
        start = time.perf_counter()
        links = {i:[] for i in range(1, end_i)}
        end = time.perf_counter()
        total_time_python += end - start
        # print(">>>>time: ", )
    print("time ratio: ",total_time,total_time_python,total_time/total_time_python)

    a_list=[i for i in range(1,end_i)]
    repeat=10**6
    total_time=0
    for i in range(repeat):
        start = time.perf_counter()
        links = dict()
        for i in a_list:
            links[i]=[]
        end = time.perf_counter()
        total_time+=end - start

    total_time_python = 0
    for i in range(repeat):
        start = time.perf_counter()
        links = {i:[] for i in a_list}
        end = time.perf_counter()
        total_time_python += end - start
        # print(">>>>time: ", )
    print("time ratio: ",total_time,total_time_python,total_time/total_time_python)

if __name__ == '__main__':
    # parse(data, raw=False, quiet=False)
    # with open(os.path.join(THIS_DIR, os.pardir, 'generic/csv-flyrna.json'), 'r', encoding='utf-8') as f:
    #     generic_csv_flyrna_json = json.loads(f.read())
    #, generic_csv_flyrna_json
    code_range()
    # dict().items()
    # enumerate()
    # total_time = 0
    # print("".join([THIS_DIR, '/generic/csv-flyrna.tsv']))
    # for i in range(1):
    #     with open("".join([THIS_DIR, '/../generic/csv-flyrna.tsv']), 'r', encoding='utf-8') as f:
    #         generic_csv_flyrna = f.read()
    #         total_time+=parse(generic_csv_flyrna, quiet=True)
    #
    # print(total_time)
    # import copy
    # copy.copy()
    # # dis.dis(parse)