'''
Created on 14/03/2014

@author: julio
'''
if __name__ == '__main__':
	import time
	import fastcp

	start_time = time.time()
	fastcp.run()
	print(str(int(time.time() - start_time)) + " segundos")
    