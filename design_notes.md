Design Notes
Q1 — Why did you structure your solution the way you did?
I structured the solution around the principle of separation of concerns, where each component has a single responsibility. This keeps the code easier to understand, test, and modify as the pipeline grows.

* APIClient handles all HTTP communication with the YouTube Data API v3. It knows nothing about what happens to the data after it's fetched—it only makes requests, handles errors, and returns responses. This means that if the API changes, there is exactly one component that needs to be updated.
* Pipeline is the orchestrator. It decides which channels to fetch, calls the APIClient, saves raw responses to the landing zone, and coordinates the transformation and loading steps in the correct order. It manages the workflow while delegating the actual work to the other components.
* Transformer is responsible for cleaning and reshaping the raw JSON into flat, analysis-ready records. Keeping transformation as a separate step ensures that the original raw data is always preserved, allowing the transformation logic to evolve without having to re-fetch data from the API.
* Database handles schema creation and loading the transformed data into SQLite. By isolating the storage layer, it would be straightforward to replace SQLite with PostgreSQL or MongoDB in the future without changing the ingestion or transformation logic.
Q2 — What would break at scale?
If the pipeline needed to fetch 50,000 videos instead of around 60, there are several bottlenecks that would become apparent:

1. API quota limits: The YouTube Data API v3 provides a default daily quota of 10,000 units. Fetching 50,000 videos along with their statistics and comments would likely exceed that limit. To address this, I would implement quota tracking, spread the workload across multiple days, or request a higher quota if appropriate.
2. Sequential requests: The current implementation processes requests one at a time with a short delay between them. While this is sufficient for a small dataset, it would take several hours to process tens of thousands of videos. I would improve this by introducing concurrent requests using `concurrent.futures` or `asyncio` while still respecting the API's rate limits.
3. Memory usage: The pipeline currently stores all transformed records in memory before writing them to the database. With a much larger dataset, this could consume a significant amount of RAM. A better approach would be to process and insert the data in batches or stream records directly into the database as they are transformed.
Q3 — What would you improve with more time?
One part of the implementation that I am not completely satisfied with is the `fetch=False` flag in the pipeline's `__main__` block. While it works, it requires modifying the source code to control the pipeline's behavior.
With more time, I would replace this with a command-line interface using Python's `argparse` module. This would allow users to execute individual stages of the pipeline independently—for example:

* `python pipeline.py --fetch`
* `python pipeline.py --transform`
* `python pipeline.py --load`
This would make the pipeline more flexible, easier to use, and more maintainable. It would also make it easier to automate the pipeline in scheduled jobs or CI/CD workflows without requiring changes to the source code.