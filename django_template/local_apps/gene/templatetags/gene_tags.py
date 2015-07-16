from django import template
from db.models import FeatureDbxref, FeatureSynonym
from elastic.elastic_settings import ElasticSettings
from elastic.query import Query, BoolQuery, RangeQuery
from elastic.search import ElasticQuery, Search

register = template.Library()


@register.inclusion_tag('gene/gene_section.html')
def show_gene_section(gene_feature):
    ''' Template inclusion tag to render a gene section given a
    chado gene feature. '''

    feature_dbxrefs = FeatureDbxref.objects.filter(feature=gene_feature)
    gene_dbxrefs = []
    for feature_dbxref in feature_dbxrefs:
        gene_dbxrefs.append(feature_dbxref.dbxref)

    feature_synonyms = FeatureSynonym.objects.filter(feature=gene_feature)
    gene_synonyms = []
    for feature_synonym in feature_synonyms:
        gene_synonyms.append(feature_synonym.synonym)

    return {'feature': gene_feature,
            'synonyms': gene_synonyms,
            'dbxrefs': gene_dbxrefs}


@register.inclusion_tag('gene/es_gene_section.html')
def show_es_gene_section(gene_symbol=None, seqid=None,
                         start_pos=None, end_pos=None):
    ''' Template inclusion tag to render a gene section given a
    chado gene feature. '''
    seqid = str(seqid).replace('chr', '')
    if gene_symbol is not None:
        ''' gene symbol query'''
        query = ElasticQuery.query_match("symbol", gene_symbol)
    elif end_pos is None:
        ''' start and end are same, range query for snp'''
        query_bool = BoolQuery(must_arr=[Query.match("chromosome", seqid),
                                         RangeQuery("start", lte=start_pos),
                                         RangeQuery("stop", gte=start_pos)])
        query = ElasticQuery.bool(query_bool)
    else:
        ''' start and end are same, range query for snp'''
        query_bool = BoolQuery(must_arr=[Query.match("chromosome", seqid),
                                         RangeQuery("start", gte=start_pos),
                                         RangeQuery("stop", lte=end_pos)])
        query = ElasticQuery.bool(query_bool)

    elastic = Search(query, idx=ElasticSettings.idx(name='GENE'))
    return {'es_genes': elastic.search().docs}
