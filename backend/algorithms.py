import shortuuid
import heapq
from collections import defaultdict

class URLShortener:
    def __init__(self):
        self.url_db = {}  # Stores short -> long URL mapping
        self.access_count = defaultdict(int)  # Stores URL access counts
        self.top_urls = []  # Min-Heap to track most visited links
        self.trie = {}  # Trie for fast lookups
        self.graph = defaultdict(list)  # Graph for URL redirections

    # 🔹 Hashing-based Short URL Generator
    def shorten_url(self, long_url):
        short_id = shortuuid.uuid()[:6]  # Generate 6-char short ID
        self.url_db[short_id] = long_url
        self.insert_into_trie(short_id)
        return short_id

    # 🔹 Retrieve URL (Trie + Redirection Tracking)
    def get_url(self, short_id):
        if short_id in self.url_db:
            self.access_count[short_id] += 1
            heapq.heappush(self.top_urls, (-self.access_count[short_id], short_id))
            self.track_redirection(short_id, self.url_db[short_id])
            return self.url_db[short_id]
        return None

    # 🔹 Trie-based URL Storage
    def insert_into_trie(self, short_id):
        node = self.trie
        for char in short_id:
            if char not in node:
                node[char] = {}
            node = node[char]
        node["end"] = True  # Mark end of short ID

    # 🔹 Heap for Most Popular URLs
    def get_top_urls(self, n=5):
        top_list = heapq.nsmallest(n, self.top_urls)
        return [self.url_db[short_id] for _, short_id in top_list]

    # 🔹 Graph-Based Redirection Tracking
    def track_redirection(self, short_id, long_url):
        self.graph[short_id].append(long_url)

    def get_redirection_history(self, short_id):
        return self.graph.get(short_id, [])
