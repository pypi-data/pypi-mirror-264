from setuptools import find_packages, setup


VERSION = '1.0.0'
DESCRIPTION = 'dillwave'
AUTHOR = 'Cross Nastasi'
AUTHOR_EMAIL = 'cross@dill.moe'
URL = 'https://dill.moe'
LICENSE = 'Apache 2.0'
KEYWORDS = ['dillwave machine learning neural vocoder tts speech']
CLASSIFIERS = [
  'Development Status :: 4 - Beta',
  'Intended Audience :: Developers',
  'Intended Audience :: Education',
  'Intended Audience :: Science/Research',
  'License :: OSI Approved :: Apache Software License',
  'Programming Language :: Python :: 3.5',
  'Programming Language :: Python :: 3.6',
  'Programming Language :: Python :: 3.7',
  'Programming Language :: Python :: 3.8',
  'Topic :: Scientific/Engineering :: Mathematics',
  'Topic :: Software Development :: Libraries :: Python Modules',
  'Topic :: Software Development :: Libraries',
]


setup(name = 'dillwave',
    version = VERSION,
    description = DESCRIPTION,
    long_description = open('README.md', 'r').read(),
    long_description_content_type = 'text/markdown',
    author = AUTHOR,
    author_email = AUTHOR_EMAIL,
    url = URL,
    license = LICENSE,
    keywords = KEYWORDS,
    packages = find_packages('src'),
    package_dir = { '': 'src' },
    install_requires = [
        'numpy',
        'torch',
        'torchaudio',
        'tqdm',
        'tensorboard',
        'packaging',
        'soundfile'
    ],
    classifiers = CLASSIFIERS)
