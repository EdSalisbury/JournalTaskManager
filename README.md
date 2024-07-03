# Journal Task Manager

Manage and update your journal entries and tasks with this Python script. Automatically generate daily journal entries, update task statuses, and carry over unfinished tasks to the next day.

## Features

- Auto-generate daily journal entries from a template
- Mark tasks as finished
- Carry over unfinished tasks
- Organize tasks by category

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/edsalisbury/journal-task-manager.git
    cd journal-task-manager
    ```

2. Ensure you have Python installed (version 3.6 or higher).

3. Install any required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Customize the paths in `journal_task_manager.py`:
    ```python
    script_path = os.path.realpath(sys.argv[0])
    notes_path = os.path.normpath(os.path.join(script_path, "..", "..", "..", "Notes"))
    journal_path = os.path.join(notes_path, "Journal")
    template_path = os.path.join(journal_path, "template.md")
    ```

2. Ensure you have a template file located at `template.md` with placeholders for `{DATE}` and `{TASKS}`.

3. Run the script:
    ```bash
    ./journal_task_manager.py
    ```

## File Structure

- `journal_task_manager.py`: Main script
- 
