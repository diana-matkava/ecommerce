# clear session
#  session.pop('_flashes', None)



# check user
# def load_user(id):
#     if not session['role']:
#         return Customer.query.get(int(id))
#     if session['role'] > 0:
#         return Seller.query.get(int(id))