import requests
import os
import json
import time
from dotenv import load_dotenv

load_dotenv()


class APIClient:
    """Handles all HTTP communication with the YouTube Data API v3."""

    BASE_URL = "https://www.googleapis.com/youtube/v3"

    def __init__(self):
        self.api_key = os.getenv("YOUTUBE_API_KEY")
        if not self.api_key:
            raise ValueError("YOUTUBE_API_KEY not found in .env file")
        self.session = requests.Session()

    def _get(self, endpoint, params):
        """Internal method for making GET requests with error handling."""
        params["key"] = self.api_key
        try:
            response = self.session.get(
                f"{self.BASE_URL}/{endpoint}",
                params=params,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            print(f"[WARNING] Request timed out for endpoint: {endpoint}")
            return None
        except requests.exceptions.HTTPError as e:
            print(
                f"[WARNING] HTTP error {e.response.status_code} for endpoint: {endpoint}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"[WARNING] Request failed: {e}")
            return None

    def get_videos_by_channel(self, channel_id, max_results=20):
        """Fetch videos from a specific channel."""
        params = {
            "part": "snippet",
            "channelId": channel_id,
            "maxResults": max_results,
            "order": "date",
            "type": "video"
        }
        return self._get("search", params)

    def get_video_stats(self, video_ids):
        """Fetch statistics for a list of video IDs."""
        params = {
            "part": "statistics,snippet",
            "id": ",".join(video_ids)
        }
        return self._get("videos", params)

    def get_comments(self, video_id, max_results=20):
        """Fetch top-level comments for a video."""
        params = {
            "part": "snippet",
            "videoId": video_id,
            "maxResults": max_results,
            "textFormat": "plainText"
        }
        return self._get("commentThreads", params)
