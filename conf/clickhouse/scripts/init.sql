CREATE DATABASE IF NOT EXISTS ugc ON CLUSTER 'ugc_cluster';

-- Progress
CREATE TABLE IF NOT EXISTS ugc.progress_queue ON CLUSTER 'ugc_cluster'
(
    user_id UUID,
    film_id UUID,
    viewed_frame Int32
)
ENGINE=Kafka('kafka:9092', 'progress-topic', 'progress-group-kafka', 'JSONEachRow');

CREATE TABLE IF NOT EXISTS ugc.progress ON CLUSTER 'ugc_cluster'
AS ugc.progress_queue
ENGINE = ReplicatedMergeTree('/clickhouse/tables/{cluster}/{shard}/progress', '{replica}_progress')
ORDER BY (user_id, film_id);

CREATE TABLE IF NOT EXISTS ugc.progress_distributed ON CLUSTER 'ugc_cluster'
AS ugc.progress
ENGINE = Distributed('ugc_cluster', ugc, progress, rand());

CREATE MATERIALIZED VIEW IF NOT EXISTS ugc.progress_consumer ON CLUSTER 'ugc_cluster' TO ugc.progress_distributed
AS SELECT user_id, film_id, viewed_frame
FROM ugc.progress_queue;

-- Bookmarks
CREATE TABLE IF NOT EXISTS ugc.bookmarks_queue ON CLUSTER 'ugc_cluster'
(
    user_id UUID,
    film_id UUID,
    bookmarked BOOL,
    bookmarked_at DATETIME
)
ENGINE=Kafka('kafka:9092', 'bookmarks-topic', 'bookmarks-group-kafka', 'JSONEachRow');

CREATE TABLE IF NOT EXISTS ugc.bookmarks ON CLUSTER 'ugc_cluster'
AS ugc.bookmarks_queue
ENGINE = ReplicatedMergeTree('/clickhouse/tables/{cluster}/{shard}/bookmarks', '{replica}_bookmarks')
ORDER BY (user_id, film_id, bookmarked_at);

CREATE TABLE IF NOT EXISTS ugc.bookmarks_distributed ON CLUSTER 'ugc_cluster'
AS ugc.bookmarks
ENGINE = Distributed('ugc_cluster', ugc, bookmarks, rand());

CREATE MATERIALIZED VIEW IF NOT EXISTS ugc.bookmarks_consumer ON CLUSTER 'ugc_cluster' TO ugc.bookmarks_distributed
AS SELECT user_id, film_id, bookmarked, bookmarked_at
FROM ugc.bookmarks_queue;
