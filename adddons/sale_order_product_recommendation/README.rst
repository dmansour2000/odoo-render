=================================
Sale Order Product Recommendation
=================================



This module adds a recommended products wizard to current sale order.

It is based on recent delivered products, and allows the salesman to quickly
know the most sold products for current customer, which results in an easy to
use hint to improve sale.

If you want a better mobile usability, the module is ready to use with the
'web_widget_numeric_step' module. Just install it and you will get a better
numeric input experience.

**Table of contents**


Configuration
=============

To configure this module you need to:

In sale order product recommendation you can display the product price unit
from list price or from last sale order price. To set the default value follow
the next steps

#. Go to *Sales > Configuration > Settings > Sale order recommendations*.
#. Assign the desired value to *Product recommendation price origin* field.
#. Press *Save* button to store the change.

In sale order product recommendation you can compute the recommendations using the
Delivery Address instead of the Customer. To set this option by default follow
the next steps

#. Go to *Sales > Configuration > Settings > Sale order recommendations*.
#. Assign the desired value to *Use delivery address* field.
#. Press *Save* button to store the change.

You can define other default values like as:

* Months backwards to generate recommendations.
* Number of recommendations to display.

You can force the addition of all the products recommended in the sale order. 
You can then edit the desired quantities directly in the sale order. 

#. Go to *Sales > Configuration > Settings > Sale order recommendations*.
#. Select *Force zero units included*

You can add a filter domain to exclude or include additional recommended products.

#. Go to *Sales > Configuration > Settings > Sale order recommendations*.
#. Add a filter in section *Sale order product recommendation domain* Example: ``[("product_type", "!=" "service")]``

Usage
=====

To use this module, you need to:

#. Create a new sale order.
#. Assign its customer.
#. Press *Recommended Products* button.
#. Configure the recommendations parameters.
#. Press *Get recommendations* button.
#. Add products into the opened wizard.
#. If you don't change quantities, the line will not be updated.
#. Press *Accept*.


