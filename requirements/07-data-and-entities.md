# Data and Entities

Early domain model, technology-neutral.

## Entity: User

**Description:**  
- ...

**Key Attributes:**  
- UserId
- Email
- FirstName
- LastName
- Status

**Relationships:**  
- User can create many Requests
- User can belong to one Role

**Implemented:** 
- [NO] / [YES]


## Entity: Request
**Description:**  
...

**Key Attributes:**  
- RequestId
- Title
- Status
- CreatedAt

**Relationships:**  
- Request belongs to one User

**Implemented:** 
- [NO] / [YES]
