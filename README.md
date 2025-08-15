# Local Food Wastage Management — Streamlit App

This is a ready-to-deploy Streamlit app that reads the *cleaned* CSVs and provides a simple dashboard with filters, KPIs, charts, and data tables.

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud
1. Push these files to a new **public GitHub repo**.
2. Go to https://share.streamlit.io, click **New app**, connect your repo.
3. Set the app file to `app.py`. (No extra secrets needed.)
4. Click **Deploy**. Done!

Data lives in the `data/` folder:
- cleaned_providers.csv
- cleaned_receivers.csv
- cleaned_food_listings.csv
- cleaned_claims.csv
- data_quality_report.md
