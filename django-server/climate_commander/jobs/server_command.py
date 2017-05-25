from computer import login_server, osdc_server
import time, os


def instantiate_server(server_model, debug=False):
    '''
    Convert a server representation in database into a connected computer.login_server.LoginServer.
    '''
    if debug:
        return
    utup = (server_model.server_name, server_model.server_location)
    cpus = server_model.server_cpus
    roots = {'data': server_model.roots_data, 'src': server_model.roots_src}
    credentials = {'userName': server_model.crdntl_user,
                   'domain': server_model.crdntl_domain,
                   'password': server_model.crdntl_password,
                   'loginNode': server_model.crdntl_loginnode,
                   'instanceIP': server_model.crdntl_instanceip,
                   'instanceName': server_model.crdntl_instanceName,
                   'pem': server_model.crdntl_pem}
    if server_model.server_name == 'Shackleton':
        server = login_server.LoginServer(utup, cpus, roots, credentials)
    elif server_model.server_name == 'Griffin':
        server = osdc_server.OSDCServer(utup, cpus, roots, credentials)
    server.connect()
    print('go', server.utup[0])
    print(server.session)
    return server


def update_cpu_util(server_model, servers_dict):
    prev_time = server_model.cpu_time
    server_model.cpu_time = get_cpu_time(servers_dict[server_model.server_name])
    server_model.save()
    post_time = server_model.cpu_time
    print(post_time)
    return calculate_cpu_util(prev_time, post_time)


def get_cpu_time(server):
    if not server.check_connection():
        server.connect()
    return server.run_command('grep cpu /proc/stat')[0]


def calculate_cpu_util(prev_time, post_time):
    prev_time = [x for x in prev_time.split('\n')][1:]
    post_time = [x for x in post_time.split('\n')][1:]
    ret = []
    for i in range(len(prev_time)):
        prev_sum = sum([int(x) for x in prev_time[i].split()[1:]])
        post_sum = sum([int(x) for x in post_time[i].split()[1:]])
        prev_busy = prev_sum - int(prev_time[i].split()[4]) - int(prev_time[i].split()[5])
        post_busy = post_sum - int(post_time[i].split()[4]) - int(post_time[i].split()[5])
        ret.append(float(post_busy - prev_busy)/(post_sum - prev_sum)*100)
    return ret


def prepare_server(server_model, servers_dict, job_model):
    server = servers_dict[server_model.server_name]
    code_url = job_model.code_url
    roots_src = server_model.roots_src
    if not server.check_connection():
        server.connect()
    # return (server, "") # message)

    message = update_codebase(server_model, server, code_url, roots_src)
    data_missed = check_data(server_model, job_model)
    copy_data(server, data_missed)
    invoke_virtualenv(server_model.server_name, server)
    return (server, message)


def update_codebase(server_model, server, code_url, roots_src):
    codebase = code_url.split("/")[-1].rstrip(".git") if code_url[-1] != '/' else code_url.split("/")[-2].rstrip(".git")
    server.cwd(roots_src + "/" + codebase)

    message = codebase + "\n"

    if server_model.server_name == 'Shackleton':
        stdout, stderr = server.run_command("git pull")
        message += stdout +  stderr + "\n"
    elif server_model.server_name == 'Griffin':
        stdout, stderr = server.run_command("with_proxy git pull")
        message += stdout +  stderr + "\n"

    if stderr:
        raise SystemExit("Cannot update %s by git pull: \n %s" % (code_url, stderr))
    if 'failed' in stdout or 'error' in stdout or 'unmerged' in stdout or 'fatal' in stdout:
        clean_codebase(server, codebase, roots_src)
        clone_codebase(server_model, server, code_url, roots_src)
        server.cwd(roots_src + "/" + codebase)

    return message


def clone_codebase(server_model, server, code_url, roots_src):
    server.cwd(roots_src)
    if server_model.server_name == 'Shackleton':
        stdout, stderr = server.run_command("git clone " + code_url)
    elif server_model.server_name == 'Griffin':
        stdout, stderr = server.run_command("with_proxy git clone " + code_url)

    # stdout, stderr = server.run_command("git clone " + code_url)
    if stderr:
        raise SystemExit("Cannot clone %s:\n %s" % (code_url, stderr))
    print(stdout)


def clean_codebase(server, codebase, roots_src):
    '''
    Get the name of the codebase by splitting the url, take the name after the last "/",
     and get rid of ".git".
    CD into the root src code folder, then remove the codebase.
    '''
    server.cwd(roots_src)
    stdout, stderr = server.run_command("rm -rf " + codebase)
    if stderr:
        raise SystemExit("Cannot remove %s:\n %s" % (codebase, stderr))
    print('removed directory: %s' % codebase)


def run_job(server_model, server, job_model, cores_used):
    code_url = job_model.code_url
    codebase = code_url.split("/")[-1].rstrip(".git") if code_url[-1] != '/' else code_url.split("/")[-2].rstrip(".git")
    roots_src = server_model.roots_src
    pid_list = []
    for i in range(cores_used):
        if not server.check_connection():
            server.connect()
        server.cwd(roots_src + "/" + codebase)
        pid, log_file = str(server.start_process(job_model.command)).split(',')[2:]
        pid_list.append((pid, log_file))
        time.sleep(5)
    return pid_list


def check_data(server_model, job_model):
    data_missed = []
    for dataset in job_model.data_used.all():
        if dataset not in server_model.data_hosted.all():
            data_missed.append(dataset)
    return data_missed


def copy_data(server, data_missed):
    # for dataset in data_missed:
    #
    return


def invoke_virtualenv(server_name, server):
    if server_name == 'Shackleton':
        server.run_command("source /home/jrising/aggregator/env/bin/activate")


def count_result_files(job_model, job_running, server):
    result_file = job_model.result_file
    result_directory = job_model.result_directory
    count = len(server.run_command("find " + result_directory + " -type f -name " + result_file)[0].split('\n'))
    print(count)
    job_running.result_nums = count
    print(job_running.result_nums)
    job_running.save()
    return count


def update_process_live(process, server):
    lines = server.run_command("ps -l %d; echo $?" % (process.pid))
    print(lines)
    if len(lines[0].split('\n')) < 3:
        process.status = 'Stopped'
        process.save()
        return False
    else:
        process.status = 'Running'
        process.save()
        return True


def kill_process(process, server):
    server.run_command("kill " + str(process.pid))


def tree_bfs(target_dir, root=False):
    if root:
        prefix = "<ul><li class='jstree-open'>" + target_dir + "<ul>"
        suffix = "</ul></li></ul>"
    else:
        prefix = "<ul><li class='jstree-closed'>"
        suffix = "</li></ul>"
    subfolders = next(os.walk(target_dir))[1]
    if subfolders:
        return prefix + "</li><li class='jstree-closed'>".join(subfolders) + suffix
    return ""
