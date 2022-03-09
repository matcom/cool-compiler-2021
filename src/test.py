import subprocess

sp = subprocess.run(['bash', './coolc.sh', "hello_world.cl"]	, capture_output=True, timeout=100)
return_code, output = sp.returncode, sp.stdout.decode()

#print(return_code)
print(output)
