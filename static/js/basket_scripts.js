function updateBasketCount(){
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById("basket_menu").innerHTML =
      this.responseText;
    }
  };
  var url = "/basket/basket_menu_update/";
  xhttp.open("GET", url, true);
  xhttp.send();
}

function updateItemsCount(){
    var sum = 0;
    $('.quantity').each(function(){
        //sum += parseInt($(this).val());
        sum += 1;
    });
    $('.count').text("В вашей корзине " + sum.toString() + " товаров.");
};

window.onload = function() {
    $('.items').on('input', 'input[type="number"]', function(event){
        var target_href = event.target;
          if (target_href){
            $.ajax({
                url: "/basket/edit/" + target_href.name + "/" + target_href.value + "/",
                success: function(data){
                    $('.items').html(data.result);
                    updateBasketCount();
                },
            });
        }
        event.preventDefault();
    });

    $('.items').on('click', 'button[type="button"]', function(event){
        var target_href = event.target;
        if (target_href){
            $.ajax({url: "/basket/remove/" + target_href.name + "/",
                success: function(data){
                    updateBasketCount();
                    if (data.result=='Empty'){

                        $('.count').text("В вашей корзине товаров не осталось:(");
                        $('.items').html('<div class="empty_list"></div>');
//                        $('.make_order').attribute("style={display: none;}");
//                        $('.basket_list').attribute("style={display: none;}");
                    }
                    else {
                        updateItemsCount();
                        $('.items').html(data.result);
                    }


                },
            });
        }
        event.preventDefault();
    });
}

