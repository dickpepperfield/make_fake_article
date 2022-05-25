import argparse

def get_args(argv=None):
    parser = argparse.ArgumentParser(description='Generate a fake news article and post it.')
    parser.add_argument('-f', '--feed', type=str, default=RSS_FEED, help="The feed to use, in XML format")
    parser.add_argument('-c', '--category', type=str, default='Technology', help="Category of RSS feed, is used for the image search as well.")
    parser.add_argument('-l', '--max-length', type=int, default=GPT_MAX_LEN, help="Number of tokens used in text generation.")
    return parser.parse_args(argv)