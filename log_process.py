from computer import login_server

credentials = {'username': 'jongkai', 'domain': 'dmas.berkeley.edu'}
roots = {'data': '~/data', 'src': '~/src'}

server = login_server.LoginServer(('berkeley', 'shackleton'), 20, roots, credentials)
server.connect()
server.run_command('python testTask.py')
