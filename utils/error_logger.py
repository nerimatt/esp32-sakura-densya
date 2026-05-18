import os

def exists(filename):
    try:
        os.stat(filename)
        return True
    except OSError:
        return False

# save any errors in sd/errors.txt
# must be the complete error saved from the logger -> include filename and line
def error_logger(error) -> bool:
    if not exists("sd/"):
        print("sd card not mounted")
        return False

    if not exists("sd/errors.txt"):
        print("creating error log file...")
        open("sd/errors.txt", "w").close()

    with open("sd/errors.txt", "a") as errorfile:
        errorfile.write("----- ERROR -----\n" + error + "\n-----------------\n\n" )
    print("error saved to sd/errors.txt")



if __name__ == "__main__":
    from utils.mount_sd_card import mount_sd_card
    mount_sd_card()

    error_logger("hello")
