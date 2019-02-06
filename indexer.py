from sqlalchemy import create_engine
from pathlib import Path
import re

db_string = "postgres://search:search123@localhost/search"

db = create_engine(db_string)


def readfile(doc):
    f = open(str(doc), 'r');
    txt = f.read()
    words = txt.split()
    return words

def parseDocument(document):
    res = db.execute("SELECT id FROM document WHERE url='"+str(document)+"'")
    if(res.rowcount == 0):
        db.execute("INSERT INTO document (url,timestamp) VALUES ('"+str(document)+"', NOW())")
        res = db.execute("SELECT id FROM document WHERE url='"+str(document)+"'")
    docID = res.fetchone()[0]

    pos = 0
    words = readfile(document)
    for word in words:
        word = word.replace("'", "''")
        word = word.replace("%", "%%")
        termres = db.execute("SELECT id FROM term WHERE value='"+word+"'")
        if termres.rowcount == 0:
            tid = db.execute("INSERT INTO term (value) Values ('"+word+"')")
            termres = db.execute("SELECT id FROM term WHERE value='"+word+"'")
        termID = termres.fetchone()[0]

        db.execute("INSERT INTO term_doc values ("+str(docID)+","+str(termID)+","+str(pos)+")")
        pos = pos+1



result = list(Path("/home/jnoer/tmp/enron/test/").rglob("*"))
for file in result:
    if not file.is_dir():
        parseDocument(file)


# Create
#db.execute("CREATE TABLE IF NOT EXISTS films (title text, director text, year text)")
#db.execute("INSERT INTO document (url,timestamp) VALUES ('test2.pdf', NOW())")

# Read
#result_set = db.execute("SELECT * FROM document")
#for r in result_set:
#    print(r)

# Update
#db.execute("UPDATE films SET title='Some2016Film' WHERE year='2016'")

# Delete
#db.execute("DELETE FROM films WHERE year='2016'")
