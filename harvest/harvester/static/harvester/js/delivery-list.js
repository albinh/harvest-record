var state_filter = "all"
var date_filter  = "all"
function set_state_filter(status) {

    if (status=="not_delivered") {
        $("#state_dropdown").html('Visar ej levererade <i class="material-icons right">arrow_drop_down</i>');}
    else if (status=="delivered"){
        $("#state_dropdown").html('Visar levererade <i class="material-icons right">arrow_drop_down</i>');
    } else {
        $("#state_dropdown").html('Visar alla <i class="material-icons right">arrow_drop_down</i>');

    }

    state_filter=status

    refilter();
}

// "all", "delivered", "not_delivered"

function set_date_filter(filter) {
    if (filter=="all") {
        $("#date_dropdown").html('Visar alla datum <i class="material-icons right">arrow_drop_down</i>');}
    else {
        $("#date_dropdown").html('Visar närliggande datum <i class="material-icons right">arrow_drop_down</i>');
    }
    // "all", "present" (+-2 dagar) "
    date_filter=filter;
    refilter();
}

function diffDays(d1, d2)
{
  var ndays;
  var tv1 = d1.valueOf();  // msec since 1970
  var tv2 = d2.valueOf();

  ndays = (tv2 - tv1) / 1000 / 86400;
  ndays = Math.round(ndays - 0.5);
  return ndays;
}

function refilter(){
    df = function () {
        d1=new Date($(this).data("date"));
                        return Math.abs(diffDays(d1,new Date())) < 3  ;
                    }

    var filtered=$(".card");

    if (date_filter=="present") {
        filtered = $(".card").filter(df)
    } else {
        filtered = $(".card")
    }

    if (state_filter=="delivered") {
        filtered=filtered.filter("[data-state='D']")
    } else if (state_filter=="not_delivered") {
       filtered=filtered.filter("[data-state!='D']")
    }
}