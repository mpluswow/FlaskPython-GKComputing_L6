import mysql.connector

# Function to create database and tables
def create_database():
    # Connect to MySQL database
    conn = mysql.connector.connect(
        host='localhost',
        port='3306',
        user='root',
        password='kulka34'
    )
    cursor = conn.cursor()

    # Create the database if it doesn't exist
    cursor.execute("CREATE DATABASE IF NOT EXISTS website")

    # Switch to the created database
    cursor.execute("USE website")

    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(100) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password_hash VARCHAR(128) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create user_profiles table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_profiles (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            full_name VARCHAR(100),
            age INT,
            town VARCHAR(100),
            hobby VARCHAR(100),
            bio TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    # Commit changes and close connection
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_database()
    print("Database and tables created successfully!")
