import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta
import os

def generate_gl_data(num_records=100, start_date=None, end_date=None):
    """
    Generate fake General Ledger data.
    
    Parameters:
    -----------
    num_records : int, optional (default=100)
        Number of records to generate.
    start_date : datetime, optional (default=None)
        Start date for the transactions. If None, defaults to 30 days ago.
    end_date : datetime, optional (default=None)
        End date for the transactions. If None, defaults to today.
    
    Returns:
    --------
    pandas.DataFrame
        DataFrame containing the generated GL data.
    """
    fake = Faker()
    
    # Set default date range if not provided
    if start_date is None:
        start_date = datetime.now() - timedelta(days=30)
    if end_date is None:
        end_date = datetime.now()
    
    # Define some account codes and names
    accounts = {
        '1000': 'Cash',
        '1010': 'Accounts Receivable',
        '1020': 'Inventory',
        '2000': 'Accounts Payable',
        '3000': 'Revenue',
        '4000': 'Expenses',
        '4010': 'Rent Expense',
        '4020': 'Utilities Expense',
        '4030': 'Salaries Expense',
        '5000': 'Purchases',
    }
    
    # Generate data
    data = []
    for _ in range(num_records):
        # Generate transaction date and posting date
        transaction_date = fake.date_between_dates(date_start=start_date, date_end=end_date)
        posting_date = transaction_date + timedelta(days=random.randint(0, 5))
        
        # Generate reference and description
        reference = f"REF-{fake.random_number(digits=6)}"
        description = fake.sentence(nb_words=6)
        
        # Generate debit and credit
        amount = round(random.uniform(10, 10000), 2)
        if random.choice([True, False]):
            debit = amount
            credit = 0
        else:
            debit = 0
            credit = amount
        
        # Select account
        account_code = random.choice(list(accounts.keys()))
        account_name = accounts[account_code]
        
        data.append({
            'transaction_date': transaction_date.strftime('%Y-%m-%d'),
            'posting_date': posting_date.strftime('%Y-%m-%d'),
            'reference': reference,
            'description': description,
            'debit': debit,
            'credit': credit,
            'account_code': account_code,
            'account_name': account_name
        })
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    return df

def save_gl_data(df, output_dir='GL_data'):
    """
    Save GL data to a CSV file with a unique filename.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame containing the GL data.
    output_dir : str, optional (default='GL_data')
        Directory where the file will be saved.
    
    Returns:
    --------
    str
        Path to the saved file.
    """
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{timestamp}_gl_data.csv"
    filepath = os.path.join(output_dir, filename)
    
    # Save to CSV
    df.to_csv(filepath, index=False)
    
    return filepath

def generate_bank_data(num_records=50, start_date=None, end_date=None, initial_balance=5000):
    """
    Generate fake Bank Statement data.
    """
    fake = Faker()
    
    # Set default date range if not provided
    if start_date is None:
        start_date = datetime.now() - timedelta(days=30)
    if end_date is None:
        end_date = datetime.now()
    
    # Define some common bank transaction descriptions
    withdrawal_descriptions = [
        "ATM WITHDRAWAL", "CHECK PAYMENT", "DEBIT CARD PURCHASE", 
        "TRANSFER TO SAVINGS", "MORTGAGE PAYMENT", "UTILITY BILL",
        "CREDIT CARD PAYMENT", "INSURANCE PREMIUM", "SUBSCRIPTION FEE"
    ]
    
    deposit_descriptions = [
        "SALARY DEPOSIT", "TRANSFER FROM SAVINGS", "CHECK DEPOSIT", 
        "REFUND", "INTEREST PAYMENT", "DIVIDEND PAYMENT",
        "CUSTOMER PAYMENT", "CASH DEPOSIT", "LOAN PROCEEDS"
    ]
    
    # Generate transaction dates and sort them
    dates = [fake.date_between_dates(date_start=start_date, date_end=end_date) 
             for _ in range(num_records)]
    dates.sort()
    
    # Generate data
    data = []
    balance = initial_balance
    
    for date in dates:
        # Decide if it's a withdrawal or deposit
        is_withdrawal = random.choice([True, False])
        
        if is_withdrawal:
            amount = round(random.uniform(10, 2000), 2)
            description = random.choice(withdrawal_descriptions)
            withdrawal = amount
            deposit = 0
            balance -= amount
        else:
            amount = round(random.uniform(50, 5000), 2)
            description = random.choice(deposit_descriptions)
            withdrawal = 0
            deposit = amount
            balance += amount
        
        # Add custom details to the description
        if "PURCHASE" in description:
            description += f" - {fake.company()}"
        elif "PAYMENT" in description:
            description += f" - {fake.company()}"
        
        data.append({
            'date': date.strftime('%Y-%m-%d'),
            'description': description,
            'withdrawal': withdrawal,
            'deposit': deposit,
            'balance': round(balance, 2)
        })
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    return df

def save_bank_data(df, output_dir='bank_data'):
    """
    Save Bank Statement data to a CSV file with a unique filename.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame containing the bank statement data.
    output_dir : str, optional (default='bank_data')
        Directory where the file will be saved.
    
    Returns:
    --------
    str
        Path to the saved file.
    """
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{timestamp}_bank_data.csv"
    filepath = os.path.join(output_dir, filename)
    
    # Save to CSV
    df.to_csv(filepath, index=False)
    
    return filepath

if __name__ == "__main__":
    # Create output directories
    os.makedirs('GL_data', exist_ok=True)
    os.makedirs('bank_data', exist_ok=True)
    
    # Generate and save GL data
    gl_data = generate_gl_data(num_records=100)
    gl_output_file = save_gl_data(gl_data)
    print(f"GL data saved to: {gl_output_file}")
    
    # Generate and save Bank data
    bank_data = generate_bank_data(num_records=50)
    bank_output_file = save_bank_data(bank_data)
    print(f"Bank data saved to: {bank_output_file}")
