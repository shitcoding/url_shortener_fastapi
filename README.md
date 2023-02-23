# FastAPI URL Shortener

A simple URL shortener application built with FastAPI and SQLAlchemy.

## Installation

#### 1. Clone the repository
```sh
$ git clone https://github.com/[YOUR_GITHUB_USERNAME]/fastapi-url-shortener.git
```

#### 2. Change into the project directory
```sh
$ cd fastapi-url-shortener
```

#### 3. Install dependencies using Poetry
```sh
$ poetry install
```

#### 4. Set environment variables

1. Make a copy of the `.env.example` file and rename it to `.env`
2. Open the newly created `.env` file in a text editor.
3. Replace the placeholder values in the `.env` file with your own desired values.
4. Save the changes to the `.env` file.

It is important to note that the values in the `.env` file should not be shared publicly, as they may contain sensitive information such as secret keys.

#### 5. Run the app

```sh
$ poetry run uvicorn main:app --reload
```

You can now access the app at http://localhost:8000 (or hostname that you specified in `.env` file)


## Usage

The following endpoints are available:

- `POST /url`: Create a new shortened URL.
- `GET /{url_key}`: Redirect to the target URL for the specified shortened URL key.
- `GET /admin/{secret_key}`: Get information about the specified shortened URL.
- `DELETE /admin/{secret_key}`: Delete the specified shortened URL.

