import pytest
from datetime import datetime
from data_loader import generate_investment_data, create_chart, update_portfolio

def test_generate_investment_data():
    ticker = "AAPL"
    start_date = datetime(2001, 1, 3)
    end_date = datetime(2013, 4, 8)

    etf_name, position, entry_price, exit_price, profit_loss = generate_investment_data(ticker, start_date, end_date)

    # Add assertions to verify the expected values
    assert etf_name == "VIX"
    assert position == 100
    assert entry_price == 150.0
    assert exit_price == 160.0
    assert profit_loss == 1000.0

    # Add more test cases as needed

# Run the tests
pytest.main()