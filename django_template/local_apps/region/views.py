from django.shortcuts import render
from elastic.elastic_model import Elastic, ElasticQuery
from elastic.elastic_settings import ElasticSettings


def region_page(request, region):
    ''' Region elastic'''
    query = ElasticQuery.query_match("attr.region_id", region)
    elastic = Elastic(query, db=ElasticSettings.idx(name='REGION'))
    context = elastic.get_result()
    context['title'] = "Region"
    print(context)
    return render(request, 'region/region.html', context,
                  content_type='text/html')
