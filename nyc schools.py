import pandas as pd

# Read in the data
schools = pd.read_csv("schools.csv")

# Which schools are best for math?
best_math_schools = schools[schools["average_math"] >= 640][["school_name", "average_math"]].sort_values("average_math", ascending=False)

# Calculate total_SAT per school
schools["total_SAT"] = schools["average_math"] + schools["average_reading"] + schools["average_writing"]

# Who are the top 10 performing schools?
top_10_schools = schools.groupby("school_name", as_index=False)["total_SAT"].mean().sort_values("total_SAT", ascending=False).head(10)

# Which NYC borough has the highest standard deviation for total_SAT?
boroughs = schools.groupby("borough")["total_SAT"].agg(["count", "mean", "std"]).round(2)
largest_std_dev = boroughs[boroughs["std"] == boroughs["std"].max()].reset_index()
largest_std_dev.rename(columns={"count": "num_schools", "mean": "average_SAT", "std": "std_SAT"}, inplace=True)