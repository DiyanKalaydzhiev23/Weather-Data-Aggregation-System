# Project Setup Instructions

## Prerequisites

To run this project, you will need:

- Python 3.10+
- [Poetry](https://python-poetry.org/docs/) for dependency management.
- PostgreSQL for the database.

## Setup Guide

### Step 1: Clone the Repository

First, clone the repository to your local machine:

```sh
git clone <repository-url>
cd <repository-directory>
```

### Step 2: Configure Environment Variables

You need to set up the environment variables to run the project. 
A `.env.template` file is included in the repository to guide you.

1. Copy the `.env.template` file:
    ```sh
    cp .env.template .env
    ```

2. Edit the `.env` file and fill in the required values, such as:
   - `SECRET_KEY`: A secret key for Django.
   - Database connection settings (`DB_NAME`, `DB_USER`, `DB_PASSWORD`, etc.).
   - `DEBUG`: Set to True for development, False for production.
   - `ALLOWED_HOSTS`: Add your allowed hosts, separated by commas.


### Step 3: Install Dependencies

Use Poetry to install the project dependencies:
```sh
poetry install
```

### Step 4: Set Up the Database

Ensure `PostgreSQL` is running and set up your database using the credentials provided in the `.env `file.

Next, run the following commands to apply database migrations:
```sh
poetry run python manage.py migrate
```


### Step 5: Create a Superuser
To access the admin panel or Swagger documentation, create a superuser account:

```sh
  poetry run python manage.py createsuperuser
```

Follow the prompts to set up the superuser credentials.

### Step 6: Run the Development Server
Run the server with the following command:

```shell
poetry run python manage.py runserver
```

By default, the server runs on http://127.0.0.1:8000/.


### Step 7: Access API Documentation
The project uses **DRF Spectacular** for Swagger documentation.
  - You can access the API documentation at http://127.0.0.1:8000/api/docs/.
  - Note: Only superusers are allowed to access the documentation.

---

### Running Tests
Tests are located in the `tests/` directory.

To run the tests:
```shell
poetry run python manage.py test
```

---

#### Next Page: [Add Station (Tutorial)](./add_station_tutorial.md)

---

<div style="display: flex">
  <a href="../README.md">
    <svg width="20" height="20" fill="blue" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" fill="#000000" version="1.1" id="Capa_1" width="800px" height="800px" viewBox="0 0 495.398 495.398" xml:space="preserve">
    <g>
        <g>
            <g>
                <path d="M487.083,225.514l-75.08-75.08V63.704c0-15.682-12.708-28.391-28.413-28.391c-15.669,0-28.377,12.709-28.377,28.391     v29.941L299.31,37.74c-27.639-27.624-75.694-27.575-103.27,0.05L8.312,225.514c-11.082,11.104-11.082,29.071,0,40.158     c11.087,11.101,29.089,11.101,40.172,0l187.71-187.729c6.115-6.083,16.893-6.083,22.976-0.018l187.742,187.747     c5.567,5.551,12.825,8.312,20.081,8.312c7.271,0,14.541-2.764,20.091-8.312C498.17,254.586,498.17,236.619,487.083,225.514z"/>
                <path d="M257.561,131.836c-5.454-5.451-14.285-5.451-19.723,0L72.712,296.913c-2.607,2.606-4.085,6.164-4.085,9.877v120.401     c0,28.253,22.908,51.16,51.16,51.16h81.754v-126.61h92.299v126.61h81.755c28.251,0,51.159-22.907,51.159-51.159V306.79     c0-3.713-1.465-7.271-4.085-9.877L257.561,131.836z"/>
            </g>
        </g>
    </g>
    </svg>
  </a>
 <a style="margin-left: 10px" href="../README.md">Home</a>
</div>


---