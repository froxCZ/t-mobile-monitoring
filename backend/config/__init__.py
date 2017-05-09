from .AppConfig import AppConfig

"""
Classes for accessing general app configuration
"""

configColl = AppConfig.getColletion()

AppConfig.loadConfigFile()

