from flask import Flask, render_template, request, jsonify
import numpy as np
import pandas as pd
import yfinance as yf
from scipy.optimize import minimize

app = Flask(__name__)

# Define ETFs for demonstration purposes
etfs = [
    {"symbol": "VTI", "name": "Vanguard Total Stock Market ETF"},
    {"symbol": "VEA", "name": "Vanguard FTSE Developed Markets ETF"},
    {"symbol": "VWO", "name": "Vanguard FTSE Emerging Markets ETF"},
    {"symbol": "BND", "name": "Vanguard Total Bond Market ETF"},
    {"symbol": "VNQ", "name": "Vanguard Real Estate ETF"},
    {"symbol": "XLE", "name": "Energy Select Sector SPDR Fund"},
]

@app.route('/')
def index():
    return render_template("index.html", etfs=etfs)

@app.route('/optimize', methods=['POST'])
def optimize():
    selected_etfs = request.form.getlist('etf')
    start_date = '2016-01-01'
    end_date = '2021-12-31'
    data = yf.download(selected_etfs, start=start_date, end=end_date)['Adj Close']
    daily_returns = data.pct_change().dropna()

    mean_returns = daily_returns.mean()
    cov_matrix = daily_returns.cov()

    def objective(weights):
        portfolio_return = np.dot(weights, mean_returns)
        portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        sharpe_ratio = portfolio_return / portfolio_volatility
        return -sharpe_ratio

    constraints = ({'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1})
    bounds = [(0, 1) for _ in range(len(selected_etfs))]

    initial_guess = np.array([1 / len(selected_etfs)] * len(selected_etfs))
    optimized_result = minimize(objective, initial_guess, method='SLSQP', bounds=bounds, constraints=constraints)

    optimal_weights = optimized_result.x
    results = {
        "selected_etfs": selected_etfs,
        "optimal_weights": optimal_weights.tolist()
    }

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)

