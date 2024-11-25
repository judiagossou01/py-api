# PY-API v1.0.0

## Introduction

An open-source mini project api coding in native Python3 to test and build projects

## Usage

- Create a `.env` file in the `src` of your project and insert
your key/value pairs in the following format :

```sh
[DATABASE]
DATABASE_URL=mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:3306/{DB_NAME}

[LOGGING]
APP_LOG_FILE=choose-your-path
SQLALCHEMY_LOG_FILE=choose-your-path

[ENVIRONMENT]
APP_ENV=""
```

- Define the paths for the application log file (`APP_LOG_FILE`) and the SQLAlchemy 
log file (`SQLALCHEMY_LOG_FILE`) by replacing choose-your-path with your desired locations.

- Assign the default value `"locale"` to the `APP_ENV` variable in the `[ENVIRONMENT]` section of the `.env` file.

## API Endpoints

- `POST` **`/sessions/register`**

	> This route allows a new user to register

	##### Parameters

	| name | type | data type | description |
	|-----------|-----------|-------------------------|-----------------------------------------------------------------------|
	| firstname | required | string | firstname |
	| lastname | required | string | lastname |
	| email | required | string | email |
	| password | required | string | password |

	##### Responses

	| http code | content-type | response |
	|---------------|-----------------------------------|-----------------------------------------------------------------------|
	| `201` | `application/json` | `{"status":"201", "message":"User created successfully"}` |
	| `400` | `application/json` | `{"status":"401", "message":"Bad Request"}` |
	| `409` | `application/json` | `{"status":"409", "message":"Email already exists"}` |

- `POST` **`/sessions/login`**

	> This route allows users to log in with their email address and password

	##### Parameters

	| name | type | data type | description |
	|-----------|-----------|-------------------------|-----------------------------------------------------------------------|
	| email | required | string | email |
	| password | required | string | password |

	##### Response
	| http code | content-type | response |
	|---------------|-----------------------------------|----------------------------------------------------------------------------|
	| `200` | `application/json` | `{"status":"200", "user":"USER_DATA_HERE", "token":"TOKEN_HERE"}` |
	| `401` | `application/json` | `{"status":"401", "message":"Incorrect password"}` |
	| `404` | `application/json` | `{"status":"500", "message":"User not found"}` |

- `GET` **`/sessions/me`**

	> This route retrieves the user's session data

	##### Parameters

	No parameters

	##### Response
	| http code | content-type | response |
	|---------------|-----------------------------------|----------------------------------------------------------------------------|
	| `200` | `application/json` | `{"status":"200", "user":"USER_DATA_HERE"}` |
	| `401` | `application/json` | `{"status":"401", "message":"Token is missing or invalid"}` |
	| `401` | `application/json` | `{"status":"401", "message":"Token is invalid or expired"}` |

- `GET` **`/sessions/logout`**

	> This route disconnects the user from his current session

	##### Parameters

	No parameters

	##### Response
	| http code | content-type | response |
	|---------------|-----------------------------------|----------------------------------------------------------------------------|
	| `200` | `application/json` | `{"status":"200", "message":"User logged out successfully"}` |
	| `401` | `application/json` | `{"status":"401", "message":"Token is missing or invalid"}` |
	| `401` | `application/json` | `{"status":"401", "message":"Token is invalid or expired"}` |
