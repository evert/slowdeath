slowdeath - a proof of concept low-traffic DOS script

WARNING

This tool is for research purposes only, and should only be used as such.
Use at your own risk. No warranty is provided.

LICENSE

This tool is licensed under the MIT public license.

EXAMPLE

	python slowdeath.py --threads 200 http://localhost/

The script will open 200 sockets to localhost, and perform a POST request. 
The connection is kept alive, and will send out small tcp packages in the 
request body.

If the server is configured for less than 200 clients, the number of
connections quickly exhausts, and the server will be unavailable for other
users.