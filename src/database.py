import sqlite3
import os


class Database:
    """Handles SQLite schema creation and data loading."""

    def __init__(self, db_path="data/youtube.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        print(f"[DB] Connected to {self.db_path}")

    def create_tables(self):
        """Create videos and comments tables."""
        self.cursor.executescript("""
            CREATE TABLE IF NOT EXISTS videos (
                video_id      TEXT PRIMARY KEY,
                title         TEXT,
                channel       TEXT,
                published_at  TEXT,
                view_count    INTEGER,
                like_count    INTEGER,
                comment_count INTEGER
            );

            CREATE TABLE IF NOT EXISTS comments (
                comment_id   TEXT PRIMARY KEY,
                video_id     TEXT,
                author       TEXT,
                text         TEXT,
                published_at TEXT,
                like_count   INTEGER,
                FOREIGN KEY (video_id) REFERENCES videos(video_id)
            );
        """)
        self.conn.commit()
        print("[DB] Tables created")

    def load_videos(self, videos):
        """Insert transformed video records into the videos table."""
        self.cursor.executemany("""
            INSERT OR IGNORE INTO videos
            (video_id, title, channel, published_at, view_count, like_count, comment_count)
            VALUES
            (:video_id, :title, :channel, :published_at, :view_count, :like_count, :comment_count)
        """, videos)
        self.conn.commit()
        print(f"[DB] Loaded {self.cursor.rowcount} videos")

    def load_comments(self, comments):
        """Insert transformed comment records into the comments table."""
        self.cursor.executemany("""
            INSERT OR IGNORE INTO comments
            (comment_id, video_id, author, text, published_at, like_count)
            VALUES
            (:comment_id, :video_id, :author, :text, :published_at, :like_count)
        """, comments)
        self.conn.commit()
        print(f"[DB] Loaded {self.cursor.rowcount} comments")

    def close(self):
        self.conn.close()
        print("[DB] Connection closed")
