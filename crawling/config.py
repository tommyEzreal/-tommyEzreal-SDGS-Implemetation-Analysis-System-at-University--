import argparse

def define_argparser():
    p = argparse.ArgumentParser()

    p.add_argument(
        "--load_chromedriver_path",
        required=True,
        help="Chromedriver path"
    )

    p.add_argument(
        "--save_path",
        required=True,
        help="Path to save dataset."
    )

    config = p.parse_args()

    return config