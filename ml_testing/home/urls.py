from django.urls import path

from . import views

urlpatterns = [
    path('home', views.home, name='home'),
    path('logout', views.logout, name='logout'),
    path('fetch_corpus', views.fetch_corpus, name='fetch_corpus'),
    path('l_models', views.l_models, name='l_models'),
    path('report', views.report, name='report'),
    path('grams', views.grams, name='grams'),
    path('getp', views.getp, name='getp'),
    path('custom', views.custom, name='custom'),
    path('spell', views.spell, name='spell'),

]
