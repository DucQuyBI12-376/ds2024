from xmlrpc.server import SimpleXMLRPCServer

def map_function(post):
    positive_keywords = ["love", "nice", "rẻ", "thèm", "beautiful"]
    negative_keywords = ["suck", "fat"]
    sentiment = "neutral"
    for word in post.split():
        if word in positive_keywords:
            sentiment = "positive"
            break
        elif word in negative_keywords:
            sentiment = "negative"
            break
    return {sentiment: 1}

def reduce_function(mapped_data):
    result = {"positive": 0, "negative": 0, "neutral": 0}
    for item in mapped_data:
        for key, value in item.items():
            result[key] += value
    return result

server = SimpleXMLRPCServer(("localhost", 8000))
print("Listening on port 8000...")
server.register_function(map_function, "map")
server.register_function(reduce_function, "reduce")
server.serve_forever()