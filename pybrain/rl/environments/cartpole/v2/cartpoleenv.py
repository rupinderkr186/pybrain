__author__ = 'Tom Schaul, tom@idsia.ch'


from scipy import array
import logging

from pybrain.rl import EpisodicTask

try: 
    import cartpolewrap as impl
except ImportError, e:
    logging.error("CartPoleTask is wrapping C code that needs to be compiled - it's simple: run .../cartpolecompile.py")
    raise e



class CartPoleTask(EpisodicTask):
    """ A Python wrapper of the standard C implentation of the pole-balancing task, directly using the 
    reference code of Faustino Gomez. """
    
    __single = None
    def __init__(self, numPoles = 1, markov = True, verbose = False):
        if self.__single != None:
            raise Exception('Singleton class - there is already an instance around', self.__single)
        self.__single = self
        impl.init(markov, numPoles)
        self.markov = markov
        self.numPoles = numPoles
        self.verbose = verbose
        self.reset()

    def reset(self):
        if self.verbose:
            print '** reset **'
        self.cumreward = 0     
        impl.res()        

    def getOutDim(self):
        if self.markov:
            return (1+self.numPoles)*2
        else:
            return 1+self.numPoles
        
    def getInDim(self):
        return 1

    def getReward(self):
        r = 1.+impl.getR()
        if self.verbose:
            print ' +r', r,
        return r
        
    def isFinished(self):
        if self.verbose:
            print '  -finished?', impl.isFinished()
        return impl.isFinished() 
    
    def getObservation(self):
        if self.verbose:
            print 'obs', impl.getObs()
        return array(impl.getObs())
        
    def performAction(self, action):
        if self.verbose:
            print 'act', action
        impl.performAction(action[0])
        self.addReward()
        
if __name__ == '__main__':
    from pybrain.rl import EpisodicExperiment
    from pybrain.rl.agents import FlatNetworkAgent
    x = CartPoleTask()
    a = FlatNetworkAgent(x.getOutDim(), x.getInDim())
    e = EpisodicExperiment(x, a)
    e.doEpisodes(2)
    