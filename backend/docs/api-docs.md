
# 📘 LAON API Documentation

## 🌐 Base URL

```
http://localhost:8000/api/v1
```

---

## 🧑‍💻 Authentication

> Authentication is based on this youtube video:
<iframe width="560" height="315" src="https://www.youtube.com/embed/AcYF18oGn6Y" frameborder="0" allowfullscreen></iframe>

### 🔐 Google Login

- **GET** `/auth/google`  
  Redirects to Google OAuth for login.

### 🔁 Google Callback

- **GET** `/auth/google/callback`  
  Handles the callback from Google after user authentication.

---

### 📝 Register

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

### 🔑 Login

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

### ♻️ Refresh Token

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

## 📊 Dashboards

### 👨‍🌾 Farmer Dashboard

- **GET** `/farmer/dashboard`  
  Secured route. Requires Bearer Token.

**Headers**:
```
Authorization: Bearer <access_token>
```

---

### 👤 Customer Dashboard

- **GET** `/customer/dashboard`  
  Secured route. Requires Bearer Token.

**Headers**:
```
Authorization: Bearer <access_token>
```

---

## 🙋 Get Current User

### 👁️ Me

- **GET** `/users/me`  
  Returns info about the currently authenticated user.

**Headers**:
```
Authorization: Bearer <access_token>
```

---

## 🏠 Root

- **GET** `/`  
  Base root endpoint. (Can be used for health checks or welcome messages.)

---

## 🚫 Rate Limiting

| Endpoint                 | Limit          |
|--------------------------|----------------|
| `/auth/login`            | 5 requests/min |
| `/auth/register`         | 5 requests/min |
| `/auth/google/callback`  | 10 requests/min |

