import pandas as pd
from credentials import credentials
def load_newbalance_data() -> dict:
    newbalance = pd.read_gbq(
        query=f"SELECT * FROM `cotatenis.cotatenis.awin-newbalance`",
        project_id="cotatenis",
        credentials=credentials,
    )
    return {'mpn' : newbalance['mpn'].tolist(), 'urls' : newbalance['merchant_deep_link'].tolist()}
