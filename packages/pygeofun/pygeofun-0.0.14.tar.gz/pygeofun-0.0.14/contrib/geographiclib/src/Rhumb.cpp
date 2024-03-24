/**
 * \file Rhumb.cpp
 * \brief Implementation for GeographicLib::Rhumb and GeographicLib::RhumbLine
 * classes
 *
 * Copyright (c) Charles Karney (2014-2022) <charles@karney.com> and licensed
 * under the MIT/X11 License.  For more information, see
 * https://geographiclib.sourceforge.io/
 **********************************************************************/

#include <algorithm>
#include <GeographicLib/Rhumb.hpp>

#if defined(_MSC_VER)
// Squelch warnings about enum-float expressions
#  pragma warning (disable: 5055)
#endif

namespace GeographicLib {

  using namespace std;

  Rhumb::Rhumb(real a, real f, bool exact)
    : _ell(a, f)
    , _exact(exact)
    , _c2(_ell.Area() / (2 * Math::td))
  {
    // Generated by Maxima on 2015-05-15 08:24:04-04:00
#if GEOGRAPHICLIB_RHUMBAREA_ORDER == 4
    static const real coeff[] = {
      // R[0]/n^0, polynomial in n of order 4
      691, 7860, -20160, 18900, 0, 56700,
      // R[1]/n^1, polynomial in n of order 3
      1772, -5340, 6930, -4725, 14175,
      // R[2]/n^2, polynomial in n of order 2
      -1747, 1590, -630, 4725,
      // R[3]/n^3, polynomial in n of order 1
      104, -31, 315,
      // R[4]/n^4, polynomial in n of order 0
      -41, 420,
    };  // count = 20
#elif GEOGRAPHICLIB_RHUMBAREA_ORDER == 5
    static const real coeff[] = {
      // R[0]/n^0, polynomial in n of order 5
      -79036, 22803, 259380, -665280, 623700, 0, 1871100,
      // R[1]/n^1, polynomial in n of order 4
      41662, 58476, -176220, 228690, -155925, 467775,
      // R[2]/n^2, polynomial in n of order 3
      18118, -57651, 52470, -20790, 155925,
      // R[3]/n^3, polynomial in n of order 2
      -23011, 17160, -5115, 51975,
      // R[4]/n^4, polynomial in n of order 1
      5480, -1353, 13860,
      // R[5]/n^5, polynomial in n of order 0
      -668, 5775,
    };  // count = 27
#elif GEOGRAPHICLIB_RHUMBAREA_ORDER == 6
    static const real coeff[] = {
      // R[0]/n^0, polynomial in n of order 6
      128346268, -107884140, 31126095, 354053700, -908107200, 851350500, 0,
      2554051500LL,
      // R[1]/n^1, polynomial in n of order 5
      -114456994, 56868630, 79819740, -240540300, 312161850, -212837625,
      638512875,
      // R[2]/n^2, polynomial in n of order 4
      51304574, 24731070, -78693615, 71621550, -28378350, 212837625,
      // R[3]/n^3, polynomial in n of order 3
      1554472, -6282003, 4684680, -1396395, 14189175,
      // R[4]/n^4, polynomial in n of order 2
      -4913956, 3205800, -791505, 8108100,
      // R[5]/n^5, polynomial in n of order 1
      1092376, -234468, 2027025,
      // R[6]/n^6, polynomial in n of order 0
      -313076, 2027025,
    };  // count = 35
#elif GEOGRAPHICLIB_RHUMBAREA_ORDER == 7
    static const real coeff[] = {
      // R[0]/n^0, polynomial in n of order 7
      -317195588, 385038804, -323652420, 93378285, 1062161100, -2724321600LL,
      2554051500LL, 0, 7662154500LL,
      // R[1]/n^1, polynomial in n of order 6
      258618446, -343370982, 170605890, 239459220, -721620900, 936485550,
      -638512875, 1915538625,
      // R[2]/n^2, polynomial in n of order 5
      -248174686, 153913722, 74193210, -236080845, 214864650, -85135050,
      638512875,
      // R[3]/n^3, polynomial in n of order 4
      114450437, 23317080, -94230045, 70270200, -20945925, 212837625,
      // R[4]/n^4, polynomial in n of order 3
      15445736, -103193076, 67321800, -16621605, 170270100,
      // R[5]/n^5, polynomial in n of order 2
      -27766753, 16385640, -3517020, 30405375,
      // R[6]/n^6, polynomial in n of order 1
      4892722, -939228, 6081075,
      // R[7]/n^7, polynomial in n of order 0
      -3189007, 14189175,
    };  // count = 44
#elif GEOGRAPHICLIB_RHUMBAREA_ORDER == 8
    static const real coeff[] = {
      // R[0]/n^0, polynomial in n of order 8
      71374704821LL, -161769749880LL, 196369790040LL, -165062734200LL,
      47622925350LL, 541702161000LL, -1389404016000LL, 1302566265000LL, 0,
      3907698795000LL,
      // R[1]/n^1, polynomial in n of order 7
      -13691187484LL, 65947703730LL, -87559600410LL, 43504501950LL,
      61062101100LL, -184013329500LL, 238803815250LL, -162820783125LL,
      488462349375LL,
      // R[2]/n^2, polynomial in n of order 6
      30802104839LL, -63284544930LL, 39247999110LL, 18919268550LL,
      -60200615475LL, 54790485750LL, -21709437750LL, 162820783125LL,
      // R[3]/n^3, polynomial in n of order 5
      -8934064508LL, 5836972287LL, 1189171080, -4805732295LL, 3583780200LL,
      -1068242175, 10854718875LL,
      // R[4]/n^4, polynomial in n of order 4
      50072287748LL, 3938662680LL, -26314234380LL, 17167059000LL,
      -4238509275LL, 43418875500LL,
      // R[5]/n^5, polynomial in n of order 3
      359094172, -9912730821LL, 5849673480LL, -1255576140, 10854718875LL,
      // R[6]/n^6, polynomial in n of order 2
      -16053944387LL, 8733508770LL, -1676521980, 10854718875LL,
      // R[7]/n^7, polynomial in n of order 1
      930092876, -162639357, 723647925,
      // R[8]/n^8, polynomial in n of order 0
      -673429061, 1929727800,
    };  // count = 54
#else
#error "Bad value for GEOGRAPHICLIB_RHUMBAREA_ORDER"
#endif
    static_assert(sizeof(coeff) / sizeof(real) ==
                  ((maxpow_ + 1) * (maxpow_ + 4))/2,
                  "Coefficient array size mismatch for Rhumb");
    real d = 1;
    int o = 0;
    for (int l = 0; l <= maxpow_; ++l) {
      int m = maxpow_ - l;
      // R[0] is just an integration constant so it cancels when evaluating a
      // definite integral.  So don't bother computing it.  It won't be used
      // when invoking SinCosSeries.
      if (l)
        _rR[l] = d * Math::polyval(m, coeff + o, _ell._n) / coeff[o + m + 1];
      o += m + 2;
      d *= _ell._n;
    }
    // Post condition: o == sizeof(alpcoeff) / sizeof(real)
  }

  const Rhumb& Rhumb::WGS84() {
    static const Rhumb
      wgs84(Constants::WGS84_a(), Constants::WGS84_f(), false);
    return wgs84;
  }

  void Rhumb::GenInverse(real lat1, real lon1, real lat2, real lon2,
                         unsigned outmask,
                         real& s12, real& azi12, real& S12) const {
    real
      lon12 = Math::AngDiff(lon1, lon2),
      psi1 = _ell.IsometricLatitude(lat1),
      psi2 = _ell.IsometricLatitude(lat2),
      psi12 = psi2 - psi1,
      h = hypot(lon12, psi12);
    if (outmask & AZIMUTH)
      azi12 = Math::atan2d(lon12, psi12);
    if (outmask & DISTANCE) {
      real dmudpsi = DIsometricToRectifying(psi2, psi1);
      s12 = h * dmudpsi * _ell.QuarterMeridian() / Math::qd;
    }
    if (outmask & AREA)
      S12 = _c2 * lon12 *
        MeanSinXi(psi2 * Math::degree(), psi1 * Math::degree());
  }

  RhumbLine Rhumb::Line(real lat1, real lon1, real azi12) const
  { return RhumbLine(*this, lat1, lon1, azi12); }

  void Rhumb::GenDirect(real lat1, real lon1, real azi12, real s12,
                        unsigned outmask,
                        real& lat2, real& lon2, real& S12) const
  { Line(lat1, lon1, azi12).GenPosition(s12, outmask, lat2, lon2, S12); }

  Math::real Rhumb::DE(real x, real y) const {
    const EllipticFunction& ei = _ell._ell;
    real d = x - y;
    if (x * y <= 0)
      return d != 0 ? (ei.E(x) - ei.E(y)) / d : 1;
    // See DLMF: Eqs (19.11.2) and (19.11.4) letting
    // theta -> x, phi -> -y, psi -> z
    //
    // (E(x) - E(y)) / d = E(z)/d - k2 * sin(x) * sin(y) * sin(z)/d
    //
    // tan(z/2) = (sin(x)*Delta(y) - sin(y)*Delta(x)) / (cos(x) + cos(y))
    //          = d * Dsin(x,y) * (sin(x) + sin(y))/(cos(x) + cos(y)) /
    //             (sin(x)*Delta(y) + sin(y)*Delta(x))
    //          = t = d * Dt
    // sin(z) = 2*t/(1+t^2); cos(z) = (1-t^2)/(1+t^2)
    // Alt (this only works for |z| <= pi/2 -- however, this conditions holds
    // if x*y > 0):
    // sin(z) = d * Dsin(x,y) * (sin(x) + sin(y))/
    //          (sin(x)*cos(y)*Delta(y) + sin(y)*cos(x)*Delta(x))
    // cos(z) = sqrt((1-sin(z))*(1+sin(z)))
    real sx = sin(x), sy = sin(y), cx = cos(x), cy = cos(y);
    real Dt = Dsin(x, y) * (sx + sy) /
      ((cx + cy) * (sx * ei.Delta(sy, cy) + sy * ei.Delta(sx, cx))),
      t = d * Dt, Dsz = 2 * Dt / (1 + t*t),
      sz = d * Dsz, cz = (1 - t) * (1 + t) / (1 + t*t);
    return ((sz != 0 ? ei.E(sz, cz, ei.Delta(sz, cz)) / sz : 1)
            - ei.k2() * sx * sy) * Dsz;
  }

  Math::real Rhumb::DRectifying(real latx, real laty) const {
    real
      tbetx = _ell._f1 * Math::tand(latx),
      tbety = _ell._f1 * Math::tand(laty);
    return (Math::pi()/2) * _ell._b * _ell._f1 * DE(atan(tbetx), atan(tbety))
      * Dtan(latx, laty) * Datan(tbetx, tbety) / _ell.QuarterMeridian();
  }

  Math::real Rhumb::DIsometric(real latx, real laty) const {
    real
      phix = latx * Math::degree(), tx = Math::tand(latx),
      phiy = laty * Math::degree(), ty = Math::tand(laty);
    return Dasinh(tx, ty) * Dtan(latx, laty)
      - Deatanhe(sin(phix), sin(phiy)) * Dsin(phix, phiy);
  }

  Math::real Rhumb::SinCosSeries(bool sinp,
                                 real x, real y, const real c[], int n) {
    // N.B. n >= 0 and c[] has n+1 elements 0..n, of which c[0] is ignored.
    //
    // Use Clenshaw summation to evaluate
    //   m = (g(x) + g(y)) / 2         -- mean value
    //   s = (g(x) - g(y)) / (x - y)   -- average slope
    // where
    //   g(x) = sum(c[j]*SC(2*j*x), j = 1..n)
    //   SC = sinp ? sin : cos
    //   CS = sinp ? cos : sin
    //
    // This function returns only s; m is discarded.
    //
    // Write
    //   t = [m; s]
    //   t = sum(c[j] * f[j](x,y), j = 1..n)
    // where
    //   f[j](x,y) = [ (SC(2*j*x)+SC(2*j*y))/2 ]
    //               [ (SC(2*j*x)-SC(2*j*y))/d ]
    //
    //             = [       cos(j*d)*SC(j*p)    ]
    //               [ +/-(2/d)*sin(j*d)*CS(j*p) ]
    // (+/- = sinp ? + : -) and
    //    p = x+y, d = x-y
    //
    //   f[j+1](x,y) = A * f[j](x,y) - f[j-1](x,y)
    //
    //   A = [  2*cos(p)*cos(d)      -sin(p)*sin(d)*d]
    //       [ -4*sin(p)*sin(d)/d   2*cos(p)*cos(d)  ]
    //
    // Let b[n+1] = b[n+2] = [0 0; 0 0]
    //     b[j] = A * b[j+1] - b[j+2] + c[j] * I for j = n..1
    //    t =  (c[0] * I  - b[2]) * f[0](x,y) + b[1] * f[1](x,y)
    // c[0] is not accessed for s = t[2]
    real p = x + y, d = x - y,
      cp = cos(p), cd =          cos(d),
      sp = sin(p), sd = d != 0 ? sin(d)/d : 1,
      m = 2 * cp * cd, s = sp * sd;
    // 2x2 matrices stored in row-major order
    const real a[4] = {m, -s * d * d, -4 * s, m};
    real ba[4] = {0, 0, 0, 0};
    real bb[4] = {0, 0, 0, 0};
    real* b1 = ba;
    real* b2 = bb;
    if (n > 0) b1[0] = b1[3] = c[n];
    for (int j = n - 1; j > 0; --j) { // j = n-1 .. 1
      swap(b1, b2);
      // b1 = A * b2 - b1 + c[j] * I
      b1[0] = a[0] * b2[0] + a[1] * b2[2] - b1[0] + c[j];
      b1[1] = a[0] * b2[1] + a[1] * b2[3] - b1[1];
      b1[2] = a[2] * b2[0] + a[3] * b2[2] - b1[2];
      b1[3] = a[2] * b2[1] + a[3] * b2[3] - b1[3] + c[j];
    }
    // Here are the full expressions for m and s
    // m =   (c[0] - b2[0]) * f01 - b2[1] * f02 + b1[0] * f11 + b1[1] * f12;
    // s = - b2[2] * f01 + (c[0] - b2[3]) * f02 + b1[2] * f11 + b1[3] * f12;
    if (sinp) {
      // real f01 = 0, f02 = 0;
      real f11 = cd * sp, f12 = 2 * sd * cp;
      // m = b1[0] * f11 + b1[1] * f12;
      s = b1[2] * f11 + b1[3] * f12;
    } else {
      // real f01 = 1, f02 = 0;
      real f11 = cd * cp, f12 = - 2 * sd * sp;
      // m = c[0] - b2[0] + b1[0] * f11 + b1[1] * f12;
      s = - b2[2] + b1[2] * f11 + b1[3] * f12;
    }
    return s;
  }

  Math::real Rhumb::DConformalToRectifying(real chix, real chiy) const {
    return 1 + SinCosSeries(true, chix, chiy,
                            _ell.ConformalToRectifyingCoeffs(), tm_maxord);
  }

  Math::real Rhumb::DRectifyingToConformal(real mux, real muy) const {
    return 1 - SinCosSeries(true, mux, muy,
                            _ell.RectifyingToConformalCoeffs(), tm_maxord);
  }

  Math::real Rhumb::DIsometricToRectifying(real psix, real psiy) const {
    if (_exact) {
      real
        latx = _ell.InverseIsometricLatitude(psix),
        laty = _ell.InverseIsometricLatitude(psiy);
      return DRectifying(latx, laty) / DIsometric(latx, laty);
    } else {
      psix *= Math::degree();
      psiy *= Math::degree();
      return DConformalToRectifying(gd(psix), gd(psiy)) * Dgd(psix, psiy);
    }
  }

  Math::real Rhumb::DRectifyingToIsometric(real mux, real muy) const {
    real
      latx = _ell.InverseRectifyingLatitude(mux/Math::degree()),
      laty = _ell.InverseRectifyingLatitude(muy/Math::degree());
    return _exact ?
      DIsometric(latx, laty) / DRectifying(latx, laty) :
      Dgdinv(Math::taupf(Math::tand(latx), _ell._es),
             Math::taupf(Math::tand(laty), _ell._es)) *
      DRectifyingToConformal(mux, muy);
  }

  Math::real Rhumb::MeanSinXi(real psix, real psiy) const {
    return Dlog(cosh(psix), cosh(psiy)) * Dcosh(psix, psiy)
      + SinCosSeries(false, gd(psix), gd(psiy), _rR, maxpow_) * Dgd(psix, psiy);
  }

  RhumbLine::RhumbLine(const Rhumb& rh, real lat1, real lon1, real azi12)
    : _rh(rh)
    , _lat1(Math::LatFix(lat1))
    , _lon1(lon1)
    , _azi12(Math::AngNormalize(azi12))
  {
    real alp12 = _azi12 * Math::degree();
    _salp =      _azi12  == -Math::hd ? 0 : sin(alp12);
    _calp = fabs(_azi12) ==  Math::qd ? 0 : cos(alp12);
    _mu1 = _rh._ell.RectifyingLatitude(lat1);
    _psi1 = _rh._ell.IsometricLatitude(lat1);
    _r1 = _rh._ell.CircleRadius(lat1);
  }

  void RhumbLine::GenPosition(real s12, unsigned outmask,
                              real& lat2, real& lon2, real& S12) const {
    real
      mu12 = s12 * _calp * Math::qd / _rh._ell.QuarterMeridian(),
      mu2 = _mu1 + mu12;
    real psi2, lat2x, lon2x;
    if (fabs(mu2) <= Math::qd) {
      if (_calp != 0) {
        lat2x = _rh._ell.InverseRectifyingLatitude(mu2);
        real psi12 = _rh.DRectifyingToIsometric(  mu2 * Math::degree(),
                                                 _mu1 * Math::degree()) * mu12;
        lon2x = _salp * psi12 / _calp;
        psi2 = _psi1 + psi12;
      } else {
        lat2x = _lat1;
        lon2x = _salp * s12 / (_r1 * Math::degree());
        psi2 = _psi1;
      }
      if (outmask & AREA)
        S12 = _rh._c2 * lon2x *
          _rh.MeanSinXi(_psi1 * Math::degree(), psi2 * Math::degree());
      lon2x = outmask & LONG_UNROLL ? _lon1 + lon2x :
        Math::AngNormalize(Math::AngNormalize(_lon1) + lon2x);
    } else {
      // Reduce to the interval [-180, 180)
      mu2 = Math::AngNormalize(mu2);
      // Deal with points on the anti-meridian
      if (fabs(mu2) > Math::qd) mu2 = Math::AngNormalize(Math::hd - mu2);
      lat2x = _rh._ell.InverseRectifyingLatitude(mu2);
      lon2x = Math::NaN();
      if (outmask & AREA)
        S12 = Math::NaN();
    }
    if (outmask & LATITUDE) lat2 = lat2x;
    if (outmask & LONGITUDE) lon2 = lon2x;
  }

} // namespace GeographicLib
