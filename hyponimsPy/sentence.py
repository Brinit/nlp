class Sentence:
	def __init__(self):
		self.links = []
		self.words = []

	def add_word(self, word, idx):
		if len(self.words) <= idx:
			self.words.extend(['']*(idx-len(self.words)+1))

		self.words[idx] = word #ok, it's actually 1-based, but I can live with it now

	def add_link(self, a, b, link_type):
		self.links.append((a, b, link_type))

	def get_paths(self, a, b):
		a_idxs = []
		b_idxs = []
		for i in range(0, len(self.words)):
			if self.words[i] == a:
				a_idxs.append(i)
			if self.words[i] == b:
				b_idxs.append(i)

		if len(a_idxs) == 0 or len(b_idxs) == 0:
			return []

		paths = []
		for a_idx in a_idxs:
			for b_idx in b_idxs:
				paths.append([])
				a_path = self.get_up_path(a_idx)
				#print(a_path)
				b_path = self.get_up_path(b_idx)
				#print(b_path)
				not_common_i = 0
				for not_common_i in range(1, min(len(a_path), len(b_path))):
					if a_path[-not_common_i] != b_path[-not_common_i]:
						break
				#print(not_common_i)

				for link in a_path[:-not_common_i]:
					paths[-1].append(link)

				for link in reversed(b_path[:-not_common_i]):
					paths[-1].append(link)

				print(len(paths[-1]))

		return paths

	def get_up_path(self, idx):
		path = []
		cur = idx
		end_of_path = False
		while not end_of_path: 
			for link in self.links:
				end_of_path = True 
				if link[0] == cur:
					path.append(link)
					cur = link[1]
					end_of_path = False
					break

		return path




