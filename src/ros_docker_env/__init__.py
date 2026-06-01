import sys

# Support Python 3.9+ standard library, or fallback for older versions
if sys.version_info >= (3, 9):
    from importlib import resources
else:
    import importlib_resources as resources

# Define the anchor path to your resources sub-package
resources_path = resources.files("ros_docker_env.resources")
