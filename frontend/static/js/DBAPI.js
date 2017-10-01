function getProductExtras(productId) {
    var dataOut = [];
    var request = new XMLHttpRequest();
    request.onreadystatechange = function() {

        if (this.readyState == 4) {
            console.log(request.response);
            var data = request.response.replaceAll("][", ",");

            //Get extra options from DB
            if (request.response != "") {
                jsonData = JSON.parse(data);
                for (var i = 0; i < jsonData.length; i++) {
                    var extraData = jsonData[i];
                    id = extraData.id;
                    extra_name = extraData.name;
                    extra_price = extraData.price;

                    dataOut.push({"text": extra_name + " - £" + extra_price, "value": id});
                }
            }
        }
    };
    request.open("GET", "/productExtra/"+productId+"/", true);
    request.send();

    return dataOut;
}

function getNumberOfOptionsCategoryToDisplay(productId, csrf) {
    var result;
    $.ajax({
        url: "/getNumberOfOptions/",
        type: 'POST',
        data: {'productId' : productId, 'csrfmiddlewaretoken' : csrf},
        async: false,
        success: function (resultFromAjax) {
            result = resultFromAjax;
        },
        error: function (xmlHttpRequest, textStatus, errorThrown) {
            console.log("error");
        }
    });

    return result;
}
