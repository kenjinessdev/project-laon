
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

# Customer endpoints

# CART

## Add to Cart

**POST** `/customer/add-to-cart` - creates a cart entry if no cart is active, and adds the item specified in the payload

Request Body:

```json
{
  "product_id": "string",
  "quantity": 1
}
```

### Success Response
```json
{
  "is_active": true,
  "id": "string",
  "customer_id": "string",
  "created_at": "2025-07-28T08:50:25.526Z",
  "updated_at": "2025-07-28T08:50:25.526Z",
  "customer": {
    "first_name": "string",
    "middle_name": "string",
    "last_name": "string",
    "suffix": "string",
    "profile_image_url": "string",
    "email": "user@example.com",
    "password": "string",
    "phone_number": "string",
    "gender": "string",
    "birthday": "2025-07-28",
    "role": "farmer",
    "id": "string",
    "created_at": "2025-07-28T08:50:25.526Z",
    "addresses": []
  },
  "cart_items": []
}
```

### Error
```json
{
  "detail": "Product not found"
}
```

## Update item quantity

**PATCH** `/customer/cart-items/{item_id}/quantity`

Request Body:

```json
{
  "quantity": 1
}

```
Response Body:

### Success

```json
{
    "id": "adce69ce-8eac-4d85-baff-c637abc28146",
    "cart_id": "915f0532-3675-4647-b3c6-ec8016f79438",
    "product_id": "88e54f80-8fac-445e-bf3e-3d668e984fea",
    "quantity": 2,
    "added_at": "2025-07-29T01:06:07.790000Z",
    "cart": null,
    "product": null
}
```

### Error

```json
{
  "detail": "Cart item not found"
}
```
## Delete cart item

**DELETE** `/customer/cart-items/{item_id}/delete`

Response Body:

### Success

```json
{
  "message": "Cart item deleted successfully"
}
```

### Error
```json
{
  "detail": "Cart item not found"
}
```
```json
{
    "detail": "Validation failed",
    "missing_fields": null,
    "format_errors": [
        {
            "field": "item_id",
            "message": "Input should be a valid UUID, invalid length: expected length 32 for simple format, found 5"
        }
    ],
    "other_errors": null
}
```
## Show the user's active cart

**GET** `/customer/cart`

Response:

### Success

```json
{
    "Message": "Active cart found",
    "cart_items_count": 1,
    "cart": {
        "id": "915f0532-3675-4647-b3c6-ec8016f79438",
        "customer_id": "f3645743-c02d-446a-953d-275150a87aca",
        "created_at": "2025-07-29T01:06:06.733000Z",
        "updated_at": "2025-07-29T01:06:06.733000Z",
        "is_active": true,
        "customer": null,
        "cart_items": [
            {
                "id": "da3bf2ba-41a3-40ed-a7b6-f7ca10a30dcd",
                "cart_id": "915f0532-3675-4647-b3c6-ec8016f79438",
                "product_id": "88e54f80-8fac-445e-bf3e-3d668e984fea",
                "quantity": 1,
                "added_at": "2025-07-29T02:12:28.091000Z",
                "cart": null,
                "product": {
                    "id": "88e54f80-8fac-445e-bf3e-3d668e984fea",
                    "user_id": "1d016f98-2ade-4f04-a356-0750392351b5",
                    "name": "apple",
                    "description": "wow",
                    "category_id": null,
                    "unit": "kg",
                    "status": "active",
                    "visibility": "public",
                    "price_per_unit": "100",
                    "stock_quantity": 100,
                    "updated_at": "2025-07-28T02:42:53.205000Z",
                    "created_at": "2025-07-28T02:42:53.205000Z",
                    "user": null,
                    "category": null,
                    "images": [],
                    "reviews": null,
                    "cart_items": null,
                    "order_item": null
                }
            }
        ]
    }
}
```

### Error

```json
{
  "message": "No active cart found"
}
```

## Checkout

**POST** `/customer/checkout`

- transfers the items in the cart to customer_orders
- wla pa na include diri ang mga payments

## Get Order

**GET** `/customer/orders/{order_id}`

Response:
```json
{
    "message": "Order found",
    "order": {
        "id": "e3a99aeb-d1f8-49e6-afba-dc8143b43f08",
        "customer_id": "f3645743-c02d-446a-953d-275150a87aca",
        "total_price": "200",
        "status": "pending",
        "updated_at": "2025-07-29T05:07:59.439000Z",
        "created_at": "2025-07-29T05:07:59.439000Z",
        "customer": {
            "id": "f3645743-c02d-446a-953d-275150a87aca",
            "first_name": "customer",
            "middle_name": "customer",
            "last_name": "customer",
            "suffix": "string",
            "profile_image_url": "string",
            "email": "customer2@example.com",
            "password": "$2b$12$MI8TYhXo.zCDh9BU1i7pJOkjL.G0MbqctdvfaPWkqOzsDiGbbfnHC",
            "phone_number": "customer12312312",
            "gender": "string",
            "role": "customer",
            "birthday": "2025-07-11T00:00:00Z",
            "created_at": "2025-07-28T02:46:12.894000Z",
            "addresses": null,
            "products": null,
            "reviews": null,
            "cart": null,
            "Order": null,
            "OrderFarm": null
        },
        "farmer_order": [
            {
                "id": 6,
                "customer_order_id": "e3a99aeb-d1f8-49e6-afba-dc8143b43f08",
                "farmer_id": "1d016f98-2ade-4f04-a356-0750392351b5",
                "status": "pending",
                "subtotal": "200",
                "created_at": "2025-07-29T05:07:59.957000Z",
                "order": null,
                "farmer": null,
                "order_item": null
            }
        ],
        "order_item": [
            {
                "id": 4,
                "customer_order_id": "e3a99aeb-d1f8-49e6-afba-dc8143b43f08",
                "farmer_order_id": 6,
                "product_id": "88e54f80-8fac-445e-bf3e-3d668e984fea",
                "quantity": 2,
                "price": "100",
                "order": null,
                "product": {
                    "id": "88e54f80-8fac-445e-bf3e-3d668e984fea",
                    "user_id": "1d016f98-2ade-4f04-a356-0750392351b5",
                    "name": "apple",
                    "description": "wow",
                    "category_id": null,
                    "unit": "kg",
                    "status": "active",
                    "visibility": "public",
                    "price_per_unit": "100",
                    "stock_quantity": 100,
                    "updated_at": "2025-07-28T02:42:53.205000Z",
                    "created_at": "2025-07-28T02:42:53.205000Z",
                    "user": null,
                    "category": null,
                    "images": null,
                    "reviews": null,
                    "cart_items": null,
                    "order_item": null
                },
                "order_farm": {
                    "id": 6,
                    "customer_order_id": "e3a99aeb-d1f8-49e6-afba-dc8143b43f08",
                    "farmer_id": "1d016f98-2ade-4f04-a356-0750392351b5",
                    "status": "pending",
                    "subtotal": "200",
                    "created_at": "2025-07-29T05:07:59.957000Z",
                    "order": null,
                    "farmer": null,
                    "order_item": null
                }
            }
        ]
    }
}
```

## Cancel order

**POST** `/customer/orders/{order_id}/cancel`

Response:

```json
{
    "message": "Order cancelled successfully",
    "order": {
        "id": "e3a99aeb-d1f8-49e6-afba-dc8143b43f08",
        "customer_id": "f3645743-c02d-446a-953d-275150a87aca",
        "total_price": "200",
        "status": "cancelled",
        "updated_at": "2025-07-29T05:15:51.583000Z",
        "created_at": "2025-07-29T05:07:59.439000Z",
        "customer": null,
        "farmer_order": null,
        "order_item": null
    }
}
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

- **PATCH** `/users/me`
  Updates user info
  Returns 400 error if email or phone number is already existing in db

  - Requires Header
  `Authorization: Bearer <access_token>`


## 🔐 Change Password

**PATCH** `/users/me/password`

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
- Content-Type: multipart/form-data
- this is in form data since you are allowed to post product images

### Fields

- `name` — string

- `description` — string

- `category_id` — (nullable, optional for now)

- `unit` — string

- `visibility` — "public" or "private"

- `status` — "active" or "inactive"

- `price_per_unit` — number

- `stock_quantity` — number

- `images` — (optional) one or more image files to upload. image/jpeg or image/png file format

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
    "images": [],
    "reviews": null,
    "id": "33799f89-9ac0-428e-9bdf-2e4d0d990268",
    "user_id": "57885b9c-f6a4-4a1c-b61b-b8986f3a5b9a"
}

```
## Show farmer products


**GET** `/farmer/products`

- NOTE: products not product
mas mag makes sense man pag plural sa get

### Params

- `name` (string, optional)

  - Filter products whose names contain this value (case-insensitive).

- `status` (string, optional)

  - Filter by product status (e.g., "active", "archived", "draft", "sold").

- `visibility` (string, optional)

  - Filter by product visibility (e.g., "public", "private").

- `min_price` (decimal, optional)

  - Include only products with price_per_unit greater than or equal to this value.

- `max_price` (decimal, optional)

  - Include only products with price_per_unit less than or equal to this value.

- `skip` (int, optional, default: 0)

  - Number of products to skip. Used for pagination.

- `take` (int, optional, default: 10)

  - Number of products to return. Used for pagination.

- `order_by` (accepts name, price_per_unit, created_at, updated_at)

  - The field by which to sort the results.

- `order` (accepts asc or desc)

  - sort direction

*sample url*

`http://localhost:8000/api/v1/farmer/products?skip=0&take=10&order_by=created_at&order=desc`

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

**PATCH** `/farmer/product/{product_id}`

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

## Add Product Image

**POST** `/farmer/product/{product_id}/images`

*Request Body*
- Content-Type: multipart/form-data

### Fields

- `file` - image/jpeg or image/png file

### Success response

```json
{
    "detail": "Image uploaded successfully"
}
```

### Failed response

```json
{
    "detail": "Upload failed"
}
```

## Delete Product Image

**DELETE** `/farmer/product/{product_id}/images/{image_id}`

### Success response

```json
{
  "detail": "Image deleted successfully"
}
```

### Failed response

```json
{
  "detail": "Failed to delete image from Supabase"
}
```

