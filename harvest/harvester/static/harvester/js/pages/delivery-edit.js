$(function(){
    $.fn.editable.defaults.placement = 'auto top';
    $.fn.editable.defaults.params = {csrfmiddlewaretoken:'{{csrf_token}}'}
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