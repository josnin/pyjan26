import os
import glob
import sass
import shutil
from pyjan26.registry import register_post_build
from pyjan26.core import settings

### START Post build ########
def scss_to_css():
    for pattern in settings.CSS_SCSS_PATTERNS:
        scss_files = glob.glob(os.path.join(settings.CONTENT_DIR, pattern))
        for scss_file in scss_files:
            with open(scss_file, 'r') as file:
                scss_content = file.read()
            #convert scss to css using libsass
            css_content = sass.compile(string=scss_content, output_style='expanded')
            css_file = f'{os.path.splitext(scss_file)[0]}.css'

            #write the scss content to output file
            with open(css_file, 'w') as file:
                file.write(css_content)
        
            print(f'SCSS generated at {css_file}')

            destination_path = css_file.replace(settings.CONTENT_DIR, settings.OUTPUT_DIR)
            print(f'Copying css files from {css_file} to {destination_path}...')
            os.makedirs(os.path.dirname(destination_path), exist_ok=True)
            shutil.copy(css_file, destination_path)


register_post_build([scss_to_css])
### END Post build ########