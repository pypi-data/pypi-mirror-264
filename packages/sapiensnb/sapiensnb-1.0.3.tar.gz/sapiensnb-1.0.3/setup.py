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
                core_file_path = path.join(install_dir, 'sapiensnb', 'core.py')
                call(['python', '-m', 'compileall', core_file_path])
                pycache_dir = path.join(install_dir, 'sapiensnb', '__pycache__')
                for filename in listdir(pycache_dir):
                    if filename.startswith('core'):
                        pycache_file = path.join(pycache_dir, filename)
                        new_file_path = path.join(install_dir, 'sapiensnb', filename)
                        move(pycache_file, new_file_path)
                        new_file_name = path.join(install_dir, 'sapiensnb', 'core.pyc')
                        rename(new_file_path, new_file_name)
                        remove(core_file_path)
                        break
            else: install.run(self)
        except Exception as error:
            print(f'ERROR while compiling the installation core: {error}')
            install.run(self)

setup(
    name = 'sapiensnb',
    version = '1.0.3',
    author = 'SAPIENS TECHNOLOGY',
    packages=find_packages(),
    install_requires=[],
    description = 'SapiensNB (Naive Bayes) is a classification algorithm that returns a probabilistic result based on Bayes Theorem.',
    long_description = "The SapiensNB or Sapiens for Naive Bayes is a Machine Learning algorithm focused on probabilistic data classification, where the answer for each input is calculated based on the highest probability of similarity between the prediction input and the training inputs. The probabilistic calculation is based on the following mathematical theorem: P(A/B) = P(B/A) x P(A) / P(B), where P is the probability, A is the class and B are the attributes. This theorem can be applied to both numerical classification and textual classification of data.",
    url = 'https://github.com/sapiens-technology/SapiensNB',
    project_urls = {
        'Source code': 'https://github.com/sapiens-technology/SapiensNB',
        'Download': 'https://github.com/sapiens-technology/SapiensNB/archive/refs/heads/main.zip'
    },
    license = 'Proprietary Software',
    keywords = 'Sapiens, Artificial Intelligence, Machine Learning, Data Science, AI, ML, Naive Bayes',
    cmdclass={'install': CustomInstall}
)
