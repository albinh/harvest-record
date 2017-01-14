from django.conf.urls import url

from . import views
from . import ajax_views
urlpatterns = [
	url(r'^deliveries/$',                           views.DeliveryList.as_view(),                   name='delivery-list'),
    url(r'^deliveries/new$',                        views.DeliveryNew.as_view(),                    name='delivery-new'),
	url(r'^deliveries/(?P<pk>\d+)/$',               views.DeliveryView.as_view(),                   name='delivery-edit', ),
	url(r'^deliveries/delete/(?P<pk>\d+)/$',               views.DeliverySingleDelete.as_view(),                   name='delivery-delete', ),

	url(r'^deliveries/add_variant/(?P<pk>\d+)/$',   views.DeliveryVariantNew.as_view(),			name='delivery_variant_new'),

	url(r'^deliveryitem/(?P<pk>\d+)/delete$', 	    views.DeliveryItemDelete.as_view(), name='delivery-item-delete'),

	url(r'^deliveries/(?P<pk>\d+)/harvests/new/(?P<url>.*)$',			  views.HarvestItemNew.as_view(),		name='delivery-edit-harvests',),
	url ( r'^harvests/(?P<pk>\d+)/(?P<url>.*)$', 						  views.HarvestItemUpdate.as_view ( ),  name='delivery-edit-harvests-update', ),
	url ( r'^harvests/delete/(?P<pk>\d+)$', 	  						  views.HarvestItemDelete.as_view ( ),  name='harvest-item-delete', ),

	url(r'^beds/', views.BedListView.as_view( ), name='beds' ),

	url(r'^crops/$',                                views.CropList.as_view(),                       name='crops'),
	url(r'^crops/(?P<pk>\d+)/$',                    views.CropEdit.as_view(),                       name='crop-edit'),

	url(r'cultures/$', views.CultureListView.as_view( ), name='cultures' ),

	url(r'ajax/deliveries_harvest_for_delivery', ajax_views.deliveries_harvest_for_delivery.as_view(), name ='deliveries_harvest_for_delivery'),
	url(r'ajax/delivery_item_edit_price', ajax_views.delivery_item_edit_price.as_view(), name='delivery_item_edit_price'),
	url(r'ajax/delivery_item_edit_amount', ajax_views.delivery_item_edit_amount.as_view(), name='delivery_item_edit_amount'),

	url(r'ajax/values_for_deliveryitem', ajax_views.values_for_deliveryitem.as_view(), name='values_for_deliveryitem'),
	url(r'ajax/delivery_edit_target_date', ajax_views.delivery_edit_target_date.as_view(), name='delivery_edit_target_date'),

	url(r'ajax/delivery_variant_edit_count', ajax_views.delivery_variant_edit_count.as_view(), name='delivery_variant_edit_count'),
	url(r'ajax/delivery_variant_included', ajax_views.delivery_variant_included.as_view(), name='delivery_variant_included'),


]