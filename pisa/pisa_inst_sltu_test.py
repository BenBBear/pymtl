#=========================================================================
# pisa_sltu_test.py
#=========================================================================

import pytest
import random
import pisa_encoding

from pymtl import Bits
from PisaSim   import PisaSim

from pisa_inst_test_utils import *

#-------------------------------------------------------------------------
# gen_basic_test
#-------------------------------------------------------------------------

def gen_basic_test():
  return """
    mfc0 r1, mngr2proc < 5
    mfc0 r2, mngr2proc < 4
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    sltu r3, r1, r2
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    mtc0 r3, proc2mngr > 0
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
    gen_rr_dest_byp_test( 5, "sltu",  1, 0, 0 ),
    gen_rr_dest_byp_test( 4, "sltu",  1, 1, 0 ),
    gen_rr_dest_byp_test( 3, "sltu",  0, 1, 1 ),
    gen_rr_dest_byp_test( 2, "sltu",  2, 1, 0 ),
    gen_rr_dest_byp_test( 1, "sltu",  2, 2, 0 ),
    gen_rr_dest_byp_test( 0, "sltu",  1, 2, 1 ),
  ]

#-------------------------------------------------------------------------
# gen_src0_byp_test
#-------------------------------------------------------------------------

def gen_src0_byp_test():
  return [
    gen_rr_src0_byp_test( 5, "sltu",  3, 2, 0 ),
    gen_rr_src0_byp_test( 4, "sltu",  3, 3, 0 ),
    gen_rr_src0_byp_test( 3, "sltu",  2, 3, 1 ),
    gen_rr_src0_byp_test( 2, "sltu",  4, 3, 0 ),
    gen_rr_src0_byp_test( 1, "sltu",  4, 4, 0 ),
    gen_rr_src0_byp_test( 0, "sltu",  3, 4, 1 ),
  ]

#-------------------------------------------------------------------------
# gen_src1_byp_test
#-------------------------------------------------------------------------

def gen_src1_byp_test():
  return [
    gen_rr_src1_byp_test( 5, "sltu",  5, 4, 0 ),
    gen_rr_src1_byp_test( 4, "sltu",  5, 5, 0 ),
    gen_rr_src1_byp_test( 3, "sltu",  4, 5, 1 ),
    gen_rr_src1_byp_test( 2, "sltu",  6, 5, 0 ),
    gen_rr_src1_byp_test( 1, "sltu",  6, 6, 0 ),
    gen_rr_src1_byp_test( 0, "sltu",  5, 6, 1 ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_byp_test
#-------------------------------------------------------------------------

def gen_srcs_byp_test():
  return [
    gen_rr_srcs_byp_test( 5, "sltu",  7, 6, 0 ),
    gen_rr_srcs_byp_test( 4, "sltu",  7, 7, 0 ),
    gen_rr_srcs_byp_test( 3, "sltu",  6, 7, 1 ),
    gen_rr_srcs_byp_test( 2, "sltu",  8, 7, 0 ),
    gen_rr_srcs_byp_test( 1, "sltu",  8, 8, 0 ),
    gen_rr_srcs_byp_test( 0, "sltu",  7, 8, 1 ),
  ]

#-------------------------------------------------------------------------
# gen_srcs_dest_test
#-------------------------------------------------------------------------

def gen_srcs_dest_test():
  return [
    gen_rr_src0_eq_dest_test( "sltu",  9, 8, 0 ),
    gen_rr_src1_eq_dest_test( "sltu",  8, 9, 1 ),
    gen_rr_src0_eq_src1_test( "sltu", 10, 0 ),
    gen_rr_srcs_eq_dest_test( "sltu", 10, 0 ),
  ]

#-------------------------------------------------------------------------
# gen_value_test
#-------------------------------------------------------------------------

def gen_value_test():
  return [

    gen_rr_value_test( "sltu", 0x00000000, 0x00000000, 0 ),
    gen_rr_value_test( "sltu", 0x00000001, 0x00000001, 0 ),
    gen_rr_value_test( "sltu", 0x00000003, 0x00000007, 1 ),
    gen_rr_value_test( "sltu", 0x00000007, 0x00000003, 0 ),

    gen_rr_value_test( "sltu", 0x00000000, 0xffff8000, 1 ),
    gen_rr_value_test( "sltu", 0x80000000, 0x00000000, 0 ),
    gen_rr_value_test( "sltu", 0x80000000, 0xffff8000, 1 ),

    gen_rr_value_test( "sltu", 0x00000000, 0x00007fff, 1 ),
    gen_rr_value_test( "sltu", 0x7fffffff, 0x00000000, 0 ),
    gen_rr_value_test( "sltu", 0x7fffffff, 0x00007fff, 0 ),

    gen_rr_value_test( "sltu", 0x80000000, 0x00007fff, 0 ),
    gen_rr_value_test( "sltu", 0x7fffffff, 0xffff8000, 1 ),

    gen_rr_value_test( "sltu", 0x00000000, 0xffffffff, 1 ),
    gen_rr_value_test( "sltu", 0xffffffff, 0x00000001, 0 ),
    gen_rr_value_test( "sltu", 0xffffffff, 0xffffffff, 0 ),

  ]

#-------------------------------------------------------------------------
# gen_random_test
#-------------------------------------------------------------------------

def gen_random_test():
  asm_code = []
  for i in xrange(100):
    src0 = Bits( 32, random.randint(0,0xffffffff) )
    src1 = Bits( 32, random.randint(0,0xffffffff) )
    dest = Bits( 32, src0 < src1 )
    asm_code.append( gen_rr_value_test( "sltu", src0.uint(), src1.uint(), dest.uint() ) )
  return asm_code

#-------------------------------------------------------------------------
# test_basic
#-------------------------------------------------------------------------

@pytest.mark.parametrize( "name,test", [
  asm_test( gen_basic_test     ),
  asm_test( gen_dest_byp_test  ),
  asm_test( gen_src0_byp_test  ),
  asm_test( gen_src1_byp_test  ),
  asm_test( gen_srcs_byp_test  ),
  asm_test( gen_srcs_dest_test ),
  asm_test( gen_value_test     ),
  asm_test( gen_random_test    ),
])
def test( name, test ):
  sim = PisaSim( trace_en=True )
  sim.load( pisa_encoding.assemble( test() ) )
  sim.run()

