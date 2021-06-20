import Helper


if __name__ == '__main__':
    try:
        while True:
            Helper.userLoop()
            if not (input("Would you like to download another clip? [Y/n]: ").lower() == "y"):
                break
    except Exception:
        print("Exception Found!!")