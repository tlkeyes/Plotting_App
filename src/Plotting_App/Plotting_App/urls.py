"""Plotting_App URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Plots.views import HomeView, ChartData, ShardView, HomeView_test
from Plots.views_test import TestApiViewDf, HomeViewDf_test

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('test', HomeView_test.as_view(), name='home-test'),
    path('testdf', HomeViewDf_test.as_view(), name='home-df-test'),
    path('api/chart/data', ChartData.as_view(), name='api-chart-data'),
    path('api/chart/data/testdf', TestApiViewDf.as_view(), name='test-api-chart-data-df'),
    path('shards', ShardView.as_view(), name='shard'),
]
