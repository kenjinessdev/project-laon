
# 📘 LAON API Documentation

##  Base URL

```
http://localhost:8000/api/v1
```

---

## 🧑‍💻 Authentication

> Authentication is based on this youtube video: [Watch](https://youtu.be/AcYF18oGn6Y)
[![Watch the video](https://img.youtube.com/vi/AcYF18oGn6Y/maxresdefault.jpg)](https://youtu.be/AcYF18oGn6Y)


### Google Login

- **GET** `/auth/google`  
  Redirects to Google OAuth for login.
  - Register user as a `customer` in default
  - `/auth/google?role=farmer` to specify the role of the user

### Google Callback

- **GET** `/auth/google/callback`  
  Handles the callback from Google after user authentication.

---

### Facebook Login
- **GET** `/auth/facebook`
  Redirects to Facebook OAuth for login
  - Register user as a `customer` in default
  - `/auth/facebook?role=farmer` to specify the role of the user

- **GET** `/auth/google/callback`  
  Handles the callback from Google after user authentication.

---

### Register

- **POST** `/auth/register`  
  Registers a new user.

**Request Body**:
```json
{
  "first_name": "string",
  "middle_name": "string",
  "last_name": "string",
  "suffix": "string",
  "profile_image_url": "string",
  "email": "user@example.com",
  "password": "securePassword",
  "phone_number": "string",
  "gender": "male",
  "birthday": "1990-01-01",
  "role": "farmer"
}
```

**Response**:
- `200 OK` with user data.
- `400 Bad Request` if email is already registered.

---

### Login

- **POST** `/auth/login`  
  Authenticates a user and returns an access token. Also sets a `refresh_token` in HttpOnly cookie.

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securePassword"
}
```

**Response**:
```json
{
  "access_token": "string",
  "token_type": "bearer"
}
```

---

### Refresh Token

- **POST** `/auth/refresh`  
  Issues a new access token using the refresh token from an HttpOnly cookie.

**Response**:
```json
{
  "access_token": "string",
  "token_type": "bearer"
}
```

---

## Dashboards

### Farmer Dashboard

- **GET** `/farmer/dashboard`  
  Secured route. Requires Bearer Token.

**Headers**:
```
Authorization: Bearer <access_token>
```

---

### Customer Dashboard

- **GET** `/customer/dashboard`  
  Secured route. Requires Bearer Token.

**Headers**:
```
Authorization: Bearer <access_token>
```

---

## Get Current User

### Me

- **GET** `/users/me`  
  Returns info about the currently authenticated user.



**Headers**:
```
Authorization: Bearer <access_token>
```

### Update User Info

- **PUT** `/users/me`
  Updates user info
  Returns 400 error if email or phone number is already existing in db

  - Requires Header
  `Authorization: Bearer <access_token>`


## 🔐 Change Password

**PUT** `/users/me/password`

Allows an authenticated user to change their password by providing the current and new passwords.

### Requires
`Authorization: Bearer <access_token>`

### 📥 Request Body
```json
{
  "current_password": "oldPassword123",
  "new_password": "newPassword456"
}


# Error Response format

## Validation error response body
```json
{
    "detail": "Validation failed",
    "missing_fields": [
        "street"
    ],
    "format_errors": [
        {
            "field": "postal_code",
            "message": "String should match pattern '^\\d{4,5}(-\\d{4})?$'"
        }
    ],
    "other_errors": null
}
```

# Farmer Side EndPoints

## Create Product

**POST** `/farmer/product`

*Request Body:*

```json
{
  "name": "farmerssss",
  "description": "string",
  "category_id": null, // wala pa nako ni na implement
  "unit": "string",
  "visibility": "public",
  "status": "active",
  "price_per_unit": 0,
  "stock_quantity": 0
}

```

*Response Body*

```json
{
    "name": "product name wowow",
    "description": "product description",
    "category_id": null,
    "unit": "string",
    "price_per_unit": 0.0,
    "stock_quantity": 0,
    "status": "active",
    "visibility": "public",
    "user": null,
    "images": null,
    "reviews": null,
    "id": "33799f89-9ac0-428e-9bdf-2e4d0d990268",
    "user_id": "57885b9c-f6a4-4a1c-b61b-b8986f3a5b9a"
}

```
## Show farmer products


**GET** `/farmer/products`

- NOTE: products not product
mas mag makes sense man pag plural sa get

*Response Body*

```json
[
    {
        "name": "farmer 2 product",
        "description": "string",
        "category_id": null,
        "unit": "string",
        "price_per_unit": 0.0,
        "stock_quantity": 0,
        "status": "active",
        "visibility": "public",
        "user": null,
        "images": null,
        "reviews": null,
        "id": "787931a7-f361-4392-95e2-3f9f561dd3b5",
        "user_id": "2ffc9b1d-769d-40f2-b6cd-733ee214b9b3"
    },
    {
        "name": "farmer 2.2 product",
        "description": "string",
        "category_id": null,
        "unit": "string",
        "price_per_unit": 0.0,
        "stock_quantity": 0,
        "status": "active",
        "visibility": "public",
        "user": null,
        "images": null,
        "reviews": null,
        "id": "caa92f41-db5a-4707-955a-05fd33b42745",
        "user_id": "2ffc9b1d-769d-40f2-b6cd-733ee214b9b3"
    }
]
```

## Product update

**PUT** `/farmer/product/{product_id}`

*Request Body*
```json
{
    "name": "shibal",
    "description": "string",
    "category_id": null,
    "unit": "string",
    "price_per_unit": 0,
    "stock_quantity": 0,
    "status": "active",
    "visibility": "public"
}
```
You are not required to enter all fields, just put the fields you want to edit
```json
{
    "name": "shibal",
}
```

*Response Body*

```json
{
    "name": "farmer 2 tangina mo",
    "description": "string",
    "category_id": null,
    "unit": "string",
    "price_per_unit": 0.0,
    "stock_quantity": 0,
    "status": "active",
    "visibility": "public",
    "user": null,
    "images": null,
    "reviews": null,
    "id": "caa92f41-db5a-4707-955a-05fd33b42745",
    "user_id": "2ffc9b1d-769d-40f2-b6cd-733ee214b9b3"
}
```

## Delete Product

**DELETE** `/farmer/product/{product_id}`

*Success Response*
```json
{
    "detail": "Product deleted successfully"
}
```

*Failed Response*
```json
{
    "detail": "Product not found"
}
```


