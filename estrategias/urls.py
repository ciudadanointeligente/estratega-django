from django.conf.urls import url

from . import views

urlpatterns = [
    # /
    url(r'^mis_estrategias', views.MisEstrategiasView.as_view(), name='mis_estrategias'),
    url(r'^nueva_estrategia', views.NuevaEstrategiaView.as_view(), name='nueva_estrategia'),

    # estrategia
    url(r'^(?P<pk>[0-9]+)/estrategia/pre$', views.EstrategiaPreView.as_view(), name='estrategia_pre'),
    url(r'^(?P<pk>[0-9]+)/$', views.EstrategiaView.as_view(), name='estrategia'),
    url(r'^(?P<pk>[0-9]+)/eliminar$', views.EstrategiaEliminarView.as_view(), name='eliminar'),

    # problematica
    url(r'^(?P<pk>[0-9]+)/problematica$', views.ProblematicaView.as_view(), name='problematica'),
    url(r'^(?P<pk>[0-9]+)/problematica/edit', views.ProblematicaEditView.as_view(), name='problematica_edit'),
    
    # causas
    url(r'^(?P<pk>[0-9]+)/causas/pre$', views.CausasPreView.as_view(), name='causas_pre'),
    url(r'^(?P<pk>[0-9]+)/causas$', views.CausasView.as_view(), name='causas'),
    url(r'^(?P<pk>[0-9]+)/causas/edit', views.CausasEditView.as_view(), name='causas_edit'),

    # solucionpolitica
    url(r'^(?P<pk>[0-9]+)/solucionpolitica/pre$', views.SolucionPoliticaPreView.as_view(), name='solucionpolitica_pre'),
    url(r'^(?P<pk>[0-9]+)/solucionpolitica$', views.SolucionPoliticaView.as_view(), name='solucionpolitica'),
    url(r'^(?P<pk>[0-9]+)/solucionpolitica/edit', views.SolucionPoliticaEditView.as_view(), name='solucionpolitica_edit'),

    # objetivos
    url(r'^(?P<pk>[0-9]+)/objetivos/pre$', views.ObjetivosPreView.as_view(), name='objetivos_pre'),
    url(r'^(?P<pk>[0-9]+)/objetivos$', views.ObjetivosView.as_view(), name='objetivos'),
    url(r'^(?P<pk>[0-9]+)/objetivos/edit$', views.ObjetivosDetailEditView.as_view(), name='objetivos_edit'),
    url(r'^(?P<pk>[0-9]+)/objetivos/nuevo$', views.ObjetivosNuevoView.as_view(), name='objetivos_nuevo'),
    url(r'^(?P<pk>[0-9]+)/objetivos/eliminar$', views.ObjetivosEliminarView.as_view(), name='objetivos_eliminar'),

    # resultadosintermedios
    url(r'^(?P<pk>[0-9]+)/resultadosintermedios/pre$', views.ResultadosIntermediosPreView.as_view(), name='resultadosintermedios_pre'),
    url(r'^(?P<pk>[0-9]+)/resultadosintermedios$', views.ResultadosIntermediosView.as_view(), name='resultadosintermedios'),
    url(r'^(?P<pk>[0-9]+)/resultadosintermedios/edit$', views.ResultadosIntermediosEditView.as_view(), name='resultadosintermedios_edit'),

    # barreras
    url(r'^(?P<pk>[0-9]+)/barreras/pre$', views.BarrerasPreView.as_view(), name='barreras_pre'),
    url(r'^(?P<pk>[0-9]+)/barreras$', views.BarrerasView.as_view(), name='barreras'),
    url(r'^(?P<pk>[0-9]+)/barreras/edit$', views.BarrerasEditView.as_view(), name='barreras_edit'),

    # factoreshabilitantes
    url(r'^(?P<pk>[0-9]+)/factoreshabilitantes/pre$', views.FactoresHabilitantesPreView.as_view(), name='factoreshabilitantes_pre'),
    url(r'^(?P<pk>[0-9]+)/factoreshabilitantes$', views.FactoresHabilitantesView.as_view(), name='factoreshabilitantes'),
    url(r'^(?P<pk>[0-9]+)/factoreshabilitantes/edit$', views.FactoresHabilitantesEditView.as_view(), name='factoreshabilitantes_edit'),

    # actoresrelevantes
    url(r'^(?P<pk>[0-9]+)/actoresrelevantes/pre$', views.ActoresRelevantesPreView.as_view(), name='actoresrelevantes_pre'),
    url(r'^(?P<pk>[0-9]+)/actoresrelevantes$', views.ActoresRelevantesView.as_view(), name='actoresrelevantes'),
    url(r'^(?P<pk>[0-9]+)/actoresrelevantes/edit$', views.ActoresRelevantesEditView.as_view(), name='actoresrelevantes_edit'),

]

