"""
Runs evaluation functions in parallel subprocesses
in order to evaluate multiple genomes at once.
"""
from multiprocessing import Pool
from tqdm import tqdm

class ParallelEvaluator(object):
    def __init__(self, num_workers, eval_function, timeout=None, initializer=None, initargs=(), maxtasksperchild=None):
        """
        eval_function should take one argument, a tuple of (genome object, config object),
        and return a single float (the genome's fitness).
        """
        self.eval_function = eval_function
        self.timeout = timeout
        self.pool = Pool(processes=num_workers, maxtasksperchild=maxtasksperchild, initializer=initializer, initargs=initargs)

    def __del__(self):
        self.pool.close()
        self.pool.join()
        self.pool.terminate()

    def evaluate(self, genomes, config):
        jobs = []
        for ignored_genome_id, genome in genomes:
            jobs.append(self.pool.apply_async(self.eval_function, (genome, config)))

        # assign the fitness back to each genome
        for job, (ignored_genome_id, genome) in tqdm(zip(jobs, genomes), total=len(jobs)):
            genome.fitness = job.get(timeout=self.timeout)