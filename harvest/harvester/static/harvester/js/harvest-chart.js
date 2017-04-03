
// Hjälpfunktion för att lägga till enhet i cirkeldiagram
function formatter_unit(unit,y,data) {
    return y+unit;
}


// uppdatera cirkeldiagram.
// result är en hash, selector är objektet som ska uppdateras.

function updateHarvestChart(result, selector) {
    var text_1;
    var text_2;
    var percentage;
    var foregroundColor="#1b5e20"
    var backgroundColor="#9e9e9e";
    var data;
    var colors;
    var OVER="#ff5722";
    var REMAINING="#9e9e9e";
    var HARVESTED="#4caf50";
    if ((result.order_unit)=="U")
    {
        if (result.harvest_remaining>0) {
            colors = [HARVESTED,REMAINING]
            data= [
                 {label: "skördat", value: result.harvested_amount},
                {label: "återstår", value: result.harvest_remaining}
            ]

        } else if (result.harvest_remaining==0) {
            colors= [HARVESTED]
            data= [
                 {label: "Skördat", value: result.harvested_amount},

            ]


        } else if (result.harvest_remaining<0) {
            colors=[OVER,HARVESTED]
            data= [
                 {label: "överskördat", value: -result.harvest_remaining},
                 {label: "Skördat", value: result.harvested_amount},

            ]


        }
    } else if (result.order_unit=="W") {
        if (result.harvested_amount==0) {
                colors = [REMAINING]
                data= [

                    {label: "återstår", value: result.harvest_remaining}
                 ]
        }
        else if (result.harvest_remaining/parseFloat(result.order_amount)>0.05) {
            colors = [HARVESTED,REMAINING]
            data= [
                 {label: "skördat", value: result.harvested_amount},
                {label: "återstår", value: result.harvest_remaining}
            ]

        }  else if (result.harvest_remaining/parseFloat(result.order_amount)<-0.05) {

            colors=[OVER,HARVESTED]
            data= [
                 {label: "överskördat", value: -result.harvest_remaining},
                 {label: "ordered", value: result.total_order_amount},

            ]
        }    	else {
                colors=[HARVESTED]
                        data= [
                 {label: "Skördat", value: result.harvested_amount},

            ]

        }
    }

    selector.html("")

    console.log(data)

       Morris.Donut({
        element: selector,
        data: data,
        colors:colors,
        formatter:formatter_unit.bind(null,result.order_unit_text_short)
});
}