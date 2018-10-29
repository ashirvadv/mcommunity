import os

def build_file_path(filename, directory):
	'''Build file path.'''
	result = os.path.join(directory, filename)
	return result

def get_all_sets():
	'''Get all dicts.'''
	directory = os.path.join(os.getcwd(), 'files')
	filenames = os.listdir(directory)
	result = []
	for filename in filenames:
		if 'FAILED' in filename:
			continue
		file_path = build_file_path(filename, directory)
		f = open(file_path, 'r')
		data = f.read()
		result.append(eval(data))
	return result

def reduce_sets(sets):
	'''Reduce sets.'''
	result = set()
	for s in sets:
		result.update(s)
	return result

def send_to_output(uniqnames):
	'''Send to output.'''
	print(uniqnames)
	output_filename = os.path.join(os.getcwd(), 'HELLO.txt')
	f = open(output_filename, 'w+')
	for i in uniqnames:
		f.write(i + '\n')
	f.close()
	print('LENGTH IS {}'.format(str(len(uniqnames))))

def main():
	'''Run main.'''
	dicts = get_all_sets()
	result = reduce_sets(dicts)
	send_to_output(result)

main()