# if current_user.display_currency_id != self.product_obj.currency_id:
#             user_cur = Currency.query.get(current_user.display_currency_id)
#             responce = requests.get(f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={self.product_obj.currency}&to_currency={user_cur}&apikey={CURRENCY_API_KEY}').json()
#             print()
#             rate = responce['Realtime Currency Exchange Rate']['5. Exchange Rate']
#             price = price * float(rate)