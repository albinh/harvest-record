function updateCustomerCategory(event) {
    console.log(event);
    var pk=$(event.target).data("pk");

    var data =
    {
        category: event.target.value
    }

    $.ajax({
    url: '/harvester/api/v1/customers/'+pk,
    type: 'PATCH',
    dataType: "json",
    contentType: "application/json; charset=utf-8",
    data: JSON.stringify(data),


})


}
$(".category").on("input", updateCustomerCategory);