"""
Reads special core analysis and core description from SPWLA formatted files.

Usage:
    ./spwla.py infile.spwla outfile.csv

Author:
    Matt Hall, ca. 2021
    © agilescientific.com

Licence:
    Apache 2.0
"""
import pandas as pd
from parsimonious import Grammar
from parsimonious import NodeVisitor

GRAMMAR = Grammar(
    r"""
    file          = file_block field_block core_groups*

    file_block    = "10" ws number ws file_data ws
    file_data     = well_name ws country ws date ws company ws

    field_block   = "15" ws number ws number ws field_row+
    field_row     = number ws number ws number ws "0" company ws field_name ws

    core_groups   = range_block data_blocks*

    range_block   = "20" ws number ws range_data ws
    range_data    = number ws number ws start_depth ws stop_depth ws number ws number ws

    data_blocks   = depth_block descr_block? data_block?
    depth_block   = "30" ws "1" ws depth ws number ws number ws
    descr_block   = "36" ws "1" ws "1" ws description ws
    data_block    = "40" ws "1" ws record_count ws data ws

    start_depth   = number+
    stop_depth    = number+
    record_count  = number+
    depth         = number+
    description   = sentence+
    field_name    = sentence+

    ws            = ~r"\s*"
    number        = ~r"[-.0-9]+"
    data          = ~r"[- .0-9]+"
    well_name     = ~r"[-/0-9]+"
    country       = ~r"[A-Z]+"i
    company       = ~r"[-_A-Z]+"i
    date          = ~r"[A-Z0-9]+"i
    sentence      = ~r"[-., /ÅA-Z0-9]"i
    """
)


class FileVisitor(NodeVisitor):
    """
    Crawl the tree collecting the data.
    """

    def __init__(self, date_fmt="%y%b%d"):
        self.date_fmt = date_fmt

    # -------------- File --------------
    def visit_file(self, node, visited_children):

        file, fields, cores = visited_children

        info = {}
        info['file'] = file
        info['fields'] = fields
        info['cores'] = cores

        return info

    # -------------- Meta --------------
    def visit_file_block(self, node, visited_children):
        *_, file_data, _ = visited_children
        return file_data

    def visit_file_data(self, node, visited_children):
        well, _, country, _, date, _, company, _ = node.children
        meta = {'well name': well.text}
        meta['country'] = country.text
        meta['company'] = company.text
        try:
            meta['date'] = pd.to_datetime(date.text, format=self.date_fmt).isoformat()
        except (TypeError, ValueError) as e:
            meta['date'] = date.text
        return meta

    # -------------- Fields --------------
    def visit_field_block(self, node, visited_children):
        *_, fields = visited_children
        return fields

    def visit_field_row(self, node, visited_children):
        *_, field, _ = node.children
        return field.text.strip()

    # -------------- Groups --------------
    def visit_core_groups(self, node, visited_children):
        core_info, core_data, *_ = visited_children

        # Prevent getting garbage if not present.
        if not isinstance(core_data, list):
            core_data = []

        return {'meta': core_info, 'samples': core_data}

    # -------------- Range --------------
    def visit_range_block(self, node, visited_children):
        *_, rnge, _ = visited_children
        return rnge

    def visit_range_data(self, node, visited_children):
        # number ws number ws start_depth ws stop_depth ws number ws number ws
        *_, start, _, stop, _, _, _, seq, _ = node.children
        meta = {'seq': int(seq.text), 'start': float(start.text), 'stop': float(stop.text)}
        return meta

    # -------------- ALL DATA --------------
    def visit_data_blocks(self, node, visited_children):
        depth, descr, data = visited_children

        if not isinstance(descr, list):
            descr = ['']

        if not isinstance(data, list):
            data = [[]]

        return {'depth': depth, 'descr': descr[0], 'data': data[0]}

    # -------------- Depth --------------
    def visit_depth_block(self, node, visited_children):
        _, _, _, _, depth, *_ = node.children
        return float(depth.text)

    # -------------- Descr --------------
    def visit_descr_block(self, node, visited_children):
        *_, descr, _ = visited_children
        return descr.strip()

    def visit_description(self, node, visited_children):
        return node.text

    # -------------- Data --------------
    def visit_data_block(self, node, visited_children):
        *_, data, _ = visited_children
        return data

    def visit_data(self, node, visited_children):
        return [float(x) for x in node.text.split()]

    # -------------- Generic --------------
    def generic_visit(self, node, visited_children):
        return visited_children or node


def parse(fname, grammar=None, date_fmt="%y%b%d"):
    """
    Given an SPWLA file and a parsimonious PEG grammar, return an abstract
    syntax tree as a dictionary.
    """
    with open(fname) as f:
        text = f.read()

    if grammar is None:
        grammar = GRAMMAR

    tree = grammar.parse(text)
    fv = FileVisitor(date_fmt=date_fmt)
    return fv.visit(tree)


def serialize(f):
    """
    Turn the abstract syntax tree into tidy data (i.e. one row per record).
    """
    records = []
    for core in f['cores']:
        for sample in core['samples']:
            record = {}
            record['well name'] = f['file']['well name']
            record['country'] = f['file']['country']
            record['company'] = f['file']['company']
            record['date'] = f['file']['date']
            record['core'] = core['meta']['seq']
            for i, field in enumerate(f['fields']):
                record['depth'] = sample['depth']
                record['descr'] = sample['descr']
                record[field] = sample['data'][i]
                records.append(record)
    return records


def to_csv(seq, fname):
    """
    Take the big list of records and save a CSV. Trivial.
    """
    df = pd.DataFrame(seq)
    df.to_csv(fname)
    return


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Use like: python spwla.py infile outfile")
    _, infile, outfile = sys.argv
    to_csv(serialize(parse(infile)))
    print("Success.")