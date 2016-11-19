function ajax_populate_select(url, froms, tos) {
	function callback() {
		params = {csrfmiddlewaretoken: "CYUyzNjBpqKvPKTDkbuVUDkN0TtwWQxv7jlbmnWTCBmH1BLACDG8oXHtftE43Vqb"}
		froms.forEach((f)=> {
			params[f.id]=f.val()
		})

		$.post(
        '/harvester/ajax/cropform_for_deliveryitem/',
        {   csrfmiddlewaretoken: "CYUyzNjBpqKvPKTDkbuVUDkN0TtwWQxv7jlbmnWTCBmH1BLACDG8oXHtftE43Vqb",
            params,
        function(response) {

            result = JSON.parse(response);

            if (result) {
            	tos.forEach(function(t) {
                	t.empty() // Use to empty the select
					values = result[t.id];
                	values.forEach(function(c, index) {
                        t.append(new Option(c.name, c.id, false, false));
                        console.log(c)
                    })
				e.trigger("change");
				})
            } else {
                console.log("error");
            }
        }

	})
	}

	froms.forEach(function(f) {
		f.on('change',callback)
	})


}
