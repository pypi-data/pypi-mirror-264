
from distutils.core import setup
setup(
  name = 'ffrnn',         # How you named your package folder (MyLib)
  packages = ['ffrnn'],   # Chose the same as "name"
  version = 'v1.0',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Flipflop recurrent neural network',   # Give a short description about your library
  author = 'Vigneswaran Chandrasekaran',                   # Type in your name
  author_email = 'vigneswaran0610@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/vigneswaran-chandrasekaran/ffrnn',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/vigneswaran-chandrasekaran/ffrnn/archive/refs/tags/v1.0.tar.gz',    # I explain this later on
  keywords = ['RNN', 'flipflops', 'Tensorflow2.x'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'tensorflow',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
  ],
)
