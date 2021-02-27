# event-loop based algorithms experiments

1. `base.py` base socket reuse sync method for one client
2. `select_base.py` syscall select based async event loop method for multiple clients 
3. `selectors_base.py` selectors library based async event loop method for multiple clients

## synthetic test

```shell
ab -c 100 -n 1000 http://localhost:5000/
```