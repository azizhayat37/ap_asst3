import pytest
from data_loader import generate_investment_data

def test_generate_investment_data():
    ticker = "VIX"
    start_date = "2022-01-01"
    end_date = "2022-01-31"

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