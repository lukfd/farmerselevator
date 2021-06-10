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

### To Do

Now:

- [ ] Finish Settings (changing row by sending variables)

- [ ] Create tables for Shop and Orders

- [ ] test /delete-account

- [ ] test change password

- [ ] shopping functionality (updating /home and /manage-shop when click buy)

- [ ] uploading profile pictures

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
