from django.conf.urls import url

from . import views
from . import ajax_views
urlpatterns = [


	url(r'^deliveries/$',                           views.DeliveryList.as_view(),                   name='delivery-list'),
    url(r'^deliveries/new$',                        views.DeliveryNew.as_view(),                    name='delivery-new'),
    url(r'^deliveries/(?P<pk>\d+)/$',               views.DeliveryEdit.as_view(),                   name='delivery-edit', ),

	url(r'^deliveries/harvests/(?P<pk>\d+)/$',		views.DeliveryEditHarvests.as_view(),				name='delivery-edit-harvests',),

    url(r'^customer_categories/',                   views.CustomerCategoryList.as_view(),           name='cusstomer-categories-list'),
	url(r'^customer_categories/(?P<pk>\d+)/$',      views.CustomerCategoryEdit.as_view(),           name='customer-category-edit'),

	url(r'^beds/',									views.Beds.as_view(),							name='beds'),

	url(r'^crops/$',                                views.CropList.as_view(),                       name='crops'),
	url(r'^crops/(?P<pk>\d+)/$',                    views.CropEdit.as_view(),                       name='crop-edit'),

	url(r'cultures/$',								views.Cultures.as_view(),						name='cultures'),


	# deliveries_new
	url(r'^ajax/deliveries_new_order_units_for_cropform/$',	ajax_views.deliveries_new_order_units_for_cropform.as_view(), 		name='deliveries_new_order_units_for_cropform'),
	url(r'^ajax/deliveries_new_crop_form_for_crop/$', 					ajax_views.deliveries_new_crop_form_for_crop.as_view(), name='deliveries_new_crop_form_for_crop'),
	url ( r'^ajax/deliveries_new_price_units_for_cropform/$', ajax_views.deliveries_new_price_units_for_cropform.as_view ( ),		  name='deliveries_new_price_units_for_cropform' ),

	url(r'ajax/deliveries_harvest_for_delivery', ajax_views.deliveries_harvest_for_delivery.as_view(), name ='deliveries_harvest_for_delivery'),





]