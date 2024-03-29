from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from sqlite3 import Connection, connect as db
from sqlalchemy import inspect
from .main import grels, save, Structure, inRels, mergeTwo
import json
import os

class Note(Structure):
    __name__ = "note"
    fillable = ["Content", "NoteId", "Title", "tagmap_collection.tag.Name as tag"]


class Base(Structure):
    pass
def merge(conn: Connection, conn2: Connection, outpath, close):
    "Merge Notes from JW Library"
    def createSession(con: Connection, startingTable: str):
        engine = create_engine("sqlite://", creator=lambda: con)
        base = automap_base()
        base.prepare(engine, reflect=True)
        session = Session(engine)
        note = base.classes[startingTable]
        q = session.query(note)
        relations = grels(note)
        tables = q.join(
            relations[0].class_attribute
        ).all()  # ONLY ONE RELATION TO PRIMARY TABLE [0]
        return {
            "tables": tables,
            "relations": relations
        }
    session = createSession(conn, "Note")
    session2 = createSession(conn2, "Note")
    with open(outpath, "w") as f:
        f.write("[\n")
        mergeTwo(
            session,
            session2,
            outpath,
            lambda x: f.write(f"\t{json.dumps(x,indent=4)},\n"),
            Note,
        )
        f.write("]")
def list(conn: Connection, conn2: Connection, outpath, close):
    global route
    route = ""
    """list"""
    engine = create_engine("sqlite://", creator=lambda: conn)
    for i, x in enumerate(inspect(engine).get_table_names()):
        print(f"{i} \{x}")
    selected = input("Select table: ")
    while not selected in inspect(engine).get_table_names():
        print("Do not exists")
        selected = input("Select table: ")
    base = automap_base()
    base.prepare(engine, reflect=True)
    route = selected
    def printTable(table, columns=True, primary=True):
        global route
        if(columns):
            print("Columns: ")
            for i, x in enumerate(table.__table__.columns):
                print("\t", i, " /", x.name, "-", str(x.type))
        print("(In)Joins: ")
        joins = grels(table)
        for i, x in enumerate(joins):
            print("\t", i, " /", x.key)
        join = input("Select join: ")
        while not join in [x.key for x in joins]:
            join = input("Select join: ")
        route += f".{join}"
        print("ROUTE", route)
        if primary:
            tores = getattr(table, join)
            printTable(tores, False, False)
        else:
            tores = [x for x in joins if x.key == join][0].entity.class_manager.class_
            printTable(tores, True, True)

    printTable(base.classes[selected])


def custom(conn: Connection, conn2: Connection, outpath, close):
    engine = create_engine("sqlite://", creator=lambda: conn)
    base = automap_base()
    base.prepare(engine, reflect=True)
    session = Session(engine)
    selected = input("Select primary table: ")
    while not selected in inspect(engine).get_table_names():
        print("Do not exists, use command 'list'")
        selected = input("Select primary table: ")
    note = base.classes[selected]
    fillable = input("Set fillable columns/joins for",selected)
    Base.__name__ = selected
    Base.fillable = fillable
    
    q = session.query(note)
    with open(outpath, "w") as f:
        f.write("[\n")
        # inst = inspect(x)
        relations = grels(note)
        for rel in relations:
            key = rel.key
            tables = q.join(rel.class_attribute).all()
            save(
                tables,
                relations,
                lambda x: f.write(f"\t{json.dumps(x,indent=4)},\n"),
                Base,
            )
            break
        f.write("]")


def saveNotes(conn: Connection, conn2: Connection, outpath, close):
    """Save all your Notes"""
    engine = create_engine("sqlite://", creator=lambda: conn)
    base = automap_base()
    base.prepare(engine, reflect=True)
    session = Session(engine)
    note = base.classes["Note"]
    q = session.query(note)
    with open(outpath, "w") as f:
        f.write("[\n")
        # inst = inspect(x)
        relations = grels(note)
        for rel in relations:
            key = rel.key
            tables = q.join(rel.class_attribute).all()
            save(
                tables,
                relations,
                lambda x: f.write(f"\t{json.dumps(x,indent=4)},\n"),
                Note,
            )
            break # ONLY ONE RELATION TO PRIMARY TABLE
        f.write("]")


def saveAll(conn: Connection, conn2: Connection, outpath, close):
    """Save All"""
    # cursor = conn.cursor
    # data = conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    # print(data)

    engine = create_engine("sqlite://", creator=lambda: conn)
    base = automap_base()
    base.prepare(engine, reflect=True)
    session = Session(engine)
    Note = base.classes["Note"]
    q = session.query(Note)
    with open(outpath, "w") as f:
        f.write("[\n")
        # inst = inspect(x)
        relations = grels(Note)
        for rel in relations:
            key = rel.key
            tables = q.join(rel.class_attribute).all()
            save(
                tables,
                relations,
                lambda x: f.write(f"\t{json.dumps(x,indent=4)},\n"),
            )
            break
        f.write("]")
