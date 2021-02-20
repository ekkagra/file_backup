import os

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
