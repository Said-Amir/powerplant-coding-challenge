
# Powerplant Coding Challenge

## Project Description

The **Powerplant-coding-challenge** project was built using **FastAPI** and **Pydantic** to meet the challenge. FastAPI was chosen for its speed, simplicity in building high-performance REST APIs, and its native support for asynchronous requests, which is ideal for handling multiple simultaneous queries. Pydantic ensures strict validation of incoming data, guaranteeing the reliability of inputs such as loads, fuel costs, and power plant configurations. Together, these tools provide a fast, secure, and efficient development framework suited to the needs of this project.

---

## Requirements

To run this project, you need the following:

- Python 3.8 or higher
- `pip` package manager
- Virtual environment support (optional but recommended)

---

## Installation Instructions

Follow these steps to set up and run the project locally:

### 1. Clone the repository

First, clone the project repository to your local machine:

```bash
git clone <your-repo-url>
cd PowerPlantAPI
```

### 2. Create and activate a virtual environment (optional but recommended)

Create a virtual environment to isolate project dependencies:

```bash
# For Linux/macOS
python3 -m venv powerplant-venv
source powerplant-venv/bin/activate

# For Windows
python -m venv powerplant-venv
powerplant-venv\Scripts\activate
```

### 3. Install project dependencies

Install the required Python packages for the API:

```bash
pip install -r requirements.txt
```

### 4. Install testing dependencies

Install the dependencies needed to run the tests:

```bash
pip install -r requirements-test.txt
```

### 5. Run the application

Launch the FastAPI application on port **8888**:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8888 --reload
```

The API will be running at `http://localhost:8888/`.

---

## Running the Tests

You can run the unit tests using `pytest`:

```bash
pytest
```

---

## Usage

### Endpoint

The API exposes a `POST` endpoint at `/productionplan` to generate a production plan based on the input payload.

### Example Payload

Here is an example of a payload you can use to test the API:

```json
{
  "load": 910,
  "fuels": {
    "gas(euro/MWh)": 13.4,
    "kerosine(euro/MWh)": 50.8,
    "co2(euro/ton)": 20,
    "wind(%)": 60
  },
  "powerplants": [
    {
      "name": "gasfiredbig1",
      "type": "gasfired",
      "efficiency": 0.53,
      "pmin": 100,
      "pmax": 460
    },
    {
      "name": "gasfiredbig2",
      "type": "gasfired",
      "efficiency": 0.53,
      "pmin": 100,
      "pmax": 460
    },
    {
      "name": "gasfiredsomewhatsmaller",
      "type": "gasfired",
      "efficiency": 0.37,
      "pmin": 40,
      "pmax": 210
    },
    {
      "name": "tj1",
      "type": "turbojet",
      "efficiency": 0.3,
      "pmin": 0,
      "pmax": 16
    },
    {
      "name": "windpark1",
      "type": "windturbine",
      "efficiency": 1,
      "pmin": 0,
      "pmax": 150
    },
    {
      "name": "windpark2",
      "type": "windturbine",
      "efficiency": 1,
      "pmin": 0,
      "pmax": 36
    }
  ]
}
```

### Making a Request

Once the API is running, you can test it with a tool like `curl` or **Postman**. Here’s how to make a `POST` request using `curl`:

```bash
curl -X POST "http://localhost:8888/productionplan" -H "Content-Type: application/json" -d '{
  "load": 910,
  "fuels": {
    "gas(euro/MWh)": 13.4,
    "kerosine(euro/MWh)": 50.8,
    "co2(euro/ton)": 20,
    "wind(%)": 60
  },
  "powerplants": [
    {
      "name": "gasfiredbig1",
      "type": "gasfired",
      "efficiency": 0.53,
      "pmin": 100,
      "pmax": 460
    },
    {
      "name": "gasfiredbig2",
      "type": "gasfired",
      "efficiency": 0.53,
      "pmin": 100,
      "pmax": 460
    },
    {
      "name": "gasfiredsomewhatsmaller",
      "type": "gasfired",
      "efficiency": 0.37,
      "pmin": 40,
      "pmax": 210
    },
    {
      "name": "tj1",
      "type": "turbojet",
      "efficiency": 0.3,
      "pmin": 0,
      "pmax": 16
    },
    {
      "name": "windpark1",
      "type": "windturbine",
      "efficiency": 1,
      "pmin": 0,
      "pmax": 150
    },
    {
      "name": "windpark2",
      "type": "windturbine",
      "efficiency": 1,
      "pmin": 0,
      "pmax": 36
    }
  ]
}'
```

### Expected Response

For the payload provided above, you should expect a response similar to this:

```json
[
    {
        "name": "windpark1",
        "p": 90.0
    },
    {
        "name": "windpark2",
        "p": 21.6
    },
    {
        "name": "gasfiredbig1",
        "p": 460.0
    },
    {
        "name": "gasfiredbig2",
        "p": 338.4
    },
    {
        "name": "gasfiredsomewhatsmaller",
        "p": 0.0
    },
    {
        "name": "tj1",
        "p": 0.0
    }
]
```

This response represents the power distribution among the powerplants, with the sum of the power generated matching the requested load of 910 MWh.
