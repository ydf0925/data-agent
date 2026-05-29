from contextlib import contextmanager


@contextmanager
def lifespan(url: str):
    print(f"建立连接")
    yield f"连接：{url}"
    print(f"断开连接")

with lifespan("http://127.0.0.1:8000/") as conn:
    print(f"基于获取的{conn}执行业务操作")