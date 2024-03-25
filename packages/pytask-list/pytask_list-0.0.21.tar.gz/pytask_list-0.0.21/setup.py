import setuptools

with open("README.md", "r") as arq:
    readme = arq.read()

setuptools.setup(name='pytask_list',
    version='0.0.21',
    license='MIT License',
    author='Pablo Troli',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='brawlixo123@gmail.com.br',
    keywords='Todo List',
    description=u'A awesome To-do List made with python in your terminal ',
    install_requires=['typer', 'rich'],
    package= setuptools.find_packages(),
    include_package_data=True,
    packages=['pytask_list']
                 )
