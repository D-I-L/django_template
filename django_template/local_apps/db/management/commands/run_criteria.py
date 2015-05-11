from elastic.elastic_model import TermsFilter, ElasticQuery, Query, Search
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    ''' Script to test run criteria searches and optimise. '''

    def handle(self, *args, **options):
        query_terms = ["GDXHsS00001", 'Ptpn22', 'ctla4', 'rs2476601', '26191', 'akt3', 'duxp', '1p13.2']
        # query_terms = [line.strip() for line in open('2000_genes')]
        query_terms_lower = [s.lower() for s in query_terms]

        terms_filter = TermsFilter.get_terms_filter("alias", query_terms_lower)
        query = ElasticQuery.filtered(Query.match_all(), terms_filter)
        elastic = Search(query, idx='marker_alias,gene_alias,locus_alias,study_alias', size=2000000)

        hits = elastic.get_json_response()['hits']['hits']
        result_dict = {}
        query_term_dict = {}
        for hit in hits:
            if hit['_index'] == 'marker_alias':
                self._add_internal_id('marker', hit['_source'], result_dict, query_term_dict, query_terms_lower)
            elif hit['_index'] == 'gene_alias':
                self._add_internal_id('gene', hit['_source'], result_dict, query_term_dict, query_terms_lower)
            elif hit['_index'] == 'locus_alias':
                self._add_internal_id('locus', hit['_source'], result_dict, query_term_dict, query_terms_lower)
            elif hit['_index'] == 'study_alias':
                self._add_internal_id('study', hit['_source'], result_dict, query_term_dict, query_terms_lower)

        for type_key in result_dict:
            terms_filter = TermsFilter.get_terms_filter("Primary id", result_dict[type_key])
            query = ElasticQuery.filtered(Query.match_all(), terms_filter)
            elastic = Search(query, idx='imb_criteria/'+type_key, size=2000000)
            hits = elastic.get_json_response()['hits']['hits']

            print()
            print(type_key+' :: '+str(len(hits)))
            for hit in hits:
                pid = hit['_source']['Primary id']
                qid = query_term_dict[type_key][pid]
                m = ''
                for q in qid:
                    if q.lower() in query_terms_lower:
                        m = q
                        break

                print(pid+' matches '+m+' '+hit['_source']['Object class']+' '+hit['_source']['Name'])

    def _add_internal_id(self, name, hit, result_dict, query_term_dict, query_terms_lower):
        internal_id = hit['internal_id']
        if name in result_dict:
            if internal_id not in result_dict[name]:
                result_dict[name].append(internal_id)
        else:
            result_dict[name] = [internal_id]

        if name not in query_term_dict:
            query_term_dict[name] = {}

        query_term_dict[name][internal_id] = hit['alias']
#         for alias in hit['alias']:
#             alias_lc = alias.lower()
#
#             if internal_id in query_term_dict[name]:
#                 if alias not in query_term_dict[name][internal_id]:
#                     query_term_dict[name][internal_id].append(alias)
#             else:
#                 query_term_dict[name][internal_id] = [alias]
