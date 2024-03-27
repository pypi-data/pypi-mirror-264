import logging
import os
import random
import string
import subprocess

from pptx import Presentation

from mediqbox.abc.abc_component import *

def add_random_suffix_to_filename(filename: str, length: int=6) -> str:
  suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
  base_name, ext = os.path.splitext(filename)
  return f"{base_name}-{suffix}{ext}"

class Md2pptxConfig(ComponentConfig):
  template: str
  section_title_size: int = 30
  page_title_size: int = 24

class Md2pptxInputData(InputData):
  working_dir: str
  md_file: str
  pptx_file: str

  """
  @model_validator(mode='after')
  def md_file_must_be_in_working_dir(self) -> 'Md2pptxInputData':
    if not (os.path.abspath(os.path.dirname(self.md_file)) ==
            os.path.abspath(self.working_dir)):
      raise ValueError(f"`md_file`({self.md_file}) is not in the `working_dir`({self.working_dir})")
    
    return self
  """

class Md2pptx(AbstractComponent):
  
  def process(self, input_data: Md2pptxInputData) -> bool:
    md_file = input_data.md_file
    pptx_file = input_data.pptx_file
    working_dir = input_data.working_dir

    # Read MD content
    with open(md_file, 'r') as fp:
      md_content = fp.read()

    # Add template info
    md_content = '\n'.join([
      f"template: {self.config.template}",
      f"sectionTitleSize: {self.config.section_title_size}",
      f"pageTitleSize: {self.config.page_title_size}"
    ]) + "\n\n" + md_content

    # Save MD content to a tmp file
    tmp_md_file = os.path.join(
      working_dir,
      add_random_suffix_to_filename(os.path.basename(md_file))
    )
    with open(tmp_md_file, 'w') as fp:
      fp.write(md_content)

    # Create PPTX
    script = os.path.join(
      os.path.abspath(os.path.dirname(__file__)),
      'martin', 'md2pptx.py'
    )
    result = subprocess.run(
      ['python', script, tmp_md_file, pptx_file],
      capture_output=True, text=True, cwd=working_dir
    )

    # Remove the tmp file
    os.remove(tmp_md_file)

    if not result.returncode == 0:
      logging.error(f"md2pptx: {result.stderr}")
      return False
    
    # Remove the first page of the PPTX
    prs = Presentation(pptx_file)
    xml_slides = prs.slides._sldIdLst # Access the underlying XML
    slides = list(xml_slides)
    xml_slides.remove(slides[0])
    prs.save(pptx_file)

    return True