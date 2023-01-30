import csv,os,json
import time,dis

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
THIS_DIR = '/mnt/zejun/smp/code1/performance/test/'

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
        iter_time = 0
        for e in cleandata:
            e
        for i in range(30):
            reader = csv.DictReader(cleandata, dialect=dialect)
            start = time.perf_counter()
            raw_output = []
            for row in reader:
                raw_output.append(row)
            # raw_output=[row for row in reader]

            end=time.perf_counter()
            print(">>>>time: ",end-start)
            print(len(raw_output))
            if i < 2:
                continue
            iter_time += end - start


        return iter_time

if __name__ == '__main__':
    # parse(data, raw=False, quiet=False)
    # with open(os.path.join(THIS_DIR, os.pardir, 'generic/csv-flyrna.json'), 'r', encoding='utf-8') as f:
    #     generic_csv_flyrna_json = json.loads(f.read())
    #, generic_csv_flyrna_json
    file_name ="/generic/csv-flyrna2.tsv"#"/generic/systemctl-luf.out"
    total_time = 0
    print("".join([THIS_DIR, file_name]))
    for i in range(1):
        with open("".join([THIS_DIR, file_name]), 'r', encoding='utf-8') as f:
            generic_csv_flyrna = f.read()
            total_time+=parse(generic_csv_flyrna, quiet=True)
    print(total_time)
    # dis.dis(parse)