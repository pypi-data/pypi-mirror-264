from setuptools import setup,find_packages

setup(name='tokidoro',
      version='0.1',
      description='Pomodoro CLI',
      url='https://github.com/nearlynithin/tokidoro',
      author='Nithin Umesh',
      author_email='nearlynithin@example.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'click',
          'rich',
          'playsound',
          'pygobject',
      ],
      package_data={
        'tokidoro': ['sounds/*', '*.json']
    },
      entry_points={
        'console_scripts': [
            'tokidoro = tokidoro.cli:cli'
        ]
    },
      zip_safe=False)
