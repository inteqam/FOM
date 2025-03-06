"""
URL configuration for features_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from features import feature, views
from .views import update_feature_description

urlpatterns = [
    path('update-feature-description/', update_feature_description, name='feature_update_description'),
    path('blank_page/', views.blank_page_view, name='blank_page_url'),
    path('',views.index, name='index'),
    path('register_client/', views.register_client, name='register_client'),
    path('clients/', views.list_clients, name='clients_list'),
    path('subcribe_feature_for_client/', views.subcribe_feature_for_client, name='subcribe_feature_for_client'),
    path('edit_client/<int:client_id>/', views.edit_client, name='edit_client'),
    path('unsubcribe_feature', views.unsubcribe_feature, name='unsubcribe_feature'),
    path('subscribe_feature_for_branch_department/', views.subscribe_feature_for_branch_department_view, name='subscribe_feature_for_branch_department'),
    path('features/', views.FeatureListView.as_view(), name='feature_list'),
    path('features/new/', views.FeatureCreateView.as_view(), name='feature_create'),
    path('features/<int:pk>/edit/', views.FeatureUpdateView.as_view(), name='feature_update'),
    path('features/<int:pk>/delete/', views.FeatureDeleteView.as_view(), name='feature_delete'),
    path('display_feature/',views.display_feature,name='display_feature'),
    path('list_commonfeature/',views.list_commonfeature,name='list_commonfeature'),
    path('list_list_commonbranchdepartmentfeature/',views.list_commonbranchdepartmentfeature,name='list_commonbranchdepartmentfeature'),
    path('list_commonclientfeature/',views.list_commonclientfeature,name='list_commonclientfeature'),




]
