
# Product Review Guardian – DB Design & API Contract

## 1. Database Design

### 1.1. Tables Overview

#### a) `users` Table
- **Purpose**: Store registered users of the system.
- **Columns**:
  - `id` (PK, integer, auto-increment)
  - `email` (string, unique, indexed, not null)
  - `hashed_password` (string, not null)
  - `is_active` (boolean, default: `true`)
  - `role` (string, default: `"user"`, e.g., `"admin"` / `"user"`)

- **Relationships**:
  - One-to-many with `reviews`  
    → One user can create many reviews.

---

#### b) `products` Table
- **Purpose**: Store products that can be reviewed.
- **Columns**:
  - `id` (PK, integer, auto-increment)
  - `name` (string, indexed, not null)
  - `category` (string, nullable)
  - `description` (text, nullable)
  - `created_at` (timestamp with timezone, default: `now()`)

- **Relationships**:
  - One-to-many with `reviews`  
    → One product can have many reviews.

---

#### c) `reviews` Table
- **Purpose**: Store user reviews on products, enriched with AI analysis.
- **Columns**:
  - `id` (PK, integer, auto-increment)
  - `user_id` (FK → `users.id`, not null)
  - `product_id` (FK → `products.id`, not null)
  - `rating` (integer, 1–5, not null)
  - `review_text` (text, not null)
  - `sentiment_score` (float, nullable)  
    → AI-generated sentiment score (e.g., range -1 to 1 or 0 to 1).
  - `toxicity_score` (float, nullable)  
    → AI-generated toxicity/abuse indication.
  - `spam_flag` (boolean, default: `false`)  
    → Indicates if AI suspects this review is spam.
  - `ai_summary` (text, nullable)  
    → Short AI-generated summary of the review.
  - `created_at` (timestamp with timezone, default: `now()`)
  - `updated_at` (timestamp with timezone, updates on change)

- **Relationships**:
  - Many-to-one with `users`
  - Many-to-one with `products`

---

### 1.2. Relationship Summary

- **User – Review**:  
  - 1 user → many reviews  
  - `reviews.user_id` → `users.id`

- **Product – Review**:  
  - 1 product → many reviews  
  - `reviews.product_id` → `products.id`


---

## 2. API Contract

Base URL (local dev):

- `http://127.0.0.1:8000`
- Interactive docs: `http://127.0.0.1:8000/docs`

---

### 2.1. Authentication APIs

#### 2.1.1. `POST /auth/register`

- **Description**: Register a new user.
- **Auth**: Not required.
- **Request Body (JSON)**:
  ```json
  {
    "email": "user1@example.com",
    "password": "pass123"
  }
  ```

- **Response (201 / 200 – UserOut)**:
  ```json
  {
    "id": 1,
    "email": "user1@example.com",
    "is_active": true,
    "role": "user"
  }
  ```

---

#### 2.1.2. `POST /auth/token`

- **Description**: Login and get JWT access token (OAuth2 password flow).
- **Auth**: Not required.
- **Request Type**: `application/x-www-form-urlencoded`
- **Form Fields**:
  - `username`: email of the user (e.g. `"user1@example.com"`)
  - `password`: plain password (e.g. `"pass123"`)

- **Response**:
  ```json
  {
    "access_token": "<JWT_TOKEN_STRING>",
    "token_type": "bearer"
  }
  ```

- **Usage**:
  - Take `access_token` from this response.
  - Use it in `Authorize` in Swagger UI or as HTTP header:

    ```http
    Authorization: Bearer <JWT_TOKEN_STRING>
    ```

---

### 2.2. Product APIs

All Product APIs require authentication with Bearer token.

#### 2.2.1. `POST /products/`

- **Description**: Create a new product.
- **Auth**: Bearer token required.
- **Request Body (JSON)**:
  ```json
  {
    "name": "Laptop",
    "category": "Electronics",
    "description": "Fast laptop with 16GB RAM"
  }
  ```

- **Response (ProductOut)**:
  ```json
  {
    "id": 1,
    "name": "Laptop",
    "category": "Electronics",
    "description": "Fast laptop with 16GB RAM"
  }
  ```

---

#### 2.2.2. `GET /products/`

- **Description**: Get list of products.
- **Auth**: Bearer token required.
- **Query Params**:
  - `skip` (int, default `0`)
  - `limit` (int, default `100`)

- **Response**:
  ```json
  [
    {
      "id": 1,
      "name": "Laptop",
      "category": "Electronics",
      "description": "Fast laptop with 16GB RAM"
    }
  ]
  ```

---

#### 2.2.3. `GET /products/{product_id}`

- **Description**: Get one product by ID.
- **Auth**: Bearer token required.
- **Path Param**:
  - `product_id` (int)

- **Response**:
  ```json
  {
    "id": 1,
    "name": "Laptop",
    "category": "Electronics",
    "description": "Fast laptop with 16GB RAM"
  }
  ```

---

#### 2.2.4. `DELETE /products/{product_id}`

- **Description**: Delete a product by ID.
- **Auth**: Bearer token required (in a real system, usually admin-only).
- **Path Param**:
  - `product_id` (int)

- **Response**:
  ```json
  {
    "detail": "Product deleted"
  }
  ```

---

### 2.3. Review APIs

#### 2.3.1. `POST /reviews/`

- **Description**: Create a new review for a product.  
  AI enriches the review with sentiment, toxicity, spam flag, and summary.
- **Auth**: Bearer token required.
- **Request Body (JSON)**:
  ```json
  {
    "product_id": 1,
    "rating": 5,
    "review_text": "Amazing product! Fast delivery and good quality."
  }
  ```

- **Response (ReviewOut)**:
  ```json
  {
    "id": 1,
    "user_id": 2,
    "product_id": 1,
    "rating": 5,
    "review_text": "Amazing product! Fast delivery and good quality.",
    "sentiment_score": 0.9,
    "toxicity_score": 0.0,
    "spam_flag": false,
    "ai_summary": "Very positive review about quality and delivery.",
    "created_at": "2025-11-15T12:34:56.789Z"
  }
  ```

---

#### 2.3.2. `GET /reviews/`

- **Description**: List all reviews.
- **Auth**: Bearer token required.
- **Query Params**:
  - `skip` (int, default `0`)
  - `limit` (int, default `100`)

- **Response**:
  ```json
  [
    {
      "id": 1,
      "user_id": 2,
      "product_id": 1,
      "rating": 5,
      "review_text": "Amazing product! Fast delivery and good quality.",
      "sentiment_score": 0.9,
      "toxicity_score": 0.0,
      "spam_flag": false,
      "ai_summary": "Very positive review about quality and delivery.",
      "created_at": "2025-11-15T12:34:56.789Z"
    }
  ]
  ```

---

#### 2.3.3. `GET /reviews/{review_id}`

- **Description**: Get one review by ID.
- **Auth**: Bearer token required.
- **Path Param**:
  - `review_id` (int)

- **Response**:
  ```json
  {
    "id": 1,
    "user_id": 2,
    "product_id": 1,
    "rating": 5,
    "review_text": "Amazing product! Fast delivery and good quality.",
    "sentiment_score": 0.9,
    "toxicity_score": 0.0,
    "spam_flag": false,
    "ai_summary": "Very positive review about quality and delivery.",
    "created_at": "2025-11-15T12:34:56.789Z"
  }
  ```

---

#### 2.3.4. `PUT /reviews/{review_id}`

- **Description**: Full replace of a review’s content (rating + text).  
  Re-runs AI analysis on the new review text.
- **Auth**: Bearer token required.  
  Only the owner of the review or an admin can update.
- **Path Param**:
  - `review_id` (int)
- **Request Body (JSON)** (same as `ReviewCreate`):
  ```json
  {
    "product_id": 1,
    "rating": 4,
    "review_text": "Good product, but delivery was slow."
  }
  ```

---

#### 2.3.5. `PATCH /reviews/{review_id}`

- **Description**: Partial update of a review (rating and/or review_text).  
  If `review_text` is updated, AI analysis is re-run.
- **Auth**: Bearer token required.  
  Only the owner or admin can update.
- **Path Param**:
  - `review_id` (int)
- **Request Body (JSON)** (all fields optional):
  ```json
  {
    "rating": 3,
    "review_text": "Average experience, packaging was not good."
  }
  ```

---

#### 2.3.6. `DELETE /reviews/{review_id}`

- **Description**: Delete a review by ID.
- **Auth**: Bearer token required.  
  Only the owner or admin can delete.
- **Path Param**:
  - `review_id` (int)

- **Response**:
  ```json
  {
    "detail": "Deleted"
  }
  ```

---

## 3. Authentication Summary (Flow)

1. **Register user**  
   - `POST /auth/register` with email + password.

2. **Login to get token**  
   - `POST /auth/token` with `username` (email) and `password`.  
   - Copy `"access_token"` from response.

3. **Authorize in Swagger UI**  
   - Click **Authorize** button (top-right in `/docs`).  
   - Enter: username and password  
   - Click **Authorize**.

4. **Call protected APIs**  
   - Example: `POST /products/`, `POST /reviews/`, etc.  
   - Swagger will automatically send the token in the `Authorization` header.

