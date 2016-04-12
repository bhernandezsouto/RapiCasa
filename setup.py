from distutils.core import setup

setup(
    name='RapiCasa',
    version='1.0',
    packages=[''],
    url='http://mundopython.org/proyecto_python',
    license='GPL',
    author='Beatriz Hernandez',
    author_email='bhernandezsouto@danielcastelao.org',
    description='Aplicacion para la gestion de una inmoviliaria',

    scripts=["RapiCasa.py","PDF.py"],
    console=["RapiCasa.py"],
    options={"py2exe": {"bundle_files": 1}},
    zipfile=None
)
