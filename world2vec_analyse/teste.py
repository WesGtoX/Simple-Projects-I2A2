# -*- coding: utf-8 -*-
import gzip



def arxiv_reader(file_object):
    while True:
        data = file_object.read()
        if not data:
            break
        yield data

with gzip.GzipFile('/home/marco/projetos/arxiv/arxiv.txt.gz', 'r') as paper:
    for paragrafo in arxiv_reader(paper):
        print(paragrafo)


