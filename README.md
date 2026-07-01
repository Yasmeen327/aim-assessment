# YouTube Data Pipeline

### AIM Technologies – Junior Data Engineer Take-Home Assessment

This project implements a small end-to-end data engineering pipeline that ingests video and comment data from the YouTube Data API v3, stores the raw API responses in a landing zone, transforms them into an analysis-ready format, and loads the results into a SQLite database for querying.

The pipeline is implemented using an object-oriented design consisting of four primary classes, each responsible for a single stage of the ETL process.

The dataset focuses on four Arabic-language educational and political YouTube channels, chosen to demonstrate correct handling of Arabic Unicode text throughout the pipeline.

---

# Project Structure

```text
aim_assessment/
├── src/
│   ├── api_client.py      # APIClient class — handles all HTTP communication
│   ├── transformer.py     # Transformer class — cleans and flattens raw data
│   ├── database.py        # Database class — schema creation and data loading
│   └── pipeline.py        # Pipeline class — orchestrates the entire pipeline
├── data/
│   ├── raw/               # Landing zone containing raw API responses
│   └── youtube.db         # SQLite database
├── queries/
│   ├── analysis.sql       # Analytical SQL queries (Part 4)
│   └── run_queries.py     # Executes queries and prints formatted results
├── diagram/
│   └── pipeline_diagram.png
├── design_notes.md        # Part 6 answers
├── requirements.txt
├── .env                   # API key (excluded from GitHub)
└── README.md
```

---

# Requirements

* Python 3.10+ (or newer)
* YouTube Data API v3 key

---

# Setup Instructions

## 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/aim_assessment.git
cd aim_assessment
```

## 2. Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure the API key

Create a `.env` file in the project root:

```text
YOUTUBE_API_KEY=your_api_key_here
```

---

# Running the Pipeline

Run the complete pipeline:

```bash
cd src
python pipeline.py
```

The pipeline will:

1. Fetch data from the YouTube Data API.
2. Save the raw API responses to the landing zone (`data/raw/`).
3. Transform the raw JSON into flat, analysis-ready records.
4. Create the SQLite database schema.
5. Load the transformed data into the database.

> **Note:** The pipeline includes a configurable `fetch` parameter that can be disabled to reuse previously saved raw API responses instead of making new API requests. In a production-ready version, this would be exposed through a command-line interface rather than modifying the source code directly.

---

# Dataset

The dataset contains data from four Arabic-language YouTube channels.

| Channel                   | Focus                               |
| ------------------------- | ----------------------------------- |
| AJ+ كبريت                 | Political analysis and commentary   |
| AlarabyTube - العربي تيوب | Arab world news                     |
| عبدالمحسن MSG             | Arabic historical documentaries     |
| Tarek Osman طارق عثمان    | Egyptian and Middle Eastern history |

**Dataset summary**

* 4 channels
* 60 videos
* 509 comments

---

# Database Design

The SQLite database consists of two relational tables:

* **videos** — stores video metadata and statistics.
* **comments** — stores comment information linked to videos through a foreign key (`video_id`).

This design models the natural one-to-many relationship between videos and their comments while supporting efficient analytical queries.

---

# Analytical Queries (Part 4)

## Query 1 — Top 10 Videos by View Count

```sql
SELECT
    title,
    channel,
    view_count,
    like_count,
    comment_count
FROM videos
ORDER BY view_count DESC
LIMIT 10;
```

**Output**

```
title                                                              | channel           | view_count | like_count | comment_count
الدحيح | هل أنت شيوعي؟                                            | AJ+ كبريت         | 522438     | 17486      | 1009
المُخبر الاقتصادي+ | هل تسمح أمريكا لإيران بفرض رسوم في هرمز... | AJ+ كبريت         | 363933     | 9111       | 462
كيف تحولت رحلة مدنية إيرانية إلى واحدة من أكبر كوارث الطيران... | AJ+ كبريت         | 167183     | 5618       | 313
كيف سقطت تونس في يد الاحتلال الفرنسي؟                            | عبدالمحسن MSG     | 163820     | 6229       | 752
أبشع جريمة في أوروبا.. كيف حاولوا محو شعب أيرلندا؟              | عبدالمحسن MSG     | 159479     | 6287       | 354
تركوهم يُذبحون! السر الأسود خلف حرب البوسنة                      | عبدالمحسن MSG     | 159348     | 9248       | 663
كيف دمرت إسبانيا نفسها؟                                          | عبدالمحسن MSG     | 111976     | 4352       | 213
كيف تأسست واستقلت كل دولة عربية؟                                 | عبدالمحسن MSG     | 109350     | 6938       | 788
عملية ميونخ: كيف تحول أكبر حفل رياضي في العالم إلى مجزرة؟       | عبدالمحسن MSG     | 102147     | 4781       | 270
المُخبر الاقتصادي+ | هل تسقط إسرائيل لو تخلت أمريكا فجأة عنها؟ | AJ+ كبريت         | 99222      | 5066       | 234
```

---

## Query 2 — Average Engagement per Channel

```sql
SELECT
    channel,
    COUNT(*) AS total_videos,
    ROUND(AVG(view_count),0) AS avg_views,
    ROUND(AVG(like_count),0) AS avg_likes,
    ROUND(AVG(comment_count),0) AS avg_comments
FROM videos
GROUP BY channel
ORDER BY avg_views DESC;
```

**Output**

```
channel                      | total_videos | avg_views | avg_likes | avg_comments
AJ+ كبريت                    | 15           | 101890    | 3456      | 162
عبدالمحسن MSG                | 15           | 98808     | 4853      | 380
AlarabyTube - العربي تيوب    | 15           | 9990      | 537       | 46
Tarek Osman طارق عثمان       | 15           | 8268      | 293       | 38
```

---

## Query 3 — Most Active Commenters

```sql
SELECT
    author,
    COUNT(*) AS total_comments,
    SUM(like_count) AS total_likes_received
FROM comments
GROUP BY author
ORDER BY total_comments DESC
LIMIT 10;
```

**Output**

```
author                  | total_comments | total_likes_received
@zeinabmoustafa6178     | 5              | 2
@mr.Beatiger9999        | 5              | 0
@MinaGabriel-g4h        | 5              | 1
@sniper.VZ57            | 4              | 0
@mohamedbouakkaz1608    | 4              | 3
@Mohammed06543          | 4              | 3
@AhmedAli-u5d9n         | 4              | 0
@التبعالخامسالتبع       | 3              | 0
@mohamedkamkami9168     | 3              | 0
@amanyabdrabo8111       | 3              | 2
```

---

# Storage Choice (Part 3)

SQLite was chosen because the transformed data is naturally relational: each video can have many comments, making a one-to-many relationship between two tables a straightforward design. SQLite also requires no server configuration, making the project easy to run locally while still supporting SQL queries and relational constraints.

MongoDB would also be a reasonable option because the raw YouTube API responses are nested JSON documents. However, since the assessment requires producing a flat, analysis-ready dataset and writing analytical SQL queries, a relational database is the more appropriate choice. For a production system requiring concurrent users, larger datasets, or more advanced database features, PostgreSQL would be my preferred option.

---

# Dependencies

* `requests` — communicates with the YouTube Data API
* `python-dotenv` — loads the API key from the `.env` file

---

# Notes

* Raw API responses are preserved in `data/raw/` before any transformation is applied.
* Arabic Unicode text is handled correctly throughout the pipeline using UTF-8 encoding.
* Videos with disabled comments are handled gracefully without interrupting pipeline execution.
* The project follows a modular object-oriented design to separate ingestion, transformation, orchestration, and storage responsibilities.