# ManufReqServer, ver. 200130 v3
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
			s.wfile.write(bytes('<br>Leg length MIN:<br><input type="text" name="leg_length_min" value="0">', "utf-8"))
			s.wfile.write(bytes('<br>Leg length MAX:<br><input type="text" name="leg_length_max" value="0">', "utf-8"))
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
		if path.find("/setLimits") != -1:
			print("Inside of /product path")
			content_len = int(s.headers.get('Content-Length'))
			post_body = s.rfile.read(content_len)
			#process string of parameters: 
			# Example: leg_length_min=70&leg_length_max=100&leg_side=5&top_lenght=150&top_width=70&top_height=7
			body = post_body.decode()
			pairs = body.split("&")
			#First pair
			pair0 = pairs[0].split("=")
			leg_length_min = int(pair0[1])
			#Second pair
			pair1 = pairs[1].split("=")
			leg_length_max = int(pair1[1])
			#Third pair
			pair2 = pairs[2].split("=")
			leg_side_min = int(pair2[1])
			#Fourth pair
			pair3 = pairs[3].split("=")
			leg_side_max = int(pair3[1])
			#Fifth pair
			pair4 = pairs[4].split("=")
			top_lenght_min = int(pair4[1])
			#Sixth pair
			pair5 = pairs[5].split("=")
			top_lenght_max = int(pair5[1])
			#Seventh pair
			pair6 = pairs[6].split("=")
			top_width_min = int(pair6[1])
			#Eighth pair
			pair7 = pairs[7].split("=")
			top_width_max = int(pair7[1])
			#Nineth pair
			pair8 = pairs[8].split("=")
			top_height_min = int(pair8[1])
			#Tenth pair
			pair9 = pairs[9].split("=")
			top_height_max = int(pair9[1])
			
			print("top_height_min", top_height_min)
			
			s.setConstrain("hasMaxLengthLeg", leg_length_max)
			s.setConstrain("hasMinLengthLeg", leg_length_min)
			s.setConstrain("hasMaxSideLeg", leg_side_max)
			s.setConstrain("hasMinSideLeg", leg_side_min)
			s.setConstrain("hasMaxLengthTop", top_lenght_max)
			s.setConstrain("hasMinLengthTop", top_lenght_min)
			s.setConstrain("hasMaxHeightTop", top_height_max)
			s.setConstrain("hasMinHeightTop", top_height_min)
			s.setConstrain("hasMinWidthTop", top_width_min)
			s.setConstrain("hasMaxWidthTop", top_width_max)
				
		
	def setConstrain(self, constrain, value):
		URL = "http://127.0.0.1:3030/kbe/update"
  
		# Step 1: defining a query to delete previous value.
		PARAMS = {'update':'PREFIX kbe:<http://kbe.openode.io/table-kbe.owl#> DELETE {?topcutter kbe:' + constrain + ' ?min.} WHERE { ?topcutter kbe:' + constrain +' ?min.}'} 
		  
		# sending get request and saving the response as response object 
		r = requests.post(url = URL, data = PARAMS) 

		#Checking the result
		print("Result for DELETE query:", r.text)
		
		# Step 2: defining a query to INSERT new value.
		# Check if it is top or leg.
		type = ''
		if constrain.find("Top") != -1:
			type = "TopCutter"
		else:
			type = "LegCutter"
		
		PARAMS = {'update':'PREFIX kbe:<http://kbe.openode.io/table-kbe.owl#> INSERT { ?topcutter kbe:' + constrain + ' "' + str(value) + '"^^<http://www.w3.org/2001/XMLSchema#int>.} WHERE { ?topcutter a kbe:' + type + '.}'} 
		  
		# sending get request and saving the response as response object 
		r = requests.post(url = URL, data = PARAMS) 

		#Checking the result
		print("Result of INSERT query:", r.text)


		
		
 
if __name__ == '__main__':
	server_class = HTTPServer
	httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
	
	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		pass
	httpd.server_close()
