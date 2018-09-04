from flask import Flask, g
from file_saver import FileSaver

app = Flask(__name__)

@app.route("/token")
def get_token():
	file_handle = open('./data/token/token.txt' , 'r')
	token_list = file_handle.readlines()
	file_handle.close()

	file_handle = open('./data/token/index.txt' , 'r+')
	current_index = int(file_handle.readlines()[0])
	current_index = (current_index+1) % len(token_list)
	file_handle.truncate(0)
	file_handle.seek(0)
	file_handle.write(str(current_index))
	file_handle.close()

	return token_list[current_index]

'''
file_name = 'token.txt'
file_saver = FileSaver('./data/token/')
file_saver.create_file(file_name)
file_saver.file_name = file_name
for x in range(1,100):
	file_saver.write_to_file(str(x))
'''
app.run()