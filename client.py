from xmlrpc.client import ServerProxy

proxy = ServerProxy('http://localhost:3000')

if __name__ == '__main__':
    print(proxy.vote("43011487800", "Minion"))
