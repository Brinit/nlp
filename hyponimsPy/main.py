import os.path
import syntagrus_parser
import thesaurus

corpus_path = "/home/venefica/syntagrus"

if __name__ == "__main__":
	with open(os.path.join(corpus_path, "syntagrus_list.txt")) as f:
		for line in f:
			fpath = os.path.join(corpus_path, line.strip())
			print (line.strip())
			sent_list = syntagrus_parser.serialize_sentences(fpath)

			for sent in sent_list:
				hyponims = thesaurus.find_hyponims(sent.words)
				if len(hyponims) > 0:
					print(hyponims)
					for h_pair in hyponims:
						print(sent.get_paths(h_pair[0], h_pair[1]))