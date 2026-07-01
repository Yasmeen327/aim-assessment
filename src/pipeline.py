import json
import os
import time
from api_client import APIClient
from transformer import Transformer
from database import Database


class Pipeline:
    """Orchestrates fetching data from the API and saving raw responses."""

    CHANNELS = {
        "AJ_Kabbrit":      "UC-4KnPMmZzwAzW7SbVATUZQ",
        "AlarabyTube":     "UCPXKFARrr9KIazKFsIdZrbg",
        "AbdulMohsen_MSG": "UCDGN5DdWZTrjXMStKgMI2qQ",
        "Tarek_Osman":     "UCj8P3WuqQN_NnuC8igAAiNw",
    }

    def __init__(self, raw_dir="data/raw"):
        self.client = APIClient()
        self.raw_dir = raw_dir
        os.makedirs(self.raw_dir, exist_ok=True)

    def _save_raw(self, filename, data):
        """Save raw API response to landing zone."""
        filepath = os.path.join(self.raw_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"[SAVED] {filepath}")

    def fetch_all(self):
        """Main method — fetch videos, stats, and comments for all channels."""
        all_videos = []
        all_comments = []

        for channel_name, channel_id in self.CHANNELS.items():
            print(f"\n[FETCHING] Channel: {channel_name}")

            # Step 1: Get video list
            video_response = self.client.get_videos_by_channel(
                channel_id, max_results=15)
            if not video_response:
                print(f"[SKIPPING] Could not fetch videos for {channel_name}")
                continue

            self._save_raw(f"{channel_name}_videos_raw.json", video_response)

            # Extract video IDs
            video_ids = [
                item["id"]["videoId"]
                for item in video_response.get("items", [])
                if item.get("id", {}).get("videoId")
            ]

            if not video_ids:
                continue

            # Step 2: Get stats for those videos
            stats_response = self.client.get_video_stats(video_ids)
            if stats_response:
                self._save_raw(
                    f"{channel_name}_stats_raw.json", stats_response)
                all_videos.extend(stats_response.get("items", []))

            # Step 3: Get comments per video
            for video_id in video_ids:
                time.sleep(0.5)
                comments_response = self.client.get_comments(
                    video_id, max_results=10)
                if comments_response:
                    self._save_raw(
                        f"{video_id}_comments_raw.json", comments_response)
                    all_comments.append({
                        "video_id": video_id,
                        "comments": comments_response.get("items", [])
                    })

        # Save combined raw data
        self._save_raw("all_videos_raw.json", all_videos)
        self._save_raw("all_comments_raw.json", all_comments)

        print(
            f"\n[DONE] Fetched {len(all_videos)} videos across {len(self.CHANNELS)} channels")
        return all_videos, all_comments

    def run(self, fetch=True):
        """End-to-end pipeline execution."""
        # Step 1: Ingest
        if fetch:
            self.fetch_all()

        # Step 2: Transform
        transformer = Transformer(raw_dir=self.raw_dir)
        clean_videos = transformer.transform_videos()
        clean_comments = transformer.transform_comments()

        # Step 3: Load
        db = Database()
        db.create_tables()
        db.load_videos(clean_videos)
        db.load_comments(clean_comments)
        db.close()


if __name__ == "__main__":
    pipeline = Pipeline()
    pipeline.run(fetch=False)
