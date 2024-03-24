// Copyright 2020 Global Phasing Ltd.

// Electron scattering factor coefficients from the International Tables.
//
// Based on International Tables for Crystallography Volume C, edition 2011,
// table 4.3.2.2 (pp. 282-283): "Elastic atomic scattering factors of electrons
// for neutral atoms and s up to 2.0 A^-1".
// The same data is included in cctbx and in CCP4 (file atomsf_electron.lib).

#ifndef GEMMI_C4322_HPP_
#define GEMMI_C4322_HPP_

#include "formfact.hpp"  // for GaussianCoef
#include "elem.hpp"      // for El

namespace gemmi {

#if defined(__GNUC__) && __GNUC__-0 > 4
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wfloat-conversion"
#endif

template<class Real>
struct C4322 {
  using Coef = GaussianCoef<5, 0, Real>;
  static Coef data[99];

  static bool has(El el) {
    return el <= El::Cf || el == El::D;
  }

  static Coef& get(El el, signed char /*charge*/=0) {
    // ordinal for X, H, ... Cf; H=1 for D; X=0 for Es, ... Og
    int pos = el <= El::Cf ? (int)el : (int)(el == El::D);
    return data[pos];
  }
};

template<class Real>
typename C4322<Real>::Coef C4322<Real>::data[99] = {
  // a1, a2, a3, a4, a5, b1, b2, b3, b4, b5
  {0.0974, 0.2921, 0.691, 0.699, 0.2039, 0.2067, 1.3815, 4.6943, 12.7105, 32.4726}, // X=O
  {0.0349, 0.1201, 0.197, 0.0573, 0.1195, 0.5347, 3.5867, 12.3471, 18.9525, 38.6269}, // H
  {0.0317, 0.0838, 0.1526, 0.1334, 0.0164, 0.2507, 1.4751, 4.4938, 12.6646, 31.1653}, // He
  {0.075, 0.2249, 0.5548, 1.4954, 0.9354, 0.3864, 2.9383, 15.3829, 53.5545, 138.7337}, // Li
  {0.078, 0.221, 0.674, 1.3867, 0.6925, 0.3131, 2.2381, 10.1517, 30.9061, 78.3273}, // Be
  {0.0909, 0.2551, 0.7738, 1.2136, 0.4606, 0.2995, 2.1155, 8.3816, 24.1292, 63.1314}, // B
  {0.0893, 0.2563, 0.757, 1.0487, 0.3575, 0.2465, 1.71, 6.4094, 18.6113, 50.2523}, // C
  {0.1022, 0.3219, 0.7982, 0.8197, 0.1715, 0.2451, 1.7481, 6.1925, 17.3894, 48.1431}, // N
  {0.0974, 0.2921, 0.691, 0.699, 0.2039, 0.2067, 1.3815, 4.6943, 12.7105, 32.4726}, // O
  {0.1083, 0.3175, 0.6487, 0.5846, 0.1421, 0.2057, 1.3439, 4.2788, 11.3932, 28.7881}, // F
  {0.1269, 0.3535, 0.5582, 0.4674, 0.146, 0.22, 1.3779, 4.0203, 9.4934, 23.1278}, // Ne
  {0.2142, 0.6853, 0.7692, 1.6589, 1.4482, 0.3334, 2.3446, 10.083, 48.3037, 138.27}, // Na
  {0.2314, 0.6866, 0.9677, 2.1882, 1.1339, 0.3278, 2.272, 10.9241, 39.2898, 101.9748}, // Mg
  {0.239, 0.6573, 1.2011, 2.5586, 1.2312, 0.3138, 2.1063, 10.4163, 34.4552, 98.5344}, // Al
  {0.2519, 0.6372, 1.3795, 2.5082, 1.05, 0.3075, 2.0174, 9.6746, 29.3744, 80.4732}, // Si
  {0.2548, 0.6106, 1.4541, 2.3204, 0.8477, 0.2908, 1.874, 8.5176, 24.3434, 63.2996}, // P
  {0.2497, 0.5628, 1.3899, 2.1865, 0.7715, 0.2681, 1.6711, 7.0267, 19.5377, 50.3888}, // S
  {0.2443, 0.5397, 1.3919, 2.0197, 0.6621, 0.2468, 1.5242, 6.1537, 16.6687, 42.3086}, // Cl
  {0.2385, 0.5017, 1.3428, 1.8899, 0.6079, 0.2289, 1.3694, 5.2561, 14.0928, 35.5361}, // Ar
  {0.4115, 1.4031, 2.2784, 2.6742, 2.2162, 0.3703, 3.3874, 13.1029, 68.9592, 194.4329}, // K
  {0.4054, 1.388, 2.1602, 3.7532, 2.2063, 0.3499, 3.0991, 11.9608, 53.9353, 142.3892}, // Ca
  {0.3787, 1.2181, 2.0594, 3.2618, 2.387, 0.3133, 2.5856, 9.5813, 41.7688, 116.7282}, // Sc
  {0.3825, 1.2598, 2.0008, 3.0617, 2.0694, 0.304, 2.4863, 9.2783, 39.0751, 109.4583}, // Ti
  {0.3876, 1.275, 1.9109, 2.8314, 1.8979, 0.2967, 2.378, 8.7981, 35.9528, 101.7201}, // V
  {0.4046, 1.3696, 1.8941, 2.08, 1.2196, 0.2986, 2.3958, 9.1406, 37.4701, 113.7121}, // Cr
  {0.3796, 1.2094, 1.7815, 2.542, 1.5937, 0.2699, 2.0455, 7.4726, 31.0604, 91.5622}, // Mn
  {0.3946, 1.2725, 1.7031, 2.314, 1.4795, 0.2717, 2.0443, 7.6007, 29.9714, 86.2265}, // Fe
  {0.4118, 1.3161, 1.6493, 2.193, 1.283, 0.2742, 2.0372, 7.7205, 29.968, 84.9383}, // Co
  {0.386, 1.1765, 1.5451, 2.073, 1.3814, 0.2478, 1.766, 6.3107, 25.2204, 74.3146}, // Ni
  {0.4314, 1.3208, 1.5236, 1.4671, 0.8562, 0.2694, 1.9223, 7.3474, 28.9892, 90.6246}, // Cu
  {0.4288, 1.2646, 1.4472, 1.8294, 1.0934, 0.2593, 1.7998, 6.75, 25.586, 73.5284}, // Zn
  {0.4818, 1.4032, 1.6561, 2.4605, 1.1054, 0.2825, 1.9785, 8.7546, 32.5238, 98.5523}, // Ga
  {0.4655, 1.3014, 1.6088, 2.6998, 1.3003, 0.2647, 1.7926, 7.6071, 26.5541, 77.5238}, // Ge
  {0.4517, 1.2229, 1.5852, 2.7958, 1.2638, 0.2493, 1.6436, 6.8154, 22.3681, 62.039}, // As
  {0.4477, 1.1678, 1.5843, 2.8087, 1.1956, 0.2405, 1.5442, 6.3231, 19.461, 52.0233}, // Se
  {0.4798, 1.1948, 1.8695, 2.6953, 0.8203, 0.2504, 1.5963, 6.9653, 19.8492, 50.3233}, // Br
  {0.4546, 1.0993, 1.7696, 2.7068, 0.8672, 0.2309, 1.4279, 5.9449, 16.6752, 42.2243}, // Kr
  {1.016, 2.8528, 3.5466, -7.7804, 12.1148, 0.4853, 5.0925, 25.7851, 130.4515, 138.6775},// Rb
  {0.6703, 1.4926, 3.3368, 4.46, 3.1501, 0.319, 2.2287, 10.3504, 52.3291, 151.2216}, // Sr
  {0.6894, 1.5474, 3.245, 4.2126, 2.9764, 0.3189, 2.2904, 10.0062, 44.0771, 125.012}, // Y
  {0.6719, 1.4684, 3.1668, 3.9557, 2.892, 0.3036, 2.1249, 8.9236, 36.8458, 108.2049}, // Zr
  {0.6123, 1.2677, 3.0348, 3.3841, 2.3683, 0.2709, 1.7683, 7.2489, 27.9465, 98.5624}, // Nb
  {0.6773, 1.4798, 3.1788, 3.0824, 1.8384, 0.292, 2.0606, 8.1129, 30.5336, 100.0658}, // Mo
  {0.7082, 1.6392, 3.1993, 3.4327, 1.8711, 0.2976, 2.2106, 8.5246, 33.1456, 96.6377}, // Tc
  {0.6735, 1.4934, 3.0966, 2.7254, 1.5597, 0.2773, 1.9716, 7.3249, 26.6891, 90.5581}, // Ru
  {0.6413, 1.369, 2.9854, 2.6952, 1.5433, 0.258, 1.7721, 6.3854, 23.2549, 85.1517}, // Rh
  {0.5904, 1.1775, 2.6519, 2.2875, 0.8689, 0.2324, 1.5019, 5.1591, 15.5428, 46.8213}, // Pd
  {0.6377, 1.379, 2.8294, 2.3631, 1.4553, 0.2466, 1.6974, 5.7656, 20.0943, 76.7372}, // Ag
  {0.6364, 1.4247, 2.7802, 2.5973, 1.7886, 0.2407, 1.6823, 5.6588, 20.7219, 69.1109}, // Cd
  {0.6768, 1.6589, 2.774, 3.1835, 2.1326, 0.2522, 1.8545, 6.2936, 25.1457, 84.5448}, // In
  {0.7224, 1.961, 2.7161, 3.5603, 1.8972, 0.2651, 2.0604, 7.3011, 27.5493, 81.3349}, // Sn
  {0.7106, 1.9247, 2.6149, 3.8322, 1.8899, 0.2562, 1.9646, 6.8852, 24.7648, 68.9168}, // Sb
  {0.6947, 1.869, 2.5356, 4.0013, 1.8955, 0.2459, 1.8542, 6.4411, 22.173, 59.2206}, // Te
  {0.7047, 1.9484, 2.594, 4.1526, 1.5057, 0.2455, 1.8638, 6.7639, 21.8007, 56.4395}, // I
  {0.6737, 1.7908, 2.4129, 4.21, 1.7058, 0.2305, 1.689, 5.8218, 18.3928, 47.2496}, // Xe
  {1.2704, 3.8018, 5.6618, 0.9205, 4.8105, 0.4356, 4.2058, 23.4342, 136.7783, 171.7561}, // Cs
  {0.9049, 2.6076, 4.8498, 5.1603, 4.7388, 0.3066, 2.4363, 12.1821, 54.6135, 161.9978}, // Ba
  {0.8405, 2.3863, 4.6139, 5.1514, 4.7949, 0.2791, 2.141, 10.34, 41.9148, 132.0204}, // La
  {0.8551, 2.3915, 4.5772, 5.0278, 4.5118, 0.2805, 2.12, 10.1808, 42.0633, 130.9893}, // Ce
  {0.9096, 2.5313, 4.5266, 4.6376, 4.369, 0.2939, 2.2471, 10.8266, 48.8842, 147.602}, // Pr
  {0.8807, 2.4183, 4.4448, 4.6858, 4.1725, 0.2802, 2.0836, 10.0357, 47.4506, 146.9976}, // Nd
  {0.9471, 2.5463, 4.3523, 4.4789, 3.908, 0.2977, 2.2276, 10.5762, 49.3619, 145.358}, // Pm
  {0.9699, 2.5837, 4.2778, 4.4575, 3.5985, 0.3003, 2.2447, 10.6487, 50.7994, 146.4179}, // Sm
  {0.8694, 2.2413, 3.9196, 3.9694, 4.5498, 0.2653, 1.859, 8.3998, 36.7397, 125.7089}, // Eu
  {0.9673, 2.4702, 4.1148, 4.4972, 3.2099, 0.2909, 2.1014, 9.7067, 43.427, 125.9474}, // Gd
  {0.9325, 2.3673, 3.8791, 3.9674, 3.7996, 0.2761, 1.9511, 8.9296, 41.5937, 131.0122}, // Tb
  {0.9505, 2.3705, 3.8218, 4.0471, 3.4451, 0.2773, 1.9469, 8.8862, 43.0938, 133.1396}, // Dy
  {0.9248, 2.2428, 3.6182, 3.791, 3.7912, 0.266, 1.8183, 7.9655, 33.1129, 101.8139}, // Ho
  {1.0373, 2.4824, 3.6558, 3.8925, 3.0056, 0.2944, 2.0797, 9.4156, 45.8056, 132.772}, // Er
  {1.0075, 2.3787, 3.544, 3.6932, 3.1759, 0.2816, 1.9486, 8.7162, 41.842, 125.032}, // Tm
  {1.0347, 2.3911, 3.4619, 3.6556, 3.0052, 0.2855, 1.9679, 8.7619, 42.3304, 125.6499}, // Yb
  {0.9927, 2.2436, 3.3554, 3.7813, 3.0994, 0.2701, 1.8073, 7.8112, 34.4849, 103.3526}, // Lu
  {1.0295, 2.2911, 3.411, 3.9497, 2.4925, 0.2761, 1.8625, 8.0961, 34.2712, 98.5295}, // Hf
  {1.019, 2.2291, 3.4097, 3.9252, 2.2679, 0.2694, 1.7962, 7.6944, 31.0942, 91.1089}, // Ta
  {0.9853, 2.1167, 3.357, 3.7981, 2.2798, 0.2569, 1.6745, 7.0098, 26.9234, 81.391}, // W
  {0.9914, 2.0858, 3.4531, 3.8812, 1.8526, 0.2548, 1.6518, 6.8845, 26.7234, 81.7215}, // Re
  {0.9813, 2.0322, 3.3665, 3.6235, 1.9741, 0.2487, 1.5973, 6.4737, 23.2817, 70.9254}, // Os
  {1.0194, 2.0645, 3.4425, 3.4914, 1.6976, 0.2554, 1.6475, 6.5966, 23.2269, 70.0272}, // Ir
  {0.9148, 1.8096, 3.2134, 3.2953, 1.5754, 0.2263, 1.3813, 5.3243, 17.5987, 60.0171}, // Pt
  {0.9674, 1.8916, 3.3993, 3.0524, 1.2607, 0.2358, 1.4712, 5.6758, 18.7119, 61.5286}, // Au
  {1.0033, 1.9469, 3.4396, 3.1548, 1.418, 0.2413, 1.5298, 5.8009, 19.452, 60.5753}, // Hg
  {1.0689, 2.1038, 3.6039, 3.4927, 1.8283, 0.254, 1.6715, 6.3509, 23.1531, 78.7099}, // Tl
  {1.0891, 2.1867, 3.616, 3.8031, 1.8994, 0.2552, 1.7174, 6.5131, 23.917, 74.7039}, // Pb
  {1.1007, 2.2306, 3.5689, 4.1549, 2.0382, 0.2546, 1.7351, 6.4948, 23.6464, 70.378}, // Bi
  {1.1568, 2.4353, 3.6459, 4.4064, 1.7179, 0.2648, 1.8786, 7.1749, 25.1766, 69.2821}, // Po
  {1.0909, 2.1976, 3.3831, 4.67, 2.1277, 0.2466, 1.6707, 6.0197, 20.7657, 57.2663}, // At
  {1.0756, 2.163, 3.3178, 4.8852, 2.0489, 0.2402, 1.6169, 5.7644, 19.4568, 52.5009}, // Rn
  {1.4282, 3.5081, 5.6767, 4.1964, 3.8946, 0.3183, 2.6889, 13.4816, 54.3866, 200.8321}, // Fr
  {1.3127, 3.1243, 5.2988, 5.3891, 5.4133, 0.2887, 2.2897, 10.8276, 43.5389, 145.6109}, // Ra
  {1.3128, 3.1021, 5.3385, 5.9611, 4.7562, 0.2861, 2.2509, 10.5287, 41.7796, 128.2973}, // Ac
  {1.2553, 2.9178, 5.0862, 6.1206, 4.7122, 0.2701, 2.0636, 9.3051, 34.5977, 107.92}, // Th
  {1.3218, 3.1444, 5.4371, 5.6444, 4.0107, 0.2827, 2.225, 10.2454, 41.1162, 124.4449}, // Pa
  {1.3382, 3.2043, 5.4558, 5.4839, 3.6342, 0.2838, 2.2452, 10.2519, 41.7251, 124.9023}, // U
  {1.5193, 4.0053, 6.5327, -0.1402, 6.7489, 0.3213, 2.8206, 14.8878, 68.9103, 81.7257}, // Np
  {1.3517, 3.2937, 5.3213, 4.6466, 3.5714, 0.2813, 2.2418, 9.9952, 42.7939, 132.1739}, // Pu
  {1.2135, 2.7962, 4.7545, 4.5731, 4.4786, 0.2483, 1.8437, 7.5421, 29.3841, 112.4579}, // Am
  {1.2937, 3.11, 5.0393, 4.7546, 3.5031, 0.2638, 2.0341, 8.7101, 35.2992, 109.4972}, // Cm
  {1.2915, 3.1023, 4.9309, 4.6009, 3.4661, 0.2611, 2.0023, 8.4377, 34.1559, 105.8911}, // Bk
  {1.2089, 2.7391, 4.3482, 4.0047, 4.6497, 0.2421, 1.7487, 6.7262, 23.2153, 80.3108}, // Cf
};

#if defined(__GNUC__) && __GNUC__-0 > 4
#pragma GCC diagnostic pop
#endif

} // namespace gemmi
#endif
