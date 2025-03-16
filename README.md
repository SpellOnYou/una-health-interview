## Introduction

### Rational behind design decision

The project follows several key architectural and technical decisions that optimize for scalability, maintainability, and developer experience:

1. **Technology Stack**
   - Django + Django REST Framework: Chosen for rapid development, robust ORM, built-in admin interface, and extensive ecosystem
   - PostgreSQL: Selected as the primary database for its reliability, ACID compliance, and excellent support for time-series data
   - Docker: Ensures consistent development and deployment environments across different platforms

2. **API Design**
   - RESTful architecture with versioned endpoints (v1) for future compatibility
   - Supports both single and bulk operations for data upload
   - Implements filtering, sorting, and pagination for efficient data retrieval
   - CSV export functionality for data analysis and integration with other systems

3. **Data Model**
   - Normalized schema focusing on essential fields (user_id, timestamp, value)
   - UUID for user identification to ensure global uniqueness
   - Timestamp stored in UTC for consistent time handling across different regions
   - Indexes on frequently queried fields (user_id, timestamp) for query performance

4. **Code Organization**
   - Modular structure with separate apps (glucose) for better maintainability
   - Custom management commands for data loading
   - Test suite for API endpoints
   - Docker Compose setup for easy development and deployment

5. **Security & Scalability**
   - Environment-based configuration for sensitive data
   - API rate limiting capability through DRF
   - Containerized architecture for easy horizontal scaling
   - Pagination implemented to handle large datasets efficiently

## Notable points for the future improvements

Here I will specify additional points that haven't been tackled on this project, but need to be managed (at least be aware of) for improvement of applicaiton.

- Currently data loading feature through Django subcommand (i.e., `manage.py load_data`) does not check uniqueness of input data, which means if we keep feeding same sample data multiple times to the database, there will be duplication. This should be tackled further via, for example, better schema normalization (Ref: [current model schema](https://github.com/SpellOnYou/una-health-interview/blob/main/glucose/models.py#L5)).
- For the exporting data via API, currently format is fixed to `csv` for the initial set up. This could be improved in the future and further formats (json, excel) could be implemented if needed.
- Only essential fields are saved to the database for now (Ref: [extracted fields](https://github.com/SpellOnYou/una-health-interview/blob/main/glucose/management/commands/load_data.py#L45)), while excluding other fields currently not being in use (e.g., `Gerät`, `Seriennummer`)
- [Error handling](https://github.com/SpellOnYou/una-health-interview/blob/main/glucose/management/commands/load_data.py#L56) for loading data through `sample-data` could be detailed further based on specified behavior.
- General security needs to be improved further (e.g., `SECRET_KEY`, database password, allowed hosts, etc).
- `requirements.txt` can be replaced with pytoml for better dependency management in the future.
- Deployment of service (e.g., through cloud platform) could be implemented further when needed
- By embracing `rest_framework.decorators.api_view`, we could help the code to be more cleaner and readable by making [the views](https://github.com/SpellOnYou/una-health-interview/blob/main/glucose/views.py) more function-based.

## Enviroment setup (How to start the service?)

Assuming it's the initial setup, you can simply run the service by creating schema for initial database setup and building image using the default build context (i.e., `[Dockerfile](https://github.com/SpellOnYou/una-health-interview/blob/main/Dockerfile)`)

```shell
docker compose run web python manage.py makemigrations glucose
docker compose run web python manage.py migrate
docker compose up --build
```

You can see the current status of containers via

```shell
docker compose ps
```

## Loading the sample data into the model / database.

Assuming the service is running on docker image, we need to firstly copy the local static data into the container, and then run the command to load data

```shell
your_sample_data_dir="/path/to/your/data"
docker cp "$your_sample_data_dir" $(docker compose ps -q web):/app/
docker compose exec web python manage.py load_data --data-path=/app/sample-data
```

- After successfully loading data, following can be used to quickly check saved data in the PostgreSQL.

```bash
docker compose exec web python manage.py shell
```

```python
from glucose.models import GlucoseLevel

# Check if any data exists
print(GlucoseLevel.objects.count())

# Retrieve the first few records
for record in GlucoseLevel.objects.all()[:5]:
    print(record.user_id, record.timestamp, record.value)
```

- Note here that [the first row is skipped](https://github.com/SpellOnYou/una-health-interview/blob/main/glucose/management/commands/load_data.py#L26) as it seems to contain the metadata
- Timezone is [set to `UTC`](https://github.com/SpellOnYou/una-health-interview/blob/main/config/settings.py#L129) and [being rendered](https://github.com/SpellOnYou/una-health-interview/blob/main/glucose/management/commands/load_data.py#L35) when loading data referring to the metadata of `sample-data`, which can be customized further on either of subcommand, database, and service setup.

## Check API endpoint

You can simply access the API via a web browser: http://0.0.0.0:8000/api/v1/ (note template for now is missing and hence [a plain json resopnse](https://github.com/SpellOnYou/una-health-interview/blob/main/config/settings.py#L61) will be rendered) or other preferred API client (e.g., Postman, Curl, etc) can be used as well.

Following can be checked to test the API after running the service and database.

### Data retrival

Note that [the default pagination is set to 10](https://github.com/SpellOnYou/una-health-interview/blob/main/config/settings.py#L64) which can be adjustable via `limit` param (see following example).

```bash
# Get All Glucose Levels for a User
curl -X GET "http://127.0.0.1:8000/api/v1/levels/?user_id=cccccccc-cccc-cccc-cccc-cccccccccccc"

# Filter by Start and Stop Timestamps
curl -X GET "http://127.0.0.1:8000/api/v1/levels/?user_id=cccccccc-cccc-cccc-cccc-cccccccccccc&start=2021-02-16T00:00:00Z&stop=2021-03-16T23:59:59Z"

# Sort by Timestamp (Descending)
curl -X GET "http://127.0.0.1:8000/api/v1/levels/?user_id=cccccccc-cccc-cccc-cccc-cccccccccccc&ordering=-timestamp"

# Limit the Number of Results
curl -X GET "http://127.0.0.1:8000/api/v1/levels/?user_id=cccccccc-cccc-cccc-cccc-cccccccccccc&limit=5"

# Paginate Results (Default Page Size: 10)
curl -X GET "http://127.0.0.1:8000/api/v1/levels/?user_id=cccccccc-cccc-cccc-cccc-cccccccccccc&page=2"

# Retrieve a particular glucose level by id
curl -X GET "http://127.0.0.1:8000/api/v1/levels/123/"
```

### Data upload

```bash
# Post endpoint for additional data upload
curl -X POST "http://127.0.0.1:8000/api/v1/upload/" \
     -H "Content-Type: application/json" \
     -d '{
           "user_id": "user123",
           "timestamp": "2025-03-16T14:30:00Z",
           "value": 120.5
         }'

# Uploading multiple glucose levels at once:
curl -X POST "http://127.0.0.1:8000/api/v1/upload/" \
     -H "Content-Type: application/json" \
     -d '[
           {"user_id": "user123", "timestamp": "2025-03-16T10:00:00Z", "value": 110.2},
           {"user_id": "user123", "timestamp": "2025-03-16T12:30:00Z", "value": 125.6}
         ]'
```

### Data export

```bash
# Export data via API
curl -X GET "http://127.0.0.1:8000/api/v1/export/"

```

## How to do unit-test?

Considering to the previous condition that service is running on Docker, one can easily check unit-test via following, which will execute all tests.

```bash
docker compose exec web pytest
```

One can find further detailed configuration file can be found [here](https://github.com/SpellOnYou/una-health-interview/blob/main/pytest.ini).

Currently three API endpoints, which are (1) retrival (2) posting data (3) exporting data, are being tested in [a pretty basic level](https://github.com/SpellOnYou/una-health-interview/blob/main/glucose/tests.py) which can be improved further in future. Also, we can consider uploading testing results to the artifacts and embrace it to CI/CD pipeline for better reporting and visualization.

*Exclaimer*: LLM service is mostly being used to enhance documentation of the code.
