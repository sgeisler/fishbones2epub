# Fishbones II ebook exporter

`fishbones2.py` fetches all available chapters of the Fischbones novel from Jisuk Cho's blog and builds an ebook (epub)
 out of these chapters. You might add a custom cover image.
 
 ```
 $ ./fishbones2.py -h
usage: fishbones2.py [-h] [--cover cover-image] file

Fetch all chapters from Fishbones II and produce an epub file

positional arguments:
  file                 output file

optional arguments:
  -h, --help           show this help message and exit
  --cover cover-image  cover image to use for the ebook
 ```
 
## Example usage:
 
 ```
 $ ls
 cover.jpg fishbones2.py  README.md  requirements.txt
 $ ./fishbones2.py fishbones2.epub --cover cover.jpg 
fetching index ...
found 23 chapters
fetching Chapter 01 ... (1 of 23)
Chapter 01 has 101 paragraphs
fetching Chapter 02 ... (2 of 23)
Chapter 02 has 175 paragraphs
fetching Chapter 03 ... (3 of 23)
Chapter 03 has 113 paragraphs
fetching Chapter 04 ... (4 of 23)
...

 ```