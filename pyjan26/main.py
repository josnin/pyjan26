import os
import shutil
import pkgutil
import pkg_resources
import argparse
from importlib import import_module


def start_project(project_name):
    # Check if project name is provided
    if not project_name:
        print("Error: Project name is required.")
        return

    # Check if project directory already exists
    if os.path.exists(project_name):
        print(f"Error: Project directory '{project_name}' already exists.")
        return

    try:
        # Create project directory
        os.makedirs(project_name)
        
        # Get package path
        package_path = os.path.dirname(__file__)
        
        # Copy default files from package to project directory
        for filename in ["settings.py", "_content/index.md", "_templates/base.html"]:
            file_content = pkgutil.get_data(__name__, f"project_structure/{filename}").decode("utf-8")
            file_path = os.path.join(project_name, filename)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w") as file:
                file.write(file_content)
        
        print(f"Project '{project_name}' created successfully.")
    except Exception as e:
        print(f"Error creating project '{project_name}': {e}")


def main():
    parser = argparse.ArgumentParser(description="PyJan26 Command Line Interface")
    parser.add_argument("command", choices=["s", "g", "c"], help="Command to execute: 's' for startproject, 'g' for generate, 'c' for copy template/static plugins")
    parser.add_argument("project_name_or_files", nargs="?", help="Project Name (only for 's' command) or Include files to generate (only for 'g' command)")

    args = parser.parse_args()

    if args.command == "s":
        start_project(args.project_name_or_files)
    elif args.command == "c":
        from pyjan26.core import copy_plugin_files, settings
        copy_plugin_files(settings.PLUGIN_MODULES, settings.CONTENT_DIR)
    elif args.command == "g":
        from pyjan26.core import PyJan26, get_markdown_files, settings
        for plugin in settings.PLUGIN_MODULES:
            import_module(plugin)

        files = get_markdown_files(args.project_name_or_files)
        gen = PyJan26(files)
        gen.generate_site()


if __name__ == '__main__':
    main()

