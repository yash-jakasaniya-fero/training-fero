# Job Board API

## Overview
A REST API for a JobBoard website built with Django REST Framework (DRF). Companies can create and publish job offers, and users can view and interact with them.

## Endpoints

- **`/api/v1/jobs/`**
  - **GET**: Retrieve all job listings.
  - **POST**: Create a new job offer.

- **`/api/v1/jobs/<int:pk>/`**
  - **GET**: Retrieve a specific job offer.
  - **PUT**: Update a job offer.
  - **DELETE**: Delete a job offer.

## Model
- `title`: CharField
- `company_name`: CharField
- `description`: TextField
- `location`: CharField
- `salary`: IntegerField (optional)
- `posted_at`: DateTimeField (auto_now_add=True)

## Features
- **Filters**: Search jobs by `title`, `company_name`, or `location`.
- **Pagination**: Paginated job listings.
