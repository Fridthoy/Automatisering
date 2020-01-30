# DFAServer, ver. 200127 v6
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests

HOST_NAME = '127.0.0.1' 
PORT_NUMBER = 1234 # Maybe set this to 1234

# Stores the path to DFAServer working directory
pathToApp = "C:/Users/fridthoy/Progging/Automatisering/"

# Read the content of the template file
f = open(pathToApp + "templates\\my_table_.dfa", "r")
data = f.read()
print("data from template:", data)

leg_length = 70
leg_side = 5
top_lenght = 150
top_width = 70
top_height = 7
i = 0
productOK = 0

data = data.replace("<PARAM1>", str(leg_length))
data = data.replace("<PARAM2>", str(leg_side))
data = data.replace("<PARAM3>", str(top_lenght))
data = data.replace("<PARAM4>", str(top_width))
data = data.replace("<PARAM5>", str(top_height))

f = open(pathToApp + "my_table_.dfa", "w")
f.write(data)
f.close()


class MyHandler(BaseHTTPRequestHandler):
	
	def do_HEAD(s):
		s.send_response(200)
		s.send_header("Content-type", "text/html")
		s.end_headers()
	def do_GET(s):
		# https://stackoverflow.com/questions/26563403/variables-not-updated-from-within-basehttpserver-class
		global productOK, leg_length, leg_side, top_lenght, top_width, top_height, i
		"""Respond to a GET request."""
		
		s.send_response(200)
		s.send_header("Content-type", "text/html")
		s.end_headers()
		
		# Check what is the path
		path = s.path
		if path.find("/info") != -1:
			s.wfile.write(bytes('<html><head><title>Cool interface.</title><meta http-equiv="refresh" content="3"></head>', 'utf-8'))
			s.wfile.write(bytes("<body><p>This is a new test. </p>" + str(i), "utf-8"))
			s.wfile.write(bytes('<a href="ntnu.no">link text</a>', "utf-8"))
			i = i+1
			# adding our message
			s.wfile.write(bytes("<p>leg_length: "+str(leg_length)+"</p>", "utf-8"))
			s.wfile.write(bytes("<p>leg_side: "+str(leg_side)+ "</p>", "utf-8"))
			s.wfile.write(bytes("<p>top_lenght: "+str(top_lenght)+ "</p>", "utf-8"))
			s.wfile.write(bytes("<p>top_width: "+str(top_width)+ "</p>", "utf-8"))
			s.wfile.write(bytes("<p>top_height: "+str(top_height)+ "</p>", "utf-8"))
			if productOK:
				s.wfile.write(bytes("<p>Product is possible to make.</p>", "utf-8"))
			else:
				s.wfile.write(bytes("<p>Product is not possible to make.</p>", "utf-8"))
				
				s.wfile.write(bytes('<svg width="200" height="100"><circle cx="50" cy="50" r="40" stroke="red" stroke-width="4" fill="red" /></svg>', "utf-8"))
				
			s.wfile.write(bytes("</body></html>", "utf-8"))
			
		if path.find("/productConfig") != -1:
			s.wfile.write(bytes('<html><body><h2>Product Configurator</h2><form action="http://127.0.0.1:1234/product" method="post">Leg length:<br><input type="text" name="leg_length" value="'+str(leg_length), "utf-8"))
			s.wfile.write(bytes('"><br>Leg side:<br><input type="text" name="leg_side" value="'+str(leg_side), "utf-8"))
			s.wfile.write(bytes('"><br>Top length:<br><input type="text" name="top_lenght" value="'+str(top_lenght), "utf-8"))
			s.wfile.write(bytes('"><br>Top width:<br><input type="text" name="top_width" value="'+str(top_width), "utf-8"))
			s.wfile.write(bytes('"><br>Top height:<br><input type="text" name="top_height" value="'+str(top_height), "utf-8"))
			s.wfile.write(bytes('"><br><br><input type="submit" value="Submit"></form><p>If you click the "Submit" button, the form-data will be sent.</p></body></html>', "utf-8"))
			
	def do_POST(s):
		#https://stackoverflow.com/questions/5975952/how-to-extract-http-message-body-in-basehttprequesthandler-do-post
		global leg_length, leg_side, top_lenght, top_width, top_height, i, productOK

		s.send_response(200)
		s.send_header("Content-type", "text/html")
		s.end_headers()
		
		# Check what is the path
		path = s.path
		print("Path: ", path)
		if path.find("/"):
			content_len = int(s.headers.get('Content-Length'))
			post_body = s.rfile.read(content_len)
			print("Body: ", post_body.decode())
			# Extract params values
			param_line = post_body.decode()
			if param_line.find("PARAM") != -1:
				if param_line.find("PARAM1") !=-1:
					param_line = param_line.replace("PARAM1 ", "")
					leg_lenght = int(param_line)
					print("leg_length updated: ", leg_lenght)
				if param_line.find("PARAM2") !=-1:
					param_line = param_line.replace("PARAM2 ", "")
					leg_side = int(param_line)
				if param_line.find("PARAM3") !=-1:
					param_line = param_line.replace("PARAM3 ", "")
					top_lenght = int(param_line)
					print("Top lenght", top_lenght)
				if param_line.find("PARAM4") !=-1:
					param_line = param_line.replace("PARAM4 ", "")
					top_width = int(param_line)
				if param_line.find("PARAM5") !=-1:
					param_line = param_line.replace("PARAM5 ", "")
					top_height = int(param_line)
			
		if path.find("/product") != -1:
			print("Inside of /product path")
			content_len = int(s.headers.get('Content-Length'))
			post_body = s.rfile.read(content_len)
			#process string of parameters: 
			# Example: leg_length=70&leg_side=5&top_lenght=150&top_width=70&top_height=7
			body = post_body.decode()
			pairs = body.split("&")
			#First pair
			pair0 = pairs[0].split("=")
			leg_length = int(pair0[1])
			#Second pair
			pair1 = pairs[1].split("=")
			leg_side = int(pair1[1])
			#Third pair
			pair2 = pairs[2].split("=")
			top_lenght = int(pair2[1])
			print("Top length (product): ", top_lenght)
			#Fourth pair
			pair3 = pairs[3].split("=")
			top_width = int(pair3[1])
			#Fifth pair
			pair4 = pairs[4].split("=")
			top_height = int(pair4[1])
			
			#Get limitations from the KB.
			URL = "http://127.0.0.1:3030/kbe/query"
			  
			# defining a query params 
			PARAMS = {'query':'PREFIX kbe:<http://kbe.openode.io/table-kbe.owl#>SELECT ?min WHERE {?topcutter a kbe:TopCutter.?topcutter kbe:hasMaxHeightTop ?min.}'} 
			  
			# sending get request and saving the response as response object 
			r = requests.get(url = URL, params = PARAMS) 

			#Checking the result
			print("Result:", r.text)
			data = r.json()
			print("JSON:", data)

			#Checking the value of the parameter
			print("Data Limitation:", data['results']['bindings'][0]['min']['value'])

			#Parameters requested by customer
			s.updateDesign(leg_length, leg_side, top_lenght, top_width, top_height) 
			
			# Calls for manuf. constrains (10 constrains in our case)
			productOK = 1
			
			s.getConstrain("hasMaxLengthLeg", "<PARAM1_max>")
			s.getConstrain("hasMinLengthLeg", "<PARAM1_min>")
			s.getConstrain("hasMaxSideLeg", "<PARAM2_max>")
			s.getConstrain("hasMinSideLeg", "<PARAM2_min>")
			s.getConstrain("hasMaxLengthTop", "<PARAM3_max>")
			s.getConstrain("hasMinLengthTop", "<PARAM3_min>")
			s.getConstrain("hasMaxHeightTop", "<PARAM5_max>")
			s.getConstrain("hasMinHeightTop", "<PARAM5_min>")
			s.getConstrain("hasMinWidthTop", "<PARAM4_min>")
			s.getConstrain("hasMaxWidthTop", "<PARAM4_max>")
			
			
			
			

	def updateDesign(self, param1, param2, param3, param4, param5):
		# Read the content of the template file
		global pathToApp
		f = open(pathToApp + "templates\\my_table_.dfa", "r")
		data = f.read()
		
		data = data.replace("<PARAM1>", str(param1))
		data = data.replace("<PARAM2>", str(param2))
		data = data.replace("<PARAM3>", str(param3))
		data = data.replace("<PARAM4>", str(param4))
		data = data.replace("<PARAM5>", str(param5))

		f = open(pathToApp + "my_table_.dfa", "w")
		f.write(data)
		f.close()
		
	def getConstrain(self, constrain, paramTag):
		global leg_length, leg_side, top_lenght, top_width, top_height, productOK
		URL = "http://127.0.0.1:3030/kbe/query"
  
		# defining a query params 
		PARAMS = {'query':'PREFIX kbe:<http://kbe.openode.io/table-kbe.owl#> SELECT ?data WHERE {?inst kbe:' + constrain + ' ?data.}'} 
		  
		# sending get request and saving the response as response object 
		r = requests.get(url = URL, params = PARAMS) 

		#Checking the result
		print("Result:", r.text)
		data = r.json()
		print("JSON:", data)

		#Checking the value of the parameter
		print("Data:", data['results']['bindings'][0]['data']['value'])
		
		# Update constrain value in design template
		dataToWrite = data['results']['bindings'][0]['data']['value']
		f = open(pathToApp + "my_table_.dfa", "r")
		data = f.read()
		
		data = data.replace(paramTag, str(dataToWrite))
		
		f = open(pathToApp + "my_table_.dfa", "w")
		f.write(data)
		f.close()
		
		#Check for validity:
		if paramTag.find("1_min")  != -1:
			if leg_length < int(dataToWrite):
				productOK = 0
		elif paramTag.find("1_max")  != -1:
			if  leg_length > int(dataToWrite):
				productOK = 0
		elif paramTag.find("2_min") != -1:
			if leg_side < int(dataToWrite):
				productOK = 0
		elif paramTag.find("2_max") != -1:
			if leg_side > int(dataToWrite):
				productOK = 0
		elif paramTag.find("3_min") != -1:
			if top_lenght < int(dataToWrite):
				productOK = 0
		elif paramTag.find("3_max") != -1:
			if top_lenght > int(dataToWrite):
				productOK = 0
		elif paramTag.find("4_min") != -1:
			if top_width < int(dataToWrite):
				productOK = 0
		elif paramTag.find("4_max") != -1:
			if top_width > int(dataToWrite):
				productOK = 0
		elif paramTag.find("5_min") != -1:
			if top_height < int(dataToWrite):
				productOK = 0
		elif paramTag.find("5_max") != -1:
			if top_height > int(dataToWrite):
				productOK = 0
			
		
 
if __name__ == '__main__':
	server_class = HTTPServer
	httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
	
	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		pass
	httpd.server_close()



