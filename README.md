# ApiPractice
mock api to practice pymongo and fastapi concepts

---

## Pending Improvements

### 1. Duplicate Validation

- [ ] Validate that a **User with the same `user_id` does not already exist**
- [ ] Validate that a **Band with the same `band_id` does not already exist**
- [ ] Return **HTTP 409 Conflict** when duplicates are detected
- [ ] Add **unique indexes** in MongoDB for:
  - `users.user_id`
  - `bands.band_id`

---

### 2. Custom Domain Exceptions

- [ ] Define domain-specific exceptions, for example:
  - `UserAlreadyExists`
  - `UserNotFound`
  - `BandAlreadyExists`
  - `BandNotFound`
- [ ] Raise domain exceptions in the persistence/service layer
- [ ] Avoid raising generic `Exception` in application logic

---

### 3. Centralized Exception Handling

- [ ] Implement global exception handlers using `@app.exception_handler`
- [ ] Map domain exceptions to HTTP responses:
  - `UserNotFound` → `404 Not Found`
  - `UserAlreadyExists` → `409 Conflict`
  - `BandNotFound` → `404 Not Found`
  - `BandAlreadyExists` → `409 Conflict`
- [ ] Remove repetitive `try/except` blocks from endpoints
- [ ] Keep endpoints thin and declarative

---

## 🔜 Optional / Future Improvements

- [ ] Separate input/output DTOs (`UserCreate`, `UserOut`, etc.)
- [ ] Add pagination for collection endpoints
- [ ] Add automated tests using `pytest` and `TestClient`
- [ ] Add OpenAPI examples for requests and responses
- [ ] Validate referential integrity (e.g. user references non-existing bands)

---