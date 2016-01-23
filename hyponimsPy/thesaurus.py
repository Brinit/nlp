import pymysql.cursors
import re

db = pymysql.connect(host="localhost",
                     user="root", 
                     passwd="",
                     charset="utf8",
                     db="rutez_lemma")
cur = db.cursor()

def find_hyponims(concepts):
	ret = []
	for concept in concepts:
		query = "SELECT label FROM concept_label WHERE concept_id IN \
					(SELECT concept1_id FROM concept_link WHERE concept_relation_id = 3 AND concept2_id IN \
						(SELECT concept_id FROM concept_label WHERE label = '"+ re.escape(concept) +"' ))"
		try:
			cur.execute(query)
			db.commit()
			for hyponim in cur.fetchall():
				if hyponim[0] in concepts and hyponim[0] != concept:
					ret.append((concept, hyponim[0]))
				
		except ProgrammingError as e:
		    print('Got error {!r}, errno is {}'.format(e, e.args[0]))

	return ret

if __name__ == "__main__":
	print(find_hyponims(['ЭКЗЕМПЛЯР']))