
import json
import os
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    filename="script.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Define file paths
DATA_FOLDER = "data"
POSTS_FILE = os.path.join(DATA_FOLDER, "posts.json")
POST_VOTES_FILE = os.path.join(DATA_FOLDER, "post_votes.json")
USERS_FILE = os.path.join(DATA_FOLDER, "users.json")
COMMENTS_FILE = os.path.join(DATA_FOLDER, "comments.json")

# Function to load JSON files
def load_json(file_path):
    if not os.path.exists(file_path):
        logging.error(f"File not found: {file_path}")
        print(f"Error: File not found - {file_path}")
        return []
    
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        logging.error(f"Failed to decode JSON in {file_path}")
        print(f"Error: Failed to decode JSON - {file_path}")
        return []

# Function to format date
def format_date(iso_date):
    try:
        return datetime.fromisoformat(iso_date.rstrip("Z")).strftime("%Y-%m-%d")
    except ValueError:
        return "Invalid date"

# Load data
posts = load_json(POSTS_FILE)
post_votes = load_json(POST_VOTES_FILE)
users = load_json(USERS_FILE)
comments = load_json(COMMENTS_FILE)

# Create mappings
posts_map = {post["id"]: post for post in posts if "id" in post and "title" in post}
users_map = {user["id"]: user for user in users if "id" in user}
comments_map = {}
for comment in comments:
    post_id = comment.get("post_id")
    user_id = comment.get("user_id")
    if post_id and user_id:
        comments_map.setdefault(post_id, {})[user_id] = comment.get("content", "")

# Function to filter and display posts
def filter_posts(keyword=""):
    filtered_posts = {post_id: post for post_id, post in posts_map.items() if keyword.lower() in post["title"].lower()}
    if not filtered_posts:
        print("\nNo posts found with that keyword.")
        return {}

    print("\nFiltered Posts:")
    for post_id, post in filtered_posts.items():
        print(f"{post_id}: {post['title']}")

    return filtered_posts

# Main loop
print("\nEnter a keyword to filter posts (or press Enter to list all). Press Ctrl+D to exit.\n")

table_data = []
try:
    while True:
        keyword = input("\nEnter keyword: ").strip()
        filtered_posts = filter_posts(keyword)

        if not filtered_posts:
            continue

        post_id_input = input("\nEnter the post_id to find voters: ").strip()

        try:
            post_id = int(post_id_input)
            if post_id not in filtered_posts:
                print("Error: Post ID not found in filtered list.")
                logging.warning(f"Invalid post_id entered: {post_id}")
                continue

            print(f"\n--- post id: {post_id}")
            found_votes = False


            for vote in post_votes:
                if vote.get("post_id") == post_id:
                    user_email = users_map.get(vote.get("user_id"), {}).get("email", "Unknown Email")
                    vote_date = format_date(vote.get("created_at", ""))
                    comment = comments_map.get(post_id, {}).get(vote.get("user_id"), "No Comment")
                    print(f"{vote_date.ljust(10)}: {user_email.ljust(20)}: {comment}")
                    found_votes = True

            if not found_votes:
                print("No votes found for this post.")

        except ValueError:
            print("Error: Please enter a valid numerical post ID.")
            logging.warning(f"Invalid input for post_id: {post_id_input}")

except EOFError:
    print("\nGoodbye!")
    logging.info("User exited the script.")
