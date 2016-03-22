import sys

with open(sys.argv[1], 'r') as test_cases:
    for test in test_cases:
        test = test.rstrip()
        time = int(test.split()[0])
        final_time = int(sys.argv[2])
        '''action = test[1]
        from_node = test[2]
        to_node  = test[3]
        info = test[4]'''
        
        if time > final_time:
            break
        
        print (test)
