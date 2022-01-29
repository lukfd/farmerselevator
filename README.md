# Farmers Elevator

Version 1.0.0
started on end January 2022

*Authors: Luca and Daniel*

An application for grain elevators ([Grain elevator - Wikipedia](https://en.wikipedia.org/wiki/Grain_elevator)) for giving them their own website and ecommerce to sell food for livestock to farmers.

The problem specifically arises today because farmers would need to call the elevator several times to complete an order. The order would take even longer in case it has been placed during the weekend.

For more technical info, visit /doc.

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
│        │   ├ chatUtils.py
│        │   ├ elevatorList.py
│        │   ├ orders.py
│        │   ├ products.py
│        │   ├ registration.py
│        │   ├ settings.py
│        │   └ usersUtils.py	
│        ├ pages/
│        │   ├ chat.py
│        │   ├ error.py
│        │   ├ index.py
│        │   ├ manageShop.py
│        │   ├ registration.py
│        │   ├ shop.py
│        │   ├ test.py
│        │   ├ about.py
│        │   ├ contuctus.py
│        │   ├ home.py
│        │   ├ logout.py
│        │   ├ profile.py
│        │   ├ settings.py
│        │   └ terms.py
│        └ helper.py
│
├─── static/
│        ├ images/
│        ├ node_modules/
│        ├ css/
│        ├ js/
│        ├ scss/
│        ├ package-lock.json
│        ├ package.json
│        └ README.md
│
├─── templates/
│
├─── uploads/
│
├─── __init__.py
│
└─── constants.py
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

To install requirements.txt python packages
```
> pip install -r requirements.txt
```

**Packages needed:**

- `pip install pysqlite3`, in case of SQLite3 DataBase usage
- `pip install bcrypt` for hasing passwords

---

### General To Do

- [ ] Switch from SQLite to a server database
- [ ] Add payments
- [ ] Send email when sending the new order
- [ ] Create PDF when creating an order
- [ ] Fix id creating for farmer_id and elevator_id
- [ ] Have a list of elegible elevators that can sign up to the platform
- [ ] SQL injection threats
- [ ] in index have map populated for searching elevators
- [ ] create live chat messages tools
- [ ] Fix css for populating results in search bar, offset to the right (index.js) use Vue.js
- [ ] All pages seems that have an extra width
- [ ] Discuss about how to store images
- [ ] Discuss if in /profile pages email and personal information should be public
- [ ] Check that when a farmer and elevator with the same id, when uploading image will have different image name in /uploads

#### Finised To do

**0.0.1 to 0.0.3**

- [x] Move to Bootstrap
- [x] Correct user_id and product_id generation
- [x] Correct the address in /settings (does not take spaces)
- [x] Correct the description of products input in /manage-shop (does not take spaces)
- [x] create blog and pages from footer
- [x] If logged in, replace signup and signin with user profile

**0.0.4 patches**

- [x] added /chat functionality
- [x] Update /home orders table for farmers and elevators using SOCKET/IO

**1.0.1**

- [ ] General bug fixes
- [ ] Send email when sign-up
- [ ] Restrict to who can signup as elevator
- [ ] Save PDF when new orders
- [ ] Populate map in index page with elevators addresses

**1.0.2**

- [ ] Security check (SQL injection)
- [ ] Save who has sent messages in /chat

### API Description

The API handles all the request for adding, deliting and modifying users. The API also handles the interaction with tables in the Database.

### DATABASE TABLES

- **farmers** is the table to store all farmer users
- **elevators** is the table to store all elevator users
- **products** stores the list of products for each elevator
- **orders** all transactions
- **deleted_products** stores all deleted products
- **contact_us_messages** stores all deleted products
- **chats** contains room ids and text history

### References

[https://flask.palletsprojects.com/en/2.0.x/quickstart/#cookies](https://flask.palletsprojects.com/en/2.0.x/quickstart/#cookies)

[https://www.mongodb.com/products/shell](https://www.mongodb.com/products/shell)

[https://flask-socketio.readthedocs.io/en/latest/getting_started.html](https://flask-socketio.readthedocs.io/en/latest/getting_started.html)

[https://pythonhosted.org/Flask-Mail/](https://pythonhosted.org/Flask-Mail/)
