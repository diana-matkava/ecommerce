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

