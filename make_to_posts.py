import os
import re

# Set the directory where the markdown files are located
folder_path = "docs"  # Update this with your folder path

# Function to add front matter to a file


def add_front_matter(file_path, category, parent=None):
    # Skip if the file is 'index.md', since it should not have a category for the top-level
    if file_path.endswith("index.md"):
        return

    # Extract the filename (without extension)
    filename = os.path.basename(file_path)
    title = os.path.splitext(filename)[0]  # Get filename without extension

    # Read the current content of the file
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    # Check if front matter with title already exists
    if re.search(r"^---\s*\ntitle:\s*" + re.escape(title) + r"\s*\n", content, re.MULTILINE):
        print(f"Front matter already exists for: {file_path}")
        return  # Exit if title already exists

    # Create the front matter with the title and category
    front_matter = f"---\ntitle: {title}\nparent: {category}\n"

    if parent:
        front_matter += f"parent: {parent}\n"  # Add parent field if provided

    front_matter += "---\n\n"

    # Add front matter at the beginning of the file
    new_content = front_matter + content

    # Write the updated content back to the file
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(new_content)
    print(f"Added front matter to: {file_path}")

# Function to add an empty index.md file in subfolders if it does not exist


def add_empty_index_file(folder_path, parent=None):
    # Check if there is an index.md file in the folder
    index_file_path = os.path.join(folder_path, "index.md")
    if not os.path.exists(index_file_path):
        # Create an empty index.md with the folder name as the title (no category)
        folder_name = os.path.basename(folder_path)
        front_matter = f"---\ntitle: {folder_name}\n"

        if parent:
            front_matter += f"parent: {parent}\n"  # Add parent if provided

        front_matter += "---\n\n"

        with open(index_file_path, "w", encoding="utf-8") as file:
            file.write(front_matter)
        print(f"Created empty index.md in: {folder_path}")
    else:
        print(f"index.md already exists in: {folder_path}")


# Iterate through all files in the folder
for root, dirs, files in os.walk(folder_path):
    # Get the name of the current folder (for category)
    folder_name = os.path.basename(root)

    # Add front matter to markdown files (except index.md files)
    for file in files:
        if file.endswith(".md"):  # You can change this to match other file types if needed
            file_path = os.path.join(root, file)
            add_front_matter(file_path, folder_name)

    # Add empty index.md file in subfolders if necessary
    for dir in dirs:
        subfolder_path = os.path.join(root, dir)

        # Determine the parent folder (if it's not the top level)
        parent_folder = folder_name if os.path.basename(
            root) != os.path.basename(folder_path) else None

        add_empty_index_file(subfolder_path, parent=parent_folder)

print("Finished processing all files and subfolders.")
