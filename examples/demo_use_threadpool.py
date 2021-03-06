# An example of how to publish a simple wsgi app under isapi_wsgi using
# the ISAPIThreadPoolHandler.
#
# Executing this script (or any server config script) will install the extension
# into your web server and will create a "loader" DLL _demo_use_threadpool.dll in the 
# current directory. As the server executes, the PyISAPI framework will load
# this module and create the Extension object.
# A Virtual Directory named "isapi-wsgi-demo-usethreadpool" is setup. This dir has the ISAPI
# WSGI extension as the only application, mapped to file-extension '*'.  
# Therefore, isapi_wsgi extension handles *all* requests in this directory.
#
# To launch this application from a web browser use a url similar to:
#
#  http://localhost/isapi-wsgi-demo-use-threadpool/
#
# A "Hello world!" and the WSGI environment should be displayed.

def demo_app(environ,start_response):
    """Demo app from wsgiref"""
    from StringIO import StringIO
    stdout = StringIO()
    print >>stdout, "Hello world!"
    print >>stdout
    h = environ.items(); h.sort()
    for k,v in h:
        print >>stdout, k,'=',`v`
    start_response("200 OK", [('Content-Type','text/plain')])
    return [stdout.getvalue()]

import isapi_wsgi
# The entry points for the ISAPI extension.
def __ExtensionFactory__():
    return isapi_wsgi.ISAPIThreadPoolHandler(demo_app)

if __name__=='__main__':
    # If run from the command-line, install ourselves.
    from isapi.install import *
    params = ISAPIParameters()
    # Setup the virtual directories - this is a list of directories our
    # extension uses - in this case only 1.
    # Each extension has a "script map" - this is the mapping of ISAPI
    # extensions.
    sm = [
        ScriptMapParams(Extension="*", Flags=0)
    ]
    vd = VirtualDirParameters(Name="isapi-wsgi-demo-use-threadpool",
                              Description = "ISAPI-WSGI ISAPIThreadPoolHandler Demo",
                              ScriptMaps = sm,
                              ScriptMapUpdate = "replace"
                              )
    params.VirtualDirs = [vd]
    HandleCommandLine(params)
