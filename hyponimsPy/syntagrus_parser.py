from sentence import Sentence
from lxml import etree

def serialize_sentences(input_file):
	f_in = open(input_file, 'rb')
	sentences = []

	context = etree.iterparse(f_in, tag='S')
	for event, sentence_elem in context:
		sent_obj = Sentence()
		for word_elem in sentence_elem.iter('W'):
			idx = word_elem.attrib['ID']
			lemma = word_elem.attrib['LEMMA']
			sent_obj.add_word(lemma, int(idx))

			dom = word_elem.attrib['DOM']
			if  dom != '_root':
				link_type = word_elem.attrib['LINK']
				sent_obj.add_link(int(idx), int(dom), link_type)
		sentences.append(sent_obj)

	return sentences



if __name__ == "__main__":
	res = serialize_sentences("/home/venefica/Documents/progTasks/build-hyponimsPatterns-Desktop-Debug/syntagrus/SynTagRus2015/2003/Anketa.tgt")
