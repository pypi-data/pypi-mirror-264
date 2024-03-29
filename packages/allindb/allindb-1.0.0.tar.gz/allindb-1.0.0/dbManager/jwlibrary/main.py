from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from sqlite3 import Connection
from sqlalchemy import inspect
from abc import ABC, abstractmethod, abstractclassmethod


def grels(table):
    try:
        inst = inspect(table)
        return [x for x in inst.mapper.relationships]
    except Exception as e:
        return None


class Structure(ABC):
    @property
    @abstractmethod
    def fillable(self):
        pass

    @property
    @abstractmethod
    def __name__(self):
        pass

    @abstractclassmethod
    def getOwn(self):
        return [x for x in self.fillable if not "." in x]

    @abstractclassmethod
    def getRels(self, level: int):
        level += 1
        final = []
        for l in [x for x in self.fillable if "." in x]:
            statement = None
            if " as " in l:
                statement = l.split(" as ", 1)[1]
                l = l.split(" as ", 1)[0]
            try:
                final.append(
                    {"value": l.split(".")[level - 1 : level][0], "alias": statement}
                )
            except:
                final.append({"value": l.split(".")[-2:-1][0], "alias": statement})
        return final


def inRels(y, gotRels):
    for x in gotRels:
        if x["value"] == y:
            return x
    return False


def cleanUp(b, gotRels, condition=lambda a: False):
    for a in b:
        if condition(a) or not bool(inRels(a.key, gotRels)):
            b.remove(a)

def generator(tables, relations, structure: Structure = None):
    cleanUp(relations, structure.getRels(0))
    for table in tables:
        global previousClasses
        previousClasses = set()
        innerClasses = set()

        def search(table, rels):

            result2 = {}
            for col in table.__table__.columns:
                if col.name in structure.getOwn() and len(col.foreign_keys) == 0:
                    result2[col.name] = getattr(table, col.name)

            def getSearch(res2, pastLevel=0, isList: bool = False):
                if res2 is None:
                    raise IndexError()
                gotRels = structure.getRels(pastLevel)

                res3 = {}
                b = grels(res2)
                if pastLevel > 1:
                    pass
                cleanUp(
                    b,
                    gotRels,
                    lambda a: (
                        a.mapper.class_manager.class_ in previousClasses
                        or a.mapper.class_manager.class_ in innerClasses
                    ),
                )
                rels2 = [x.key for x in b]
                for col in res2.__table__.columns:
                    if len(col.foreign_keys) == 0:
                        # if bool(inRels(col.name)):
                        #     print(col.name)
                        condition = col.name in structure.getOwn()
                        if pastLevel > 0:
                            condition = bool(inRels(col.name, gotRels))
                        else:
                            pass
                        if condition:
                            res3[col.name] = getattr(res2, col.name)
                pastLevel += 1
                for rel2 in rels2:
                    try:
                        innerClasses.add(res2.__class__)
                        tores2 = getattr(res2, rel2)
                        if isinstance(tores2, list):
                            if len(tores2) == 0:
                                raise IndexError()
                        res3[rel2] = getSearch(tores2, pastLevel)
                    except Exception as e:
                        continue
                innerClasses.clear()
                if not bool(res3):
                    if type(res2).__name__ == "Tag":
                        pass
                    raise ValueError()
                return res3

            for col in [x.key for x in relations]:
                pastLevel = 0
                try:
                    previousClasses.add(table.__class__)
                    res4 = getattr(table, col)
                    pastLevel = 1
                    irr = inRels(col, structure.getRels(0))
                    if bool(irr) and isinstance(res4, list):
                        if not hasattr(
                            result2, irr["alias"] if bool(irr) else col.name
                        ):
                            result2[irr["alias"] if bool(irr) else col.name] = []
                        for l in res4:
                            try:
                                result2[irr["alias"] if bool(irr) else col.name].append(
                                    getSearch(l, pastLevel, True)
                                )
                            except Exception as e:
                                pass
                    else:
                        result2[col] = getSearch(res4, pastLevel)
                except Exception as e:
                    continue
            # if hasattr(result2, "tagmap_collection"):
            #     pass
            return result2

        yield search(table, relations)
def save(tables, relations, callback=None, structure: Structure = None):
        for result in generator(tables, relations, structure):
            if callable(callback):
                callback(result)
def mergeTwo(session1, session2, outpath, callback = None, structure: Structure = None):
    """Tengo que hacer ingenería inversa para crear notas en JW Library..."""
    for result in generator(session1["tables"], session1["relations"], structure):
        if callable(callback):
            callback(result)
        found = False
        for result2 in generator(session2["tables"], session2["relations"], structure):
            if not found and result2["Title"] != result["Title"]:
                found = True
            else:
                found = False
        if callable(callback) and found:
            callback(result2)