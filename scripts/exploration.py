import pandas as pd
DATA_PATH = "data/netflix_final.csv"
DIVIDER   = "─" * 50



df = pd.read_csv(DATA_PATH)


#Dataset overview

print(f"\n── Dataset Overview {DIVIDER[:31]}")
print(f"  Rows            : {len(df):,}")
print(f"  Columns         : {df.shape[1]}")
print(f"  Memory usage    : {df.memory_usage(deep=True).sum() / 1e6:.1f} MB")

print(f"\n  Missing values per column:")
missing = df.isnull().sum()
missing = missing[missing > 0]
for col, count in missing.items():
    pct = count / len(df) * 100
    print(f"    {col:<25} {count:>5,}  ({pct:.1f}%)")


#Content Type

print(f"\n── Content Type {DIVIDER[:35]}")
type_counts = df["type"].value_counts()
for content_type, count in type_counts.items():
    pct = count / len(df) * 100
    print(f"  {content_type:<12} : {count:,}  ({pct:.1f}%)")


#Top Countries

print(f"\n── Top 10 Countries {DIVIDER[:31]}")
top_countries = (
    df["country"]
    .str.split(",")
    .explode()
    .str.strip()
    .value_counts()
    .head(10)
)
for country, count in top_countries.items():
    print(f"  {country:<30} {count:,}")


#Content added over time

print(f"\n── Content Added per Year {DIVIDER[:25]}")
by_year = df["year_added"].value_counts().sort_index().dropna()
for year, count in by_year.items():
    bar = "█" * (count // 50)
    print(f"  {int(year)}  {bar}  {count:,}")


#Top genres

print(f"\n── Top 10 Genres {DIVIDER[:34]}")
top_genres = (
    df["listed_in"]
    .str.split(",")
    .explode()
    .str.strip()
    .value_counts()
    .head(10)
)
for genre, count in top_genres.items():
    print(f"  {genre:<35} {count:,}")


#IMDB scores

print(f"\n── IMDB Scores {DIVIDER[:36]}")
scores = df["imdb_score"].dropna()
print(f"Titles with score  : {len(scores):,}")
print(f"Average            : {scores.mean():.2f}")
print(f"Highest            : {scores.max():.1f}")
print(f"Lowest             : {scores.min():.1f}")
print(f"Above 8.0          : {(scores >= 8).sum():,}")
print(f"Below 5.0          : {(scores < 5).sum():,}")


#Average IMDB score by genre

print(f"\n── Avg IMDB Score by Genre (Top 10) {DIVIDER[:15]}")
genre_scores = (
    df[["listed_in", "imdb_score"]]
    .dropna()
    .assign(genre=df["listed_in"].str.split(","))
    .explode("genre")
    .assign(genre=lambda x: x["genre"].str.strip())
    .groupby("genre")["imdb_score"]
    .agg(avg="mean", count="count")
    .query("count >= 30")           # only genres with enough titles
    .sort_values("avg", ascending=False)
    .head(10)
)
for genre, row in genre_scores.iterrows():
    print(f"  {genre:<35} {row['avg']:.2f}  (n={int(row['count'])})")


#Insights

most_active_year = int(by_year.idxmax())
most_active_count = int(by_year.max())
top_country = top_countries.index[0]
top_genre = top_genres.index[0]
best_genre = genre_scores.index[0]
best_genre_score = genre_scores.iloc[0]["avg"]

print(f"\n── Key Insights {DIVIDER[:35]}")
print(f"  Most active year   : {most_active_year} ({most_active_count:,} titles added)")
print(f"  Top country        : {top_country}")
print(f"  Most common genre  : {top_genre}")
print(f"  Best rated genre   : {best_genre} (avg {best_genre_score:.2f})")
print(f"  Movies vs TV Shows : {type_counts.get('Movie', 0):,} vs {type_counts.get('TV Show', 0):,}")
print()