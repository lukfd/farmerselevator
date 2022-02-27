# AWS Lightsail database

This is a guide for creating an AWS lightsail 's database.

## Tables

We are going to create these tables
- chats
- elevators 
- products   
- contact_us_messages  
- farmers            
- deleted_products     
- orders

## Users

| User | Password |
| ---- | -------- |
| root | root     |

## How to connect

#### In our flask

#### to AWS lightsail

#### /constants.py

## Before version 1.0.1 - sqlite with base.db
We have started with base.db: a sqlite3 database.

Tables that we have used were:

**chats** stores messages
| Column      | Description |
| ----------- | ----------- |
| room_id     | varchar     |
| farmer_id   | int         |
| elevator_id | int         |
| messages    | text        |

**contact_us_messages**
| Column        | Description                  |
| ------------- | ---------------------------- |
| id            | integer not null primary key |
| message_title | text                         |
| sender_email  | varchar(255)                 |
| message_text  | text                         |
| date          | date                         |

**deleted_products**
| Column             | Description  |
| ------------------ | ------------ |
| elevator_id        | int          |
| name               | text         |
| product_id         | int          |
| quantity_available | int          |
| measure            | varchar(255) |
| price              | int          |
| description        | text         |

**elevators**
| Column          | Description                       |
| --------------- | --------------------------------- |
| name            | varchar(40)                       |
| elevator_id     | integer primary key autoincrement |
| primary_contact | text                              |
| email           | varchar(255)                      |
| password        | char(60)                          |
| username        | varchar(20)                       |
| phone           | int                               |
| website         | varchar(50)                       |
| shop_url        | varchar(50)                       |
| address         | text                              |
| profile_image   | varch                             |
| status          | boolean                           |

**farmers**
| Column        | Description                         |
| ------------- | ----------------------------------- |
| name          | varchar(20)                         |
| lastname      | varchar(20)                         |
| username      | varchar(20)                         |
| email         | varchar(255)                        |
| password      | char(60)                            |
| profile_image | varchar                             |
| farmer_id     | integer primary  key  autoincrement |
| address       | text                                |
| phone         | int                                 |
| status        | boolean                             |

**orders**
| Column         | Description                       |
| -------------- | --------------------------------- |
| order_id       | integer primary key autoincrement |
| farmer_id      | int                               |
| elevator_id    | int                               |
| date           | date                              |
| status         | varchar(255)                      |
| product_id     | int                               |
| quantity_int   | int                               |
| quantity_type  | varchar(50)                       |
| description    | text                              |
| completed_date | date                              |
| payment        | varchar(255)                      |
| product_name   | text                              |

**products**
| Column             | Description                       |
| ------------------ | --------------------------------- |
| elevator_id        | int                               |
| name               | text                              |
| product_id         | integer primary key autoincrement |
| quantity_available | int                               |
| measure            | varchar(255)                      |
| price              | int                               |
| description        | text                              |


## References

- [pymysql commands](https://pymysql.readthedocs.io/en/latest/modules/cursors.html)
- [flask-mysql home page](https://flask-mysql.readthedocs.io/en/stable/#configuration)
- [flask-mysql source code](https://github.com/cyberdelia/flask-mysql/blob/master/flaskext/mysql.py)