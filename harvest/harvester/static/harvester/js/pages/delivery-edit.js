function recalc(pk ) {

    function response_cb(response)  {
        	result = JSON.parse(response);

            if (result) {
                $('tr[data-pk='+result.pk+'] .ordered_value' ).html(result.ordered_value )
                $('tr[data-pk='+result.pk+'] .harvested_value').html(result.harvested_value)
                $('tr[data-pk='+result.pk+'] .box_value').html(result.box_value)
                $('tr[data-pk='+result.pk+'] .total_order_amount').html(result.total_order_amount)
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
    $.fn.editable.defaults.placement = 'auto top';

    $.fn.editable.defaults.params = {csrfmiddlewaretoken:csrf_token}
    $('.editable').editable();
});


// Uppdatera cropform när crop ändras
$(function() {
$("#crop-select").change(function() {

 cropforms = cropform_data[$(this).val()]

 var selectbox = $("#crop-form")
 selectbox.empty();
 var list = '';
 var i = cropform_data[$(this).val()]
 if (i) {
     for (var j = 0; j < i.length; j++) {
         list += "<option value='" + i[j].pk + "'>" + i[j].name + "</option>";
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
 c_pk = parseInt($("#crop-select").val())
 for (var j = 0; j < cropform_data[c_pk].length; j++) {
     if (cropform_data[c_pk][j].pk == pk) {
         list = '';
         list += '<option value="W">kg</option>'
         if (cropform_data[c_pk][j].countable) {
             list += '<option value="U">st ' + cropform_data[c_pk][j].name + '</option>';
         }

         var selectbox = $("#units")
         selectbox.empty();
         selectbox.html(list);


     }
 }

})

// Se till att cropform uppdateras
$("#crop-select").trigger("change");
})


