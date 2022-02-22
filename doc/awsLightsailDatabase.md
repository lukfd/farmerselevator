# AWS Lightsail database

## Tables

## Users

## How to connect

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
| password        | varchar(50)                       |
| username        | varchar(20)                       |
| phone           | int                               |
| website         | varchar(50)                       |
| shop_url        | varchar(50)                       |
| address         | text                              |
| profile_image   | blob                              |
| status          | boolean                           |

**farmers**
| Column        | Description                         |
| ------------- | ----------------------------------- |
| name          | varchar(20)                         |
| lastname      | varchar(20)                         |
| username      | varchar(20)                         |
| email         | varchar(255)                        |
| password      | varchar(50)                         |
| profile_image | blob                                |
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