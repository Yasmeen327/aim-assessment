import json
import os


class Transformer:
    """Cleans and reshapes raw API responses into analysis-ready flat records."""

    def __init__(self, raw_dir="data/raw"):
        self.raw_dir = raw_dir

    def _load_json(self, filename):
        filepath = os.path.join(self.raw_dir, filename)
        if not os.path.exists(filepath):
            print(f"[WARNING] File not found: {filepath}")
            return []
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    def transform_videos(self):
        """Flatten raw video data into one record per video."""
        raw_videos = self._load_json("all_videos_raw.json")
        transformed = []

        for video in raw_videos:
            snippet = video.get("snippet", {})
            stats = video.get("statistics", {})

            transformed.append({
                "video_id":      video.get("id"),
                "title":         snippet.get("title", "N/A"),
                "channel":       snippet.get("channelTitle", "N/A"),
                "published_at":  snippet.get("publishedAt", "N/A"),
                "view_count":    int(stats.get("viewCount", 0)),
                "like_count":    int(stats.get("likeCount", 0)),
                "comment_count": int(stats.get("commentCount", 0)),
            })

        print(f"[TRANSFORMED] {len(transformed)} videos")
        return transformed

    def transform_comments(self):
        """Flatten raw comment data into one record per comment."""
        raw_comments = self._load_json("all_comments_raw.json")
        transformed = []

        for entry in raw_comments:
            video_id = entry.get("video_id")
            for item in entry.get("comments", []):
                top = item.get("snippet", {}).get("topLevelComment", {})
                snippet = top.get("snippet", {})

                transformed.append({
                    "comment_id":   top.get("id", "N/A"),
                    "video_id":     video_id,
                    "author":       snippet.get("authorDisplayName", "N/A"),
                    "text":         snippet.get("textDisplay", "N/A"),
                    "published_at": snippet.get("publishedAt", "N/A"),
                    "like_count":   int(snippet.get("likeCount", 0)),
                })

        print(f"[TRANSFORMED] {len(transformed)} comments")
        return transformed
