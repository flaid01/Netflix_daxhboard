import re
import pandas as pd


NETFLIX_PATH = "data/netflix_titles.csv"
IMDB_PATH    = "data/Netflix TV Shows and Movies.csv"
OUTPUT_PATH  = "data/netflix_final.csv"


def normalize_title(title: str) -> str:

    if pd.isna(title):
        return ""
    title = title.lower().strip()
    title = re.sub(r"[^a-z0-9\s]", "", title)
    title = re.sub(r"\s+", " ", title)
    return title


netflix = pd.read_csv(NETFLIX_PATH)
imdb    = pd.read_csv(IMDB_PATH)
print(f"  Netflix : {len(netflix):,} rows")
print(f"  IMDB    : {len(imdb):,} rows")

netflix["director"].fillna("Unknown", inplace=True)
netflix["cast"].fillna("Unknown", inplace=True)
netflix["country"].fillna("Unknown", inplace=True)
netflix["rating"].fillna("Not Rated", inplace=True)

netflix["date_added"] = pd.to_datetime(netflix["date_added"].str.strip(), errors="coerce")
netflix["year_added"]  = netflix["date_added"].dt.year
netflix["month_added"] = netflix["date_added"].dt.month

netflix["duration_value"] = netflix["duration"].str.extract(r"(\d+)").astype(float)
netflix["duration_unit"]  = netflix["duration"].str.extract(r"([a-zA-Z ]+)").apply(
    lambda x: x.str.strip() if x is not None else x
)




imdb["type"] = imdb["type"].str.strip().str.upper()
imdb["type"] = imdb["type"].replace({"MOVIE": "Movie", "SHOW": "TV Show"})



netflix["title_key"] = netflix["title"].apply(normalize_title)
imdb["title_key"]    = imdb["title"].apply(normalize_title)


imdb_cols = ["title_key", "release_year", "type", "imdb_score", "imdb_votes",
             "age_certification", "runtime"]

merged = netflix.merge(
    imdb[imdb_cols],
    on=["title_key", "release_year", "type"],
    how="left"
)

merged.drop(columns=["title_key"], inplace=True)



matched   = merged["imdb_score"].notna().sum()
unmatched = merged["imdb_score"].isna().sum()
pct       = matched / len(merged) * 100


merged.to_csv(OUTPUT_PATH, index=False)
print(f"\n✅ Exported → {OUTPUT_PATH}") 