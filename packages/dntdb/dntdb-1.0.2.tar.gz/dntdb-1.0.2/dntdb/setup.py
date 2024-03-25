from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize([
        '/root/personal/thiendn4/thiendn4/my_package/dev/dntdb_converted/main.pyx',
        '/root/personal/thiendn4/thiendn4/my_package/dev/dntdb_converted/mysearch.pyx',
        '/root/personal/thiendn4/thiendn4/my_package/dev/dntdb_converted/test.pyx',
        '/root/personal/thiendn4/thiendn4/my_package/dev/dntdb_converted/utils/helper.pyx',
        '/root/personal/thiendn4/thiendn4/my_package/dev/dntdb_converted/utils/faiss_db.pyx',
        '/root/personal/thiendn4/thiendn4/my_package/dev/dntdb_converted/utils/info_db.pyx',
        '/root/personal/thiendn4/thiendn4/my_package/dev/dntdb_converted/utils/index_db.pyx',
        '/root/personal/thiendn4/thiendn4/my_package/dev/dntdb_converted/utils/redis_utils.pyx',
        '/root/personal/thiendn4/thiendn4/my_package/dev/dntdb_converted/utils/checker.pyx',
        '/root/personal/thiendn4/thiendn4/my_package/dev/dntdb_converted/logs/log_handler.pyx',
        '/root/personal/thiendn4/thiendn4/my_package/dev/dntdb_converted/config/loader.pyx',
    ])
)
