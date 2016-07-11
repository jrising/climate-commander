from computer import login_server

credentials = {'username': 'jongkai', 'domain': 'dmas.berkeley.edu'}
roots = {'data': '~/data', 'src': '~/src'}

server = login_server.LoginServer(('berkeley', 'shackleton'), 20, roots, credentials)

print server.run_command("ls")

#stdout, stderr = server.run_command("git pull")
#if "Error" in stdout or "Error" in stderr:
#    server.run_command("rm -rf *")
#    server.run_command("git clone ...")
