# mymiddleware.py

class MyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 在请求处理前执行的代码
        print("Custom middleware before request")

        response = self.get_response(request)

        # 在请求处理后执行的代码
        print("Custom middleware after response")

        return response
