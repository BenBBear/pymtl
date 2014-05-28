#=========================================================================
# pisa_andi_test.py
#=========================================================================

import pytest
import random
import pisa_encoding

from new_pymtl import Bits
from new_pymtl.helpers import sext,zext
from PisaSim   import PisaSim

from pisa_inst_test_utils import *

#-------------------------------------------------------------------------
# gen_basic_test
#-------------------------------------------------------------------------

def gen_basic_test():
  return """
    mfc0 r1, mngr2proc < 0x0f0f0f0f
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    andi r3, r1, 0x00ff
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    mtc0 r3, proc2mngr >0x0000000f
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
  """

#-------------------------------------------------------------------------
# gen_dest_byp_test
#-------------------------------------------------------------------------

def gen_dest_byp_test():
  return [
    gen_rimm_dest_byp_test( 5, "andi", 0x00000f0f, 0x00ff, 0x0000000f ),
    gen_rimm_dest_byp_test( 4, "andi", 0x0000f0f0, 0x0ff0, 0x000000f0 ),
    gen_rimm_dest_byp_test( 3, "andi", 0x00000f0f, 0xff00, 0x00000f00 ),
    gen_rimm_dest_byp_test( 2, "andi", 0x0000f0f0, 0xf00f, 0x0000f000 ),
    gen_rimm_dest_byp_test( 1, "andi", 0x00000f0f, 0x00ff, 0x0000000f ),
    gen_rimm_dest_byp_test( 0, "andi", 0x0000f0f0, 0x0ff0, 0x000000f0 ),
  ]

#-------------------------------------------------------------------------
# gen_src_byp_test
#-------------------------------------------------------------------------

def gen_src_byp_test():
  return [
    gen_rimm_src_byp_test( 5, "andi", 0x00000f0f, 0x00ff, 0x0000000f ),
    gen_rimm_src_byp_test( 4, "andi", 0x0000f0f0, 0x0ff0, 0x000000f0 ),
    gen_rimm_src_byp_test( 3, "andi", 0x00000f0f, 0xff00, 0x00000f00 ),
    gen_rimm_src_byp_test( 2, "andi", 0x0000f0f0, 0xf00f, 0x0000f000 ),
    gen_rimm_src_byp_test( 1, "andi", 0x00000f0f, 0x00ff, 0x0000000f ),
    gen_rimm_src_byp_test( 0, "andi", 0x0000f0f0, 0x0ff0, 0x000000f0 ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dest_test
#-------------------------------------------------------------------------

def gen_srcs_dest_test():
  return [
    gen_rimm_src_eq_dest_test( "andi", 0x00000f0f, 0xff00, 0x00000f00 ),
  ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [
    gen_rimm_value_test( "andi", 0xff00ff00, 0x0f0f, 0x00000f00 ),
    gen_rimm_value_test( "andi", 0x0ff00ff0, 0xf0f0, 0x000000f0 ),
    gen_rimm_value_test( "andi", 0x00ff00ff, 0x0f0f, 0x0000000f ),
    gen_rimm_value_test( "andi", 0xf00ff00f, 0xf0f0, 0x0000f000 ),
  ]

#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():
  asm_code = []
  for i in xrange(100):
    src  = Bits( 32, random.randint(0,0xffffffff) )
    imm  = Bits( 16, random.randint(0,0xffff) )
    dest = src & zext(imm,32)
    asm_code.append( gen_rimm_value_test( "andi", src.uint(), imm.uint(), dest.uint() ) )
  return asm_code

#-------------------------------------------------------------------------
# test_basic
#-------------------------------------------------------------------------

@pytest.mark.parametrize( "name,test", [
  asm_test( gen_basic_test     ),
  asm_test( gen_dest_byp_test  ),
  asm_test( gen_src_byp_test   ),
  asm_test( gen_srcs_dest_test ),
  asm_test( gen_value_test     ),
  asm_test( gen_random_test    ),
])
def test( name, test ):
  sim = PisaSim( trace_en=True )
  sim.load( pisa_encoding.assemble( test() ) )
  sim.run()

