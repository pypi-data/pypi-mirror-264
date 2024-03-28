# DataLLM Client

## Installation
```
pip install datallm
```

## Enrich a DataFrame
```python
import pandas as pd
from datallm import DataLLM

datallm = DataLLM(api_key='INSERT_API_KEY')

df = pd.DataFrame({
    "age in years": [5, 10, 13, 19, 30, 40, 50, 60, 70, 80],
    "gender": ["m", "f", "m", "f", "m", "f", "m", "f", "m", "f"],
    "country code": ["AT", "DE", "FR", "IT", "ES", "PT", "GR", "UK", "SE", "FI"],
})

# enrich the DataFrame with a new column containing the official country name
df["country"] = datallm.enrich(df, prompt="official name of the country")

# enrich the DataFrame with first name and last name
df["first name"] = datallm.enrich(df, prompt="the first name of that person")
df["last name"] = datallm.enrich(df, prompt="the last name of that person")

# enrich the DataFrame with a categorical
df["age group"] = datallm.enrich(
    df, prompt="age group", categories=["kid", "teen", "adult", "elderly"]
)

# enrich with a boolean value and a integer value
df["isMale"] = datallm.enrich(df, prompt="is Male?", dtype="boolean")
df["income"] = datallm.enrich(df, prompt="annual income in EUR", dtype="integer")

print(df)
```

## Create a DataFrame from Scratch
```python
import pandas as pd
from datallm import DataLLM

datallm = DataLLM(api_key='INSERT_API_KEY')
df = datallm.mock(
    n=10,
    data_description="Members of the Austrian ski team",
    columns={
        "full name": {
            "prompt": "the full name of the person",
        },
        "age in years": {
            "dtype": "integer",
        },
        "body weight": {
            "prompt": "the body weight in kg",
            "dtype": "integer",
        },
        "body height": {
            "prompt": "the body height in cm",
            "dtype": "integer",
        },
        "gender": {
            "categories": ["male", "female"],
        }
    }
)

print(df)
```