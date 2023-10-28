# asar.web

asar.web is the web and API component of the [asar project](https://github.com/space-codes/asar.core).

## Installation

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/space-codes/asar.web.git
    cd asar.web
    ```

2. **Create a Virtual Environment:**
    ```bash
    python -m venv venv
    ```

3. **Activate the Virtual Environment:**
    - On Windows:
        ```bash
        venv\Scripts\activate
        ```
    - On Unix or MacOS:
        ```bash
        source venv/bin/activate
        ```

4. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Run the Flask Application:**
    ```bash
    flask run
    ```

    The application will be accessible at `http://127.0.0.1:5000/` by default.

2. **Access the Web Application:**
    Open your web browser and navigate to `http://127.0.0.1:5000/` to interact with the web interface.

3. **Access the API Endpoints:**
    The API endpoints can be accessed using HTTP requests using Swagger UI documentation by `http://127.0.0.1:5000/api/swagger`
