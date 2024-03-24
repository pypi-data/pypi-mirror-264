/*! \file minimol_utils.h
  Header file for minimol utils */

//C Copyright (C) 2000-2006 Kevin Cowtan and University of York
//L
//L  This library is free software and is distributed under the terms
//L  and conditions of version 2.1 of the GNU Lesser General Public
//L  Licence (LGPL) with the following additional clause:
//L
//L     `You may also combine or link a "work that uses the Library" to
//L     produce a work containing portions of the Library, and distribute
//L     that work under terms of your choice, provided that you give
//L     prominent notice with each copy of the work that the specified
//L     version of the Library is used in it, and that you include or
//L     provide public access to the complete corresponding
//L     machine-readable source code for the Library including whatever
//L     changes were used in the work. (i.e. If you make changes to the
//L     Library you must distribute those, but you do not need to
//L     distribute source or object code to those portions of the work
//L     not covered by this licence.)'
//L
//L  Note that this clause grants an additional right and does not impose
//L  any additional restriction, and so does not affect compatibility
//L  with the GNU General Public Licence (GPL). If you wish to negotiate
//L  other terms, please contact the maintainer.
//L
//L  You can redistribute it and/or modify the library under the terms of
//L  the GNU Lesser General Public License as published by the Free Software
//L  Foundation; either version 2.1 of the License, or (at your option) any
//L  later version.
//L
//L  This library is distributed in the hope that it will be useful, but
//L  WITHOUT ANY WARRANTY; without even the implied warranty of
//L  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
//L  Lesser General Public License for more details.
//L
//L  You should have received a copy of the CCP4 licence and/or GNU
//L  Lesser General Public License along with this library; if not, write
//L  to the CCP4 Secretary, Daresbury Laboratory, Warrington WA4 4AD, UK.
//L  The GNU Lesser General Public can also be obtained by writing to the
//L  Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
//L  MA 02111-1307 USA


#ifndef CLIPPER_MINIMOL_UTILS
#define CLIPPER_MINIMOL_UTILS


#include "minimol.h"


namespace clipper {


  //! Class for holding the indices of an atom within a MiniMol molecule class
  /*! The indices remain valid only while no changes are made to the
    MiniMol object. */
  class MAtomIndex {
  public:
    //! null constructor
    MAtomIndex() { p = -1; }
    //! constructor: from polymer, monomer and atom numbers.
    MAtomIndex( const int& polymer, const int& monomer, const int& atom ) : p(polymer), m(monomer), a(atom) {}
    //! test if object has been initialised
    bool is_null() const { return p >= 0; }
    const int& polymer() const { return p; }  //!< return polymer index
    const int& monomer() const { return m; }  //!< return monomer index
    const int& atom()    const { return a; }  //!< return atom index
    friend inline bool operator < ( MAtomIndex i1, MAtomIndex i2 ) { return ( i1.p < i2.p || ( i1.p == i2.p && ( i1.m < i2.m || ( i1.m == i2.m && i1.a < i2.a ) ) ) ); }
  private:
    int p, m, a;
  };

  //! Class for holding the indices of an atom within a MiniMol molecule class
  /*! The indices remain valid only while no changes are made to the
    MiniMol object. This class can also hold the number of a symmetry
    operator. */
  class MAtomIndexSymmetry : public MAtomIndex {
  public:
    //! null constructor
    MAtomIndexSymmetry() {}
    //! constructor: from polymer, monomer and atom numbers.
    MAtomIndexSymmetry( const int& polymer, const int& monomer, const int& atom , const int& symm ) : MAtomIndex(polymer,monomer,atom), s(symm) {}
    const int& symmetry() const { return s; }  //!< return symmetry index
  private:
    int s;
  };

  //! Find atoms in the vicinity of some coordinate in real space
  /*! Uses a fast non-bonded atom search. */
  class MAtomNonBond {
  public:
    //! null constructor
    MAtomNonBond() {}
    //! constructor: from MiniMol and grid radius
    MAtomNonBond( const clipper::MiniMol& mol, double rad = 5.0 );
    //! get a list of atoms in the rough vicinity of a coordinate
    std::vector<MAtomIndexSymmetry> atoms_near( const clipper::Coord_orth& co, double rad ) const;
    std::vector<MAtomIndexSymmetry> operator() ( const clipper::Coord_orth& co, double rad ) const;
    void debug() const;
  private:
    const MiniMol* mol_;
    double rad_;
    Spacegroup spgr;
    Cell cell;
    Grid_sampling grid;
    std::vector<int> lookup;
    std::vector<MAtomIndexSymmetry> atoms;
  };

} // namespace clipper

#endif

