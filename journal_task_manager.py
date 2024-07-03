#!/usr/bin/env python

import calendar
import datetime
import os
import sys

script_path = os.path.realpath(sys.argv[0])
notes_path = os.path.normpath(os.path.join(script_path, "..", "..", "..", "Notes"))
journal_path = os.path.join(notes_path, "Journal")
template_path = os.path.join(journal_path, "template.md")
current_date = datetime.datetime.now()
yesterday_date = current_date - datetime.timedelta(days=1)

def get_journal_filename(date):
    """Return the filename for the journal entry of a specific date."""
    filename = f"Journal {date.year}-{date.month:02d}-{date.day:02d}.md"
    return os.path.join(journal_path, filename)

def write_journal_entry(output):
    """Write the journal entry to the appropriate file."""
    month = calendar.month_name[current_date.month]
    datestr = f"{month} {current_date.day}, {current_date.year}"
    filename = get_journal_filename(current_date)
    
    output = output.replace("{DATE}", datestr)
    
    if os.path.isfile(filename):
        print(f"Skipping existing {filename}")
        return False

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    try:
        with open(filename, "w") as file:
            print(f"Writing to file {filename}")
            file.write(output)
    except IOError as e:
        print(f"Failed to write to {filename}: {e}")

def load_template(template_path):
    """Load the journal template from the specified path."""
    try:
        with open(template_path, "r") as file:
            return file.read()
    except IOError as e:
        print(f"Failed to read template {template_path}: {e}")
        return ""

def find_task_files(root_dir):
    """Find all 'Tasks.md' files within the root directory."""
    tasks_md_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename == "Tasks.md":
                tasks_md_files.append(os.path.join(dirpath, filename))
    return tasks_md_files

def get_tasks(filename, finished=False):
    """Retrieve tasks from a file, filtering by finished status."""
    tasks = []
    x = get_x(finished)
    try:
        with open(filename, "r") as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith(f"- [{x}] "):
                    task = line.split(f"- [{x}] ")[1]
                    tasks.append(task.strip())
    except IOError as e:
        print(f"Failed to read {filename}: {e}")
    return tasks

def get_x(finished=False):
    """Return the appropriate checkbox mark based on the finished status."""
    return "X" if finished else " "

def get_task_md(task, category="", finished=False):
    """Format a task with markdown syntax."""
    x = get_x(finished)
    if category:
        return f"- [{x}] {task} ({category})\n"
    return f"- [{x}] {task}\n"

def get_unfinished_tasks():
    """Retrieve unfinished tasks from yesterday's journal."""
    filename = get_journal_filename(yesterday_date)
    return get_tasks(filename)

def get_finished_tasks():
    """Retrieve finished tasks from yesterday's journal."""
    filename = get_journal_filename(yesterday_date)
    return get_tasks(filename, finished=True)

def get_tasks_filename(root_dir, category):
    """Construct the filename for tasks within a specific category."""
    return os.path.join(root_dir, category, "Tasks.md")

def read_file(filename):
    """Read the contents of a file."""
    try:
        with open(filename, "r") as file:
            return file.readlines()
    except IOError as e:
        print(f"Failed to read {filename}: {e}")
        return []

def write_file(filename, lines):
    """Write lines to a file."""
    try:
        with open(filename, "w") as file:
            file.writelines(lines)
    except IOError as e:
        print(f"Failed to write {filename}: {e}")

def finish_task(filename, task):
    """Mark a task as finished in the specified file."""
    lines = read_file(filename)
    x = get_x(True)
    updated_lines = []
    for line in lines:
        if line.startswith("- [ ] ") and task in line:
            updated_lines.append(f"- [{x}] {task}\n")
        else:
            updated_lines.append(line)
    write_file(filename, updated_lines)

def split_task(task):
    """Split a task into its name and category components."""
    name, category = task.split(" (")[0], task.split(" (")[1].rstrip(")")
    return name, category

def update_tasks_files(root_dir, finished_tasks):
    """Update tasks files with finished tasks."""
    for task in finished_tasks:
        name, category = split_task(task)
        filename = get_tasks_filename(root_dir, category)
        finish_task(filename, name)

def main():
    """Main function to orchestrate the journal update process."""
    finished_tasks = get_finished_tasks()
    update_tasks_files(notes_path, finished_tasks)

    template = load_template(template_path)
    if not template:
        print("No template loaded, exiting.")
        return

    unfinished_tasks = get_unfinished_tasks()
    task_output = ""

    chosen_tasks = []
    all_task_files = find_task_files(notes_path)
    for file in all_task_files:
        category = os.path.basename(os.path.dirname(file))
        tasks = get_tasks(file)
        for task in tasks:
            if task not in unfinished_tasks:
                chosen_tasks.append(get_task_md(task, category))
                break
    
    for task in chosen_tasks:
        task_output += task

    output = template.replace("{TASKS}", task_output)
    write_journal_entry(output)

if __name__ == "__main__":
    main()
