import sys
from pathlib import Path
import psycopg2
from datetime import datetime

db_string = "postgres://search:search123@localhost/search"

sql_doc = "SELECT id,timestamp FROM document WHERE url=%s;"
sql_doc_ins = "INSERT INTO document (url,timestamp) VALUES (%s, %s) RETURNING id"
sql_doc_upd = "UPDATE document SET timestamp = %s WHERE id=%s"
sql_term = "SELECT id FROM term WHERE value=%s"
sql_term_ins = "INSERT INTO term (value) Values (%s) RETURNING id"
sql_term_doc_ins = "INSERT INTO term_doc values (%s, %s, %s)"
sql_term_doc_del = "DELETE FROM term_doc WHERE docid=%s"


def get_words(file):
    with file.open('r') as fd:
        txt = fd.read()
        words = txt.split()
        return words


def parse_document(file):
    file_timestamp = datetime.fromtimestamp(file.lstat().st_mtime)
    with conn.cursor() as cur:
        cur.execute(sql_doc, [str(file)])
        if cur.rowcount == 0:
            print("Adding document " + str(file))
            cur.execute(sql_doc_ins, [str(file), file_timestamp])
            doc_id = cur.fetchone()[0]
        else:
            row = cur.fetchone()
            doc_id = row[0]
            timestamp = row[1]
            if not timestamp == file_timestamp:
                print("Updating document " + str(file))
                cur.execute(sql_doc_upd, [file_timestamp, doc_id])
                cur.execute(sql_term_doc_del, [doc_id])
            else:
                return

        pos = 0
        words = get_words(file)
        for word in words:
            cur.execute(sql_term, [word])
            if cur.rowcount == 0:
                cur.execute(sql_term_ins, [word])
            term_id = cur.fetchone()[0]

            cur.execute(sql_term_doc_ins, (doc_id, term_id, pos))
            pos = pos+1
        conn.commit()


if len(sys.argv) < 2:
    print("Usage: indexer.py <folder to scan>")
    exit(1)
result = list(Path(sys.argv[1]).rglob("*"))
with psycopg2.connect(db_string) as conn:
    for file in result:
        if file.is_file():
            parse_document(file)
