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


    linedata = list(filter(None, data.splitlines()))

    if 1:
        start=time.perf_counter()
        cleandata = []
        # clean up non-ascii characters, if any
        for entry in linedata:
            cleandata.append(entry.encode('ascii', errors='ignore').decode())
        end=time.perf_counter()
        print(">>>>time: ",end-start)
        print(len(cleandata))
        return end-start

if __name__ == '__main__':
    # parse(data, raw=False, quiet=False)
    # with open(os.path.join(THIS_DIR, os.pardir, 'generic/csv-flyrna.json'), 'r', encoding='utf-8') as f:
    #     generic_csv_flyrna_json = json.loads(f.read())
    #, generic_csv_flyrna_json
    total_time = 0
    file_name="/generic/systemctl-ls.out"#'/generic/csv-flyrna.tsv'
    print("".join([THIS_DIR, file_name]))
    for i in range(100):
        with open("".join([THIS_DIR, file_name]), 'r', encoding='utf-8') as f:
            generic_csv_flyrna = f.read()
            total_time+=parse(generic_csv_flyrna, quiet=True)
    print(total_time)
    dis.dis(parse)