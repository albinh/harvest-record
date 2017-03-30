function updateModalChart() {

    var result_o=$("#add_harvest_modal").data("info");

    var result = JSON.parse(JSON.stringify(result_o));

	var now_amount;
	if (result.order_unit == "W" )
		now_amount = parseFloat($("#add_harvest_modal input[name='kg']").val());
	else
	 		now_amount = parseFloat($("#add_harvest_modal input[name='st']").val());
    if (isNaN(now_amount)) 
    	{now_amount=0.0;}
    result.harvest_remaining-=now_amount;
    result.harvested_amount+=now_amount;


    var harvest_remaining = result.order_amount-result.harvested_amount-now_amount

    updateHarvestChart(result, $("[name='modal_chart']"));

}



// Called when the modal is opened.
function updateAddHarvestModal(modal,trigger) {
    var pk=trigger.data("pk")
    var data = $(".delivery_item[data-pk='"+pk+"']").data("info");
    $("#add_harvest_modal").data("info",data);
    console.log(data);

    if (data.countable) {
        modal.find("div.count").show()
    } else {
            modal.find("div.count").hide()
    }
	console.log("test")
    modal.find("[name='kg']").val("");
    modal.find("[name='st']").val("");

	updateModalChart();


}
