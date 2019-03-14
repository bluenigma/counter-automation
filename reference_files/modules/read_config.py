def read_config():
    conf = []
    with open('config','r') as config:
        for line in config:
            i = line.split('=')
            conf.append(i[1])
    return conf

if __name__ == '__main__':
    read_config()
