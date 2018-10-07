
function updateBasketCount(){
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById("basket_menu").innerHTML =
      this.responseText;
    }
  };
//  var params = "user="+user_id;
  var url = "/basket/basket_menu_update/";
  xhttp.open("GET", url, true);
  xhttp.send();
}

window.onload = function(){
    updateBasketCount();
    $('.buy').on('click', function(event){
        var target_href = event.target;
        if (target_href){
            $.ajax({
                url: "/basket/add/" + target_href.name,
                success: function(data){
                    $('#basket_menu').html(data.result);
                },
            });
        }
        event.preventDefault();
    } );
}

function getSelectValues(id){
var el = document.getElementById(id);
var result = [];
var options = el.options;
var opt;

for (var i=0, iLen = options.length; i<iLen; i++ ){
    opt = options[i];
    if (opt.selected) {
        result.push(opt.value || opt.text);
    }
}
return result;
}

function loadDoc(authors, categories) {
  cat = getSelectValues(categories);
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementsByClassName("items_list")[0].innerHTML =
      this.responseText;
    }
  };
  var params = "authors="+authors+"&categories="+cat;
  var url = "/catalog_update/" + "?" + params;
  xhttp.open("GET", url, true);
  xhttp.send();
}

