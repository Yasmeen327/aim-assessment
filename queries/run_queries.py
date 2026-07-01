import sqlite3
import os


def run_query(cursor, title, sql):
    print(f"\n{'='*60}")
    print(f"Query: {title}")
    print('='*60)
    cursor.execute(sql)
    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()

    # Print header
    print(" | ".join(f"{col:25}" for col in columns))
    print("-" * (27 * len(columns)))

    # Print rows
    for row in rows:
        print(" | ".join(f"{str(val):25}" for val in row))

    print(f"\nTotal rows returned: {len(rows)}")


def main():
    db_path = os.path.join(os.path.dirname(__file__), "../data/youtube.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    run_query(cursor, "Top 10 Videos by View Count", """
        SELECT 
            title,
            channel,
            view_count,
            like_count,
            comment_count
        FROM videos
        ORDER BY view_count DESC
        LIMIT 10
    """)

    run_query(cursor, "Average Engagement per Channel", """
        SELECT
            channel,
            COUNT(*)                     AS total_videos,
            ROUND(AVG(view_count), 0)    AS avg_views,
            ROUND(AVG(like_count), 0)    AS avg_likes,
            ROUND(AVG(comment_count), 0) AS avg_comments
        FROM videos
        GROUP BY channel
        ORDER BY avg_views DESC
    """)

    run_query(cursor, "Most Active Commenters", """
        SELECT
            author,
            COUNT(*)         AS total_comments,
            SUM(like_count)  AS total_likes_received
        FROM comments
        GROUP BY author
        ORDER BY total_comments DESC
        LIMIT 10
    """)

    conn.close()


if __name__ == "__main__":
    main()