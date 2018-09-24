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

window.onload = function() {
    $('.basket_list').on('input', 'input[type="number"]', function(event){
        var target_href = event.target;
          if (target_href){
            $.ajax({
                url: "/basket/edit/" + target_href.name + "/" + target_href.value + "/",
                success: function(data){
                    updateBasketCount();
                    $('.basket_list').html(data.result);
                },
            });
        }
        event.preventDefault();
    });

    $('.basket_list').on('click', 'button[type="button"]', function(event){
        var target_href = event.target;
        if (target_href){
            $.ajax({url: "/basket/remove/" + target_href.name + "/",
                success: function(data){
                    updateBasketCount();
                    if (data.result=='Empty'){
                        $('.caption').text("Empty");
//                        $('.make_order').attribute("style={display: none;}");
//                        $('.basket_list').attribute("style={display: none;}");
                    }
                    else {
                        $('.basket_list').html(data.result);
                    }


                },
            });
        }
        event.preventDefault();
    });
}

