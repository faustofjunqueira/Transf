if __name__ != "__main__":

	class Target:
		def __str__(self):
			return self.ip + ":" + str(self.port)
