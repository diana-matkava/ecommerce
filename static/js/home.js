function likeProduct(id) {
    $.ajax({
        type: 'PUT',
        url: '/like_product',
        data: {
            'id': id
        }
    })
    console.log('Good')
}