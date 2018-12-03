__author__ = 'asanghavi'
import logging
import logging.config
import logging.handlers

from core_framework.config import global_cfg


'''
####################################################################################################################################################################################
###################################################################################################################################################################################
# Class Name:   LogObj
#
# Purpose:      Facilitates logging for every class
#
# Arguments:    Module name
#
# Return Value: An instance of this class 
#
#
###################################################################################################################################################################################

####################################################################################################################################################################################

'''

class logger():

    logger                  = ""
    level                   = ""
    logfile                 = ""

    def __init__(self,module):
        self.logger     = logging.getLogger(module)
        if(not global_cfg.logger_flag):
            global_cfg.logger_flag = True
            self.logger.setLevel(logging.DEBUG)
            logging.config.fileConfig(global_cfg.log_config_path,disable_existing_loggers=0)
            self.logfile    = global_cfg.log_file

    '''
    ####################################################################################################################################################################################
    ###################################################################################################################################################################################
    # Method Name:   setFileHandlers
    #
    # Purpose:      Sets log file handler for the logger
    #
    # Arguments:    None
    #
    # Return Value: None
    #
    #
    ###################################################################################################################################################################################

    ####################################################################################################################################################################################
    '''

    def setFileHandlers(self):
        handler = logging.handlers.RotatingFileHandler(self.logfile, maxBytes=2000, backupCount=100)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    '''
    ####################################################################################################################################################################################
    ###################################################################################################################################################################################
    # Method Name:   logDebug
    #
    # Purpose:      logger messages for given level
    #
    # Arguments:    None
    #
    # Return Value: None
    #
    #
    ###################################################################################################################################################################################

    ####################################################################################################################################################################################
    '''

    def logDebug(self,msg):
        self.logger.debug(msg)


    '''
    ####################################################################################################################################################################################
    ###################################################################################################################################################################################
    # Method Name:   logError
    #
    # Purpose:      logger messages for given level
    #
    # Arguments:    None
    #
    # Return Value: None
    #
    #
    ###################################################################################################################################################################################

    ####################################################################################################################################################################################
    '''

    def logError(self,msg):
        self.logger.error(msg)

    '''
    ####################################################################################################################################################################################
    ###################################################################################################################################################################################
    # Method Name:   logWarning
    #
    # Purpose:      logger messages for given level
    #
    # Arguments:    None
    #
    # Return Value: None
    #
    #
    ###################################################################################################################################################################################

    ####################################################################################################################################################################################
    '''

    def logWarning(self,msg):
        self.logger.warning(msg)


    '''
    ####################################################################################################################################################################################
    ###################################################################################################################################################################################
    # Method Name:   logException
    #
    # Purpose:      logger messages for given level
    #
    # Arguments:    None
    #
    # Return Value: None
    #
    #
    ###################################################################################################################################################################################

    ####################################################################################################################################################################################
    '''

    def logException(self,msg):
        self.logger.exception(msg)
