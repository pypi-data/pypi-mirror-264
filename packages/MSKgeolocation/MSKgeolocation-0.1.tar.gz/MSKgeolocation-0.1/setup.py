from setuptools import setup

setup(
    name = 'MSKgeolocation',
    version = '0.1',
    author = 'Massaki Igarashi',
    author_email = 'prof.massaki@gmail.com',
    packages = ['MSKgeolocation'],
    description = 'Biblioteca teste desenvolvida pelo Prof. Massaki de O. Igarashi',
    long_description =  'Funções e operações básicas: soma, sub, mult, div. \n'
                        + 'exemplo de uso: '
                        + 'soma(x,y) '
                        + ' sub(x,y) '
                        + 'mult(x,y) '
                        + ' div(x,y) ',

    url = 'https://github.com/massakiigarashi2/MSKlib',
    project_urls = {
        'Código fonte': 'https://github.com/massakiigarashi2/MSKlib',
        'Download': 'https://github.com/massakiigarashi2/MSKlib/raw/main/MSK002-0.2.tar.gz'},
    license = 'MIT',
    keywords = 'Funções Matemáticas Básicas',
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Portuguese (Brazilian)',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Internationalization',
        'Topic :: Scientific/Engineering :: Physics'])