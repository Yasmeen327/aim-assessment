-- Query 1: Top 10 videos by view count
SELECT 
    title,
    channel,
    view_count,
    like_count,
    comment_count
FROM videos
ORDER BY view_count DESC
LIMIT 10;

-- Query 2: Average views, likes, and comments per channel
SELECT
    channel,
    COUNT(*)                    AS total_videos,
    ROUND(AVG(view_count), 0)   AS avg_views,
    ROUND(AVG(like_count), 0)   AS avg_likes,
    ROUND(AVG(comment_count), 0) AS avg_comments
FROM videos
GROUP BY channel
ORDER BY avg_views DESC;

-- Query 3: Most active commenters across all videos
SELECT
    author,
    COUNT(*)            AS total_comments,
    SUM(like_count)     AS total_likes_received
FROM comments
GROUP BY author
ORDER BY total_comments DESC
LIMIT 10;