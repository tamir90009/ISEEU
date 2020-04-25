import os

def main():
    addval = "/test/virus"
    if os.environ.get("LD_LIBRARY_PATH", None):
        os.environ["LD_LIBRARY_PATH"] = os.environ["LD_LIBRARY_PATH"] + ":" + addval
    else:
        os.environ["LD_LIBRARY_PATH"] = addval


if __name__ == "__main__":
    main()