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

if __name__ == '__main__':
    # parse(data, raw=False, quiet=False)
    # with open(os.path.join(THIS_DIR, os.pardir, 'generic/csv-flyrna.json'), 'r', encoding='utf-8') as f:
    #     generic_csv_flyrna_json = json.loads(f.read())
    #, generic_csv_flyrna_json
    total_time = 0
    print("".join([THIS_DIR, '/generic/csv-flyrna.tsv']))
    for i in range(1):
        with open("".join([THIS_DIR, '/../generic/csv-flyrna.tsv']), 'r', encoding='utf-8') as f:
            generic_csv_flyrna = f.read()
            total_time+=parse(generic_csv_flyrna, quiet=True)

    print(total_time)
    # dis.dis(parse)