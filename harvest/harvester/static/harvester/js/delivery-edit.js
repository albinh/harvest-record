"use strict"

function debounce(func, wait, immediate,pk) {
	var timeout;
	return function() {
		var context = this, args = arguments;
		var later = function() {
			timeout = null;
			if (!immediate) func.apply(context, args);
		};
		var callNow = immediate && !timeout;
		clearTimeout(timeout);
		timeout = setTimeout(later, wait);
		if (callNow) func.apply(context, args);
		$("#progress_"+pk).show();
		console.log("postpone");
	};
};


// CB för att uppdatera deliveryitem-card.
function callbackReloadDeliveryItem(reload_editable,result) {
    var card = $(".delivery_item[data-pk='"+result.pk+"']");
    card.data("info", result);

    $("#progress_"+result.pk).hide();
    if (reload_editable) {
        card.find("[name='price']").val(result.price);
        card.find("[name='order_amount']").val(result.order_amount);
        card.find("[name='order_comment']").val(result.order_comment);
        card.find("[name='order_comment']").trigger('autoresize');
    }

    card.find(".order_unit_text_short").text(result.order_unit_text_short)
    card.find(".harvested_amount").text(result.harvested_amount +" "+ result.order_unit_text_short)
    card.find(".ordered_value").text(result.ordered_value + "kr")
    card.find(".harvest_remaining").text(result.harvest_remaining)

    card.find("select[name='order_unit'] option[value='"+result.order_unit+"']").prop('selected', true);
    card.find("select[name='price_unit'] option[value='"+result.price_type+"']").prop('selected', true);

    card.find("input.total_order_amount").val(result.total_order_amount +result.order_unit_text_short )

    if (result.harvest_remaining>=0){
        card.find("label.relation").text("återstår")
        card.find("input.relation").val(result.harvest_remaining+result.order_unit_text_short)
        card.find("input.relation").toggleClass("invalid",false);
    } else {
        card.find("label.relation").text("överskördat")
        card.find("input.relation").val(-result.harvest_remaining+result.order_unit_text_short)
        card.find("input.relation").toggleClass("invalid",true);
    }

var has_listed_price = result.listed_price != null;
    if (has_listed_price) {
    var same_price =  (parseFloat(result.listed_price.price) == parseFloat(card.find("[name='price']").val())  ) &&
                (result.listed_price.unit == card.find("[name='price_unit']").val()  );
                } else {same_price=false }
    var has_listed_price = result.listed_price != null;

    var zero_price = card.find("[name='price']").val()==0

    if (same_price) {
                      card.find(".price_status_missing").hide()
        card.find(".price_status_different").hide()
        card.find(".no_price").hide()
              }

    else if (has_listed_price) {
                  if (result.listed_price.unit="W") {
                                card.find(".listed_price").text(result.listed_price.price + " kr/kg")
                            } else {
                                card.find(".listed_price").text(result.listed_price.price + " kr/st")
                            }

                            card.find(".no_price").hide()
                            card.find(".price_status_missing").hide()
                            card.find(".price_status_different").show()
                  } else if (zero_price) {
                   card.find(".price_status_missing").hide()
        card.find(".price_status_different").hide()
        card.find(".no_price").show()
                  } else {
                                    card.find(".price_status_missing").show()
        card.find(".price_status_different").hide()
        card.find(".no_price").hide()
                  }





    refilter();
    updateHarvestChart(result,card.find(".delivery_progress"))
}

function reset_price_link(e) {
        var card = $(e.target).closest('.delivery_item')
        var result = card.data("info")
        card.find("[name='price']").val(result.listed_price.price);
        card.find("select[name='price_unit'] option[value='"+result.listed_price.type+"']").prop('selected', true);
        card.trigger("push_changes")
    }

function callbackSavePrice(card) {
    card.trigger('push_changes');
}

function save_price_link(e) {
    var card = $(e.target).closest('.delivery_item')
    var result= card.data("info")
    var data = {
        pk : result.pk,
        price : card.find("[name='price']").val(),
        price_type:card.find("[name='price_unit']").val()

    }

        $.ajax({
    url: '/harvester/api/v1/save_price_from_delivery_item_to_pricelist/',
    type: 'POST',
    data:data,
    success: callbackSavePrice.bind(null,card)
});
}

$(document).ready( function(){
    $('.reset_price_link').click(reset_price_link)
    $('.save_price_link').click(save_price_link)
})


function sendDeliveryItem(pk) {
    $("#progress_"+pk).show();
    var card = $(".delivery_item[data-pk='"+pk+"']");

    var data =
    {
        order_amount:card.find("[name='order_amount']").val(),
        price:card.find("[name='price']").val(),
        order_comment:card.find("[name='order_comment']").val(),
        order_unit:card.find("[name='order_unit']").val(),
        price_type:card.find("[name='price_unit']").val()
    }

    $.ajax({
    url: '/harvester/api/v1/delivery_items/'+pk,
    type: 'PATCH',
    data:data,
    success: callbackReloadDeliveryItem.bind(null,false)
});

}

function changeHandler(pk) {
    $("#progress_"+pk).show();
    return debounce(sendDeliveryItem,2000,false,pk).bind(null,pk);
}

function refresHandler(pk) {
    $("#progress_"+pk).show();
    return debounce(reloadDeliveryItem,500,false,pk).bind(null,pk);

}

function reloadDeliveryItem (pk) {
    $.ajax({
    url: '/harvester/api/v1/delivery_items/'+pk,
    type: 'GET',
    success: callbackReloadDeliveryItem.bind(null,true)
});
};


function updateAddHarvestModal(modal,trigger) {
    var pk=trigger.data("pk")
    var data = $(".delivery_item[data-pk='"+pk+"']").data("info");
    $("#add_harvest_modal").data("info",data);
    console.log(data);

		updateModalChart();

}

$(document).ready(function() {
    $('select').material_select();




    $('.modal').modal( {
        ready: updateAddHarvestModal
        }

    );



});


// Uppdatera cropform när crop ändras
$(function() {
$("#crop-select").change(function() {
    var crop_id=parseInt(($(this).val()))


    var selectbox = $("#crop-form")
    selectbox.empty();

    if (crop_id<0 || isNaN(crop_id))
     {return;
     }
    var list = '';
    var i = cropform_data[crop_id].priced
        console.log(i)
       function o(cf) {
       return '<option data-crop="'+cf.name+'" data-countable="'+cf.countable+'" value="' + cf.pk + '">' + cf.name + "</option>";
       }
 if (i) {
     if (i.length>1) {
        list += '<option>Välj form</option>'
     }
     for (var j = 0; j < i.length; j++) {
         list += o(i[j])
     }
 }

 var i = cropform_data[crop_id].not_priced

 if (i) {
    if (i.length>0) {
    list+='<optgroup label="Ej i prislista">'
     for (var j = 0; j < i.length; j++) {
         list += o(i[j]);
     }
     list+='</optgroup>'
     }
 }



 selectbox.html(list);
 selectbox.trigger("change");
 selectbox.material_select();

})

// Uppdatera enhet när cropform ändras
$("#crop-form").change(function() {
 var pk = parseInt($(this).val())

 if (!pk) {
     return
 };

  var list = '';
  list += '<option value="W">kg</option>'
  if ($("option:selected", this).data("countable")) {
    list += '<option value="U">st ' +$("option:selected", this).data("crop") + '</option>';
  }

         var selectbox = $("#units")
         selectbox.empty();
         selectbox.html(list);
         selectbox.material_select();


})

// Se till att cropform uppdateras
$("#crop-select").trigger("change");
})

function toggleVariant(selector)
{
    var state = !$(selector).hasClass("included");
    console.log(state);
    $(selector).toggleClass("included",state);
}



function callbackReloadDeliveryVariant(reload_editable, result) {
    console.log(result);

    $('.crop-count[data-variant="'+result.pk+'"]').val(result.crop_count);
    $('.value[data-variant="'+result.pk+'"]').val(result.value+" kr");

    $('.delivery_item').each(function (i,e) {
        $(e).trigger("refresh")
    })
}

function reloadDeliveryVariant (pk) {
    $.ajax({
    url: '/harvester/api/v1/delivery_variants/'+pk,
    type: 'GET',
    success: callbackReloadDeliveryVariant.bind(null,true)
});
}

function pushVariant(v) {
    var checked = $('.included_checkbox[data-variant="'+v+'"]:not(:checked)');
    var ids = checked.map(function() {return $(this).data("deliveryitem")}).toArray()

    var count = $('.box-count[data-variant="'+v+'"]').val()
    console.log(count)
    var data =
    {
        extempt_ids:ids,
        count: count
    }

    $.ajax({
    url: '/harvester/api/v1/delivery_variants/'+v,
    type: 'PATCH',
    dataType: "json",
    contentType: "application/json; charset=utf-8",
    data: JSON.stringify(data),
    success: callbackReloadDeliveryVariant.bind(null,false)

})
}

function updateVariant(event) {
    console.log(event);
    var v=$(event.target).data("variant");
    pushVariant(v)
}


$(document).ready( function(){
    $('div.delivery_item').each(function() {
        $(this).on('push_changes', changeHandler($(this).data("pk")));
        $(this).on('refresh',      refresHandler($(this).data("pk")));

        $(this).trigger('refresh');
    })
});

$(".included_checkbox").on("change", updateVariant);
$(".box-count").on("input",updateVariant);

function refilter(){
/*
    var filtered=$([]);

    if ($("#show_completed").is(':checked')) {
        filtered=filtered.add( $(".card").filter("[data-status=2]")  ).add( $(".card").filter("[data-status=3]")  )
    }

    if ($("#show_not_completed").is(':checked')) {
        filtered=filtered.add( $(".card").filter("[data-status=0]")  ).add( $(".card").filter("[data-status=1]")  )
    }

    $(".delivery_item").hide();
    filtered.show();
    */
}

$(document).ready(function() {
    $("#show_completed").on("change",refilter);
    $("#show_not_completed").on("change",refilter);
})


function callbackReloadDelivery(reload_editable, result) {
    $('.total-order-value ').val(result.total_order_value+" kr")
    if (reload_editable) {
        $('.delivery-date').val(result.date)
    }
    $("#progress_head").hide();
}

function pushDelivery() {
    $("#progress_head").show();
    var pk=$('#delivery').data("pk")
    var data =
    {
        date: $('.delivery-date').val()
    }

    $.ajax({
    url: '/harvester/api/v1/delivery/'+pk,
    type: 'PATCH',
    dataType: "json",
    contentType: "application/json; charset=utf-8",
    data: JSON.stringify(data),
    success: callbackReloadDelivery.bind(null,false)

})

}

function reloadDelivery() {
    var pk=$('#delivery').data("pk")
    $.ajax({
    url: '/harvester/api/v1/delivery/'+pk,
    type: 'GET',
    success: callbackReloadDelivery.bind(null,true)
});

}

var pushDeliveryDebounced = debounce (pushDelivery,false,"head")
var reloadDeliveryDebounced = debounce (reloadDelivery,false,"head")

$(document).ready(function() {
    reloadDeliveryDebounced()

})

$("#delivery-date").on("input",pushDeliveryDebounced);
