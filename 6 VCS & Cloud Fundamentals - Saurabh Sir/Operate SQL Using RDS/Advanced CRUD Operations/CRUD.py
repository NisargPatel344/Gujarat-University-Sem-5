import mysql.connector

# Establish a connection to the MySQL database
mydb = mysql.connector.connect(
    host="database-2.ctifqxiyrkpp.eu-north-1.rds.amazonaws.com",
    user="admin",
    password="11111111"
)

# Create a cursor to execute SQL queries
mycursor = mydb.cursor()

# Initialize empty attributes list and table_name
attributes = []  
table_name = ""

# Execute a query to show available databases
mycursor.execute("SHOW DATABASES")
databases = [db[0] for db in mycursor.fetchall()]

# Function to create a new record
def create_record():
    if not attributes:
        print("No attributes defined. Please select or create a table first.")
        return
    values = []
    placeholders = []
    for attribute in attributes:
        if attribute[0] == 'id':
            continue
        value = input(f"Enter {attribute[0]}: ")
        values.append(value)
        placeholders.append("%s")
    insert_query = f"INSERT INTO {table_name} ("
    insert_query += ", ".join([attribute[0] for attribute in attributes if attribute[0] != 'id'])
    insert_query += ") VALUES ("
    insert_query += ", ".join(placeholders)
    insert_query += ")"
    try:
        mycursor.execute(insert_query, values)
        mydb.commit()
        print("\nRecord created successfully\n")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Function to read all records
def read_records():
    mycursor.execute(f"SELECT * FROM {table_name}")
    records = mycursor.fetchall()
    if not records:
        print("No records found")
    else:
        for record in records:
            print(record)

# Function to update a record
def update_record():
    if not attributes:
        print("No attributes defined. Please select or create a table first.")
        return
    record_id = input("Enter the ID of the record you want to update: ")
    values = []
    for attribute in attributes:
        value = input(f"Enter new {attribute[0]}: ")
        values.append(value)
    update_query = f"UPDATE {table_name} SET "
    update_query += ", ".join([f"{attribute[0]} = %s" for attribute in attributes])
    update_query += " WHERE id = %s"  # Assuming the primary key is 'id'
    values.append(record_id)
    try:
        mycursor.execute(update_query, values)
        mydb.commit()
        print("\nRecord updated successfully\n")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Function to delete a record
def delete_record():
    if not attributes:
        print("No attributes defined. Please select or create a table first.")
        return
    record_id = input("Enter the ID of the record you want to delete: ")
    delete_query = f"DELETE FROM {table_name} WHERE id = %s"  # Assuming the primary key is 'id'
    try:
        mycursor.execute(delete_query, (record_id,))
        mydb.commit()
        print("\nRecord deleted successfully\n")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

print("Options:")
print("1. Create a new database")
print("2. Select an existing database")
choice = input("Enter your choice (1/2): ")

if choice == "1":
    # Create a new database
    database_name = input("Enter the database name: ")
    mycursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
    mycursor.execute(f"USE {database_name}")
    table_name = input("Enter the table name (not a reserved keyword): ")
    attributes = []
    while True:
        attribute_name = input("Enter an attribute name (or 'done' to finish): ")
        if attribute_name.lower() == 'done':
            break
        attribute_datatype = input(f"Enter the datatype for {attribute_name}: ")
        attribute_length = input(f"Enter the length for {attribute_name} (or 'max' for maximum length): ")
        attributes.append((attribute_name, attribute_datatype, attribute_length))
    create_table_query = f"CREATE TABLE IF NOT EXISTS `{table_name}` ("
    create_table_query += f"id INT AUTO_INCREMENT PRIMARY KEY, "
    for attribute in attributes:
        attribute_name, attribute_datatype, attribute_length = attribute
        if attribute_length.lower() == 'max':
            create_table_query += f"`{attribute_name}` {attribute_datatype}, "
        else:
            create_table_query += f"`{attribute_name}` {attribute_datatype}({attribute_length}), "
    create_table_query = create_table_query[:-2] + ")"
    mycursor.execute(create_table_query)

elif choice == "2":
    # Select an existing database
    print("Available Databases:")
    for db in databases:
        print(f"- {db}")
    selected_database = input("Enter the existing database name: ")
    if selected_database in databases:
        mycursor.execute(f"USE {selected_database}")
        mycursor.execute(f"SHOW TABLES IN {selected_database}")
        tables = [table[0] for table in mycursor.fetchall()]
        if tables:
            print(f"Tables in {selected_database}:")
            for table in tables:
                print(f"- {table}")
            table_name = input("Enter the existing table name: ")
            mycursor.execute(f"DESCRIBE `{table_name}`")
            table_attributes = mycursor.fetchall()
            attributes = [(attr[0], attr[1]) for attr in table_attributes]
            
            # Check if the 'id' column is in the attributes list and remove it
            attributes = [attr for attr in attributes if attr[0] != 'id']
        else:
            print(f"No tables found in {selected_database}. You can create a new table.")
            table_name = input("Enter the table name: ")
    else:
        print("Database not found. You can create a new database.")
        database_name = input("Enter the database name: ")


while True:
    print("\nCRUD Operations:")
    print("1. Create a new record")
    print("2. Read all records")
    print("3. Update a record")
    print("4. Delete a record")
    print("5. Quit\n")
    choice = input("Enter your choice (1/2/3/4/5):")
    if choice == "1":
        create_record()
    elif choice == "2":
        read_records()
    elif choice == "3":
        update_record()
    elif choice == "4":
        delete_record()
    elif choice == "5":
        break
    else:
        print("Invalid choice. Please enter a valid option.")

# Close the database connection
mydb.close()