book = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_"
key = "CQTZKHGJYMUWPBDEVRASONFILXp4qvh1a053s98cti27ugkrnm6_yjfbxdewozl"


def encode(s):
    if s.startswith("algo_"):
        # print("It has been already a confused model name.")
        return s
    encoded = ""
    for c in s:
        idx = book.find(c)
        if idx != -1:
            encoded += key[book.find(c)]
        else:
            encoded += c
    return "algo_" + encoded


def decode(s):
    if not s.startswith("algo_"):
        # print("It's not a confused model name.")
        return s
    else:
        s = s[len("algo_"):]  # delete prefix "algo_"
    decoded = ""
    for c in s:
        idx = key.find(c)
        if idx != -1:
            decoded += book[key.find(c)]
        else:
            decoded += c
    return decoded
s = decode('algo_gglattv95sh')
print(s)