import xmlrpc.client

file_path = "comments.txt"
def map_reduce_client(file_path, chunk_size=50):
    try:
        with xmlrpc.client.ServerProxy("http://localhost:8000/") as proxy:
            results = []
            with open(file_path, 'r', encoding="utf-8") as file:
                while True:
                    lines = []
                    for _ in range(chunk_size):
                        line = file.readline().strip()
                        if line == '':
                            break
                        lines.append(line)
                    if not lines:
                        break
                    mapped = [proxy.map(line) for line in lines]
                    reduced = proxy.reduce(mapped)
                    results.append(reduced)
            return results
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
print(map_reduce_client(file_path))