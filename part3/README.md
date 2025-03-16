# HBnB - Part 3: Data Persistence and Authentication

## Overview

Part 3 of the HBnB project enhances the application from Part 2 by adding database persistence with SQLAlchemy and implementing secure JWT-based authentication. These improvements create a more robust, secure, and production-ready application.

## Key Enhancements

### 1. Database Integration
- Replaced in-memory storage with SQLAlchemy ORM
- Implemented proper database relationships (one-to-many, many-to-many)
- Created SQL schema with foreign key constraints
- Added migration from memory-based repositories to SQL repositories

### 2. Authentication & Authorization
- Added JWT-based authentication system
- Implemented role-based access control (admin/regular users)
- Protected sensitive endpoints with `@jwt_required()` decorator
- Added user password hashing with Bcrypt

### 3. Enhanced Architecture
- Split monolithic facade into specialized facades:
  - UserFacade
  - PlaceFacade
  - ReviewFacade
  - AmenityFacade
- Added dependency injection between facades
- Implemented automated database initialization
- Created default admin user on startup

### 4. New API Features
- Added authentication endpoint (`/api/v1/auth/login`)
- Added relationship-based endpoints:
  - User places: `/api/v1/users/<user_id>/places`
  - User reviews: `/api/v1/users/<user_id>/reviews`
  - Place reviews: `/api/v1/places/<place_id>/reviews`
  - Amenity places: `/api/v1/amenities/<amenity_id>/places`
- Enhanced input validation and error handling

## Technical Details

### Model Changes
- Models now extend SQLAlchemy's `db.Model`
- Added proper database field types and constraints
- Implemented relationship definitions

### Repository Pattern Updates
- Replaced `InMemoryRepository` with `SQLAlchemyRepository`
- Added transaction support

### Security Implementation
- Added JWT token generation and validation
- Implemented password hashing and verification
- Added user identity verification for sensitive operations

## Setup and Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python run.py
```

3. Access the API at:
```bash
http://localhost:5000/api/v1/
```

4. Default admin credentials:

Email: admin@example.com
Password: adminpassword

## Configuration

SQLite database for development (can be configured for MySQL/PostgreSQL)
JWT tokens signed with a secret key defined in configuration
Configurable token expiration time