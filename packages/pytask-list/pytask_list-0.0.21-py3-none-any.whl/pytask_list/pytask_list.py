import typer
from rich.console import Console
from rich.table import Table
from model import Todo  # Assuming this file defines the Todo class
from database import get_all_task, remove_task, insert_task, done_task, update_task

console = Console()

app = typer.Typer()


@app.command(short_help='add a task for task/category')
def add(task: str, category: str):
    """
    Want to organize your ideas/tasks for today? Then add it here and organize your day
    """

    to_do = Todo(task, category)
    insert_task(to_do)
    show()
    typer.echo(f"\nAdded task: {task}, in the {category} category")

@app.command(short_help="Remove a task from your To-Do list")
def remove(position: int):
    """
    Don't wanna continue with this task? Remove it here
    """

    remove = typer.confirm("Are you sure you wanna delete it?")
    if not remove:
        typer.echo("Removal canceled")
        raise typer.Abort()
    typer.echo(f"Deleting task at position {position}")
    remove_task(position - 1)
    show()

@app.command(short_help="Update a task from your To-Do list")
def update(position: int, task: str = None, category: str = None):
    """
    have you made any changes to your task? Update it here
    """

    typer.echo(f"Updating task at position {position} with {task} and category of : {category}")
    update_task(position - 1, task, category)
    show()

@app.command(short_help="See all tasks on your To-Do list.")
def show():
    """
    See all tasks on your To-Do list.
    Want to see what's hot today? See all your tasks here!
    """

    tasks = get_all_task()
    console.print("\n[bold magenta]Your To-Do List:[/bold magenta]\n",)

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("ID", style="dim", width=6, justify="center")
    table.add_column("To do", min_width=20, justify="center")
    table.add_column("Category", min_width=12, justify="center")
    table.add_column("Done", min_width=12, justify="center")

    def get_category_color(category):
        """
        Assigns a color based on the category (optional).
        """
        COLORS = {'FrontEnd': 'cyan', 'Youtube': 'red', 'Work': 'purple', 'BackEnd': 'green'}
        if category in COLORS:
            return COLORS[category]
        return 'white'

    for id, task in enumerate(tasks, start=1):
        color = get_category_color(task.category)
        is_done = '✅' if task.status == 2 else '❌'
        table.add_row(str(id), task.task, f'[{color}]{task.category}[/{color}]', is_done)
    console.print(table)

@app.command(short_help="A checker for tasks done.")
def task_done(position: int):
    """
    Have you finished your task? Check your completed task here!
    """

    typer.echo(f"The Task in position: {position} has been sucessufully completed")
    done_task(position - 1)
    show()

if __name__ == "__main__":
  app()

