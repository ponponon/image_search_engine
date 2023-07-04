from loggers import logger


def retry(count: int = 2):
    """ count 表示重试次数 """

    def wrapper(func):
        def inner(*args, **kwargs):
            """
            retry 修饰器只负责重试, 不修改入参和返回值
            如果在指定次数内依旧报错，则向外抛出异常链
            """
            flag = 0
            last_error = Exception()
            for i in range(count):
                try:
                    return func(*args, **kwargs)
                except Exception as error:
                    logger.exception(f'第 {flag} 次重试: {error}')
                    flag += 1
                    last_error = error
            raise Exception('重试无效, retry failure !') from last_error

        return inner

    return wrapper
