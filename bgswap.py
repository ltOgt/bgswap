#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# <O> :o:
# =============================================== IMPORTS
import sys
import os
import ctypes

# =============================================== GLOBALS
ROOT_DIR=os.path.dirname(os.path.realpath(__file__))
SEP = os.path.sep
IMAGE_TYPES = [
    "png",
    "jpg",
    "jpeg"
]
OPPACITY = 100
DEFAULT = ROOT_DIR+"/.default"
CURRENT = ROOT_DIR+"/.current"


# =============================================== FUNCTIONS
def print_usage():
    print("bgswap (-l|--list) [-v]   List all available wallpapers.")
    print("bgswap (-s|--set)  [NUM]  Set wallpaper (to NUM).")
    print("bgswap (-d|--def)  [NUM]  Set default (to NUM).")
    print("bgswap (-r|--reset)       Reset to default.")
    print("bgswap (-c|--curr)        Print current wallpaper.")
    print("bgswap (-n|--next)        Switch wallpaper to next.")
    print("bgswap (-p|--prev)        Switch wallpaper to previous.")
    print("bgswap (-h|--help)        Print this help message.")


# +-------+
# | PYWAL |
# +-------+
def set_wallpaper(img_path):
    """Set the given path as wallpaper and generate colorprofiles via <wal>."""
    if os.name == "nt":
        # WINDOWS
        ctypes.windll.user32.SystemParametersInfoW(20, 0, img_path, 0)
    else:
        rc = os.system("wal -i "+img_path+" -a "+str(OPPACITY))
        if rc != 0:
            print("Please make sure pywal is installed.")
        else:
            with open(CURRENT, 'w') as c:
                c.write(img_path)


def pad_path(images, i):
    """Pad with 0 to fill up to total number, also remove base path and leading /"""
    return "0" * (len(str(len(images))) - len(str(i))) + str(i) + ": " + images[i].split(ROOT_DIR)[1][1:]


def is_number(number):
    """Check wether a string is a number"""
    try:
        n = int(number)
        return True
    except Exception:
        return False


def get_current():
    """Read in the current wallpaper and its index.

        RETURNS:
            if successful:
                tuple(Index, Current-Path, list(Images))
            otherwise:
                tuple(None, None, None)
    """
    if os.path.isfile(CURRENT):
        with open(CURRENT, 'r') as c:
            curr = c.readline()
        if os.path.isfile(curr):
            images = list_wps(verbose=0)

            res=None
            for i in range(len(images)):
                if curr == images[i]:
                    res = i
                    break

            if res is not None:
                return res, curr, images
            else:
                print("Image does no longer exist in wallpaper diretory: " + curr)
        else:
            print(path + " does no longer exist.")
    else:
        print("No current wallpaper (set by "+__file__+").")
    return None, None, None


def input_until(prompt, func, images):
    """Read in input and react to it until condition specified by func is met.

        prompt:
            (str)
            The message to print when prompting the user for input.
        func:
            (callable(input)->boolean)
            The condition when to return.
        images:
            (list(str))
            The list containing all image paths.

        RETURNS:
            The input that meets the requirements established by func.
    """
    print()
    _input = input(prompt)
    while not func(_input):
        if type(_input) is str:
            if _input == "":
                print("Exit.")
                sys.exit()
            # see if part of path
            for i in range(len(images)):
                if _input in images[i]:
                    print(pad_path(images, i))
        print()
        _input = input(prompt)
    return _input


def list_wps(root=ROOT_DIR, verbose=0, _recursion=0):
    """Generate a list containing all images under the root directory.

        root:
            (str)
            The root directory to search.
            Used espeacially for DFS directory recursion.
        verbose:
            (int)
            0: Build list only, no prints.
            1: Build list and print it with numbers.
            2: Build list and additionaly print the search.
        _recursion:
            (int)
            Used internally for recursion control and verbose printing.

        RETURNS:
            A list containing all image paths.
    """
    images = []
    for item in os.listdir(root):
        path = root + SEP + item
        t = "? "
        if os.path.isfile(path):
            t = "f "
        elif os.path.isdir(path):
            t = "d "
        elif os.path.islink(path):
            t = "l "

        if verbose == 2:
            print("."*_recursion + t + path)

        if t == "d ":
            images += list_wps(root=path, verbose=verbose, _recursion=_recursion+1)
        elif t == "f " and path.split(".")[-1].lower() in IMAGE_TYPES:
            images += [path]

    if verbose == 2:
        print()
    if verbose and _recursion == 0:
        for i in range(len(images)):
            print(pad_path(images, i))

    return images


def set_default(img_path):
    """Store the given path as default."""
    with open(DEFAULT, 'w') as d:
        d.write(img_path)
    print("Done.")


def select_image(args, func=set_wallpaper, prompt="Set wallpaper to number: ", verbose=1):
    """Loop over images and promt user to select one.
        args:
            (list(str))
            Commandline arguments.
        func:
            (callable(selection))
            Action to perform on selection.
        prompt:
            (str)
            The message to print when prompting the user for input.
        verbose:
            (int)
            0: Build list only, no prints.
            1: Build list and print it with numbers.
            2: Build list and additionaly print the search.

        RETURNS:
            Nothing, calls func instead.
    """
    if len(args) < 2:
        # Get paths of all images
        images = list_wps(verbose=verbose)
        # Select image
        n = int(
            input_until(
                prompt=prompt,
                func=lambda _input: is_number(_input),
                images=images
        ))
    else:
        images = list_wps(verbose=0)
        n = int(args[1])

    if n < len(images) and n >= 0:
        func(images[n])
    else:
        print(str(n) + " does not exists.")


def main():
    """Parse command line arguments."""
    args = sys.argv[1:]

    if not args:
        print_usage()
        sys.exit(1)

    if args[0] in ["-h","--help"]:
        print_usage()

    elif args[0] in ["-l","--list"]:
        if len(args) < 2:
            # print only enumeration after recursions
            verbose=1
        elif args[1] == "-v":
            # print extra verbose (all found files and dirs)
            verbose=2
        else:
            print("<{}> not a valid option. Try --help.".format(args[1]))
            return

        images = list_wps(verbose=verbose)
        _ = input_until(prompt="Search results (ENTER to exit): ", func=lambda _input: _input == "", images=images)

    elif args[0] in ["-s","--set"]:
        select_image(args=args, func=set_wallpaper, prompt="Set wallpaper to number: ")

    elif args[0] in ["-d","--def"]:
        select_image(args=args, func=set_default, prompt="Set default to number: ")

    elif args[0] in ["-r","--reset"]:
        if os.path.isfile(DEFAULT):
            with open(DEFAULT, 'r') as d:
                path = d.readline()
            if os.path.isfile(path):
                set_wallpaper(path)
            else:
                print(path + " does not exist. Try --help.")
        else:
            print("No default set. Try --help.")

    elif args[0] in ["-c","--curr"]:
        number, path, images = get_current()
        if not number is None:
            print(str(number) + ":\n" + path)

    elif args[0] in ["-n","--next"]:
        number, path, images = get_current()
        if not number is None:
            set_wallpaper(images[(number + 1) % len(images)])

    elif args[0] in ["-p","--prev"]:
        number, path, images = get_current()
        if not number is None:
            set_wallpaper(images[(number - 1) % len(images)])

    else:
        print("<{}> not a valid option. Try --help.".format(args[0]))


# =============================================== ENTRY
if __name__ == '__main__':
    main()

