# Phase II: Design Report 

## Detailed Design

**Methods:**

Function: `order_item(cust_id, authentication_token, item_id, cc_info)`

Input: The front end will send the id of the customer and will also provide an authentication token to verify his identity. The id of the dish the customer wishes to order will also be provided

Output: This method will output the order ID if it was placed successfully. A successful order requires valid authentication, valid inputs for all fields, and a successful transaction using the given credit card. A number of error codes will be sent back if the order failed:

 * 400 – Invalid cust\_id or item\_id
 * 401 – User failed to authenticate
 * 404 – Server is currently offline

Function: `rate_dish(authentication_token, order_id, rating, review_text)`

Input: An authentication token must be provided to authenticate the reviewer. The order id contains all the data needed to find the item. It includes: customer id, item id, and time of delivery. Finally, the customer must provide a rating (1-5) and optional review text.

Output: This function will return whether or not the review was successfully submitted. A valid review requires: 


* Rating between 1-5 inclusive
* Valid order id
* Valid authentication token for the customer specified in the order id
* Review text must not be blank or null if the user rates 3 or below.


Function: `bid\_order(authentication\_token, order\_id, bid)`

Input: An authenticated deliverer will bid on a specific order. Authentication, order id, and bid price must be provided

Output: This function will return a boolean value to signify whether the bid went through successfully. A successful bid requires proper authentication, an order to bid on, and a price which is lower than the current lowest bid. 

Function: `make\_payment(authentication\_token ,cc\_info, order\_id)`

Input: Credit card information is mandatory for making a payment. The order id will determine to which restaurant the payment goes to, how much will be paid, and which order we will pay for. Both must be valid.

Output: This function will call upon an external payment system to process this payment. Should the payment be successful, the function will return true. This function will be called by place\_order.

Function: `add\_cook(authentication\_token, restaurant\_id, name)`

Input: The manager authenticates himself and then adds a new cook to the restaurant. His name will have to be provided.

Output: If everything is valid, the given name will be registered as a cook for the given restaurant. The function will return the cook’s ID.

A similar function add\_seller will be used to add sellers. The only difference between add seller and add cook is that add seller will instead add the name to a list of sellers.

Function: `add\_dish(authentication\_token, cook, dish\_name, dish\_description dish\_price)`

Input: The cook will have to authenticate himself and then provide a dish name, a dish price, and a description.

Output: The given dish will be added to the database and will be available for customers to buy.

Function: `fire\_cook(authentication\_token,cook\_id)`

Input: A manager will provide his authentication token along with the id of the cook he wishes to fire.

Output: The cook will be marked as fired and will lose his ability to add dishes. All of his dishes will be removed from listings and marked as invalid.

register(id, email, password)

Input:  A vald email address and a proper password should be provided. 

Output: The user will have a pending registration if the email and password are valid. After a manager approves his registration, he will receive an email confirming that he is registered.

Function: `verify\_registration(auth\_token, manager\_id, cust\_id)`

Input:  A manager should validate himself with his token + id and provide a customer id.

Output: The given customer, if he is unverified, will be marked as verified and his account will be successfully registered.

Function: `change\_address(cust\_id, cust\_password, new\_address)`

Input:  Customer inputs his credentials with a new address.

Output: The customer's address will be changed.

Function: `add\_credit\_card(cust\_id, cust\_password, new\_address)`

Input:  Customer inputs his credentials  alongwith a  credit card.

Output: The credit card is registered to the customer.

Function: `mark\_as\_ready(auth\_token, cook\_id, order\_id)`

Input:  Cook verifies himself and then marks an order as cooked and ready for delivery

Output: The item is marked as ready for the delivery person.

Function: `mark\_as\_delivered(auth\_token, cook\_id, order\_id)`

Input:  Deliverer verifies himself and then marks an order as delivered

Output: The item is marked as delivered.

