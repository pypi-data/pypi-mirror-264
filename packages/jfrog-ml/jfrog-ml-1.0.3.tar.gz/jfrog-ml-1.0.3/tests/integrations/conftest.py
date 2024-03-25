def pytest_addoption(parser):
    parser.addoption("--rt_host", action="store", default="http://localhost:8081")
    parser.addoption("--rt_token", action="store", default="")
    parser.addoption("--repo_name", action="store", default="ml-local")