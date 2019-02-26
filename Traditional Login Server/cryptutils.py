
import random
import string




def base64decode(text):
	import base64
	return base64.b64decode(text)

def base64encode(text):
	import base64
	return base64.b64encode(text)


def sha_256(text):
	from Crypto.Hash import SHA256
	sha = SHA256.new()
	sha.update(text)
	return sha.digest()


def generate_chal(username):
	print("chal generated")
	chal_len = 10
	chal = ""
	generator = random.SystemRandom()
	char_set = string.ascii_letters + string.digits
	
	for i in range(chal_len):
		rand = generator.randint(0, len(char_set) - 1)
		chal = chal + char_set[rand]
	
	return chal



def verify(svk, response, chal):
	from Crypto.Signature import PKCS1_v1_5
	from Crypto.Hash import SHA256
	from Crypto.PublicKey import RSA
	import codecs

	# import RSA key
	key = RSA.importKey(base64decode(svk))

	sha = SHA256.new(chal.encode())
    
	# initialize verifier object with PKCS#1_v1_5 standard
	verifier = PKCS1_v1_5.new(key)

	# decode hexadecimal
	decoder = codecs.getdecoder('hex')
	decoded_resp = decoder(response)[0]

	return verifier.verify(sha, decoded_resp)



"""

def verify2(svk, response, chal):
	from Crypto.PublicKey import RSA 
	from Crypto.Signature import PKCS1_v1_5 
	from Crypto.Hash import SHA256 
	from base64 import b64decode 

	import codecs

	chal = "hello"

	path = "app/static/key.txt"
	path2= "app/static/key2.txt"
	pub_key = open(path, "r").read()
	prv_key = open(path2,"r").read()

	print(pub_key)
	print(prv_key)

	rsakey = RSA.importKey(pub_key)
	rsakey2= RSA.importKey(prv_key)

	signer = PKCS1_v1_5.new(rsakey) 

	signer2 = PKCS1_v1_5.new(rsakey2) 

	digest = SHA256.new()

	print(chal)

	digest.update(chal.encode())
	print(digest.hexdigest())

	sig = signer2.sign(digest)
	hexify = codecs.getencoder('hex')
	x = hexify(sig)
	print("sig--------------------------")
	print(x[0])
	print("------------------------------")
	print(sig)
	print("sig--------------------------")

	anti = codecs.getdecoder('hex')
	y = anti(response)[0]
	print("response--------------------------")
	print(response)
	print("------------------------------")
	print(y)
	print("response--------------------------")

	if signer.verify(digest, y):
		print("done")
		return True
	else:
		return False

"""





