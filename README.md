# DiffSinger Project Visualizer
A utility to visualize DiffSinger Project (.ds) files

## Getting Started
### Environments and dependencies
* Python 3.7 or later
* Dependencies (can be installed using `pip` or `conda`)
  * numpy
  * matplotlib

### Usage
```bash
python3 main.py -i /path/to/project.ds -o /path/to/output.svg
```
#### Command Line Arguments
These command line arguments can be used for specifying input and output files, and changing the appearance of visualization.

| Argument             | Description                                    | Required | Example                           |
|----------------------|------------------------------------------------|----------|-----------------------------------|
| `-i`<br />`--input`  | Path to input `.ds` file                       | Yes      | `-i /home/apple/myproject.ds`     |
| `-o`<br />`--output` | Path to output image file (`.svg` recommended) | No       | `-o /home/apple.myproject.svg`    |
| `--color-head`       | Color of "head" phonemes (e.g. consonants)     | No       | `--color-head 8c2128`             |
| `--color-body`       | Color of "body" phonemes (e.g. vowels)         | No       | `--color-body d34343`             |
| `--color-f0`         | Color of pitch curve                           | No       | `--color-f0 e0e0e0`               |
| `--color-text`       | Color of texts (lyrics, phonemes)              | No       | `--color-text 000000`             |
| `--width`            | Width of figure                                | No       | `--width 960`                     |
| `--height`           | Height of figure                               | No       | `--height 15`                     |
| `--dpi`              | Dots per inch (DPI) of figure                  | No       | `--dpi 50`                        |
| `--aspect`           | Aspect ratio of figure                         | No       | `--aspect 0.125`                  |
| `--font-name`        | Font file name                                 | No       | `--font-name /path/to/myfont.otf` |
| `--font-size`        | Font size                                      | No       | `--font-size 12`                  |
| `--font-style`       | Font style (normal, bold, italic, ...)         | No       | `--font-style normal`             |
| `--no-f0`            | Do not display pitch curve                     | No       | `--no-f0`                         |

Note:
* If output file path (`-o` or `--output`) is not specified, the output file will be stored in current working directory, in `.svg` format.
* Due to limitations of matplotlib, the output image size (specified by `--width`, `--height` and `--dpi`) cannot be too large.

## License
* This project is licensed under **MIT License**.
* This project includes fonts from [Noto CJK fonts](https://github.com/notofonts/noto-cjk).