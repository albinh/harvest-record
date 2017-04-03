function updateModalChart() {
	var now_amount;

	var result2 = JSON.parse(JSON.stringify(result));
	if (result.order_unit == "W" )
		now_amount = parseFloat($("#id_weight").val());
	else
	 	now_amount = parseFloat($("#id_count").val());

    if (isNaN(now_amount))
    	{now_amount=0.0;}

    result2.harvest_remaining-=now_amount;
    result2.harvested_amount+=now_amount;


    var harvest_remaining = result.order_amount-result.harvested_amount-now_amount

    updateHarvestChart(result2, $("[name='modal_chart']"));
 }




$(document).ready(function() {
    $("#id_weight").on("input",updateModalChart);
    $("#id_count").on("input",updateModalChart);
})