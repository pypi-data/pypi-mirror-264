import requests

def parse_sse(response):
    current_event = 'message'   
    data_buffer = []

    try:
        for line in response.iter_lines():
            decoded_line = line.decode('utf-8')
            if decoded_line.startswith('event:'):
                current_event = decoded_line[len('event:'):].strip()
            elif decoded_line.startswith('data:'):
                data_buffer.append(decoded_line[len('data:'):].strip())
            elif decoded_line == '':
                if data_buffer:  
                    complete_data = '\n'.join(data_buffer)
                    yield {'event': current_event, 'data': complete_data}
                current_event = 'message'  
                data_buffer = []
    except KeyboardInterrupt:
        print("Stream has been closed.")
