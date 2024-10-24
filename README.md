# application-test
Test repo for application

## Install

```bash
poetry install 
```

## Run with

```bash
poetry run uvicorn main:app --reload
```
## Example 

```bash
curl -G --data-urlencode "host=google.com; arp -a" "http://localhost:8000/ping"
```