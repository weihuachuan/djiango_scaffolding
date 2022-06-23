import base64
import hmac
import time
import json
import copy


class Jwt:
    @staticmethod  # 静态方法的装饰器封装一下  专门负责做计算用的函数
    def encode(self_payload, key, exp=300):
        # self_payload  含有私有声明的字典
        # key 自定的key
        # exp 过期时间

        # 生成header
        header = {'typ': 'JWT', 'alg': 'HS256'}
        # header_json = json.dumps(header)  # 这样转为json串不行，有空格，损耗带宽
        header_json = json.dumps(header, separators=(',', ':'), sort_keys=True)
        # 这样逗号冒号前后就没有空格了,sort_keys=True 使出来的json串变的有序了，在做hmac或其他哈希的计算的时候，串值一定是稳定的
        # separators分割符 第一个参数代表的是每个键值对之间用什么分割，第二个参数是每个键和值之间用什么分割
        # sort_keys 生成有序的json串
        header_json_base64 = Jwt.b64encode(header_json.encode())

        # init payload
        self_payload_copy = copy.deepcopy(self_payload)  # 为了不污染传进来的字典
        # 给拷贝出来的字典中加入公有声明
        self_payload_copy["exp"] = time.time() + exp  # 过期时间
        self_payload_copy_json = json.dumps(self_payload_copy, separators=(',', ':'), sort_keys=True)
        self_payload_copy_json_base64 = Jwt.b64encode(self_payload_copy_json.encode())

        # init sign
        hm = hmac.new(key.encode(), header_json_base64 + b'.' + self_payload_copy_json_base64,
                      digestmod="SHA256")  # 两个都是字节码所以连接符*点*也要是字节码
        hm_base64 = Jwt.b64encode(hm.digest())  # 取hm的二进制结果，然后进行base64的转码

        # jwt token 诞生  字节码
        token = header_json_base64 + b'.' + self_payload_copy_json_base64 + b'.' + hm_base64
        return token.decode('utf-8')

    @staticmethod
    def b64encode(js):  # 为了将base64转换修改为urlsafe
        return base64.urlsafe_b64encode(js).replace(b"=", b"")

    @staticmethod
    def b64decode(bs):
        # 加回来等号
        rem = len(bs) % 4  # 取余
        if rem > 0:
            bs += b'=' * (4 - rem)

        return base64.urlsafe_b64decode(bs)

    @staticmethod
    def decode(token, key):
        # 返回结果
        result = {}
        try:
            # 传入jwt的值(令牌) 和只有调用者知道的key
            # 校验签名
            token = token.encode('utf-8')
            header_bs, payload_bs, signature_bs = token.split(b".")  # 因为是字节串
            hm = hmac.new(key.encode(), header_bs + b"." + payload_bs, digestmod="SHA256")
            if signature_bs != Jwt.b64encode(hm.digest()):  # 将签名结果和传过来的sign进行对比
                result['user_id'] = ' '
                result['message'] = '非法token'
                return result

            # 校验时间
            payload_js = Jwt.b64decode(payload_bs)  # 解码为json
            payload = json.loads(payload_js)  # 解码为字典

            now = time.time()  # 当前时间
            if int(now) > int(payload["exp"]):  # 登录时间过期
                result['user_id'] = ' '
                result['message'] = '登錄超時'
                return result
            result['user_id'] = payload['user_id']
            result['user_name'] = payload['user_name']
            result['authority'] = payload['authority']
            result['message'] = '登錄成功'
            return result  # 返回自定义内容
        except Exception as e:
            print(e)
            result['user_id'] = ' '
            result['user_name'] = ' '
            result['authority'] = ' '
            result['message'] = '非法token'
            return result


if __name__ == '__main__':
    # 测试
    s = Jwt.encode({"user_id": "F1238775","user_name": "魏华川"}, "1234567", 24*60*60)  # 制作令牌
    print(s)
    print(Jwt.decode(s, "1234567"))  # 校验令牌 返回payload明文 字典类型
