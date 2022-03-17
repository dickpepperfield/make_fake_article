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
python -m venv make_fake_article
```

Enter the virtual environment and install requisite packages
```bash
cd make_fake_article
source bin/activate
pip install requirements.txt
```

Correct .env file with required values
```bash
cp env.example .env
vim .env
```

