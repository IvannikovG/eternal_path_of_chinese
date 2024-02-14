from redis import Redis

r = Redis(host='localhost', port=6379, decode_responses=True)

# docker run -it -p redis 6379:6379

r.hset('foo2', 'aa')

print(r.get('foo'))