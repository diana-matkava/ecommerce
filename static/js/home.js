function likeProduct(id) {
    el = document.getElementById("like"+id);
    num = document.getElementById('like_num'+id);
  if(el.style.color === 'grey'){
    el.style.color = 'red';
    num.textContent = Number(num.textContent) + Number(1)
  } else {
    el.style.color = 'grey';
    num.textContent = Number(num.textContent) - Number(1)
  }
    $.ajax({
        type: 'PUT',
        url: '/like_product',
        data: {
            'id': id
        }
    })
}

function changeAmountOfProduct(quantity, operator, order_id) {
  $.ajax({
    type: 'POST',
    url: '/change_product_amount',
    data: {
      'order_id': order_id,
      'operator': operator,
      success: function() {
        el = document.getElementById('order'+order_id)
        total_price = document.getElementById('total_price')
        order_price = document.getElementById('order_price'+order_id)
        total_amount = document.getElementById('total_amount')
        if (operator === '+') {
          el.innerHTML = Number(el.textContent) + Number(1);
          total_amount.innerHTML = Number(total_amount.textContent) + Number(1);
          total_price.innerHTML = Number(total_price.textContent) + Number(order_price.textContent);
        } else {
          el.innerHTML = Number(el.textContent) - Number(1);
          total_amount.innerHTML = Number(total_amount.textContent) + Number(1);
          total_price.innerHTML = Number(total_price.textContent) - Number(order_price.textContent);
        }
      }
    }
  })
}

function deleteOrder(order_id) {
  $.ajax ({
    type: 'POST',
    url: '/delete_order',
    data: {
      'order_id': order_id,
    },
    success: function () {
        block = document.getElementById('order_block'+ order_id);
        block_btn = document.getElementById('order_edit_btn'+order_id)
        block.style.display = 'none'
        block_btn.style.display = 'none'
    }
  })
}