/**
Address editable input.
Internally value stored as {city: "Moscow", street: "Lenina", building: "15"}

@class address
@extends abstractinput
@final
@example
<a href="#" id="address" data-type="address" data-pk="1">awesome</a>
<script>
$(function(){
    $('#address').editable({
        url: '/post',
        title: 'Enter city, street and building #',
        value: {
            city: "Moscow", 
            street: "Lenina", 
            building: "15"
        }
    });
});
</script>
**/
(function ($) {
    "use strict";
    
    var AmountAndUnit = function (options) {
        this.init('amount_and_unit', options, AmountAndUnit.defaults);
    };

    //inherit from Abstract input
    $.fn.editableutils.inherit(AmountAndUnit, $.fn.editabletypes.abstractinput);

    $.extend(AmountAndUnit.prototype, {
        /**
        Renders input from tpl

        @method render() 
        **/        
        render: function() {
        console.log(this.$tpl);
           this.$input = this.$tpl //.find('input');
        },
        
        /**
        Default method to show value in element. Can be overwritten by display option.
        
        @method value2html(value, element) 
        **/
        value2html: function(value, element) {
            if(!value) {
                $(element).empty();
                return; 
            }


            var units=JSON.parse(this.options.scope.dataset['units'])
            var unit = units[value.unit]
            var html = $('<div>').text(value.amount).html() + ' ' + $('<div>').text(unit).html() ;
            $(element).html(html); 
        },
        
        /**
        Gets value from element's html
        
        @method html2value(html) 
        **/        
        html2value: function(html) {        
          /*
            you may write parsing method to get value by element's html
            e.g. "Moscow, st. Lenina, bld. 15" => {city: "Moscow", street: "Lenina", building: "15"}
            but for complex structures it's not recommended.
            Better set value directly via javascript, e.g. 
            editable({
                value: {
                    city: "Moscow", 
                    street: "Lenina", 
                    building: "15"
                }
            });
          */ 
          return null;  
        },
      
       /**
        Converts value to string. 
        It is used in internal comparing (not for sending to server).
        
        @method value2str(value)  
       **/
       value2str: function(value) {
           var str = '';
           if(value) {
               for(var k in value) {
                   str = str + k + ':' + value[k] + ';';  
               }
           }
           return str;
       }, 
       
       /*
        Converts string to value. Used for reading value from 'data-value' attribute.
        
        @method str2value(str)  
       */
       str2value: function(str) {
           /*
           this is mainly for parsing value defined in data-value attribute. 
           If you will always set value by javascript, no need to overwrite it
           */


           return str;
       },                
       
       /**
        Sets value of input.
        
        @method value2input(value) 
        @param {mixed} value
       **/         
       value2input: function(value) {
           if(!value) {
             return;
           }
           this.$input.filter('[name="amount"]').val(value.amount);

           var units=JSON.parse(this.options.scope.dataset['units'])
           console.log(units)
           if (Object.keys(units).length>1) {
                var html = '<select name="unit" class="form-control">'
                for (var key in units) {
                    var option = '<option value="W">'+units[key]+'</option>'
                    html += option
                }
                html += '</select>'
                $('#unit-container').html(html)
                // Add hidden option
           } else {
                // add options
           }
           this.$input.filter('[name="unit"]').val(value.unit);

       },       
       
       /**
        Returns value of input.
        
        @method input2value() 
       **/          
       input2value: function() { 
           return {
              amount: this.$input.filter('[name="amount"]').val(),
              unit: this.$input.find('[name="unit"]').val()
           };
       },        
       
        /**
        Activates input: sets focus on the first field.
        
        @method activate() 
       **/        
       activate: function() {
            this.$input.filter('[name="amount"]').focus();
       },  
       
       /**
        Attaches handler to submit form in case of 'showbuttons=false' mode
        
        @method autosubmit() 
       **/       
       autosubmit: function() {
           this.$input.keydown(function (e) {
                if (e.which === 13) {
                    $(this).closest('form').submit();
                }
           });
       }       
    });

    AmountAndUnit.defaults = $.extend({}, $.fn.editabletypes.abstractinput.defaults, {
        tpl:'<input style="" class="form-control" name="amount" step="0.01" type="number" /><div id="unit-container"></div>' //+
                    //'<select style="" class="form-control" name="unit">'+
                    //'<option value="W" selected="selected">kr/kg</option>'+
                    //'<option value="U">kr/'+"" +'</option>'+
    //'</select>'

    ,

        inputclass: ''
    });

    $.fn.editabletypes.amount_and_unit = AmountAndUnit;

}(window.jQuery));