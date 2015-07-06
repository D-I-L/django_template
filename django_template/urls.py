from django.conf.urls import include, url
from db.api import CvtermResource, CvtermFullResource, CvResource
from db.api import CvtermpropResource, FeaturelocResource
from db.api import FeaturelocFullResource, FeatureResource, FeatureFullResource
from db.api import FeaturepropResource, FeaturepropFullResource
from db.api import OrganismResource
from tastypie.api import Api
from elastic.tastypie.api import GeneResource, DiseaseResource,\
    MarkerResource
from db.models import Cv, Cvterm, Feature
from rest_framework import serializers, viewsets, routers
from elastic.rest_framework.api import PublicationViewSet, DiseaseViewSet,\
    MarkerViewSet


# Serializers define the API representation.
class CvtermSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cvterm
        fields = ('name', 'cvterm_id', 'definition', 'cv')
        depth = 1


class CvSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cv
        fields = ('name', 'definition', 'cv_id')
        depth = 1


class FeatureSerializer(serializers.ModelSerializer):

    class Meta:
        model = Feature
        fields = ('name', 'uniquename', 'type', 'organism')
        depth = 2


# ViewSets define the view behavior.
class CvViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Cv.objects.all()
    serializer_class = CvSerializer
    filter_fields = ('name', 'cv_id')


class CvtermViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Cvterm.objects.all()
    serializer_class = CvtermSerializer
    filter_fields = ('cv', 'name', 'cvterm_id', 'cv__name')


class FeatureViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer
    filter_fields = ('name', 'uniquename', 'type__name')

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'cv', CvViewSet)
router.register(r'cvterm', CvtermViewSet)
router.register(r'feature', FeatureViewSet)
router.register(r'pubs', PublicationViewSet, base_name='pubs')
router.register(r'disease', DiseaseViewSet, base_name='disease')
router.register(r'marker', MarkerViewSet, base_name='marker')

# register tastypie api
api = Api(api_name='dev')
api.register(CvtermResource())
api.register(CvtermFullResource())
api.register(CvResource())
api.register(OrganismResource())
api.register(FeaturelocResource())
api.register(FeaturelocFullResource())
api.register(FeatureResource())
api.register(FeatureFullResource())
api.register(FeaturepropResource())
api.register(FeaturepropFullResource())
api.register(CvtermpropResource())

# register tastypie api
elastic_api = Api(api_name='dev')
elastic_api.register(GeneResource())
elastic_api.register(DiseaseResource())
elastic_api.register(MarkerResource())

urlpatterns = [url(r'^', include('bands.urls', namespace="bands")),
               url(r'^api/', include(api.urls)),
               url(r'^elastic/', include(elastic_api.urls)),
               url(r'^search/', include('elastic.urls', namespace="elastic")),
               url(r'^gene/', include('gene.urls')),
               url(r'^marker/', include('marker.urls')),
               url(r'^region/', include('region.urls')),
               url(r'^rest/', include(router.urls, namespace="rest")),
               url(r'^rest-docs/', include('rest_framework_swagger.urls')),
               ]
