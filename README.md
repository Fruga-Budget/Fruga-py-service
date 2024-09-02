# README

## Project Setup

### Python version
- **Python**: 3.12.4

### FastAPI version
- **FastAPI**: latest

### Installation
1. Fork then Clone the repo to your machine:
    ```sh
    git clone <git@github.com:Fruga-Budget/Fruga-py-service.git>
    cd <repo_directory>
    ```
2. Create and activate a virtual environment:
    ```sh
    python3 -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```
3. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```
4. Set up the environment variable(s):
  - Create a '.env' file in the root directory of your project.
  - Add your OpenAI API key to the '.env' file
    ```sh
    OPENAI_API_KEY=your_openai_api_key
    ```

### Running the Application

1. Run the application - Start the FastAPI server(The server will be running at http://127.0.0.1:8000.):
    ```sh
    uvicorn main:app --reload
    ```
### Running the Tests

1. Run the tests:
    ```sh
    pytest
    ```
2. Running the tests with coverage with pytest-cov:
    ```sh
    pytest --cov=app --cov-report=term --cov-report=html
    ```
## Endpoints

### Create a Subscription
- **Endpoint**: 'POST /v1/generate_advice'
- **Example URL**: `http://localhost:8000/v1/generate_advice`
- **Request Body**:
    ```
  {
    "total_income": 10000,
    "needs": [
        {"name": "Rent", "cost": 2000, "description": "Monthly rent payment", "isNegotiable": false},
        {"name": "Utilities", "cost": 1500, "description": "Electricity, water, etc.", "isNegotiable": true},
        {"name": "Groceries", "cost": 1500, "description": "Monthly groceries", "isNegotiable": true}
    ],
    "wants": [
        {"name": "Dining Out", "cost": 1500, "description": "Eating out at restaurants"},
        {"name": "Entertainment", "cost": 1500, "description": "Movies, concerts, etc."}
    ],
    "savings": [
        {"name": "401k", "cost": 2000, "description": "Retirement savings"}
    ]
  }
    ```
- **Response Body**: meets 50/30/20 rule
  {
    "advice": "Congratulations, you're on the right track for the 50/30/20 rule of budgeting!"
  }
- **Response Body**: example snippet when budget does not meet 50/30/20 rule
  {
    "advice": "The user's current budget does not match the 50/30/20 rule. \nRecommendations: \n1. Reduce Dining Out and Entertainment expenses by $100 each.\n2. Increase savings by $200.\n\nRevised Budget Breakdown:\n- Needs (50%): $2500\n- Wants (30%): $1500\n- Savings (20%): $1000\n\nAdjusted Budget:\n- Rent: $1500\n- Utilities: $500 (Negotiable)\n-"
  }   

## Future Addition Ideas
- Add more endpoints for different types of financial advice.
- Integrate additional third-party APIs for extended functionalities.
- Implement authentication and authorization for accessing the API.


## Test Coverage as of 8/2/24
```
---------- coverage: platform darwin, python 3.12.4-final-0 ----------
Name              Stmts   Miss  Cover
-------------------------------------
app/__init__.py       0      0   100%
app/main.py          38     24    37%
-------------------------------------
TOTAL                38     24    37%
Coverage HTML written to dir htmlcov
```

## Fruga-Team
- Steddmnn Bell [GitHub](https://github.com/Steddy1Love)
- Nico Shanstrom [GitHub](https://github.com/NicoShanstrom)
- Grant Davis [GitHub](https://github.com/grantdavis303)
- Lydia Sims [GitHub](https://github.com/LISims88)
- Brandon [GitHub](https://github.com/BrandonDoza)
