<img width="100" src="https://my.ipaymu.com/asset/images/logo-ipaymu.png">

## Usage

### Requirement

First, get your apikey & va number from iPaymu dashboard.

Install requirements:
```python
pip install requirements.txt
```

### Initialization

```python
from ipaymu import Main

api_key = 'your-apikey'
va = 'your-va'
production = true

ipaymu = Main(api_key, va, production)
```

### General

### Check Balance

```python
ipaymu.check_balance()
```

### Check Transaction
Param: Transaction ID
```python
status = ipaymu.check_transaction(id)
```

#### Set URL

```python
url = {
    ureturn: "your-return-url",
    ucancel: "your-cancel-url",
    unotify: "your-notify-url",
}

ipaymu.set_url(url)
```

#### Set Buyer

```python
buyer = {
    name: "buyer name",
    email: "buyer email",
    phone: "buyer phone",
}

ipaymu.set_buyer(buyer)
```

### Payment

There are 2 payment methods: Payment Direct & Payment Redirect, with the following parameters:

##### paymentMethod

- va => Virtual Account
- banktransfer => Transfer Bank
- cstore => Convenience Store
- cod => Cash on Delivery

#### paymentChannel

##### va

- bag => Bank Artha Graha
- bni => Bank Negara Indonesia
- cimb => Bank Cimb Niaga
- mandiri => Bank Mandiri
- bri => Bank BRI
- bca => Bank BCA

##### banktransfer

- bca => Bank Central Asia

##### cstore

- indomaret
- alfamart

##### cod

- rpx

### Paramaters

| Parameter Request | Description                                                                                               | Type            | Mandatory |
| ----------------- | --------------------------------------------------------------------------------------------------------- | --------------- | --------- |
| account           | VA Number                                                                                                 | numeric         | Y         |
| name              | Customer Name                                                                                             | string          | Y         |
| email             | Customer E-mail                                                                                           | string          | Y         |
| phone             | Customer Phone                                                                                            | numeric         | Y         |
| amount            | Total Amount (price \* qty)                                                                               | numeric         | Y         |
| paymentMethod     | va, banktransfer, cstore, cod                                                                             | string          | Y         |
| paymentChannel    | <p>"**va:**" bag, bni, cimb, mandiri, bri, bca</p><p>"**cstore:**" indomaret, alfamart </p>"**cod:**" rpx | string          | Y         |
| notifyUrl         | Return url when payment success                                                                           | string          | Y         |
| expired           | Expiration in hour                                                                                        | numeric         | N         |
| description       | Text description                                                                                          | string          | N         |
| referenceId       | Shopping cart order id                                                                                    | string          | N         |
| product           | Product Name                                                                                              | [array] string  | Y         |
| qty               | Quantity                                                                                                  | [array] numeric | Y         |
| price             | Product Price                                                                                             | [array] numeric | Y         |
| weight            | Product Weight                                                                                            | [array] numeric | Y         |
| length            | Product Length                                                                                            | [array] numeric | Y         |
| width             | Product Width                                                                                             | [array] numeric | Y         |
| height            | Product Height                                                                                            | [array] numeric | Y         |
| deliveryArea      | Postal Code Customer                                                                                      | numeric         | Y         |
| deliveryAddress   | Customer Address                                                                                          | string          | Y         |
| pickupArea        | Postal Code Shipper (Default Merchant Postal Code)                                                        | numeric         | N         |
| pickupAddress     | Shipper Address (Default Merchant Address)                                                                | string          | N         |

#### Add Product to Cart

First, please add product to shopping cart first before using this method

```python
data = {
    'product': ['product 1 ', 'product2 '],
    'quantity': ['1', '2'],
    'price': ['10000', '50000'],
    'description': ['product-desc', 'product-desc 2'],
    'weight': [1, 2],       # nullable (kilogram)
    'height': [10, 10],     
    'length': [30, 40],     
    'width': [10, 50],      
}

ipaymu.add_cart(data)

# assign cart to var
cart = ipaymu.carts
```
> **IMPORTANT:** The `height`, `length`, `width` attribute must be filled with the same dimension of array. If the one of items hasn't one of those attribute fill with 0 (zero)

#### Set COD (Only if COD method)

```php
$delivery = $iPaymu->setCOD([
        'deliveryArea' => "76111",
        'deliveryAddress' => "Denpasar",
]);
```

### Payment Direct

Payment direct method allows you to accept payment on your checkout page directly, this method works for any payment channel except for credit card.

```php
$payment = $iPaymu->directPayment($directData);
```

### Payment Redirect

In order accepting credit card, you must use Payment Redirect method. Upon checkout, you will be redirected to iPaymu.com payment page for further payment processing.

```php
$payment = $iPaymu->redirectPayment($redirectData);
```