// Vid förändring av någon av element i arrayen from skicka ett ajax-request till url.

function ajax_populate_select(url, froms, to, prefix="",initial=false) {

	function setCallback(f) {
        cb=change_callback.bind(this);
		f.on('change',cb)
	}

	function populate(element,valuelist) {

		valuelist.forEach(function(c) {
				element.append(new Option(c.name, c.id, false, false));
				})

	}


	function response_cb(response) {
	    to_element = $('#'+prefix+to).first();
		result = JSON.parse(response);

            if (result) {


            		to_element.empty();
            		var te=to_element[0];

            		populate(te,result);
            		to_element.trigger("change")


            } else {

            }

	}

	function change_callback(e) {

	    from_elements = froms.map((x)=>$('#'+prefix+x).first())
		params = {csrfmiddlewaretoken: csrf_token}
		// Add parameters to AJAX-call

		from_elements.forEach((f)=> {

			var id=f[0].id.replace(prefix,"");
			var v=f[0].value[0];
			if (v==null) {
			    return;
			    }
			params[id]=v;
		})
		$.post(
            url,
            params,
            response_cb)
	}
    function trigger(e) {
        e.trigger('change');
    }
    from_elements = froms.map((x)=>$('#'+prefix+x).first())
	from_elements.forEach(setCallback);
    if (initial) {
        from_elements.forEach(trigger);
    }
}

function reload_harvest_button(id) {
    function response_cb(btn, response) {
        result = JSON.parse(response);

        color=""


        switch (result.status) {
            case 0:
                color="primary"
                break;
             case 1:
                color="warning"
                break;
             case 2:
                color="success"
                break;
             case 3:
                color="danger";
                break;
               }
        try {
        	h=btn.getElementsByClassName("harvested")[0]
        if (h) {h.innerHTML=result.harvested_amount ;}
        } finally {}
        try {
        	h=btn.getElementsByClassName("target")[0]
        if (h) {h.innerHTML=result.target_amount ;}
        } finally {}

        try {
            h=btn.getElementsByClassName("relation")[0]
            if (h) {h.innerHTML=result.harvest_relation ; };
        } finally {}
        btn.classList.remove("btn-primary");
        btn.classList.remove("btn-warning");
        btn.classList.remove("btn-success");
        btn.classList.remove("btn-danger");
        btn.classList.remove("btn-default");
        btn.classList.add("btn-"+color)


    }

    btn = document.getElementById(id);
    id  = btn.dataset.id;
    url = btn.dataset.queryUrl;
    params = {csrfmiddlewaretoken: csrf_token, 'id':id}

    $.post(
        url,
        params,
        response_cb.bind(null, btn)
    )
 }

 var notLocked = true;
$.fn.animateHighlight = function(highlightColor, duration) {
    var highlightBg = highlightColor || "#FFFF9C";
    var animateMs = duration || 1500;
    var originalBg = this.css("backgroundColor");
    if (notLocked) {
        notLocked = false;
        this.stop().css("background-color", highlightBg)
            .animate({backgroundColor: originalBg}, animateMs);
        setTimeout( function() { notLocked = true; }, animateMs);
    }
};
