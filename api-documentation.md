# API Documentation

## Base URL

- Base URL: `http://127.0.0.1:8000/`

## Authentication

- Authentication: Token-based authentication using the `Authorization` header with the value `Token <token>`.

## Endpoints

## Accounts App API Documentation

### User Registration

#### Register as a Patient

- URL: `/accounts/api/patient-register/`
- Method: `POST`
- Parameters: `username`, `password1`, `password2`, `email`, `first_name`, `last_name`, `country`, `gender`, `Phone_number`
- Response: Registered user details.

#### Register as a Doctor

- URL: `/accounts/api/doctor-register/`
- Method: `POST`
- Parameters: `username`, `password1`, `password2`, `email`, `first_name`, `last_name`, `country`, `gender`, `Phone_number`, `specialist`, `certificate`, `hospital_or_center`, `cv`
- Response: Registered user details.

### User Login

- URL: `/accounts/api/login/`
- Method: `POST`
- Parameters: `username`, `password`
- Response: User details, authentication token and redireaction link to the user dashboard.

### User Logout

- URL: `/accounts/api/logout/`
- Method: `POST`
- Response: Logout confirmation.

### User Profile

#### Patient Profile

- URL: `/accounts/api/patient-profile/`
- Method: `GET`
- Response: Patient profile details.

### Doctor Profile

- URL: `/accounts/api/dr-profile/`
- Method: `GET`
- Response: Doctor profile details.

### Doctor CRUD Operations

#### List Doctors

- URL: `/accounts/api/doctors/`
- Method: `GET`
- Response: List of all doctors.

#### Retrieve Doctor

- URL: `/accounts/api/doctors/<doctor_id>/`
- Method: `GET`
- Response: Details of the specified doctor.

#### Update Doctor

- URL: `/accounts/api/doctors/<doctor_id>/`
- Method: `PUT` or `PATCH`
- Parameters: `first_name`, `last_name`, `country`, `gender`, `Phone_number`, `specialist`, `certificate`, `hospital`, `cv`
- Response: Updated details of the doctor.

#### Delete Doctor

- URL: `/accounts/api/doctors/<doctor_id>/`
- Method: `DELETE`
- Response: Deletes the specified doctor.

Note: Replace `<doctor_id>` in the URLs with the actual ID of the doctor.


## Consultation App API Documentation

The Consultation App API allows you to interact with various resources related to hospitals, doctors, reviews, surveys, reports, ML models, and consultations. This document provides details and usage instructions for each API endpoint.

### Hospitals

- URL: `/consult-now/api/doctors/<doctor_id>/`
- Method: `GET /hospitals/`: Retrieves a list of all hospitals.
- Method: `GET /hospitals/{id}/`: Retrieves details of a specific hospital.

### Doctors

- URL: `/consult-now/api/doctors/<doctor_id>/`
- Method: `GET /doctors/`: Retrieves a list of all doctors.
- Method: `GET /doctors/{id}/`: Retrieves details of a specific doctor.

### Surveys

- URL: `/consult-now/api/survey/`
- Method: `GET /survey/`: Retrieves a list of all surveys.
- Method: `POST /survey/`: Creates a new survey.
- Method: `GET /survey/{id}/`: Retrieves details of a specific survey.
- Method: `PUT /survey/{id}/`: Updates details of a specific survey.
- Method: `DELETE /survey/{id}/`: Deletes a specific survey.

### ML Models

- URL: `/consult-now/api/survey/{id}/intial-diagnosis`
- Method: `GET /survey/{id}/intial-diagnosis/`: Retrieves a list of all ML models for a specific survey.
- Method: `GET /survey/{id}/intial-diagnosis/{id}/`: Retrieves details of a specific ML model.

### Consultation Requests

- URL: `/consult-now/api/survey/{id}/requests`
- Method: `GET /survey/{id}/requests/`: Retrieves a list of all consultation requests for the user who logged in for a specific survey.
- Method: `POST /survey/{id}/requests/`: Creates a new consultation request.
- Method: `GET /survey/{id}/requests/{id}/`: Retrieves details of a specific consultation request.
- Method: `PUT /survey/{id}/requests/{id}/`: Updates details of a specific consultation request, only patients can edit.
- Method: `PUT {BaseUrl}/consult-now/api/requests/{id}/`:Updates details of a specific consultation request, only Doctor or Hospitals can accept or reject the requests sent from patients.
- Method: `DELETE /survey/{id}/requests/{id}/`: Deletes a specific consultation request, only patient do that.

### Reports

- URL: `/consult-now/api/survey/{id}/reports/`
- Method: `GET /reports/`: Retrieves a list of all reports.
- Method: `POST /reports/`: Creates a new report, only doctors or hospitals.
- Method: `GET /reports/{id}/`: Retrieves details of a specific report.
- Method: `PUT /reports/{id}/`: Updates details of a specific report, only doctors or hospitals.
- Method: `DELETE /reports/{id}/`: Deletes a specific report.

### Reviews

- URL: `/consult-now/api/survey/{id}/reports/{id}/review/`
- Method: `GET /survey/{id}/reports/{id}/review/`: Retrieves a list of all reviews.
- Method: `POST /survey/{id}/reports/{id}/review/`: Creates a new review, only patients.
- Method: `GET /survey/{id}/reports/{id}/review/{id}/`: Retrieves details of a specific review.
- Method: `PUT /survey/{id}/reports/{id}/review/{id}/`: Updates details of a specific review, only patients.
- Method: `DELETE /survey/{id}/reports/{id}/review/{id}/`: Deletes a specific review, only patients.

<hr>

## Postman Documentation

For interactive API documentation and examples, you can refer to our [Postman documentation](https://documenter.getpostman.com/view/23311056/2s93m7Wgpn). It provides a detailed overview of the API endpoints, request formats, and response structures. You can also test the API directly from the documentation using the provided examples.

<hr>

## Request and Response Formats

### Request Format

The API accepts and returns data in JSON format. Ensure that your requests include the `Content-Type: application/json` header.

### Response Format

Responses from the API are also in JSON format. The standard response structure includes a `status` field indicating the success or failure of the request and a `data` field containing the response data. In case of an error, an additional `message` field provides details about the error

### Error Responses

- Error responses will include appropriate HTTP status codes and error messages in the response body.

## Conclusion

This API documentation provides an overview of the available endpoints and their usage instructions for the Consultation App API. Make sure to include the required authentication, follow the request and response formats, and handle errors appropriately while integrating with the API. For detailed information on the request payload and response structure for each endpoint, refer to the corresponding endpoint documentation.

If you have any further questions or require assistance, please reach out to our support [team](mailto:pydevazmi@gmail.com).