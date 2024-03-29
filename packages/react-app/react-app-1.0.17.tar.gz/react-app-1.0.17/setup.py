from setuptools import setup
from pathlib import Path

cwd = Path(__file__).parent
long_description = (cwd / "README.md").read_text()
setup(
  name="react-app",
  version="1.0.17",
  package_dir={"react_app": "build"},
  package_data={"react_app": ["**/*.*"]},
  long_description=long_description,
  long_description_content_type="text/markdown"
)
