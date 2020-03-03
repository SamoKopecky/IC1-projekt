import subprocess
command = 'netsh advfirewall firewall add rule name="Open Port 80" dir=in action=allow protocol=TCP localport=80'
args = command.split(" ")
args2 = args[5] + args[6] + args[7]
#print(args)
del args[5]
del args[5]
del args[5]
temp = args
args = temp[:5]
args.append(args2)
args = args + temp[5:]
#print(args)
to_run = ['cmd', '/c']
for arg in args:
    to_run.append(arg)
#print(to_run)
result = subprocess.run(to_run)
print(result)
