"""
FileSaver
folder
file_name

def create_file(self.folder, new_file_name)

def write_to_file(self.folder, self.file, text)


PostSaver(FileSaver)

max_num_of_line

def get_lastest_file:
	file_index = 0
	file_name = ''
	for file in files_of_folder:
		if file.name.to_int() > file_index:
			file_name = file.name
			file_index = file_name.to_int()
	return file_name,file_index

def get_file_to_save:
	self.file_name,file_index = get_lastest_file()
	if file_index == 0:
		self.file_name = '1.txt'
		create_file(self.file_name)
	
	else:
		file_handle = open(folder+file_name, 'r')
		lineList = file_handle.readlines()

		if len(lineList) >= max_num_of_line:
			file_handle.close()
			file_index += 1
			file_name = (file_index+1) + '.txt'
			create_file(self.file_name)

"""
import os


class FileSaver(object):
	
	def __init__(self):
		self.folder = './'
		self.file_name = ''

	def create_file(self, new_file_name):
		file_path = self.folder + new_file_name
		file_handle = open(file_path, 'w')
		file_handle.close()		

	def write_to_file(self, new_line_text):
		file_path = self.folder + self.file_name
		file_handle = open(file_path, 'a')
		file_handle.write(new_line_text + '\n')
		file_handle.close()

		
class PostSaver(FileSaver):
	
	def __init__(self):
		super(PostSaver, self).__init__()
		self.max_num_of_line = 1000		
		self.folder = './post/'
		self.update_file_name()
	
	def get_lastest_file(self):				
		list_file_names = os.listdir(self.folder)
		if len(list_file_names) > 0:
			return list_file_names[-1], len(list_file_names)
		return '', 0

	def update_file_name(self):
		self.file_name, file_index = self.get_lastest_file()
		if file_index == 0:
			self.file_name = '1.txt'
			self.create_file(self.file_name)	
		else:
			file_handle = open(self.folder + self.file_name, 'r')
			lineList = file_handle.readlines()

			if len(lineList) >= self.max_num_of_line:
				file_handle.close()
				file_index += 1
				self.file_name = str(file_index) + '.txt'
				self.create_file(self.file_name)

	def write_to_file(self, new_line_text):
		self.update_file_name()
		super(PostSaver, self).write_to_file(new_line_text)