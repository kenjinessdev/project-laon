
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


## 🚫 Rate Limiting

| Endpoint                 | Limit          |
|--------------------------|----------------|
| `/auth/login`            | 5 requests/min |
| `/auth/register`         | 5 requests/min |
| `/auth/google/callback`  | 10 requests/min |

