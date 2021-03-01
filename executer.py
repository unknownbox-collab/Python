
import subprocess,re
ip = str(subprocess.check_output("ifconfig"))
ip = re.findall('inet (\\d*\.\\d*\.\\d*\.\\d*)',ip)[1]
robotConnecter = subprocess.Popen("co")
robotConnecter.stdin.write('11111111\n')
robotConnecter.stdin.flush()

getContents = str(subprocess.check_output("open"))
getContents = re.findall()

robotConnecter = subprocess.Popen("open")
robotConnecter.communicate(input='')
pythonExecuter = subprocess.Popen("co")