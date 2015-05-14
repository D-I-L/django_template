from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.core.cache import cache

from db.models import Feature, Featureloc, Cv, Cvterm

import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


def cvlist(request):
    cv_list = Cv.objects.all()
    context = {'cv_list': cv_list, 'title': 'CV terms'}
    return render(request, 'bands/cvlist.html', context)


# 60 mins cache
@cache_page(60 * 60)
def cytobands_ws(request, org):
    srcIds = Featureloc.objects.getSrcFeatures(org)  # @UndefinedVariable
    srcfeatures = (Feature.objects
                   .filter(featureloc_srcfeature=srcIds))  # @UndefinedVariable

    # order by chr number  (assumes chr prefix)
    srcfeatures = sorted(srcfeatures,
                         key=(lambda srcfeature:
                              (int(srcfeature.uniquename.replace("chr", ""))
                               if (srcfeature.uniquename.replace("chr", "")
                                   .isnumeric())
                               else 1000)))

    cv = Cv.objects.get(name="DIL")
    cvtermDIL = Cvterm.objects.filter(cv=cv)

    context = {'srcfeatures': srcfeatures, 'org': org,
               'cvtermDIL': cvtermDIL, 'title': 'Cytobands'}
    return render(request, 'bands/bands-ws.html', context,
                  content_type='text/html')


def _getcontext(org):
    ''' Get info for cytobands and diseases. '''
    bands = Featureloc.objects.getCytoBands(org)  # @UndefinedVariable
    srcIds = bands.distinct('srcfeature_id')
    srcfeatures = (Feature.objects
                   .filter(featureloc_srcfeature=srcIds))  # @UndefinedVariable

    # order by chr number (assumes chr prefix)
    srcfeatures = sorted(srcfeatures,
                         key=(lambda srcfeature:
                              (int(srcfeature.uniquename.replace("chr", ""))
                               if (srcfeature.uniquename.replace("chr", "")
                                   .isnumeric())
                               else 1000)))

    cv = Cv.objects.get(name="DIL")
    cvtermDIL = Cvterm.objects.filter(cv=cv)

    return {'bands': bands, 'srcfeatures': srcfeatures,
            'org': org, 'cvtermDIL': cvtermDIL,
            'title': 'Cytobands'}


def cytobands(request, org):
    context = cache.get('bands-context')
    if context is None:
        context = _getcontext(org)
        # 60 mins cache
        cache.set('bands-context', context, 360)

    return render(request, 'bands/bands.html', context)


# 60 mins cache
def cytobandsHuman(request):
    return cytobands(request, 'human_GRCh38')
