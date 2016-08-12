from computer import login_server


def instantiate_server(model_entry):
    utup = (model_entry.server_name, model_entry.server_location)
    cpus = model_entry.server_cpus
    roots = {'data': model_entry.roots_data, 'src': model_entry.roots_src}
    credentials = {'username': model_entry.crdntl_user, 'domain': model_entry.crdntl_domain, 'password': model_entry.crdntl_password}
    server = login_server.LoginServer(utup, cpus, roots, credentials)
    server.connect()
    return server


def get_cpu_time(server):
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


def update_cpu_util(server, servers_dict):
    prev_time = server.cpu_time
    server.cpu_time = get_cpu_time(servers_dict[server.server_name])
    server.save()
    post_time = server.cpu_time
    return calculate_cpu_util(prev_time, post_time)
