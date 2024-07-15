# README

## Project Setup

### Python version
- **Python**: 3.12.4

### FastAPI version
- **FastAPI**: latest

### Installation
1. Fork then Clone the repo to your machine:
    ```sh
    git clone <github_repo_url>
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


## Refactor Ideas
- Create api mocking for tests using VCR or another that can be dynamic to limit API calls during tests
- Refactor error messages into error serializer
