import pandas as pd
import numpy as np
from factors import industry_sectors, regions, company_credit_rating  

np.random.seed(42) 

def generate_interest_rate(debt_to_income_ratio, loan_to_value_ratio, 
                           annual_income, loan_amount, collateral_value, 
                           region_name, sector_name, loan_term_years, 
                           company_credit_rating_value, subordination):
    credit_rating_weight = 0.4
    dti_weight = 0.10
    ltv_weight = 0.10
    income_weight = 0.05
    loan_amount_weight = 0.05
    loan_term_weight = 0.05
    collateral_weight = 0.05
    political_stability_weight = 0.05
    sector_weight = 0.05
    subordination_weight = 0.05

    political_stability_index = regions[region_name]
    sector_index = industry_sectors[sector_name]


    # Normalize inputs
    max_income = 200000
    max_loan_amount = 5000000
    max_collateral_value = 50000000
    max_loan_term = 30  # 30 years
    max_subordination = 5

    # Calculate normalized values
    normalized_credit_rating = company_credit_rating_value / max(company_credit_rating.values())
    normalized_political_stability_index = political_stability_index / max(regions.values())
    normalized_sector_index = sector_index / max(industry_sectors.values())
    normalized_dti = 1 - debt_to_income_ratio  
    normalized_ltv = 1 - loan_to_value_ratio / 1.2  
    normalized_income = annual_income / max_income
    normalized_loan_amount = 1 - loan_amount / max_loan_amount  
    normalized_subordination = 1 - subordination / max_subordination   
    normalized_collateral = collateral_value / max_collateral_value
    normalized_loan_term = loan_term_years / max_loan_term 

    # Calculate overall score
    score = (normalized_credit_rating * credit_rating_weight +
             normalized_dti * dti_weight +
             normalized_ltv * ltv_weight +
             normalized_income * income_weight +
             normalized_loan_amount * loan_amount_weight +
             normalized_collateral * collateral_weight +
             normalized_political_stability_index * political_stability_weight +
             normalized_sector_index * sector_weight + 
             normalized_subordination * subordination_weight + 
             normalized_loan_term * loan_term_weight)

    risk_free_rate = 15  
    interest_rate = risk_free_rate * (1 - score)  # Lower score means higher interest rate
    return interest_rate

# Function to simulate realistic data
def generate_sample_data(num_samples):
    debt_to_income_ratio = np.random.uniform(0.1, 0.6, num_samples)
    loan_to_value_ratio = np.random.uniform(0.5, 1.2, num_samples)
    annual_income = np.random.uniform(30000, 200000, num_samples)
    loan_amount = np.random.uniform(5000, 500000, num_samples)
    collateral_value = np.random.uniform(10000, 1000000, num_samples)
    loan_term_years = np.random.choice([0.5, 3, 7, 15, 30], num_samples, p=[0.1, 0.3, 0.3, 0.2, 0.1])  # Weighted choice
    subordination = np.random.choice([1, 2, 3, 4, 5], num_samples, p=[0.1, 0.3, 0.3, 0.2, 0.1]) 
    region = np.random.choice(list(regions.keys()), num_samples)
    sector = np.random.choice(list(industry_sectors.keys()), num_samples)
    credit_rating_keys = list(company_credit_rating.keys())
    assigned_credit_ratings = np.random.choice(credit_rating_keys, num_samples)
    credit_rating_values = [company_credit_rating[rating] for rating in assigned_credit_ratings]

    interest_rates = [generate_interest_rate(debt_to_income_ratio[i], 
                                             loan_to_value_ratio[i], 
                                             annual_income[i], loan_amount[i], 
                                             collateral_value[i], region[i],sector[i],
                                             loan_term_years[i], credit_rating_values[i], subordination[i]) 
                      for i in range(num_samples)]


    data = {
        "Loan_ID": np.arange(1, num_samples + 1),
        "Debt_to_Income_Ratio": debt_to_income_ratio,
        "Loan_to_Value_Ratio": loan_to_value_ratio,
        "Annual_Income": annual_income,
        "Loan_Amount": loan_amount,
        "Interest_Rate": interest_rates,
        "Loan_Term_Years": loan_term_years,
        "Subordination": subordination,
        "Collateral_Value": collateral_value,
        "Sector": sector, 
        "Region": region,
        "Assigned_Credit_Rating": assigned_credit_ratings
    }
    
    return pd.DataFrame(data)

# Generate sample data
num_samples = 20000
df = generate_sample_data(num_samples)

df.to_csv("data.csv", index=False)

