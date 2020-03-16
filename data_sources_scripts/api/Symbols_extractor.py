import os
from iex import reference
reference.output_format = "json"

symbols = []
for company in reference.symbols():
    symbols.append(company["symbol"])
