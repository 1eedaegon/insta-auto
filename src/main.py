import configparser
from opt import timed
from opt import config


@timed
def init():
    print("Initialize...")


if __name__ == "__main__":
    init()
    print(config["CRAWL"]["SITE"])
