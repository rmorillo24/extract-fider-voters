=======================================
Post Votes Lookup Script - README
=======================================

DESCRIPTION:
This script allows you to search for posts by title, select a post by ID, and retrieve a list of user emails and vote dates for that post.

USAGE INSTRUCTIONS:
1. Place your data files in the `data/` folder (default location).
2. Ensure you have the following JSON files in `data/`:
   - posts.json (contains post details)
   - post_votes.json (contains voting records)
   - users.json (contains user details)
3. Run the script using Python: python3 main.py
4. Enter a keyword to filter posts by title or press Enter to list all posts.
5. Enter a `post_id` from the filtered list to see who voted on that post.
6. The script will display:
- Date of the vote (YYYY-MM-DD format)
- Email of the user who voted
7. Repeat the process or press `Ctrl+D` to exit.

LOGGING:
- Errors and warnings are logged in `script.log`.

DEFAULT DATA LOCATION:
- The script expects the JSON files to be inside a `data/` folder in the same directory as the script.

REQUIREMENTS:
- Python 3.x
