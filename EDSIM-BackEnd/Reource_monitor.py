from functools import wraps

# Code From : https://simpy.readthedocs.io/en/latest/topical_guides/monitoring.html
# More detail about resources at: https://simpy.readthedocs.io/en/latest/api_reference/simpy.resources.html

def patch_resource(resource, pre=None, post=None):
     """Patch *resource* so that it calls the callable *pre* before each
     put/get/request/release operation and the callable *post* after each
     operation.  The only argument to these functions is the resource
     instance.

     """
     def get_wrapper(func):
         # Generate a wrapper for put/get/request/release
         @wraps(func)
         def wrapper(*args, **kwargs):
             # This is the actual wrapper
             # Call "pre" callback
             if pre:
                 pre(resource)

             # Perform actual operation
             ret = func(*args, **kwargs)

             # Call "post" callback
             if post:
                 post(resource)

             return ret
         return wrapper

     # Replace the original operations with our wrapper
     for name in ['put', 'get', 'request', 'release']:
         if hasattr(resource, name):
             setattr(resource, name, get_wrapper(getattr(resource, name)))


def monitor(data, resource):
     """This is our monitoring callback."""
     item = (
         resource._env.now,  # The current simulation time
         resource.count,  # The number of users
         len(resource.queue),  # The number of queued processes
     )
     data.append(item)
