import os
import rarfile
#from rarfile import RarCannotExec
import shutil
import zipfile
from pathlib import Path


pwd = os.getcwd()


def create_temp():
	try:
		os.mkdir('temp')
	except FileExistsError:
		print('File temp already exists')


def remove_temp():
	try:
		tmp_path = Path('temp/')
		shutil.rmtree(tmp_path)
	except FileNotFoundError:
		print('Something went wrong no temp file')


def collect_files():
	files = os.listdir(f'{pwd}/files')
	cb_files = []
	for file in files:
		if file.endswith('.cbr') or file.endswith('.cbz'):
			cb_files.append(file)
	return files


def unpac_file(file_name):
	print(f"Unpacing file {file_name}")
	clean_name = file_name.split(".")[0]
	temp_path1 = os.path.join('temp', clean_name)
	#print(f"temp_path1 is {temp_path1}")
	
	if file_name.endswith('z'):
		#print("EXTRACTING FILE THAT ENDS WITH Z")
		zfile = zipfile.ZipFile(os.path.join("files",file_name), 'r')
		zfile.extractall(temp_path1)
		extract_files = os.listdir(temp_path1)
		#print(f"EXTRACT FILES ARE \n {extract_files}")
	if file_name.endswith('r'):
		try:
			#print("EXTRACTING FILE THAT ENDS WITH R")
			rarfile.UNRAR_TOOL='unrar'
			r1 = rarfile.RarFile(os.path.join('files', file_name))
			r1.extractall(path=temp_path1)
			extract_files = os.listdir(temp_path1)
		except:
			#print("EXTRACTING FILE THAT ENDS WITH Z")
			zfile = zipfile.ZipFile(os.path.join("files",file_name), 'r')
			zfile.extractall(temp_path1)
			extract_files = os.listdir(temp_path1)
			#print(f"EXTRACT FILES ARE \n {extract_files}")
			#print(f"EXTRACT FILES ARE \n {extract_files}"
	

	try:
		if len(extract_files) <= 2:
			extract_files = os.listdir(temp_path1)
			#print("len of extract files is less than 2")
			file_name2 = os.listdir(temp_path1)
			#print(f"FILE NAME 2 is:{file_name2}")
			temp_path2 = os.path.join(temp_path1, file_name2[0])
			#print(f"temp_path2 is {temp_path2}")
			try:
				extract_files = os.listdir(temp_path2)
			except NotADirectoryError:
				temp_path2 = os.path.join(temp_path1, file_name2[1])
				extract_files = os.listdir(temp_path2)
			#print(f"extract files are: {extract_files}")
			jf = find_junk_file(clean_name, extract_files)
			os.remove(os.path.join(temp_path2, jf))
			print(f'REMOVED: {jf}')
			
		else:
			#print("Len of extract_files is upper than 2")
			jf = find_junk_file(clean_name ,extract_files)
			os.remove(os.path.join(temp_path1, jf))
			print(f'REMOVED: {jf}')
			
		#print(extract_files)
		#print("RARIG FILES")
		rar_it(clean_name)
	except UnboundLocalError as e:
		print(f"{file_name} IS BAD FILE!!!")

def find_junk_file(file_name, file_list):
	file_list.sort()
	junk_file = file_list[-1]
	print(f"Junk file is: {junk_file}")
	return junk_file
'''
def delete_junk(file_name, fl_file):
	# INTERESTING PART
	for f in file_list:
		if 
'''
def rar_it(file_name):
	shutil.make_archive(os.path.join('new_files', file_name), 'zip', root_dir=os.path.join('temp', file_name))
	os.rename(os.path.join('new_files',f'{file_name}.zip'), os.path.join('new_files', f'{file_name}.cbr'))
	print("RARED")

def main():
	print('Starting the program')
	print('Creating temperary file')
	create_temp()
	fs = collect_files()
	for f in fs:
		unpac_file(f)
	print('Finshed...')
	print('Deleting temp files')
	remove_temp()
	print('FINISHED! You will find all commics in new_files folder')


main()
