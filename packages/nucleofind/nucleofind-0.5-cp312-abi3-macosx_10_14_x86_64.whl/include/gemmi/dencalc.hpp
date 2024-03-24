// Copyright 2019 Global Phasing Ltd.
//
// Tools to prepare a grid with values of electron density of a model.

#ifndef GEMMI_DENCALC_HPP_
#define GEMMI_DENCALC_HPP_

#include <cassert>
#include "addends.hpp"  // for Addends
#include "formfact.hpp" // for ExpSum
#include "grid.hpp"     // for Grid
#include "model.hpp"    // for Structure, ...

namespace gemmi {

template<int N, typename Real>
Real determine_cutoff_radius(Real x1, const ExpSum<N, Real>& precal, Real cutoff_level) {
  Real y1, dy;
  std::tie(y1, dy) = precal.calculate_with_derivative(x1);
  // Generally, density is supposed to decrease with radius.
  // But if we have addends (in particular -Z for Mott-Bothe),
  // it can first rise, then decrease. We want to be after the maximum.
  while (dy > 0) { // unlikely
    x1 += 1.0f;
    std::tie(y1, dy) = precal.calculate_with_derivative(x1);
  }
  Real x2 = x1;
  Real y2 = y1;
  if (y1 < cutoff_level) {
    while (y1 < cutoff_level) {
      x2 = x1;
      y2 = y1;
      x1 -= 0.5f;
      std::tie(y1, dy) = precal.calculate_with_derivative(x1);
      // with addends it's possible to land on the left side of the maximum
      if (dy > 0) { // unlikely
        while (dy > 0 && x1 + 0.1f < x2) {
          x1 += 0.1f;
          std::tie(y1, dy) = precal.calculate_with_derivative(x1);
        }
        if (y1 < cutoff_level)
          return x1;
        break;
      }
      if (x1 < 0) { // unlikely
        x1 = 0;
        y1 = precal.calculate(x1 * x1);
        break;
      }
    }
  } else {
    while (y2 > cutoff_level) {
      x1 = x2;
      y1 = y2;
      x2 += 0.5f;
      y2 = precal.calculate(x2 * x2);
    }
  }

  return x1 + (x1 - x2) / (y1 - y2) * (cutoff_level - y1);
}

// approximated radius of electron density (IT92) above cutoff=1e-5 for C
template <typename Real>
Real it92_radius_approx(Real b) {
  return (8.5f + 0.075f * b) / (2.4f + 0.0045f * b);
}

inline double get_minimum_b(const Model& model) {
  double b_min = 1000.;
  for (const Chain& chain : model.chains)
    for (const Residue& residue : chain.residues)
      for (const Atom& atom : residue.atoms) {
        if (atom.occ == 0) continue;
        double b = atom.b_iso;
        if (atom.aniso.nonzero()) {
          std::array<double,3> eig = atom.aniso.calculate_eigenvalues();
          b = std::min(std::min(eig[0], eig[1]), eig[2]) * u_to_b();
        }
        if (b < b_min)
          b_min = b;
      }
  return b_min;
}

// Usual usage:
// - set d_min and optionally also other parameters,
// - set addends to f' values for your wavelength (see fprime.hpp)
// - use set_grid_cell_and_spacegroup() to set grid's unit cell and space group
// - check that Table has SF coefficients for all elements that are to be used
// - call put_model_density_on_grid()
// - do FFT using transform_map_to_f_phi()
// - if blur is used, multiply the SF by reciprocal_space_multiplier()
template <typename Table, typename GReal>
struct DensityCalculator {
  // GReal = type of grid; CReal = type of coefficients in Table
  using CReal = typename Table::Coef::coef_type;
  Grid<GReal> grid;
  double d_min = 0.;
  double rate = 1.5;
  double blur = 0.;
  float cutoff = 1e-5f;
#if GEMMI_COUNT_DC
  size_t atoms_added = 0;
  size_t density_computations = 0;
#endif
  Addends addends;

  double requested_grid_spacing() const { return d_min / (2 * rate); }

  void set_refmac_compatible_blur(const Model& model) {
    double spacing = requested_grid_spacing();
    if (spacing <= 0)
      spacing = grid.min_spacing();
    double b_min = get_minimum_b(model);
    blur = std::max(u_to_b() / 1.1 * sq(spacing) - b_min, 0.);
  }

  // pre: check if Table::has(atom.element)
  void add_atom_density_to_grid(const Atom& atom) {
    Element el = atom.element;
    do_add_atom_density_to_grid(atom, Table::get(el, atom.charge), addends.get(el));
  }

  // Parameter c is a constant factor and has the same meaning as either addend
  // or c in scattering factor coefficients (a1, b1, ..., c).
  void add_c_contribution_to_grid(const Atom& atom, float c) {
    do_add_atom_density_to_grid(atom, GaussianCoef<0, 1, CReal>{0}, c);
  }

  template<int N>
  CReal estimate_radius(const ExpSum<N, CReal>& precal, CReal b) const {
    if (N == 1)
      return std::sqrt(std::log(cutoff / std::abs(precal.a[0])) / precal.b[0]);
    CReal x1 = it92_radius_approx(b);
    return determine_cutoff_radius(x1, precal, (CReal)cutoff);
  }

  template<typename Coef>
  void do_add_atom_density_to_grid(const Atom& atom, const Coef& coef, float addend) {
#if GEMMI_COUNT_DC
    ++atoms_added;
#endif
    Fractional fpos = grid.unit_cell.fractionalize(atom.pos);
    if (!atom.aniso.nonzero()) {
      // isotropic
      CReal b = static_cast<CReal>(atom.b_iso + blur);
      auto precal = coef.precalculate_density_iso(b, addend);
      CReal radius = estimate_radius(precal, b);
      grid.template use_points_around<true>(fpos, radius, [&](GReal& point, double r2) {
          point += GReal(atom.occ * precal.calculate((CReal)r2));
#if GEMMI_COUNT_DC
          ++density_computations;
#endif
      }, /*fail_on_too_large_radius=*/false);
    } else {
      // anisotropic
      auto aniso_b = atom.aniso.scaled(CReal(u_to_b())).added_kI(CReal(blur));
      // rough estimate, so we don't calculate eigenvalues
      CReal b_max = std::max(std::max(aniso_b.u11, aniso_b.u22), aniso_b.u33);
      auto precal_iso = coef.precalculate_density_iso(b_max, addend);
      double radius = estimate_radius(precal_iso, b_max);
      auto precal = coef.precalculate_density_aniso_b(aniso_b, addend);
      int du = (int) std::ceil(radius / grid.spacing[0]);
      int dv = (int) std::ceil(radius / grid.spacing[1]);
      int dw = (int) std::ceil(radius / grid.spacing[2]);
      grid.template use_points_in_box<true>(
          fpos, du, dv, dw,
          [&](GReal& point, double, const Position& delta, int, int, int) {
            point += GReal(atom.occ * precal.calculate(delta));
#if GEMMI_COUNT_DC
            ++density_computations;
#endif
          },
          false, radius);
    }
  }

  void initialize_grid() {
    grid.data.clear();
    double spacing = requested_grid_spacing();
    if (spacing > 0)
      grid.set_size_from_spacing(spacing, GridSizeRounding::Up);
    else if (grid.point_count() > 0)
      // d_min not set, but a custom grid has been setup by the user
      grid.fill(0.);
    else
      fail("initialize_grid(): d_min is not set");
  }

  void add_model_density_to_grid(const Model& model) {
    grid.check_not_empty();
    for (const Chain& chain : model.chains)
      for (const Residue& res : chain.residues)
        for (const Atom& atom : res.atoms)
          add_atom_density_to_grid(atom);
  }

  void put_model_density_on_grid(const Model& model) {
    initialize_grid();
    add_model_density_to_grid(model);
    grid.symmetrize_sum();
  }

  void set_grid_cell_and_spacegroup(const Structure& st) {
    grid.unit_cell = st.cell;
    grid.spacegroup = st.find_spacegroup();
  }

  // The argument is 1/d^2 - as outputted by unit_cell.calculate_1_d2(hkl).
  double reciprocal_space_multiplier(double inv_d2) const {
    return std::exp(blur * 0.25 * inv_d2);
  }

  double mott_bethe_factor(const Miller& hkl) const {
    double inv_d2 = grid.unit_cell.calculate_1_d2(hkl);
    double factor = -mott_bethe_const() / inv_d2;
    return blur == 0 ? factor : factor * reciprocal_space_multiplier(inv_d2);
  }
};

} // namespace gemmi
#endif
