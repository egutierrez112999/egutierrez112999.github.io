# Documentation

## Resources
**Adoption Centers**
### Attributes
- name (string)
- location (string)
- rating (integer)
- url (string)
- selection (string)

**Users**
### Attributes
- email (string)
- encrypted password (string)
- first name (string)
- last name (string)


## Database Schema

### Adoption Centers
```sql
CREATE TABLE adoptionscenters 
(id INTEGER PRIMARY KEY, 
name TEXT, 
location TEXT, 
rating INTEGER, 
url TEXT, 
selection TEXT);
```
### Users
```sql
CREATE TABLE users 
(id INTEGER PRIMARY KEY, 
email TEXT, 
epasswd TEXT, 
firstname TEXT, 
lastname TEXT);
```


## REST Endpoints


| Name | HTTP Method | Path |
| --- | --- | --- |
| Retrieve Adoption Centers | GET | /adoptioncenters |
| Retrieve Adoption Centers Member | GET | /adoptioncenters/*\<id\>* |
| Create Adoption Centers Member | POST | /adoptioncenters |
| Delete Adoption Centers Member | DELETE | /adoptioncenters/*\<id\>* |
| Update Adoption Centers Member | UPDATE | /adoptioncenters/ *\<id\>* |
| Create Users Member | POST | /users |
| Create Sessions Member | POST | /sessions |


#### BCrypt was used to encrypt and verify all passwords
