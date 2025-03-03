# import json
# import os
# import logging

# # Setup logging
# logging.basicConfig(
#     filename="script.log",
#     level=logging.INFO,
#     format="%(asctime)s - %(levelname)s - %(message)s",
# )

# # Define file paths
# DATA_FOLDER = "data"
# POSTS_FILE = os.path.join(DATA_FOLDER, "posts.json")
# POST_VOTES_FILE = os.path.join(DATA_FOLDER, "post_votes.json")
# USERS_FILE = os.path.join(DATA_FOLDER, "users.json")

# # Function to load JSON files
# def load_json(file_path):
#     if not os.path.exists(file_path):
#         logging.error(f"File not found: {file_path}")
#         print(f"Error: File not found - {file_path}")
#         return []
    
#     try:
#         with open(file_path, "r", encoding="utf-8") as file:
#             return json.load(file)
#     except json.JSONDecodeError:
#         logging.error(f"Failed to decode JSON in {file_path}")
#         print(f"Error: Failed to decode JSON - {file_path}")
#         return []

# # Load data
# posts = load_json(POSTS_FILE)
# post_votes = load_json(POST_VOTES_FILE)
# users = load_json(USERS_FILE)

# # Create mappings
# posts_map = {post["id"]: post["title"] for post in posts if "id" in post and "title" in post}
# votes_map = {vote["post_id"]: [] for vote in post_votes if "post_id" in vote and "user_id" in vote}
# users_map = {user["id"]: user["email"] for user in users if "id" in user and "email" in user}

# # Associate votes with users
# for vote in post_votes:
#     if vote["post_id"] in votes_map and vote["user_id"] in users_map:
#         votes_map[vote["post_id"]].append(users_map[vote["user_id"]])

# # Function to display posts based on filter
# def filter_posts(keyword=""):
#     filtered_posts = {post_id: title for post_id, title in posts_map.items() if keyword.lower() in title.lower()}
#     if not filtered_posts:
#         print("\nNo posts found with that keyword.")
#         return {}
    
#     print("\nFiltered Posts:")
#     for post_id, title in filtered_posts.items():
#         print(f"{post_id}: {title}")
    
#     return filtered_posts

# # Main loop
# print("\nEnter a keyword to filter posts (or press Enter to list all). Press Ctrl+D to exit.\n")

# try:
#     while True:
#         keyword = input("\nEnter keyword: ").strip()
#         filtered_posts = filter_posts(keyword)

#         if not filtered_posts:
#             continue

#         post_id_input = input("\nEnter the post_id to find voters: ").strip()

#         try:
#             post_id = int(post_id_input)
#             if post_id not in filtered_posts:
#                 print("Error: Post ID not found in filtered list.")
#                 logging.warning(f"Invalid post_id entered: {post_id}")
#             else:
#                 voters = votes_map.get(post_id, [])
#                 if voters:
#                     print("\nUsers who voted for this post:")
#                     for email in voters:
#                         print(email)
#                 else:
#                     print("No votes for this post.")
#         except ValueError:
#             print("Error: Please enter a valid numerical post ID.")
#             logging.warning(f"Invalid input for post_id: {post_id_input}")

# except EOFError:
#     print("\nGoodbye!")
#     logging.info("User exited the script.")


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

# Create mappings
posts_map = {post["id"]: post for post in posts if "id" in post and "title" in post}
users_map = {user["id"]: user for user in users if "id" in user}

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
                    print(f"{vote_date}: {user_email}")
                    found_votes = True


            if not found_votes:
                print("No votes found for this post.")

        except ValueError:
            print("Error: Please enter a valid numerical post ID.")
            logging.warning(f"Invalid input for post_id: {post_id_input}")

except EOFError:
    print("\nGoodbye!")
    logging.info("User exited the script.")
