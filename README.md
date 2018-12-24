# Flask-Mocking-Payment
Using flask to mock a payment system (db: SQLAlchemy)

Since I am not a web programmer expert, I spent some time to choose the main tools for this project. I took a look at Ruby on Rails and .Net Core, but they are "too robust" - and I wanted the feeling of building it from scratch. Given that, I used Python + Flask + SQLAlchemy in order to achieve it.

As for the task, with the MVC as pattern, the proposed Client, Buyer, Payment and Card models were created. Each one has a String as id (randomly created in runtime) because I didn't want to use integers. Althought I am not sure about the best way to do that, random strings look safer as hash keys.

Payment contains a link to Card, which contains a link to Buyer, which contains a link to Client. Because a card is required to create a payment, only payments done via credit card are inserted in the database. In case it was not a requirement, I would choose to use a "blank card" for all payments made via boleto.

Tests were created in order to make the code robust, but these are not unit ones (task to be completed). All the inputs provided to the form are tested to guarantee that valid data will be inserted in the database. Also another test step is done before trying to insert the data, AFTER the form validation and BEFORE the actual insertion, so we can avoid the errors that arise from database unique and primary keys restrictions.

Looking forward to hearing from you so I can realize how professional production-level code is architectured. ;)

How to run:

After requirements have been installed (check requirements.txt) run:

python run.py runserver

... And access http://localhost:5000.

TO BE COMPLETED: unit tests 
TO BE ADDED: Docker

PS: https://github.com/moip is offline! (Couldn't get the hints ;p)
