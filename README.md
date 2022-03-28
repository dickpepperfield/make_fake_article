# realfakenews.space
# AI Generated news, posted 4 times a day.

Make a fake article and post it to a wordpress site

# Prerequisites

- Python 3.8+
- python-venv
- Wordpress
- Jetpack post by email: https://jetpack.com/support/post-by-email/
- An SMTP Server

# Installation
### For Linux
Clone the repo

```bash
git clone https://github.com/dickpepperfield/make_fake_article
```

Create the virtual environment
```bash
python3 -m venv make_fake_article
```

Enter the virtual environment and install requisite packages
```bash
cd make_fake_article
source bin/activate 
pip install -r requirements.txt
```

Correct .env file with required values
```bash
cp env.example .env
vim .env
```

------

### For Windows
Clone the repo
```batch
git clone https://github.com/dickpepperfield/make_fake_article
```

Create the virtual environment
```batch
python -m venv make_fake_article
```

Enter the virtual environment and install requisite packages
```batch
cd make_fake_article
Scripts\activate 
pip install -r requirements.txt
```

Correct .env file with required values
```batch
copy env.example .env /a
notepad .env 
```

# Usage
Simple commmand usage

```bash
# With defaults
python make_fake_article.py

# With modifiers
python make_fake_article.py --feed https://www.zdnet.com/au/rss.xml --category Technology
```

Example feeds have been provided in `example_feeds.txt`

First run through may take a while as it downloads the GPT2 dataset.

# Windows and GPU notes

Follow this setup guide
https://www.tensorflow.org/install/gpu

CUDNN Library must be accessible and loaded 
```batch
SET PATH=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.0\bin;%PATH%
SET PATH=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.0\extras\CUPTI\lib64;%PATH%
SET PATH=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.0\include;%PATH%
SET PATH=C:\Program Files\NVIDIA\CUDNN\v8.3\bin;%PATH%
```

# TODOs

- Split the single file into a proper python application, with module functions.
- add more categories, and rss feeds
- GPU processing

# ENV information for CUDA procesing

```powershell
SET PATH=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.6\bin;%PATH%
SET PATH=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.6\extras\CUPTI\lib64;%PATH%
SET PATH=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.6\include;%PATH%
SET PATH=C:\Program Files\NVIDIA\CUDNN\v8.3\bin;%PATH%
```
