from django.shortcuts import render
from elastic.search import Search, ElasticQuery
from elastic.elastic_settings import ElasticSettings


def region_page(request, region):
    ''' Region elastic'''
    query = ElasticQuery.query_match("attr.region_id", region)
    elastic = Search(query, idx=ElasticSettings.idx(name='REGION'))
    context = elastic.get_result()
    context['title'] = "Region"
    print(context)
    return render(request, 'region/region.html', context,
                  content_type='text/html')
