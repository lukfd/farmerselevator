# Farmers Elevator
### Version 0.0.1
**started on may 2021 - end september 2021**
for different system structure


*Authors: Luca and Daniel*

An application for grain elevators ([Grain elevator - Wikipedia](https://en.wikipedia.org/wiki/Grain_elevator)) for giving them their own website and ecommerce to sell food for livestock to farmers.

The problem specifically arises today because farmers would need to call the elevator several times to complete an order. The order would take even longer in case it has been placed during the weekend.

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

- [ ] Correct the address in /settings (does not take spaces)

- [ ] Correct the description of products input in /manage-shop (does not take spaces)

- [ ] Update /home orders table for farmers and elevators using SOCKET/IO

- [ ] Add payment and send email when sending the new order

- [ ] Correct user_id and product_id generation

- [ ] If logged in, replace signup and signin with user profile

- [ ] SQL injection threats

- [ ] stay consistant with variables in the code

- [ ] creating functions for redundancy in the code

- [ ] have homepage search bar working

- [ ] in homepage make a map for searching elevators

- [ ] finish contact-page: send email to us, blogging for developers

- [ ] create live chat messages tools

- [ ] Better css for internal pages

- [ ] Fix css for populating results in search bar, offset to the right (index.js)



Completed:

- [x] Populate /shop tables and the buy functionality

- [x] test /delete-account

- [x] test change password

- [x] uploading profile pictures

- [x] Finish Settings (changing row by sending variables)

- [x] Finish /profile

- [x] Password hasing



Future goals:

- 



### API Description

The API handles all the request for adding, deliting and modifying users. The API also handles the interaction with tables in the Database.

### DATABASE TABLES

- **farmers** is the table to store all farmer users
- **elevators** is the table to store all elevator users
- **products** stores the list of products for each elevator
- **orders stores** all transactions
- **deleted_products** stores all deleted products

### References

[https://flask.palletsprojects.com/en/2.0.x/quickstart/#cookies](https://flask.palletsprojects.com/en/2.0.x/quickstart/#cookies)

[https://www.mongodb.com/products/shell](https://www.mongodb.com/products/shell)

[https://flask-socketio.readthedocs.io/en/latest/getting_started.html](https://flask-socketio.readthedocs.io/en/latest/getting_started.html)

### AWS deployment

https://www.youtube.com/watch?v=dhHOzye-Rms
