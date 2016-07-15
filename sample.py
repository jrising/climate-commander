from computer import login_server
import os.path

credentials = {'username': 'jongkai', 'domain': 'dmas.berkeley.edu'}
roots = {'data': '~/data', 'src': '~/src'}
codes = {'climate-commander': 'https://github.com/GitOnion/climate-commander.git'}

server = login_server.LoginServer(('berkeley', 'shackleton'), 20, roots, credentials)
server.connect()


def get_directory_content(target, flag=""):
    if flag:
        flag = "-" + flag + " "
    stdout, stderr = server.run_command("ls " + flag + target)
    if stderr:
        raise SystemExit("Cannot get content from directory %s:\n %s" % (target, stderr))
    return stdout


def change_directory(target, root=""):
    if root:
        target = os.path.join(roots['src'], codebase)
    stdout, stderr = server.run_command("cd " + target)
    if stderr:
        raise SystemExit("Cannot change to directory %s:\n %s" % (target, stderr))
    print("Current Directory: " + server.run_command('pwd')[0])


def clone_codebase(codebase):
    stdout, stderr = server.run_command("git clone " + codes[codebase])
    if stderr:
        raise SystemExit("Cannot clone %s:\n %s" % (codebase, stderr))
    print(stdout)


def clean_codebase(codebase, root=""):
    if root:
        codebase = os.path.join(roots['src'], codebase)
    stdout, stderr = server.run_command("rm -rf " + codebase)
    if stderr:
        raise SystemExit("Cannot remove %s:\n %s" % (codebase, stderr))
    print('removed directory: %s' % codebase)


def update_codebase(codebase, root=""):
    stdout, stderr = server.run_command("git pull")
    print(stdout, stderr)
    if stderr:
        raise SystemExit("Cannot update %s by git pull: \n %s" % (codebase, stderr))
    if 'CONFLICT' in stdout or 'error' in stdout:
        clean_codebase(codebase, root=root)
        clone_codebase(codebase)


# Mission of this code:
# Check if target codebase is in the '~/src' directory
# if the codebase isn't there, clone it,
# if it is, git pull (update it).
# if git pull errs: remove the whole directory then clone a new one.

content_src = get_directory_content(roots['src'], "al")
for codebase in codes.keys():
    if codebase not in content_src:
        change_directory(roots['src'])
        clone_codebase(codebase)
        change_directory('-')
    else:
        change_directory(codebase, root=roots['src'])
        update_codebase(codebase, root=roots['src'])
        change_directory('-')

print("don't know why")

# TODO: Test on Data
# TODO:
# What are the expected workflows using Github?
# What are some potential failure of Github?
