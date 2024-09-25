# DiffSinger Project Converter
A utility to convert DiffSinger Project (.ds) files to dsinfer input data

## Getting Started
### Environments and dependencies
* Python 3.7 or later
* Dependencies (can be installed using `pip` or `conda`)
  * numpy

### Usage
```bash
python3 main.py -i /path/to/project.ds -o /path/to/output/directory
```
#### Command Line Arguments
These command line arguments can be used for specifying input and output files.

| Argument             | Description              | Required | Example                           |
|----------------------|--------------------------|----------|-----------------------------------|
| `-i`<br />`--input`  | Path to input `.ds` file | Yes      | `-i /home/apple/myproject.ds`     |
| `-o`<br />`--output` | Path to output directory | Yes      | `-o /home/apple/myproject_dsinfer |


## License
* This project is licensed under **MIT License**.