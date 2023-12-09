

def printhex(data, fmt=' '):
    if fmt == ' 0x':
        print(' '.join('0x%02x' % i for i in data))
    elif fmt == '':
        print(''.join('%02x' % i for i in data))
    else:
        print(' '.join('%02x' % i for i in data))
        

def limit_max_min(val, minv=-1023, maxv=1023):
    ret = int(val)
    if val < minv:
        ret = int(minv)
    elif val > maxv:
        ret = int(maxv)
    return ret
    
    
    
def util_test():
    data = b'hello'
    printhex(data)
    

if __name__ == '__main__':
    util_test()
    



