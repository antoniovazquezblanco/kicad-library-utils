# -*- coding: utf-8 -*-

from rules.rule import *

class Rule(KLCRule):
    """
    Create the methods check and fix to use with the kicad_mod files.
    """
    def __init__(self, module, args):
        super(Rule, self).__init__(module, args, 'Rule 9.6', 'Minimum annular ring')
        
    def checkPad(self, pad):
        
        if not 'size' in pad['drill']:
            self.addMessage("Pad {n} drill data has no 'size' attribute".format(
                n = pad['number']))
            return True
        
        drill_size = pad['drill']['size']
        drill_x = drill_size['x']
        drill_y = drill_size['y']
        
        pad_size = pad['size']
        pad_x = pad_size['x']
        pad_y = pad_size['y']

        err = False
        
        MIN_RING = 0.15
        
        # Circular pad
        if drill_x == drill_y and pad_x == pad_y:
            ring = (pad_x - drill_x) / 2
            
            if ring < MIN_RING:
                self.addMessage("Pad {n} annular ring ({d}mm) is below minimum ({mr}mm)".format(
                    n = pad['number'],
                    d = ring,
                    mr = MIN_RING))
                err = True
            
        # Non circular pad
        else:
            ring_x = (pad_x - drill_x) / 2
            
            if ring_x < MIN_RING:
                self.addMessage("Pad {n} x-dimension annular ring ({d}mm) is below minimum ({mr}mm)".format(
                    n = pad['number'],
                    d = ring_x,
                    mr = MIN_RING))
                err = True
                    
            ring_y = (pad_y - drill_y) / 2
            
            if ring_y < MIN_RING:
                self.addMessage("Pad {n} y-dimension annular ring ({d}mm) is below minimum ({mr}mm)".format(
                    n = pad['number'],
                    d = ring_y,
                    mr = MIN_RING))
                err = True
                
        return err        
        
    def check(self):
        """
        Proceeds the checking of the rule.
        The following variables will be accessible after checking:
            * pin1_position
            * pin1_count
        """
        module = self.module
        
        return any([self.checkPad(pad) for pad in module.filterPads('thru_hole')])
        
    def fix(self):
        """
        Proceeds the fixing of the rule, if possible.
        """
        self.addFixMessage("Fix - not supported for this rule")
        
