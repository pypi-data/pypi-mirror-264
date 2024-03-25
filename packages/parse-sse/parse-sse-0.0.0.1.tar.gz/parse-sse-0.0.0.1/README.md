# parse-sse

```python
from parse_sse import parse_sse
url = 'http://localhost:8000/your_endpoint'
response = requests.get(url, stream=True)
for event in parse_sse(response):
    print(f"Event: {event['event']}")
    print(f"Data: {event['data']}")
    print("---")  
```
