# Task List App with Typer, Rich and Python

## Introduction

This document describes a task list application developed with Typer and documented in Markdown. Typer is a Python library that makes it easy to create interactive command line interfaces, while Markdown is a lightweight markup language for text formatting.

### Application Features

The application offers the following functionalities:

* **Add tasks:** Add new tasks to the list with name and category.
* **Remove tasks:** Delete tasks from the list by position.
* **Update tasks:** Modify the name or category of a task.
* **Show all tasks:** Display all tasks in a formatted table.
* **Mark tasks as done:** Mark tasks as completed with a visual indicator.

#### Feature options

Install completion for the current shell (bash, fish, zsh and etc...)

	 $ --install-completion

Show completion for the current shell, to copy it or customize the installation. 
	
	 $  --show-completion
	

Show information that can help you and then exit this option
	
	 $ --help
	

### Example of using CLI commands

#### 1. Command Add
Add a new task to the list.

**Arguments:**

 `task`:  Name of the task.
 
 `category`:  Category of the task.

**Example:**

**For use with Python**
	
	 $ python pytask_list.py add "Task 1" "category 1"
	

#### 2. Command Remove
Delete a task from the list by position.

**Arguments:**

`position`: Position (ID) of the task in the list (starting at 1).

**Example:**

**For use with Python**
	
	 $ python pytask_list.py remove 1 
	

#### 3. Command Update
Modify the task or category of a task.

**Arguments:**

`position`: Position of the task in the list (starting at 1).

`task`: New name of the task (optional).

`category`: New category of the task (optional).

**Example:**

**For use with Python**
	
	 $ python pytask_list.py update 1 "Buy bread, milk and fruits" House
	

#### 4.  Command Show
Display all tasks in a formatted table.

**Example:**
    
	| ID | Task  | Category | Completed |
	| 1 | Study_sql | Database | Done ✅ |
	| 2 | Study_bash | DevOps | Pendent ❌ |

#### 5. Command task-done
Mark a task as completed.

**Arguments:**

`position`: Position of the task in the list (starting at 1).

**Example:**

**For use with Python**
	
	 $ python pytask_list.py task_done 1
	

## License
This project is licensed under the MIT License. This permissive license allows you to freely use, modify, and distribute the code for any purpose, commercial or non-commercial. A copy of the MIT License can be found in the `LICENSE` file within this repository.

##  Acknowledgements
I appreciate the contributions of these open-source projects that made this application possible (.i.g Typer, Rich, Python's community). Beacuse encourage you to contribute to this project and help me improve it!
