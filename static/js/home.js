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


function deleteOrder(order_id, cart_id, discount=0) {
  total_amount = document.getElementById('total_amount')
  order_amount = document.getElementById('order'+order_id)
  order_price = document.getElementById('order_price'+order_id)
  total_price = document.getElementById('total_price')
  $.ajax ({
    type: 'POST',
    url: '/delete_order',
    data: {
      'order_id': order_id,
    },
    success: function () {
      if (Number(total_amount.textContent) - Number(order_amount.textContent) === 0) {
        $.ajax({
          type: 'GET',
          url: '/delete_cart/'+cart_id
        }),
        block = document.getElementById('cart_block');
        empty_block = document.getElementById('empty_cart');
        cart_badge = document.getElementById('cart_badge')
        block.style.display = 'none';
        empty_block.style.display = 'flex';
        cart_badge.style.display = 'none';
      } else {
        if (order_amount != 1) {
          total_amount.innerHTML = Number(total_amount.textContent) - Number(order_amount.textContent);
          total_price.innerHTML = Number(total_price.textContent) - Number(order_amount.textContent) * Number(order_price.textContent);
          if (discount) {
            order_discount_price = document.getElementById('order_discount_price'+order_id).textContent;
            total_discount_price = document.getElementById('total_discount_price');
            total_discount_price.innerHTML = (
              Number(total_discount_price.textContent) - Number(order_amount.textContent) * Number(order_discount_price)).toFixed(2);
            if (Number(total_discount_price.textContent) === Number(total_price.textContent)) {
              discount_description = document.getElementById('discount_description')
              total_description = document.getElementById('total_price')
              total_description.style.color = 'black';
              total_description.style.textDecoration = 'none';
              discount_description.style.display = 'none';
            }
          }
        }
        block = document.getElementById('order_block'+ order_id);
        block_btn = document.getElementById('order_edit_btn'+order_id);
        block.style.display = 'none';
        block_btn.style.display = 'none';
      }
    }
  })
}


function changeAmountOfProduct(quantity, operator, order_id, cart_id, discount=0) {
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
          if (discount) {
            order_discount_price = document.getElementById('order_discount_price'+order_id).textContent;
            total_discount_price = document.getElementById('total_discount_price');
            total_discount_price.innerHTML = (Number(total_discount_price.textContent) + Number(order_discount_price)).toFixed(2);
            console.log(total_discount_price)
          }
        } else {
          total_amount.innerHTML = Number(total_amount.textContent) - Number(1);
          total_price.innerHTML = Number(total_price.textContent) - Number(order_price.textContent);
          el.innerHTML = Number(el.textContent) - Number(1);
          if (discount) {
            order_discount_price = document.getElementById('order_discount_price'+order_id).textContent;
            total_discount_price = document.getElementById('total_discount_price');
            total_discount_price.innerHTML = (Number(total_discount_price.textContent) - Number(order_discount_price)).toFixed(2);
            console.log(total_discount_price)
          }
          if (Number(el.textContent) - Number(1) < 0) {
            block = document.getElementById('order_block'+ order_id);
            block_btn = document.getElementById('order_edit_btn'+order_id);
            block.style.display = 'none';
            block_btn.style.display = 'none';
            if (discount) {
              deleteOrder(order_id, cart_id, 1)
            } else {
              deleteOrder(order_id, cart_id)
            }
            if (Number(total_amount.textContent) - Number(1) < 0) {
              $.ajax({
                type: 'GET',
                url: '/delete_cart/'+cart_id
              }),
              cart_badge = document.getElementById('cart_badge')
              block = document.getElementById('cart_block');
              empty_block = document.getElementById('empty_cart');
              block.style.display = 'none';
              empty_block.style.display = 'flex';
              cart_badge.style.display = 'none';
          }
        }
      }
      }
    }
  })
}


function applyPromotion() {
  id_coupon = document.getElementById('id_coupon').value
  $.ajax ({
    type: 'POST',
    url: '/promotion/apply_promotion',
    data: {
      'code': id_coupon
    },
    success: function(data) {
      location.reload()
    }
  })
}


function findCoupon() {
  code = document.getElementById('code').value
  $.ajax ({
    type: 'PUT',
    url: '/promotion/find_coupon',
    data: {
      'code': code
    },
    success: function(data) {
      if (data.promotion) {
        el = document.getElementById('promotion_message')
        f_btn = document.getElementById('find_promotion')
        id_coupon = document.getElementById('id_coupon')
        id_coupon.value = data.promotion
        a_btn = document.getElementById('apply_promotion')
        if (data.type === 'persent') {
          el.innerHTML = `Promotion ${data.title} with ${data.value}% discount was found`
        } else {
          el.innerHTML = `Promotion ${data.title} with ${data.value} ${data.type} discount was found`
        }
        f_btn.style.display = 'none'
        a_btn.style.display = 'block'
        el.style.color = 'blue'
        el.style.display = 'block'
      } else {
        el = document.getElementById('promotion_message')
        el.style.display = 'block'
      }
    }
  })
}
