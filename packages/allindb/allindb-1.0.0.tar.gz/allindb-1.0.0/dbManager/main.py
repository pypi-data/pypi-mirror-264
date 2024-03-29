import zipfile
import os
import sqlite3 as db
import dbManager.jwlibrary
from inspect import getmembers, isfunction
from io import BytesIO
import tempfile
from pathlib import Path
from py3Settings import Attribute, AppSettings as Settings, Option
import argparse
import sys
"""
    JWLIBRARY DB SQLITE RELATIONAL OPENER
"""
def setup():
    isFile = lambda x: os.path.isfile(x)
    isDir = lambda x: os.path.isdir(x)

    return Settings(
        [
            Option(
                "output_dir",
                [Attribute("output_dir", str, os.path.dirname(__file__), isDir)],
            ),
            Option("input_db", [Attribute("input_db", str, "", isFile)]),
            Option("second_db", [Attribute("second_db", str, "", isFile)]),
        ]
    )

def imports(module):
    for val in getmembers(module, isfunction):
        yield val

def main(out=None, file=None, file2=None, settings: Settings = None, args = None):
    def assign(attr):
        if hasattr(args,attr):
            return getattr(args,attr)
        else:
            return None
    optres = None
    normal = None
    if args:
        file = assign("file")
        file2 = assign("file2")
        out = assign("output")
        optres = assign("action")
        normal = assign("normal")

    if not out or not file:
        out = input("Enter output path:")
        if not os.path.isdir(out):
            out = os.path.dirname(__file__)
            print("Selecting default cwd directory")
        file = input("Enter absolute path of file: ")
        while not os.path.isfile(file) or os.stat(file).st_size == 0:
            print("Not a file!")
            file = input("Enter absolute path of file: ")
        file2 = input("Enter absolute path of file 2: ")
        while not os.path.isfile(file2) or os.stat(file2).st_size == 0:
            print("Not a file!")
            file2 = input("Enter absolute path of file 2: ")
    if settings:
        settings.writeSetting("input_db", "input_db", file)
        settings.writeSetting("second_db", "second_db", file2)
    out = os.path.join(out, Path(file2 or file).stem + ".json")
    data = ""
    close = None
    if normal is None:
        normal = input("jwlibrary file or sqlite3? (0,1) ")
        while not normal in ("0", "1"):
            normal = input("jwlibrary file or sqlite3? (0,1) ")
        normal = bool(int(normal))
    connection = None
    connection2 = None
    if not normal:
        # connection = db.connect("file::memory:?cache=shared")
        def connectJw(jw):
            with zipfile.ZipFile(jw, "r") as zip_ref:
                for x in zip_ref.namelist():
                    if not os.path.isdir(x) and x.lower().endswith(".db"):
                        with zip_ref.open(x) as f:
                            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                                data = tmp.name
                                tmp.write(f.read())
                                close = tmp.close
            # data = BytesIO(data).read()
            return db.connect(data)
        connection = connectJw(file)
        if args and args.file2:
            connection2 = connectJw(file2)
    else:
        connection = db.connect(file)
        if args and args.file2:
            connection2 = db.connect(file2)
    options = {}
    for x in imports(jwlibrary):
        options[x[0]] = x[1]
    print("Options: ")
    for i,x in enumerate(options.keys()):
        print(f"\t{i} - {x}")
    if len(options) == 0:
        print("No options!")
        return
    opt = lambda:int(input(f"Select 0-{len(options)-1}: "))
    optres = opt() if not optres else int(optres)
    keys = list(options.keys())
    while not args and optres < 0 and optres > len(keys)-1:
        optres = opt()
    options[keys[optres]](connection, connection2, out, close)
    print("Success!")
    if not args:
        try:
            ask = os.path.abspath(input("Save settings? (<filename>, n)"))
            settings.saveFile(ask)
        except:
            pass


def entry():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a","--file", help="File 1 (Required)")
    parser.add_argument("-b", "--file2", help="File 2 (Optional)", required=False)
    parser.add_argument("-O","--output", help="Output dir")
    parser.add_argument("-z","--action", help="Action")
    parser.add_argument("-n","--normal", help="Mode", type=bool)
    parser.add_argument(
        "-j",
        "--jwlibrary",
        help="Mode",
        type=bool,
        action=argparse.BooleanOptionalAction,
        dest="normal"
    )
    parser.set_defaults(normal=False)
    args = parser.parse_args()
    settings = setup()
    try:
        assert len(vars(args)) == 0
        settings.loadFile("set.json")
        main(
            settings.getSetting("output_dir", None),
            settings.getSetting("input_db", None),
            settings.getSetting("second_db", None),
        )
    except:
        print("Failed to recover settings!")
        print("Must exist a set.json file in execution directory")
        close = ""
        while len(close) == 0 and not len(vars(args)):
            main(settings=settings)
            close = input("close?")
        if len(vars(args)):
            main(args=args)
if __name__ == "__main__":
    entry()    
