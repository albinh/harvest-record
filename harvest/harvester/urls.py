from django.conf.urls import url

from .api_views import delivery_item_element, delivery_variant_element
from . import views
from . import ajax_views
urlpatterns = [


	url(r'cropsprices/$', views.CropsPrices.as_view(), name='crops-prices'),
	url(r'^deliveries/$',                           views.DeliveryList.as_view(),                   name='delivery-list'),
    url(r'^deliveries/new$',                        views.DeliveryNew.as_view(),                    name='delivery-new'),
	url(r'^deliveries/(?P<pk>\d+)/$',               views.DeliveryView.as_view(),                   name='delivery-edit', ),
	url(r'^deliveries/delete/(?P<pk>\d+)/$',               views.DeliverySingleDelete.as_view(),                   name='delivery-delete', ),

	url(r'^harvests/(?P<days>\d+)/$', views.HarvestsView.as_view(),name='harvests'),

	url(r'deliveries/set_deliveried/(?P<pk>\d+)/$', views.DeliverySetDelivered.as_view(), name='delivery-setdelivered',),
	url(r'deliveries/spec/(?P<pk>\d+)/$', views.DeliverySpec.as_view(),name='delivery-spec'),


	url(r'^deliveries/add_variant/(?P<pk>\d+)/$',   views.DeliveryVariantNew.as_view(),			name='delivery_variant_new'),

	url(r'^deliveryitem/(?P<pk>\d+)/delete$', 	    views.DeliveryItemDelete.as_view(), name='delivery-item-delete'),

	url(r'^deliveries/(?P<pk>\d+)/harvests/new/(?P<url>.*)$',			  views.HarvestItemNew.as_view(),		name='delivery-edit-harvests',),
	url ( r'^harvests/(?P<pk>\d+)/(?P<url>.*)$', 						  views.HarvestItemUpdate.as_view ( ),  name='delivery-edit-harvests-update', ),
	url ( r'^harvests/delete/(?P<pk>\d+)$', 	  						  views.HarvestItemDelete.as_view ( ),  name='harvest-item-delete', ),

	# url(r'ajax/deliveries_harvest_for_delivery', ajax_views.deliveries_harvest_for_delivery.as_view(), name ='deliveries_harvest_for_delivery'),
	# url(r'ajax/delivery_item_edit_price', ajax_views.delivery_item_edit_price.as_view(), name='delivery_item_edit_price'),
	# url(r'ajax/delivery_item_edit_amount', ajax_views.delivery_item_edit_amount.as_view(), name='delivery_item_edit_amount'),
    #
	# url(r'ajax/values_for_deliveryitem', ajax_views.values_for_deliveryitem.as_view(), name='values_for_deliveryitem'),
	# url(r'ajax/delivery_edit_date', ajax_views.delivery_edit_date.as_view(), name='delivery_edit_date'),
    #
	# url(r'ajax/delivery_variant_edit_count', ajax_views.delivery_variant_edit_count.as_view(), name='delivery_variant_edit_count'),
	# url(r'ajax/delivery_variant_included', ajax_views.delivery_variant_included.as_view(), name='delivery_variant_included'),
	# url(r'ajax/cropform_price/', ajax_views.cropform_price.as_view(),name='ajax_cropform_price'),
    # url(r'ajax/edit_harvest_state', ajax_views.edit_harvest_state.as_view(),name='ajax-edit-harvest-state'),
	# url(r'ajax/reset_price_deliveryitem', ajax_views.reset_price.as_view(),name='reset_price'),
	# url(r'ajax/deliveryitem_delivery_comment', ajax_views.deliveryitem_delivery_comment.as_view(),name ='deliveryitem_delivery_comment'),
	# url(r'ajax/deliveryitem_order_comment', ajax_views.deliveryitem_order_comment.as_view(),name ='deliveryitem_order_comment'),
	url(r'cropform_new/', views.cropform_new.as_view(), name='cropform-new'),
	url(r'crop_new',views.CropNew.as_view(),name='crop-new'),
	url(r'customercategory_new', views.CustomerCategoryNew.as_view(),name='customercategory-new'),
	url(r'bedsandcultures/',views.BedsAndCultures.as_view(),name='bedsandcultures'),
	url(r'^api/v1/delivery_items/(?P<pk>[0-9]+)$', delivery_item_element),
	url(r'^api/v1/delivery_variants/(?P<pk>[0-9]+)$', delivery_variant_element)

]