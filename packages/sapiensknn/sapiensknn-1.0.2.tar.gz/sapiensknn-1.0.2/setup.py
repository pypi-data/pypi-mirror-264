from setuptools import setup, find_packages
from setuptools.command.install import install
from os import environ, path, listdir, remove, rename
from subprocess import call
from shutil import move

class CustomInstall(install):
    def run(self):
        try:
            if 'COLAB_GPU' not in environ and 'KAGGLE_KERNEL_RUN_TYPE' not in environ:
                install.run(self)
                install_dir = self.install_lib
                core_file_path = path.join(install_dir, 'sapiensknn', 'core.py')
                call(['python', '-m', 'compileall', core_file_path])
                pycache_dir = path.join(install_dir, 'sapiensknn', '__pycache__')
                for filename in listdir(pycache_dir):
                    if filename.startswith('core'):
                        pycache_file = path.join(pycache_dir, filename)
                        new_file_path = path.join(install_dir, 'sapiensknn', filename)
                        move(pycache_file, new_file_path)
                        new_file_name = path.join(install_dir, 'sapiensknn', 'core.pyc')
                        rename(new_file_path, new_file_name)
                        remove(core_file_path)
                        break
            else: install.run(self)
        except Exception as error:
            print(f'ERROR while compiling the installation core: {error}')
            install.run(self)

setup(
    name = 'sapiensknn',
    version = '1.0.2',
    author = 'SAPIENS TECHNOLOGY',
    packages=find_packages(),
    install_requires=[],
    description = 'SapiensKNN (K-Nearest Neighbors) is an algorithm for classification and regression that returns the result based on the Euclidean distance between the input values.',
    long_description = "The SapiensKNN or Sapiens for K-Nearest Neighbors is a Machine Learning algorithm focused on data classification, where the response for each input is calculated based on the smallest Euclidean distance between the prediction input and the training inputs. The returned value for classification will always be one of the labels from the learning DataSet. If the value of the parameter K is greater than 1, the class that is most repeated among the nearest neighbors represented in K will be returned. Although the algorithm's primary focus is on data classification, it can also potentially be used for regression by returning the average of the values of the selected neighbors with the parameter K.",
    url = 'https://github.com/sapiens-technology/SapiensKNN',
    project_urls = {
        'Source code': 'https://github.com/sapiens-technology/SapiensKNN',
        'Download': 'https://github.com/sapiens-technology/SapiensKNN/archive/refs/heads/main.zip'
    },
    license = 'Proprietary Software',
    keywords = 'Sapiens, Artificial Intelligence, Machine Learning, Data Science, AI, ML, KNN, K-Nearest Neighbors',
    cmdclass={'install': CustomInstall}
)
