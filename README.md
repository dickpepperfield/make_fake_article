# make_fake_article

Make a fake article adn post it to a wordpress site

# Prerequisites

Python 3.8+
python-venv
Wordpress
jetpack post by email: https://jetpack.com/support/post-by-email/
SMTP Server

# Installation

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

# TODOs

- Split the single file into a proper python application, with module functions.
- add more categories, and rss feeds
- GPU processing
