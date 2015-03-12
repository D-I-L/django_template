from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
from django.core.urlresolvers import NoReverseMatch
import json
import requests
import re


@csrf_exempt
def reverse_proxy(request):
    '''
    Reverse proxy for elasticsearch on different port.
    Based on https://gist.github.com/JustinTArthur/5710254.
    To be used ONLY in DEBUG mode.
    '''
    if(not settings.DEBUG):
        raise NoReverseMatch
    path = request.get_full_path()
    url = "%s%s" % (settings.ELASTICSEARCH_URL, path)
    requestor = getattr(requests, request.method.lower())
    proxy_resp = requestor(url, data=request.body, files=request.FILES)
    return HttpResponse(proxy_resp.content,
                        content_type=proxy_resp.headers.get('content-type'))


def search(request, query,
           search_db=settings.MARKERDB + ',' +
           settings.GENEDB + ',' +
           settings.REGIONDB):
    ''' Renders a search results page based on the query '''
    fields = ["gene_symbol", "hgnc", "synonyms", "id",
              "dbxrefs.*", "attr.*", "featureloc.seqid"]
    data = {"query": {"query_string": {"query": query, "fields": fields}}}
    context = elastic_search(data, 0, 20, db=search_db)
    return render(request, 'search/searchresults.html', context,
                  content_type='text/html')


def range_search(request, src, start, stop,
                 search_db=settings.MARKERDB + ',' +
                 settings.GENEDB + ',' +
                 settings.REGIONDB):
    ''' Renders a search result page based on the src, start and stop '''

    must = [{"match": {"seqid": src}},
            {"range": {"start": {"gte": start, "boost": 2.0}}},
            {"range": {"end": {"lte": stop, "boost": 2.0}}}]
    query = {"bool": {"must": must}}
    data = {"query": query}
    context = elastic_search(data, db=search_db)
    context["chromosome"] = src
    context["start"] = start
    context["stop"] = stop
    return render(request, 'search/searchresults.html', context,
                  content_type='text/html')


def elastic_search(data, search_from=0, size=20, db=settings.MARKERDB):
    '''
    Query the elasticsearch server for given search data and return the
    context dictionary to pass to the template
    '''
    url = (settings.ELASTICSEARCH_URL + '/' +
           db + '/_search?size=' + str(size) +
           '&from='+str(search_from))
    response = requests.post(url, data=json.dumps(data))
    context = {"query": data}
    c_dbs = {}
    dbs = db.split(",")
    for this_db in dbs:
        stype = "Gene"
        if "snp" in this_db:
            stype = "Marker"
        if "region" in this_db:
            stype = "Region"
        c_dbs[this_db] = stype
    context["dbs"] = c_dbs
    context["db"] = db

    content = []
    if response.status_code != 200:
        context["error"] = ("Error: elasticsearch response " +
                            json.dumps(response.json()))
        return context

    if(len(response.json()['hits']['hits']) >= 1):
        for hit in response.json()['hits']['hits']:
            _addInfo(content, hit)
            hit['_source']['idx_type'] = hit['_type']
            hit['_source']['idx_id'] = hit['_id']
            content.append(hit['_source'])
            #print(hit['_source']) @IgnorePep8

    context["data"] = content
    context["total"] = response.json()['hits']['total']
    if(int(response.json()['hits']['total']) < size):
        context["size"] = response.json()['hits']['total']
    else:
        context["size"] = size
    return context


def _addInfo(content, hit):
    ''' Parse VCF INFO field and add to the search hit '''
    if 'info' not in hit['_source']:
        return
    ''' Split and add INFO tags and values '''
    infos = re.split(';', hit['_source']['info'])
    for info in infos:
        if "=" in info:
            parts = re.split('=', info)
            if parts[0] not in hit['_source']:
                hit['_source'][parts[0]] = parts[1]
        else:
            if info not in hit['_source']:
                hit['_source'][info] = ""


def filtered_range_search(request, src, start, stop, db):
    '''
    Pass the range parameters to the range_search routine.
    '''
    return range_search(request, src, start, stop, db)


def filtered_search(request, query, db):
    '''
    Pass the search parameters to the regular search routine
    '''
    return search(request, query, db)
