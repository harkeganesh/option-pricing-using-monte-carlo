# Option Pricing Application

![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)


This application calculates the price of a option using the geometric Brownian motion and the Black-Scholes model. It provides a graphical representation of the Brownian paths using Matplotlib and can be accessed through a Streamlit web interface.

## Installation
To install and run the application, follow these steps:
 
 ```
 pip install -r requirements.txt
```

## Usage
To start the application, run the following command:

```
streamlit run app.py
```

This will launch a web interface where you can interact with the option pricing application.


## Docker
Alternatively, you can use Docker to run the application. A Dockerfile is provided for easy containerization.

Build the Docker image:
```
docker build -t option-pricing-app .
```
Run the Docker container:
```
docker run -p 8501:8501 option-pricing-app
```

The application will be accessible at http://localhost:8501 in your web browser.

