import time

class Log:
	verbose = False

	def set_verbose(b: bool):
		Log.verbose = b

	def log(msg):
		if Log.verbose: print(msg)

class Timeout:
	duration = 0

	def set_duration(t: float):
		Timeout.duration = t

	def timeout():
		time.sleep(Timeout.duration)
