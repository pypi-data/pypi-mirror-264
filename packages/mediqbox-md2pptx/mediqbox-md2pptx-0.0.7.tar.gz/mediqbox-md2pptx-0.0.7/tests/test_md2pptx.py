import os

from mediqbox.md2pptx import (
  Md2pptx,
  Md2pptxConfig,
  Md2pptxInputData
)

def test_md2pptx():
  base_dir = os.path.dirname(__file__)
  data_dir = os.path.join(base_dir, 'data')
  template_dir = os.path.join(base_dir, 'templates')
  result_dir = os.path.join(base_dir, 'test_results')

  md_file = os.path.join(data_dir, 'Francesco.md')
  template_file = os.path.join(template_dir, 'default.pptx')
  pptx_file = os.path.join(result_dir, 'Francesco.pptx')

  pptx_creator = Md2pptx(Md2pptxConfig(template=template_file))
  result = pptx_creator.process(Md2pptxInputData(
    working_dir=base_dir, md_file=md_file, pptx_file=pptx_file
  ))

  assert result

if __name__ == '__main__':
  test_md2pptx()