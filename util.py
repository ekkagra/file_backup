import os
import re
r1 = re.compile(r"^[A-z]:(/|\\)$")

def split_path(pth):
	pth1 = pth.replace('\\','/')
	out = []
	p, file = os.path.split(pth1)
	keep_running = True
	while keep_running:
		parent, child = os.path.split(p)
		out.append(child)
		if parent == "/" or parent == "":
			keep_running = False
		elif r1.match(parent):
			keep_running = False
			out.append(parent)
		else:
			p = parent
	return out[::-1], file


def convert_paths_to_dict(inp_list):
	res = {}
	for f in inp_list:
		file_path = f.strip()
		root_list, file = split_path(file_path)
		current_dict = res
		for i, root in enumerate(root_list):
			if root not in current_dict:
				current_dict[root] = {}
				if i == len(root_list)-1:
					current_dict[root]["_files"] = []
			current_dict = current_dict[root]
		current_dict["_files"].append(file)
	return res


if __name__ == '__main__':
	import sys
	import json
	try:
		input_file = sys.argv[1]
		with open(input_file) as f:
			contents = f.readlines()

		print(contents[:10])
		out_dict = convert_paths_to_dict(contents)
		with open(f"{input_file}_dict.json", 'w') as f:
			json.dump(out_dict, f, indent=4)
	except Exception:
		pass