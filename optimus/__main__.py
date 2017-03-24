docstr = """
Optimus

Usage: optimus.py [-h] (<file> <config>) [-o <output.json>]

Options:
  -h --help                                     show this message and exit
  -o <output.json> --output=<output.json>       optional output file for results

"""
import csv

from docopt import docopt
import dateutil.parser as date_parser
import yaml

from .project_specific import hcv_target

_file = '<file>'
_config = '<config>'
_output = '--output'

# config magic strings
_subj = 'subject' # this refers to the column that holds the subject id
_ev = 'event' # this refers to the column that holds the event decider
_id = 'identifier' # identifies the row as the results of a particular test
_delim = 'delimiter' # how the csv is delimited
_qc = 'quotechar' # how things are quoted
_map = 'mappings'
__field_delete = '__DELETE__'

# config mapping magic strings
_rk = 'row_key'
_hdr = 'headers'
_hk = 'header_key'
_fld = 'field'
_v = 'value'
_t = 'transform'

transforms = {
    'format_date': lambda d : date_parser.parse(d).strftime('%Y-%m-%d')
}

def main(args=docopt(docstr)):
    with open(args[_config], 'r') as config_file:
        global config
        config = yaml.load(config_file.read())

    csv_file = open(args[_file], 'r')
    data = csv.DictReader(csv_file, delimiter=config[_delim], quotechar=config[_qc])

    csv_output_data = []
    for row in data:
        row_data = get_row_data(row)
        for item in row_data:
            csv_output_data.append(item)

    csv_file.close()

    if args.get(_output):
        with open(args[_output], 'w') as outfile:
            # outfile.write(autobots.transform_and_roll_out())
            pass
    else:
        pass
        # print(autobots.transform_and_roll_out())

def get_row_data(row):
    data_for_row = []
    for row_map in config['rows']:
        if row[config['key_header']] == row_map['row_key']:
            outputs = row_map['outputs']
            for out in outputs:
                datum = {
                    'datum': row[out['datum']],
                    'field': out['field'],
                    'date': row[out['date']],
                    'subj': row[out['subj']],
                }
                data_for_row.append(datum)
    return data_for_row or []


if __name__ == '__main__':
    args = docopt(docstr)
    main(args)
    exit()

