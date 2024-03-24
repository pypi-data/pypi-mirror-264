# DbUnify | Database Management

**DbUnify** (Database Management) is a versatile Python library that simplifies database connectivity and management using SQLite.

## Installation
   Install the DbUnify library from PyPI or GitHub.
   
   ```bash
   pip install DbUnify
   ```
   
   or
   
   ```bash
   git clone https://github.com/Sepehr0Day/DbUnify.git
   ```
## Connect To Database
```python
import DbUnify.sync as sync

# Initialize a database manager with the name 'database.db'
db_manager = sync.Manager('database.db')

   ```

## Create Table
```python
import DbUnify.sync as sync

# Create a table named 'employees' with specified columns
db_manager.create_table('employees', [
    ('id', 'INTEGER PRIMARY KEY'), 
    ('name', 'TEXT'),
    ('age', 'INTEGER'),
    ('department', 'TEXT')
    ])


   ```


## Documentation DbUnify:

   For more information and advanced usage, refer to the [DbUnify documentation](https://Sepehr0day.github.io/DbUnify.html).

  
## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/Sepehr0Day/DbUnify/blob/main/LICENSE) file for details.

<a href="https://pypi.org/project/DbUnify/"><img src="https://img.shields.io/badge/DbUnify-1.5-blue"></a> 

## Developer
- **Telegram**: [t.me/Sepehr0Day](https://t.me/Sepehr0Day)

---

*Your Database Management DbUnify, made easy with DbUnify.*
