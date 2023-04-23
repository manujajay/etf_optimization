# etf_optimization
A web app as a starting point for **building a portfolio of ETFs** using an optimization model.

The above code is a Python script that defines a Flask web application for optimizing a portfolio of ETFs.

The code imports several libraries, including Flask, NumPy, Pandas, yfinance, and scipy.optimize.

The script defines a Flask application and sets up two routes - '/' and '/optimize'. The first route, '/', renders an HTML template that displays a list of ETFs. The second route, '/optimize', is used to optimize the selected ETFs by calculating the optimal portfolio weights.

When the user selects the ETFs and submits the form on the webpage, a POST request is sent to the '/optimize' route, which triggers the optimization process. The selected ETFs are downloaded using the yfinance library, and the daily returns are calculated using Pandas.

The optimization process aims to maximize the Sharpe ratio, which is calculated using the portfolio weights, mean returns, and covariance matrix. The optimization problem is defined using the minimize function from scipy.optimize, which uses the SLSQP method to solve the problem subject to constraints.

The optimal weights for the selected ETFs are calculated, and the results are returned as a JSON object using the jsonify function from Flask.

If the script is run directly, the Flask application is started and runs on a local web server. The debug flag is set to True, which enables debugging mode and provides more detailed error messages.
