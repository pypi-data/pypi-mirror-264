import ipaymu

main = ipaymu.Main()
main.set_va("0000008999927923")
main.set_api_key("SANDBOX76A13A0D-AD50-4061-9832-F5AF22B541D8-20220316213052")

carts = {
    'product': ['product 1 ', 'product2 '],
    'quantity': ['1', '2'],
    'price': ['10000', '50000'],
    'description': ['product-desc', 'product-desc 2'],
    'weight': [1, 2],       # nullable (kilogram)
    'height': [10, 10],     
    'length': [30, 40],     
    'width': [10, 50],
}

main.add_cart(carts)
a = main.redirect_payment({})
print(a)