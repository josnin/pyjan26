import os
import shutil
import pkgutil
import pkg_resources
import argparse
from importlib import import_module
from pyjan26.core import PyJan26


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
        for filename in ["settings.py", "custom_collections.py", "custom_filters.py", "custom_pages.py",
        "_content/index.md", "_templates/base.html"]:
            file_content = pkgutil.get_data(__name__, f"project_structure/{filename}").decode("utf-8")
            file_path = os.path.join(project_name, filename)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w") as file:
                file.write(file_content)
        
        print(f"Project '{project_name}' created successfully.")
    except Exception as e:
        print(f"Error creating project '{project_name}': {e}")


#def generate_file(file_path: str, default_file: str) -> None:
#
#    if not os.path.exists(file_path):
#        default_path = pkg_resources.resource_filename(__name__, default_file)
#        shutil.copy(default_path, file_path)
#        print(f"Created {file_path} from {default_path}")

def main():
    parser = argparse.ArgumentParser(description="PyJan26 Command Line Interface")
    parser.add_argument("command", choices=["s", "g"], help="Command to execute: 's' for startproject, 'g' for generate")
    parser.add_argument("project_name", nargs="?", help="Name of the project")

    args = parser.parse_args()

    if args.command == "s":
        start_project(args.project_name)
    elif args.command == "g":
        #generate_file('custom_pages.py', 'default_custom_pages.py')
        #generate_file('custom_collections.py', 'default_custom_collections.py')
        #generate_file('custom_filters.py', 'default_custom_filters.py')

        custom_pages_module = os.environ.setdefault('PYJAN26_PAGES_MODULE', 'custom_pages')
        collections_module = os.environ.setdefault('PYJAN26_COLLECTIONS_MODULE', 'custom_collections')
        filters_module = os.environ.setdefault('PYJAN26_FILTERS_MODULE', 'custom_filters')

        import_module(custom_pages_module) # type: ignore
        import_module(collections_module) # type: ignore
        import_module(filters_module) # type: ignore

        gen = PyJan26()
        gen.generate_site()

if __name__ == '__main__':
    main()

