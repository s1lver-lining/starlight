import os
import sys
import re
import json

"""
This script is used to produce a signle Markdown file from the content of the subdirectories.
Run this when you make any changes to the subdirectories.

It will:
- Reset the README.md file (DO NOT EDIT THIS FILE)
- Add titles from the subdirectories names with apropriate size and add the content of their respective README.md files
- Update the links to it's context (the root of this repository)
- Insert emotes like :heart: to the corresponding HTML code

Requirements:
- All the directories must have different names for the same-file links to work
- Relative links in the README.md files must be valid from their respective directories. They most start with ./ or ../

Directories that starts with . or _ will be ignored. The Tools directories will be ignored as well.
"""

# Parameters
OUTPUT_MD_FILE = "./README.md"

# Read topics from topics.json
with open("./topics.json", "r", encoding='utf-8') as topics_fd:
    TOPICS = json.load(topics_fd)

special_words = {
    ":heart:": "<span style=\"color:red\">❤️</span>"
}

def output_write(content:str) -> None:
    """
    Append content to the global output file named OUTPUT_MD_FILE

    Args:
        content (str): The content to write
    """
    with open(OUTPUT_MD_FILE, "a", encoding='utf-8') as output_fd:
        output_fd.write(content)


def update_links(content:str, topic_path:str) -> str:
    """
    Update the links in the content to be valid from the root of the repository
    
    Args:
        content (str): The content of a README.md file
        topic_path (str): The path to the topic directory

    Returns:
        str: The content of the README.md file with updated links
    """

    # Get potential links to other resources in the content: Search for [text](link)
    links = re.findall(r"\[([^\]]+)\]\(([^\)]+)\)", content)

    # Add src="" links: Search for src="link"
    links += re.findall(r"(src)=\"([^\"]+)\"", content)

    # For each link, update the link if the link is a local link
    for link in links:

        # Link to a local markdown file -> Same file link
        if link[1].endswith("README.md") and not "http" in link[1]:

            # If the link have at least a directory, make it a same file link with the last directory name as the anchor
            if "/" in link[1]:
                dir_name = link[1].split("/")[-2]
                new_link = "#" + dir_name.lower().replace(" ", "-").replace("%20", "-")
                content = content.replace(link[1], new_link)
            continue

        # Relative link to a local file in the same directory -> Relative link from the root of the repository
        if link[1].startswith("./"):
            topic_path = topic_path.replace(" ", "%20")
            new_link = link[1].replace("./", topic_path + "/")
            content = content.replace(link[1], link[1].replace("./", topic_path + "/"))
            continue

        # Relative link to a local file in another directory : Replace the ../ by the topic name minus the last directory if exists
        if link[1].startswith("../"):
                i = 0
                while not i > len(topic_path) and topic_path[-i] != "/":
                    i += 1
                if i > len(topic_path):
                    i = 0
                dotdot_path = topic_path[:-i] + "/"
                dotdot_path = dotdot_path.replace(" ", "%20")
                new_link = link[1].replace("../", dotdot_path)
                content = content.replace(link[1], new_link)
                continue

    return content

def update_titles(content:str, depth:int=0) -> str:
    """
    Update the titles in the content to be valid from the root of the repository
    
    Args:
        content (str): The content of a README.md file
        depth (int): The depth of the topic in the table of contents

    Returns:
        str: The content of the README.md file with updated titles
    """

    # Get the title of the content
    titles = re.findall(r"^(#+) (.*)", content, re.MULTILINE)

    # Update the titles
    for t in titles:
        new_title = "#" * (len(t[0]) + (depth+1)) + " " + t[1]
        content = content.replace(t[0] + " " + t[1], new_title)

    return content


def replace_special_words(content:str, special_words:str={}) -> str:
    """
    Replace special words with their corresponding code

    Args:
        content (str): The content of a README.md file
        special_words (dict): A dictionary of special words and their corresponding code

    Returns:
        str: The content of the README.md file with the special words replaced
    """
    for word in special_words:
        # Escape the special characters
        word = re.escape(word)
        # Replace all occurrences of the word
        regex = re.compile(word)
        content = re.sub(regex, special_words[word], content)
    return content


def add_topic(topic:str, depth:int=0) -> None:
    """
    Append the content of a topic to the global output file, OUTPUT_MD_FILE.
    Does not add the title of the topic, it must be added before calling this function.

    Args:
        topic (str): The path to the topic directory
        depth (int): The depth of the topic in the table of contents
    """

    # Get the content of the topic directory
    files = os.listdir(topic)
    directories = [d for d in files if os.path.isdir(os.path.join(topic, d))]

    # Add links to the subdirectories of the topic
    for directory in directories:
        if not directory.startswith(".") and not directory.startswith("_") and not directory == "Tools":
            output_write("⇨ [" + directory + "](#" + directory.lower().replace(" ", "-") + ")<br>")
    output_write("\n\n")
        
    # If there is a README.md file, add it's content
    if "README.md" in files:
        dir = "README.md"
        with open(topic + "/" + dir, "r", encoding='utf-8') as local_readme_fd:
            content = local_readme_fd.read()
        content = update_links(content, topic)
        content = update_titles(content, depth)
        content = replace_special_words(content, special_words)
        output_write(content)

    # For each subdirectory, add the title and the content of the subtopic
    for dir in directories:
        if not dir.startswith(".") and not dir.startswith("_") and not dir == "Tools":
            output_write("\n\n##" + "#" * depth + " " + dir + "\n\n")
            add_topic(topic + "/" + dir, depth=depth+1)
            output_write("\n\n")

def main() -> None:
    """
    Main function.
    Generates the root markdown file.
    """

    # Reset the README.md file
    with open(OUTPUT_MD_FILE, "w", encoding='utf-8') as output_fd:
        output_fd.write("")

    # Introduction
    add_topic("Introduction")

    # Add auto generated warning
    output_write("\nThis file is auto generated using [build.py](build.py). To update it, update the README.md files in the subdirectories and run the build.py script.\n")

    # Table of Contents
    output_write("\n# Table of Contents\n")
    for topic in TOPICS:
        output_write("* [" + topic + "](#" + topic.lower().replace(" ", "-") + ")\n")

    # For each topic, add the topic name and the links to the README.md file
    for topic in TOPICS:
        output_write("\n<br><br>\n\n# " + topic + "\n\n")
        add_topic(topic)

if __name__ == "__main__":
    main()