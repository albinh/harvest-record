from django.conf.urls import url

from .api_views import delivery_item_element, delivery_variant_element, customer_element
from . import views

urlpatterns = [


	url(r'cropsprices/$', views.CropsPrices.as_view(), name='crops-prices'),
	url(r'^deliveries/$',                           views.DeliveryList.as_view(),                   name='delivery-list'),
    url(r'^deliveries/new$',                        views.DeliveryNew.as_view(),                    name='delivery-new'),
	url(r'^deliveries/(?P<pk>\d+)/$',               views.DeliveryView.as_view(),                   name='delivery-edit', ),
	url(r'^deliveries/delete/(?P<pk>\d+)/$', views.DeliveryDelete.as_view( ), name='delivery-delete', ),

	url(r'^harvests/(?P<days>\d+)/$', views.HarvestsView.as_view(),name='harvests'),

	url(r'deliveries/set_deliveried/(?P<pk>\d+)/$', views.DeliverySetDelivered.as_view(), name='delivery-setdelivered',),
	url(r'deliveries/spec/(?P<pk>\d+)/$', views.DeliverySpec.as_view(),name='delivery-spec'),


	url(r'^deliveries/add_variant/(?P<pk>\d+)/$',   views.DeliveryVariantNew.as_view(),			name='delivery_variant_new'),

	url(r'^deliveryitem/(?P<pk>\d+)/delete$', 	    views.DeliveryItemDelete.as_view(), name='delivery-item-delete'),

	url(r'^deliveries/(?P<pk>\d+)/harvests/new/(?P<url>.*)$',			  views.HarvestItemNew.as_view(),		name='delivery-edit-harvests',),
	url ( r'^harvests/(?P<pk>\d+)/(?P<url>.*)$', 						  views.HarvestItemUpdate.as_view ( ),  name='delivery-edit-harvests-update', ),
	url ( r'^harvests/delete/(?P<pk>\d+)$', 	  						  views.HarvestItemDelete.as_view ( ),  name='harvest-item-delete', ),

	url(r'cropform_new/', views.cropform_new.as_view(), name='cropform-new'),
	url(r'crop_new',views.CropNew.as_view(),name='crop-new'),

	url(r'^customers/new$', views.CustomerNew.as_view ( ), name='customer-new' ),
	url(r'^customers/$',views.CustomerList.as_view(),name='customer-list'),
	url(r'customercategory_new', views.CustomerCategoryNew.as_view(),name='customercategory-new'),

	url(r'^api/v1/delivery_items/(?P<pk>[0-9]+)$', delivery_item_element),
	url(r'^api/v1/delivery_variants/(?P<pk>[0-9]+)$', delivery_variant_element),
	url(r'^api/v1/customers/(?P<pk>[0-9]+)$', customer_element)
]