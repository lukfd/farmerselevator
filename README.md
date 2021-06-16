# Farmers Elevator

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

- [ ] Update /home orders table for farmers and elevators

- [ ] Finish /manage-shop (add delete row and modify exisiting products)

- [ ] Populate /shop tables and the buy functionality

- [ ] Make a clever way for user_id and product_id

- [x] test /delete-account

- [x] test change password

- [x] uploading profile pictures

- [x] Finish Settings (changing row by sending variables)

- [x] Finish /profile

Future:

- [x] Password hasing

- [ ] SQL injection threats

- [ ] Generate better ID for farmers and elevators

- [ ] stay consistant with variables

- [ ] creating functions for redundant code

- [ ] Style

- [ ] In homepage have a search bar for searching elevator's shop

### References

[https://flask.palletsprojects.com/en/2.0.x/quickstart/#cookies](https://flask.palletsprojects.com/en/2.0.x/quickstart/#cookies)

[https://www.mongodb.com/products/shell](https://www.mongodb.com/products/shell)

[https://flask-socketio.readthedocs.io/en/latest/getting_started.html](https://flask-socketio.readthedocs.io/en/latest/getting_started.html)
