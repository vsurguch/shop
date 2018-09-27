
window.onload = function () {

var _quantity, _price;
var quantity_array = [];
var price_array = [];

var TOTAL_FORMS = parseInt($('input[name="orderitems-TOTAL_FORMS"]').val());
var order_total_quantity = parseInt($('.order_total_quantity').text()) || 0;
var order_total_cost = parseFloat($('.order_total_cost').text()) || 0;

for (var i=0; i<TOTAL_FORMS; i++){
    _quantity = parseInt($('input[name="orderitems-'+i+'-quantity"]').val());
    _price = parseFloat($('.itemprice_'+i).text().replace(',','.'));

    quantity_array[i] = _quantity;
    if (_price) {
        price_array[i] = _price;
    } else {
        price_array[i] = 0;
    }
}

function orderSummaryRecalc(){
    order_total_quantity = 0;
    order_total_cost = 0;

    for (var i=0; i < TOTAL_FORMS; i++){
        order_total_quantity += quantity_array[i]
        order_total_cost += quantity_array[i] * price_array[i]
    }
    $('.order_total_quantity').html(order_total_quantity.toString());
    $('.order_total_cost').html(order_total_cost.toString());
}

if (!order_total_quantity){
    orderSummaryRecalc();
}

function orderSummaryUpdate(item_price, quantity_change) {
    cost_change = item_price * quantity_change;
    order_total_quantity += quantity_change;
    order_total_cost += cost_change;
    $('.order_total_quantity').html(order_total_quantity.toString());
    $('.order_total_cost').html(order_total_cost.toString());
};

function updateData(data, orderitem_i) {
    if (data.price) {
        price_array[orderitem_i] = parseFloat(data.price);
        if (isNaN(quantity_array[orderitem_i])){
            quantity_array[orderitem_i] = 0;
        }
        $('.itemprice_'+orderitem_i).text(data.price.toString());
        orderSummaryRecalc();
    }
};

function onOrderItemChange() {

    var target = event.target;
    orderitem_i = parseInt(target.name.replace('orderitems-','').replace('-item',''));
    var orderitem_pk = target.options[target.selectedIndex].value;

    if (orderitem_pk) {
        $.ajax({
            url: '/order/item/' + orderitem_pk.toString() + '/price',
            success: function (data){
                updateData(data, orderitem_i);
            },
        });
    }
};

function onOrderFormNumberClick () {

    var target = event.target;
    orderitem_i = parseInt(target.name.replace('orderitems-','').replace('-quantity',''));

    if (price_array[orderitem_i]) {
        item_quantity = parseInt(target.value);
        quantity_change = item_quantity - quantity_array[orderitem_i];
        quantity_array[orderitem_i] = item_quantity;
        orderSummaryUpdate(price_array[orderitem_i], quantity_change);
    }
};

function onOrderFormCheckboxClick () {

    var target = event.target;
    orderitem_i = parseInt(target.name.replace('orderitems-','').replace('-DELETE',''));

    if (target.checked) {
        quantity_change = - quantity_array[orderitem_i];
    } else {
        quantity_change = quantity_array[orderitem_i];
    }
    orderSummaryUpdate(price_array[orderitem_i], quantity_change);

};

$('.order_item_select').change(onOrderItemChange);
$('.order_form').on('change', 'input[type="number"]', onOrderFormNumberClick);
$('.order_form').on('click', 'input[type="checkbox"]', onOrderFormCheckboxClick);
}