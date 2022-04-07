$('#m_select').on('change', function () {
    
    var isDirty = !this.options[this.selectedIndex].defaultSelected;

    if (isDirty) {
        select_value = document.getElementById('m_select').value
        quantity = document.getElementById('m_quantity')
        button = document.getElementById('m_button')
        coupon = document.getElementById('m_coupon')
        instant = document.getElementById('instant')
        if (select_value == 'multiple') {
            quantity.style.display = 'block'
            button.style.display = 'block'
            coupon.style.display = 'block'
            instant.style.display = 'none'
        } else {
            quantity.style.display = 'none'
            button.style.display = 'none'
            coupon.style.display = 'none'
            instant.style.display = 'flex'
        }
    }
});


function generateCoupons() {
    quantity = document.getElementById('coupon_quantity').value
    if (Number(quantity) > 0) {
        $.ajax ({
            type: 'PUT',
            url: '/checkout/generate_coupon',
            data: {'quantity': quantity},
            success: function(data) {
                var text_content = String()
                for (const element of data.list_of_data) {
                    text_content += element + '\n'
                  }
                textarea = document.getElementById('m_coupons')
                textarea.innerHTML = text_content

                button = document.getElementById('g_button')
                button.style.color = 'red'
            }
        })
    }
}