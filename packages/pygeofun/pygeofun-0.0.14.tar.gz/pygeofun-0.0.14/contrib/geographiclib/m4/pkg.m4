# pkg.m4 - Macros to locate and utilise pkg-config.            -*- Autoconf -*-
# serial 1 (pkg-config-0.24)
#
# Copyright © 2004 Scott James Remnant <scott@netsplit.com>.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
# As a special exception to the GNU General Public License, if you
# distribute this file as part of a program that contains a
# configuration script generated by Autoconf, you may include it under
# the same distribution terms that you use for the rest of that program.

# PKG_PROG_PKG_CONFIG([MIN-VERSION])
# ----------------------------------
AC_DEFUN([PKG_PROG_PKG_CONFIG],
[m4_pattern_forbid([^_?PKG_[A-Z_]+$])
m4_pattern_allow([^PKG_CONFIG(_(PATH|LIBDIR|SYSROOT_DIR|ALLOW_SYSTEM_(CFLAGS|LIBS)))?$])
m4_pattern_allow([^PKG_CONFIG_(DISABLE_UNINSTALLED|TOP_BUILD_DIR|DEBUG_SPEW)$])
AC_ARG_VAR([PKG_CONFIG], [path to pkg-config utility])
AC_ARG_VAR([PKG_CONFIG_PATH], [directories to add to pkg-config's search path])
AC_ARG_VAR([PKG_CONFIG_LIBDIR], [path overriding pkg-config's built-in search path])

if test "x$ac_cv_env_PKG_CONFIG_set" != "xset"; then
	AC_PATH_TOOL([PKG_CONFIG], [pkg-config])
fi
if test -n "$PKG_CONFIG"; then
	_pkg_min_version=m4_default([$1], [0.9.0])
	AC_MSG_CHECKING([pkg-config is at least version $_pkg_min_version])
	if $PKG_CONFIG --atleast-pkgconfig-version $_pkg_min_version; then
		AC_MSG_RESULT([yes])
	else
		AC_MSG_RESULT([no])
		PKG_CONFIG=""
	fi
fi[]dnl
])# PKG_PROG_PKG_CONFIG

# PKG_CHECK_EXISTS(MODULES, [ACTION-IF-FOUND], [ACTION-IF-NOT-FOUND])
#
# Check to see whether a particular set of modules exists.  Similar
# to PKG_CHECK_MODULES(), but does not set variables or print errors.
#
# Please remember that m4 expands AC_REQUIRE([PKG_PROG_PKG_CONFIG])
# only at the first occurence in configure.ac, so if the first place
# it's called might be skipped (such as if it is within an "if", you
# have to call PKG_CHECK_EXISTS manually
# --------------------------------------------------------------
AC_DEFUN([PKG_CHECK_EXISTS],
[AC_REQUIRE([PKG_PROG_PKG_CONFIG])dnl
if test -n "$PKG_CONFIG" && \
    AC_RUN_LOG([$PKG_CONFIG --exists --print-errors "$1"]); then
  m4_default([$2], [:])
m4_ifvaln([$3], [else
  $3])dnl
fi])

# _PKG_CONFIG([VARIABLE], [COMMAND], [MODULES])
# ---------------------------------------------
m4_define([_PKG_CONFIG],
[if test -n "$$1"; then
    pkg_cv_[]$1="$$1"
 elif test -n "$PKG_CONFIG"; then
    PKG_CHECK_EXISTS([$3],
                     [pkg_cv_[]$1=`$PKG_CONFIG --[]$2 "$3" 2>/dev/null`
		      test "x$?" != "x0" && pkg_failed=yes ],
		     [pkg_failed=yes])
 else
    pkg_failed=untried
fi[]dnl
])# _PKG_CONFIG

# _PKG_SHORT_ERRORS_SUPPORTED
# -----------------------------
AC_DEFUN([_PKG_SHORT_ERRORS_SUPPORTED],
[AC_REQUIRE([PKG_PROG_PKG_CONFIG])
if $PKG_CONFIG --atleast-pkgconfig-version 0.20; then
        _pkg_short_errors_supported=yes
else
        _pkg_short_errors_supported=no
fi[]dnl
])# _PKG_SHORT_ERRORS_SUPPORTED


# PKG_CHECK_MODULES(VARIABLE-PREFIX, MODULES, [ACTION-IF-FOUND],
# [ACTION-IF-NOT-FOUND])
#
#
# Note that if there is a possibility the first call to
# PKG_CHECK_MODULES might not happen, you should be sure to include an
# explicit call to PKG_PROG_PKG_CONFIG in your configure.ac
#
#
# --------------------------------------------------------------
AC_DEFUN([PKG_CHECK_MODULES],
[AC_REQUIRE([PKG_PROG_PKG_CONFIG])dnl
AC_ARG_VAR([$1][_CFLAGS], [C compiler flags for $1, overriding pkg-config])dnl
AC_ARG_VAR([$1][_LIBS], [linker flags for $1, overriding pkg-config])dnl

pkg_failed=no
AC_MSG_CHECKING([for $1])

_PKG_CONFIG([$1][_CFLAGS], [cflags], [$2])
_PKG_CONFIG([$1][_LIBS], [libs], [$2])

m4_define([_PKG_TEXT], [Alternatively, you may set the environment variables $1[]_CFLAGS
and $1[]_LIBS to avoid the need to call pkg-config.
See the pkg-config man page for more details.])

if test $pkg_failed = yes; then
   	AC_MSG_RESULT([no])
        _PKG_SHORT_ERRORS_SUPPORTED
        if test $_pkg_short_errors_supported = yes; then
	        $1[]_PKG_ERRORS=`$PKG_CONFIG --short-errors --print-errors --cflags --libs "$2" 2>&1`
        else
	        $1[]_PKG_ERRORS=`$PKG_CONFIG --print-errors --cflags --libs "$2" 2>&1`
        fi
	# Put the nasty error message in config.log where it belongs
	echo "$$1[]_PKG_ERRORS" >&AS_MESSAGE_LOG_FD

	m4_default([$4], [AC_MSG_ERROR(
[Package requirements ($2) were not met:

$$1_PKG_ERRORS

Consider adjusting the PKG_CONFIG_PATH environment variable if you
installed software in a non-standard prefix.

_PKG_TEXT])[]dnl
        ])
elif test $pkg_failed = untried; then
     	AC_MSG_RESULT([no])
	m4_default([$4], [AC_MSG_FAILURE(
[The pkg-config script could not be found or is too old.  Make sure it
is in your PATH or set the PKG_CONFIG environment variable to the full
path to pkg-config.

_PKG_TEXT

To get pkg-config, see <http://pkg-config.freedesktop.org/>.])[]dnl
        ])
else
	$1[]_CFLAGS=$pkg_cv_[]$1[]_CFLAGS
	$1[]_LIBS=$pkg_cv_[]$1[]_LIBS
        AC_MSG_RESULT([yes])
	$3
fi[]dnl
])# PKG_CHECK_MODULES

# PKG_INSTALLDIR(DIRECTORY)
# -------------------------
# Substitutes the variable pkgconfigdir as the location where a module
# should install pkg-config .pc files. By default the directory is
# $libdir/pkgconfig, but the default can be changed by passing
# DIRECTORY. The user can override through the --with-pkgconfigdir
# parameter.
AC_DEFUN([PKG_INSTALLDIR],
[m4_pushdef([pkg_default], [m4_default([$1], ['${libdir}/pkgconfig'])])
m4_pushdef([pkg_description],
    [pkg-config installation directory @<:@]pkg_default[@:>@])
AC_ARG_WITH([pkgconfigdir],
    [AS_HELP_STRING([--with-pkgconfigdir], pkg_description)],,
    [with_pkgconfigdir=]pkg_default)
AC_SUBST([pkgconfigdir], [$with_pkgconfigdir])
m4_popdef([pkg_default])
m4_popdef([pkg_description])
]) dnl PKG_INSTALLDIR


# PKG_NOARCH_INSTALLDIR(DIRECTORY)
# -------------------------
# Substitutes the variable noarch_pkgconfigdir as the location where a
# module should install arch-independent pkg-config .pc files. By
# default the directory is $datadir/pkgconfig, but the default can be
# changed by passing DIRECTORY. The user can override through the
# --with-noarch-pkgconfigdir parameter.
AC_DEFUN([PKG_NOARCH_INSTALLDIR],
[m4_pushdef([pkg_default], [m4_default([$1], ['${datadir}/pkgconfig'])])
m4_pushdef([pkg_description],
    [pkg-config arch-independent installation directory @<:@]pkg_default[@:>@])
AC_ARG_WITH([noarch-pkgconfigdir],
    [AS_HELP_STRING([--with-noarch-pkgconfigdir], pkg_description)],,
    [with_noarch_pkgconfigdir=]pkg_default)
AC_SUBST([noarch_pkgconfigdir], [$with_noarch_pkgconfigdir])
m4_popdef([pkg_default])
m4_popdef([pkg_description])
]) dnl PKG_NOARCH_INSTALLDIR


# PKG_CHECK_VAR(VARIABLE, MODULE, CONFIG-VARIABLE,
# [ACTION-IF-FOUND], [ACTION-IF-NOT-FOUND])
# -------------------------------------------
# Retrieves the value of the pkg-config variable for the given module.
AC_DEFUN([PKG_CHECK_VAR],
[AC_REQUIRE([PKG_PROG_PKG_CONFIG])dnl
AC_ARG_VAR([$1], [value of $3 for $2, overriding pkg-config])dnl

_PKG_CONFIG([$1], [variable="][$3]["], [$2])
AS_VAR_COPY([$1], [pkg_cv_][$1])

AS_VAR_IF([$1], [""], [$5], [$4])dnl
])# PKG_CHECK_VAR

# PKG_WITH_MODULES(VARIABLE-PREFIX, MODULES,
#                  [ACTION-IF-FOUND],[ACTION-IF-NOT-FOUND],
#                  [DESCRIPTION], [DEFAULT])
#
# Prepare a "--with-" configure option using the lowercase [VARIABLE-PREFIX]
# name, merging the behaviour of AC_ARG_WITH and PKG_CHECK_MODULES in a single
# macro
#
# --------------------------------------------------------------
AC_DEFUN([PKG_WITH_MODULES],
[
m4_pushdef([with_arg], m4_tolower([$1]))

m4_pushdef([description],
           [m4_default([$5], [build with ]with_arg[ support])])

m4_pushdef([def_arg], [m4_default([$6], [auto])])
m4_pushdef([def_action_if_found], [AS_TR_SH([with_]with_arg)=yes])
m4_pushdef([def_action_if_not_found], [AS_TR_SH([with_]with_arg)=no])

m4_case(def_arg,
            [yes],[m4_pushdef([with_without], [--without-]with_arg)],
            [m4_pushdef([with_without],[--with-]with_arg)])

AC_ARG_WITH(with_arg,
     AS_HELP_STRING(with_without, description[ @<:@default=]def_arg[@:>@]),,
    [AS_TR_SH([with_]with_arg)=def_arg])

AS_CASE([$AS_TR_SH([with_]with_arg)],
            [yes],[PKG_CHECK_MODULES([$1],[$2],$3,$4)],
            [auto],[PKG_CHECK_MODULES([$1],[$2],
                                        [m4_n([def_action_if_found]) $3],
                                        [m4_n([def_action_if_not_found]) $4])])

m4_popdef([with_arg])
m4_popdef([description])
m4_popdef([def_arg])

]) dnl PKG_WITH_MODULES

# PKG_HAVE_WITH_MODULES(VARIABLE-PREFIX, MODULES,
#                       [DESCRIPTION], [DEFAULT])
#
# Convenience macro to trigger AM_CONDITIONAL after
# PKG_WITH_MODULES check.
#
# HAVE_[VARIABLE-PREFIX] is exported as make variable.
#
# --------------------------------------------------------------
AC_DEFUN([PKG_HAVE_WITH_MODULES],
[
PKG_WITH_MODULES([$1],[$2],,,[$3],[$4])

AM_CONDITIONAL([HAVE_][$1],
               [test "$AS_TR_SH([with_]m4_tolower([$1]))" = "yes"])
])

# PKG_HAVE_DEFINE_WITH_MODULES(VARIABLE-PREFIX, MODULES,
#                              [DESCRIPTION], [DEFAULT])
#
# Convenience macro to run AM_CONDITIONAL and AC_DEFINE after
# PKG_WITH_MODULES check.
#
# HAVE_[VARIABLE-PREFIX] is exported as make and preprocessor variable.
#
# --------------------------------------------------------------
AC_DEFUN([PKG_HAVE_DEFINE_WITH_MODULES],
[
PKG_HAVE_WITH_MODULES([$1],[$2],[$3],[$4])

AS_IF([test "$AS_TR_SH([with_]m4_tolower([$1]))" = "yes"],
        [AC_DEFINE([HAVE_][$1], 1, [Enable ]m4_tolower([$1])[ support])])
])
