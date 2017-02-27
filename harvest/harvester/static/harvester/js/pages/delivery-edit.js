String.prototype.trimRight = function(charlist) {
  if (charlist === undefined)
    charlist = "\s";

  return this.replace(new RegExp("[" + charlist + "]+$"), "");
};



function recalc(pk ) {

    function response_cb(response)  {
        	result = JSON.parse(response);

            if (result) {
                di = $('div[data-pk='+result.pk+']')

                ordered=result.ordered_amount
                harvested=result.harvested_amount


                relation = ordered-harvested

                r = function (f) {
                    return f.toFixed(2).trimRight("0").trimRight(".");
                }

                if (relation<0) {
                    di.find('span.over').show().html( r(-relation) + " "+result.unit )
                    di.find('div.under').show().html("")



                    over_width = Math.min(25,((harvested/ordered-1)*0.75*100)).toFixed(0)+"%"

                    di.find('.harvested').show().width("75%");
                    di.find('.remaining').hide();
                    di.find('.overflow').show().width(over_width);



                } else {
                    di.find('span.under').show().html( r(relation) + " "+result.unit )
                    di.find('div.over').hide(  )

                    remaining_width = (((ordered-harvested)/ordered)*0.75*100).toFixed(0)+"%";
                    harvested_width = (((harvested)/ordered)*0.75*100).toFixed(0)+"%";
                    di.find('.harvested').show().width(harvested_width);
                    di.find('.remaining').show().width(remaining_width);
                    di.find('.overflow').hide()


                }

                di.find('.ordered_amount').html(result.total_order_amount )
                di.find('.harvested_amount').html(result.harvested_amount + " "+result.unit)


                     di.find('div.under').toggleClass('bg-danger', result.under_error)
                     di.find('div.over').toggleClass('bg-danger', result.over_error)




                $('div[data-pk='+result.pk+'] .price_state').toggleClass('bg-danger', !result.is_price_as_listed)

                $('div[data-pk='+result.pk+'] .ordered_value' ).html(result.ordered_value )
                $('div[data-pk='+result.pk+'] .harvested_value').html(result.harvested_value)
                $('div[data-pk='+result.pk+'] .box_value').html(result.box_value)
                $('div[data-pk='+result.pk+'] .total_order_amount').html(result.total_order_amount)

                console.log(result)
                $('#harvested_sum').html(result.sum_harvested_value)
                $('#order_sum').html(result.sum_ordered_value)
                console.log( )
                for (i=0;i<result.box_num; i++) {
                    console.log(result.sum_box_values_and_counts[i])
                    pk=result.sum_box_values_and_counts[i].pk
                    $('#box_sum_value-'+pk).html(result.sum_box_values_and_counts[i].value)
                    $('#box_sum_count-'+pk).html(result.sum_box_values_and_counts[i].count)
                }




            }

    }

    url="/harvester/ajax/values_for_deliveryitem"
    params = {csrfmiddlewaretoken: csrf_token,
              pk:pk}
    $.post(
            url,
            params,
            response_cb)
    console.log(pk)
}

$(function(){

        $('.inlinesparkline').sparkline('html',{width:'80%', type:'bullet', borderWidth:1, targetColor: '#000000',
        performanceColor: '#666666',});

        $.fn.editable.defaults.placement = 'auto top';
        if (is_delivered) {
             $.fn.editable.defaults.disabled = true;
        }

        $.fn.editable.defaults.params = {csrfmiddlewaretoken:csrf_token}

        $('.editable').editable();
});


// Uppdatera cropform när crop ändras
$(function() {
$("#crop-select").change(function() {
    crop_id=parseInt(($(this).val()))


    var selectbox = $("#crop-form")
    selectbox.empty();

    if (crop_id<0)
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

})

// Uppdatera enhet när cropform ändras
$("#crop-form").change(function() {
 pk = parseInt($(this).val())

 if (!pk) {
     return
 };

  list = '';
  list += '<option value="W">kg</option>'
  if ($("option:selected", this).data("countable")) {
    list += '<option value="U">st ' +$("option:selected", this).data("crop") + '</option>';
  }

         var selectbox = $("#units")
         selectbox.empty();
         selectbox.html(list);


})

// Se till att cropform uppdateras
$("#crop-select").trigger("change");
})


