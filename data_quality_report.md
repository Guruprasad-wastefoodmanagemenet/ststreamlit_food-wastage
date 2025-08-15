# Data Quality Report

## Summary
- Providers: input 25 → cleaned 25 (duplicates removed: 0, rejected: 0)
- Receivers: input 40 → cleaned 40 (duplicates removed: 0, rejected: 0)
- Food listings: input 80 → cleaned 80 (duplicates removed: 0, rejected: 0)
- Claims: input 120 → cleaned 120 (duplicates removed: 0, rejected: 120)

## Rules Applied
- Standardized strings (trimmed whitespace, de-duplicated spaces)
- Title-cased cities
- Validated categories:
  - Provider_Type ∈ ['Restaurant', 'Grocery Store', 'Supermarket']
  - Receiver_Type ∈ ['NGO', 'Community Center', 'Individual']
  - Food_Type ∈ ['Vegetarian', 'Non-Vegetarian', 'Vegan']
  - Meal_Type ∈ ['Breakfast', 'Lunch', 'Dinner', 'Snacks']
  - Status ∈ ['Pending', 'Completed', 'Cancelled']
- Phone numbers normalized to +91-XXXXXXXXXX where possible
- Dates parsed to ISO; Expiry_Date as date, Timestamp as datetime
- Quantities coerced to numeric and kept if > 0
- Duplicates dropped by natural keys (IDs)
- Referential integrity:
  - Food.Provider_ID must exist in Providers
  - Claims.Food_ID and Claims.Receiver_ID must exist in Food and Receivers

## Next Steps
- Load cleaned CSVs into SQL with proper primary & foreign keys
- Use rejected_*.csv to fix or backfill source data
