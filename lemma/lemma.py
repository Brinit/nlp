# -*- coding: utf-8 -*-
import re

import mysql.connector as dbc
from pymystem3 import Mystem

def prepare_content(id, analysis):
    gr = analysis['gr']
    wc, gr = tuple(re.split('[=,\,]', gr, 1))
    return id, analysis['lex'], gr, wc

def produce_lemmas(connection, tableName, outputTableName):
    mystem = Mystem()
    cursor = connection.cursor()
    inserter = connection.cursor()

    query = 'DELETE FROM `%s`' % outputTableName
    inserter.execute(query)
    connection.commit()

    query = 'SELECT * FROM `%s`' % tableName
    cursor.execute(query)
    query = 'INSERT INTO `' + outputTableName + '` (`' + tableName + '_id`, `word_class_id`, `lex`, `gr`)' \
            'SELECT %i, `id`, "%s", "%s" FROM `word_classes` WHERE `abbr`="%s"'
    for id, concept, scheme in cursor:
        lemmas = mystem.analyze(concept)
        for lemma in lemmas:
            for analysis in lemma.get('analysis', []):
                inserter.execute(query % prepare_content(id, analysis))
    connection.commit()

    cursor.close()

def main():
    conn_config = {
        'host' : '127.0.0.1',
        'user' : 'root',
        'password' : '***',
        'database' : 'rutez',
        'buffered' : True
    }
    connection = dbc.connect(**conn_config)
    produce_lemmas(connection, 'concept', 'concept_lemma')
    produce_lemmas(connection, 'term', 'term_lemma')
    connection.close()


#if __name__ == 'main':
# try:
#     main()
# except Exception as e:
#     print 'Something wrong: %s' % e
main()