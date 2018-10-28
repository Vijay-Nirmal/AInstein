import ChatBase as cb

def Chat():
    while True:
        request = input("User: ")
        if isExitRequest(request):
            print("AInstein: Goodbye")
            break
        print("AInstein: " + cb.responceFor(request))

def isExitRequest(request):
    request.lower() in ["exit", "goodbye"]

if __name__ == '__main__':
    print("Hello, I am AInstein")
    Chat()
