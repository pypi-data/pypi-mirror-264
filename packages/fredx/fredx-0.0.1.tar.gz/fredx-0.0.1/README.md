# Fred API

Optimized with httpx

- Single client re-use
- Async

## Import

```python
from fred import Fred
```

## Create Object

```python
API_KEY = ""
fred = Fred(API_KEY)
```

## Get list of series

```python
series_list_df = await (
    fred
    .get_series_list(
      tags = ["india", "monthly"],
      limit = 2
    )
)
```

## Get series data

```python
series_list = list(series_list_df["id"])
series_data = await fred.get_series(
    series_id_list = series_list,
    limit = 1
)
```