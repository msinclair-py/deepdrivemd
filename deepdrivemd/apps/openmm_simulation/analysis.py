import MDAnalysis
from MDAnalysis.analysis import align, distances, rms
from MDAnalysis.analysis.base import AnalysisBase
import numpy as np
import numpy.typing as npt
from pathlib import Path
from typing import Callable, Dict, Optional, Tuple

type AnalysisDict = Dict[str, List[Callable, str]]

class Analyzer(AnalysisBase):
    def __init__(self, u: MDAnalysis.Universe, *args, **kwargs):
        super().__init__(u.trajectory)
        self.analyses: AnalysisDict = None
        self.box = u.atoms.dimensions
        
    def _prepare(self):
        """Preprocessing for analysis. Data object initialized and
        relevant atom selections created."""
        self.result = np.zeros((self.n_frames, len(self.analyses)))
        
        self.sels = dict()
        for analysis in self.analyses.values():
            self.sels.update{name: self.u.select_atoms(sel) 
                             for name, sel in analysis['sels'].items()}
        
        self.refs = dict()
        
    def _single_frame(self):
        """Analyses to be performed on a single frame."""
        for i, analysis in enumerate(self.analyses.values()):
            func, args = analysis['call']
            self.result[self.ts._frame_index, i] = func(args)
    
    def _conclude(self):
        """Any post-processing or normalization goes here."""
        pass
        
    def rmsd(self, 
             sel_name: str, 
             ref_name: str) -> npt.ArrayLike:
        positions = self.sels[sel_name].positions
        ref_positions = self.refs[ref_name].positions
        return self._rmsd(positions, ref_positions)
    
    @staticmethod
    def _rmsd(positions: npt.ArrayLike,
              ref_positions: npt.ArrayLike) -> npt.ArrayLike:
        return rms.rmsd(positions, ref_positions,
                        center=True, superposition=True)
    
    def distance(self,
                 sel1_name: str,
                 sel2_name: str) -> npt.ArrayLike:
        sel1 = self.sels[sel1_name]
        sel2 = self.sels[sel2_name]
        return self._distance(sel1, sel2)
    
    @staticmethod
    def _distance(sel1: MDAnalysis.AtomGroup,
                  sel2: MDAnalysis.AtomGroup) -> npt.ArrayLike:
        return distances.dist(sel1, sel2, box=self.box)[:, 2]
    
    def contact_map(self,
                    ):
        positions = 
        
        cm = self._contact_map(positions, cutoff).tocoo()
        
        pass
    
    @staticmethod
    def _contact_map(self,
                     positions: npt.ArrayLike,
                     cutoff: float) -> npt.ArrayLike:
        return distances.contact_matrix(positions, cutoff, box=self.box,
                                        returntype='sparse')