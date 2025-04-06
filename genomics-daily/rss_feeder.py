import os
from datetime import datetime
import markdown 

# Function to create a new RSS feed file
def create_new_rss_feed(base_url="https://emmecola.github.io/genomics-daily/", output_file="feed.xml"):
    # Ensure the base URL ends with a slash
    if not base_url.endswith('/'):
        base_url += '/'
        
    feed_url = f"{base_url}feed.xml"
    
    rss_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>Genomics Daily</title>
    <link>{base_url}</link>
    <description>AI-generated daily summary of genomics papers</description>
    <language>en-us</language>
    <lastBuildDate>{datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000")}</lastBuildDate>
    <atom:link href="{feed_url}" rel="self" type="application/rss+xml" />
  </channel>
</rss>
"""
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(rss_content)

# Function to add a new entry to the RSS feed
def add_rss_entry(base_url="https://emmecola.github.io/genomics-daily/", input_file="summary.md", output_file="feed.xml"):
    # Check if feed.xml exists, if not create it
    if not os.path.exists(output_file):
        create_new_rss_feed(base_url, output_file)
    
    # Read the current summary.md content
    with open(input_file, "r", encoding="utf-8") as f:
        markdown_content = f.read()
        
    # Convert Markdown to HTML
    try:
        html_content = markdown.markdown(markdown_content)
    except Exception as e:
        print(f"Warning: Error converting Markdown to HTML: {e}")
        # Fall back to raw markdown if conversion fails
        html_content = markdown_content
    
    # Get current date
    today_date = datetime.now()
    formatted_date = today_date.strftime("%Y-%m-%d")
    pub_date = today_date.strftime("%a, %d %b %Y %H:%M:%S +0000")
    
    # Ensure the base URL ends with a slash
    if not base_url.endswith('/'):
        base_url += '/'
        
    # Create new RSS item
    new_item = f"""  <item>
    <title>Genomics Daily - {formatted_date}</title>
    <link>{base_url}</link>
    <description><![CDATA[{html_content}]]></description>
    <pubDate>{pub_date}</pubDate>
    <guid isPermaLink="false">{base_url}#{today_date.strftime('%Y%m%d%H%M%S')}</guid>
  </item>
"""
    
    # Read the current feed
    with open(output_file, "r", encoding="utf-8") as f:
        feed_content = f.read()
    
    # Update lastBuildDate
    current_time = datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000")
    
    # Check if lastBuildDate tag exists in the feed content
    if "<lastBuildDate>" in feed_content and "</lastBuildDate>" in feed_content:
        last_build_old = feed_content.split("<lastBuildDate>")[1].split("</lastBuildDate>")[0]
        feed_content = feed_content.replace(
            f"<lastBuildDate>{last_build_old}</lastBuildDate>",
            f"<lastBuildDate>{current_time}</lastBuildDate>"
        )
    else:
        # If lastBuildDate doesn't exist, add it right before the atom:link tag
        if "<atom:link" in feed_content:
            insertion_point = feed_content.find("<atom:link")
            feed_content = (
                feed_content[:insertion_point] + 
                f"    <lastBuildDate>{current_time}</lastBuildDate>\n    " + 
                feed_content[insertion_point:]
            )
        # Or as a fallback, add it right before the channel closing tag
        else:
            insertion_point = feed_content.find("</channel>")
            feed_content = (
                feed_content[:insertion_point] + 
                f"    <lastBuildDate>{current_time}</lastBuildDate>\n  " + 
                feed_content[insertion_point:]
            )
    
    # Add new item after <channel> tag
    insertion_point = feed_content.find("</channel>")
    updated_feed = feed_content[:insertion_point] + new_item + feed_content[insertion_point:]
    
    # Write the updated feed back to the file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(updated_feed)
    
    print(f"Added new entry for {formatted_date} to RSS feed at {output_file}")

# Run the function
if __name__ == "__main__":
    import sys
    import argparse
    
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='Generate RSS feed from Markdown content')
    parser.add_argument('--url', type=str, default="https://emmecola.github.io/genomics-daily/",
                        help='Base URL for the feed (default: https://emmecola.github.io/genomics-daily/)')
    parser.add_argument('--input', type=str, default="summary.md",
                        help='Input Markdown file (default: summary.md)')
    parser.add_argument('--output', type=str, default="feed.xml",
                        help='Output RSS feed file (default: feed.xml)')
    
    args = parser.parse_args()
    
    # Run with the provided arguments
    add_rss_entry(base_url=args.url, input_file=args.input, output_file=args.output)