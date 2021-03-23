# Flask Store Demo

This is a capstone project completed for the Springboard, Software Engineering course. The purpose of this demo is to highlight the following skills:

- Python
- Flask
- API development (via Python and Flask)
- Integration with a 3rd party API (Stripe)
- Basic link encryption (via Bcrypt)
- PostgreSQL
- Several Flask libraries, including: SQLAlchemy, Flask Uploads and Flask WTForms

This is not a fully functional online store and there are numerous security, design, and error checking enhancements that would need to be implemented before this application could be used in a real-world environment.

## Outward Public Interface

The outward, public interface will allow to select items to add to their shopping card. The user can opt to either "quick add" a single cart item or select a preview of the item where the user can add additional product. Once an item (or items) is added to the cart, the user can then go view the cart and start the checkout process.

## Admin Dashboard/Interface
For simplicity, the administrator section can quickly jump to the admin section by clicking on the bottom left button. A user will be required to log in, but for demonstration purposes, an admin can create a new account as well. The ‘Product Manager’ dashboard allows the administrator to add (POST), edit (PATCH) or delete (DELETE) a store product. Under the ‘Orders’ tab, the admin can see each order and click on the reference number to see all of the order details. The administrator can also delete (DELETE) an order once it has theoretically shipped to the customer.

## Project Link
The live version of this project can be found at [https://flask-shop1993.herokuapp.com/](https://flask-shop1993.herokuapp.com/)