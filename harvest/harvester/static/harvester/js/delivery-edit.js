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

    updateHarvestChart(result,card.find("[name='chart']"))
}

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

    console.log(ids)

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