# ManufReqServer, ver. 200130 v1
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests

HOST_NAME = '127.0.0.1' 
PORT_NUMBER = 4321 # Maybe set this to 1234


class MyHandler(BaseHTTPRequestHandler):
	
	def do_HEAD(s):
		s.send_response(200)
		s.send_header("Content-type", "text/html")
		s.end_headers()
	def do_GET(s):
		# https://stackoverflow.com/questions/26563403/variables-not-updated-from-within-basehttpserver-class
		"""Respond to a GET request."""
		
		s.send_response(200)
		s.send_header("Content-type", "text/html")
		s.end_headers()
		
		# Check what is the path
		path = s.path
		if path.find("/process") != -1:
			s.wfile.write(bytes('<html><body><h2>Process limits</h2><form action="http://127.0.0.1:4321/setLimits" method="post">', "utf-8"))
			s.wfile.write(bytes('Leg length MIN:<br><input type="text" name="leg_length_min" value="0">', "utf-8"))
			s.wfile.write(bytes('Leg length MAX:<br><input type="text" name="leg_length_max" value="0">', "utf-8"))
			s.wfile.write(bytes('<br>Leg side MIN:<br><input type="text" name="leg_side_min" value="0">', "utf-8"))
			s.wfile.write(bytes('<br>Leg side MAX:<br><input type="text" name="leg_side_max" value="0">', "utf-8"))
			s.wfile.write(bytes('<br>Top length MIN:<br><input type="text" name="top_lenght_min" value="0">', "utf-8"))
			s.wfile.write(bytes('<br>Top length MAX:<br><input type="text" name="top_lenght_max" value="0">', "utf-8"))
			s.wfile.write(bytes('<br>Top width MIN:<br><input type="text" name="top_width_min" value="0">', "utf-8"))
			s.wfile.write(bytes('<br>Top width MIN:<br><input type="text" name="top_width_max" value="0">', "utf-8"))
			s.wfile.write(bytes('<br>Top height MIN:<br><input type="text" name="top_height_min">', "utf-8"))
			s.wfile.write(bytes('<br>Top height MAX:<br><input type="text" name="top_height_max">', "utf-8"))
			s.wfile.write(bytes('<br><br><input type="submit" value="Submit"></form><p>If you click the "Submit" button, the form-data will be sent.</p></body></html>', "utf-8"))
			
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
			
			print("hei")
			
		if path.find("/setLimits"):
			content_len = int(s.headers.get('Content-Length'))
			post_body = s.rfile.read(content_len)
			print("Body: ", post_body.decode())
			# Extract params values
			param_line = post_body.decode()
			
			print("hei")	
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
			
			
			
		
	def setConstrain(self, constrain, paramTag):
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





