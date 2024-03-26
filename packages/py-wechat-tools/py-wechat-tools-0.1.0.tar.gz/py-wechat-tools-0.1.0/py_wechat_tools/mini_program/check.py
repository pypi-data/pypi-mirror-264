import hashlib


class Check:

    @staticmethod
    def message_push_check(signature, timestamp, nonce, token):
        """
        验证服务器地址的有效性
        用于消息接口配置域名时的校验方法。
        注意：验证通过后，接口原样返回echostr 参数即可

        微信官方文档：
        https://developers.weixin.qq.com/miniprogram/dev/framework/server-ability/message-push.html#option-url

        从get请求中获取这些参数，直接返回该接口的返回结果即可

        :param token: 开发者生成的token
        :param signature: 微信加密签名，signature结合了开发者填写的token参数和请求中的timestamp参数、nonce参数。
        :param timestamp: 时间戳
        :param nonce: 随机数
        :return: 校验通过直接返回True，否则返回False
        """

        arr = [token, timestamp, nonce]
        arr.sort()
        arr_str = "".join(arr)
        sha1 = hashlib.sha1(arr_str.encode())
        hashcode = sha1.hexdigest()
        return hashcode == signature
