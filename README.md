# userFlask

- [ ] need to fix password hashing
- [ ] add css design library

users.db file is not included
It can be created by writing the following sqlite3 code:
```
CREATE TABLE 'users' (
'username' VARCHAR(255) PRIMARY KEY,
'name' VARCHAR(255),
'email' VARCHAR(255),
'password' INTEGER
);
```
