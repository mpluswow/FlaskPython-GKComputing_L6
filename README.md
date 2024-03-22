# My Flask App

My Flask App is a web application built using Flask, a lightweight WSGI web application framework. It provides a simple interface for managing user accounts and accessing various pages.

## Features

- User account management: Allows users to create, login, and logout of their accounts.
- Profile management: Users can update their profiles with information such as full name, age, town, hobby, and bio.
- Page title management: Provides endpoints to fetch page titles dynamically based on their IDs.
- HTTPS support: Enforces HTTPS using SSLify for enhanced security.

## Installation

Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

Configure the app:

    - Create a `config.py` file based on the provided `config.example.py` and fill in the necessary configurations.
    - Generate SSL certificates and update the configuration accordingly.

Run the app:

    ```bash
    python app.py
    ```

## Usage

- Access the home page at [https://localhost:443/](https://localhost:443/).


## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.


