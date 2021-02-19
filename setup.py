from setuptools import setup

setup(name='wheelgame',
      version='0.0.1',
      description='Who Wants to Be a Wheel of Fortune',
      author='Kyle Bittinger',
      author_email='kylebittinger@gmail.com',
      url='https://github.com/kylebittinger/wheelgame',
      packages=['wheelgamelib'],
      entry_points = {
          'console_scripts': [
              'wheelgame=wheelgamelib.command:main',
          ],
      }
)
