# Farmers Elevator

Version 0.0.3
started on september 2021 - now for different system structure

*Authors: Luca and Daniel*

An application for grain elevators ([Grain elevator - Wikipedia](https://en.wikipedia.org/wiki/Grain_elevator)) for giving them their own website and ecommerce to sell food for livestock to farmers.

The problem specifically arises today because farmers would need to call the elevator several times to complete an order. The order would take even longer in case it has been placed during the weekend.

### Structure

```
farmerselevator
│
├─── database/
│        ├ base.db
│        ├ schemas.txt
│        └ db
│
├─── src/
│        ├ api/
│        │   ├ buy.py
│        │   ├ elevatorList.py
│        │   ├ orders.py
│        │   ├ products.py
│        │   ├ registration.py
│        │   └ settings.py
│        ├ pages/
│        │   ├ contuctus.py
│        │   ├ error.py
│        │   ├ home.py
│        │   ├ index.py
│        │   ├ logout.py
│        │   ├ manageShop.py
│        │   ├ profile.py
│        │   ├ registration.py
│        │   ├ settings.py
│        │   └ shop.py
│        └ helper.py
│
├─── static/
│
├─── templates/
│
└ ─── uploads/
```

### Installation guide

From the website [flask.palletsprojects.com/en/2.0.x/installation](https://flask.palletsprojects.com/en/2.0.x/installation/)
Create a project folder and a venv folder within:

```
> py -3 -m venv venv
```

Before you work on your project, activate the corresponding environment:

```
> venv\Scripts\activate
```

Then can install Flask within the activated environment

```
> pip install Flask
```

**Packages needed:**

- `pip install pysqlite3`, in case of SQLite3 DataBase usage
- `pip install bcrypt` for hasing passwords

### To Do

Now:

- [x] Correct the address in /settings (does not take spaces)

- [x] Correct the description of products input in /manage-shop (does not take spaces)

- [ ] Update /home orders table for farmers and elevators using SOCKET/IO

- [ ] Add payments

- [ ] Send email when sending the new order

- [ ] Create PDF when creating an order

- [x] Correct user_id and product_id generation

- [ ] When creating an id it will be the same for elevator and farmer

- [ ] Have a list of elegible elevators that can suscribe to the platform

- [ ] If logged in, replace signup and signin with user profile

- [ ] SQL injection threats

- [ ] in homepage have map populated for searching elevators

- [ ] finish contact-page: send email to us, blogging for developers

- [ ] create blog and pages from footer

- [ ] create live chat messages tools

- [x] Move to Bootstrap

- [ ] Fix css for populating results in search bar, offset to the right (index.js) use Vue.js


### API Description

The API handles all the request for adding, deliting and modifying users. The API also handles the interaction with tables in the Database.

### DATABASE TABLES

- **farmers** is the table to store all farmer users
- **elevators** is the table to store all elevator users
- **products** stores the list of products for each elevator
- **orders** all transactions
- **deleted_products** stores all deleted products
- **contact_us_messages** stores all deleted products

### References

[https://flask.palletsprojects.com/en/2.0.x/quickstart/#cookies](https://flask.palletsprojects.com/en/2.0.x/quickstart/#cookies)

[https://www.mongodb.com/products/shell](https://www.mongodb.com/products/shell)

[https://flask-socketio.readthedocs.io/en/latest/getting_started.html](https://flask-socketio.readthedocs.io/en/latest/getting_started.html)

[https://pythonhosted.org/Flask-Mail/](https://pythonhosted.org/Flask-Mail/)
