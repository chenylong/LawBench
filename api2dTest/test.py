import json

# {'id': 'chatcmpl-8b1CRkYUdjYQr77quLDzEOZyCrMD9', 'object': 'chat.completion', 'created': 1703833439, 'model': 'gpt-3.5-turbo-0613', 'choices': [{'index': 0, 'message': {'role': 'assistant', 'content': '细雨湿衣看不见，\n闲窗春意正如诗。\n绿杨拂面花枝笑，\n满院新晴造化宜。'}, 'logprobs': None, 'finish_reason': 'stop'}], 'usage': {'prompt_tokens': 14, 'completion_tokens': 48, 'total_tokens': 62, 'pre_token_count': 4096, 'pre_total': 42, 'adjust_total': 41, 'final_total': 1}, 'system_fingerprint': None}

json_str = '{"id":"chatcmpl-8b17HeiFGHfcz4zgeP0R5qRqD5BTY","object":"chat.completion","created":1703833119,"model":"gpt-3.5-turbo-0613","choices":[{"index":0,"message":{"role":"assistant","content":"好的，这是一个关于程序员的笑话：\n\n有一天，一个程序员走进一家咖啡店，他点了一杯咖啡并扫描了他的手机付款。接下来，他问服务员：“这里有Wi-Fi吗？”\n服务员回答：“当然有，我们的Wi-Fi密码是‘JavaC0ff33’。”\n程序员听后惊讶地说：“等一下，你是说Java咖啡吗？”\n\n这个笑话打趣了程序员喜欢使用 Java 编程语言，将其与咖啡联系在一起。这个笑话通常会引起程序员的微笑和共鸣。"},"logprobs":null,"finish_reason":"stop"}],"usage":{"prompt_tokens":18,"completion_tokens":182,"total_tokens":200,"pre_token_count":4096,"pre_total":42,"adjust_total":40,"final_total":2},"system_fingerprint":null}'
string = '{"name": "John", "age": 30, "city": "New York"}'
json_data = json.loads(string)
print(json_data)
data = json.loads(json_str, strict=False)
content = data['choices'][0]['message']['content']
print(content)