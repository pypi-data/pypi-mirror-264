/* ENO interpolation in 2-D */
/*
  Copyright (C) 2004 University of Texas at Austin

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program; if not, write to the Free Software
  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
*/

#include "eno.h"
#include "eno2.h"

#include "alloc.h"
#include "ngspice/cm.h"


struct Eno2 {
    int order, ng, n1, n2;
    sf_eno jnt, *ent;
    double *f, *f1;
};
/* concrete data type */

sf_eno2
sf_eno2_init (int order,      /* interpolation order */
              int n1, int n2  /* data dimensions */)
/*< Initialize interpolation object >*/
{
    int xrc = 0;
    sf_eno2 pnt = (sf_eno2) NULL;

    if ((pnt = (sf_eno2) sf_alloc(
            1, sizeof(*pnt))) == (sf_eno2) NULL) {
        cm_message_printf("Unable to allocate sf_eno2 structure "
                "in sf_eno2_init");
        xrc = -1;
        goto EXITPOINT;
    }

    pnt->order = order;
    pnt->n1 = n1;
    pnt->n2 = n2;
    pnt->ng = 2 * order - 2;
    if (pnt->ng > pnt->n2) {
        cm_message_printf("%s: ng=%d is too big", __FILE__, pnt->ng);
        xrc = -1;
        goto EXITPOINT;
    }

    if ((pnt->jnt = sf_eno_init(order, pnt->ng)) == (sf_eno) NULL) {
        cm_message_printf("Unable to initialize field jnt "
                "in sf_eno2_init");
        xrc = -1;
        goto EXITPOINT;
    }

    if ((pnt->f  = sf_doublealloc (pnt->ng)) == (double *) NULL) {
        cm_message_printf("Unable to allocate field f in sf_eno2_init()");
        xrc = -1;
        goto EXITPOINT;
    }

    if ((pnt->f1  = sf_doublealloc (pnt->ng)) == (double *) NULL) {
        cm_message_printf("Unable to allocate field f1 in sf_eno2_init()");
        xrc = -1;
        goto EXITPOINT;
    }

    if ((pnt->ent = (sf_eno *) sf_alloc(
            n2, sizeof(sf_eno))) == (sf_eno *) NULL) {
        cm_message_printf("Unable to allocate field ent in sf_eno2_init()");
        xrc = -1;
        goto EXITPOINT;
    }

    {
        int i2;
        for (i2 = 0; i2 < n2; i2++) {
            if ((pnt->ent[i2] = sf_eno_init(
                    order, n1)) == (sf_eno) NULL) {
                cm_message_printf("Unable to initialize field ent[%d] "
                        "in sf_eno3_init()",
                        i2);
                xrc = -1;
                goto EXITPOINT;
            }
        }
    }

EXITPOINT:
    if (xrc != 0) {
        if (pnt != (sf_eno2) NULL) {
            sf_eno2_close(pnt);
            pnt = (sf_eno2) NULL;
        }
    }
    return pnt;
}

void
sf_eno2_set (sf_eno2 pnt, double **c /* data [n2][n1] */)
/*< Set the interpolation table. c can be changed or freed afterwords. >*/
{
    int i2;

    for (i2 = 0; i2 < pnt->n2; i2++)
        sf_eno_set (pnt->ent[i2], c[i2]);
}

void
sf_eno2_close (sf_eno2 pnt)
/*< Free internal storage >*/
{
    int i2;

    if (!pnt)
        return;

    sf_eno_close (pnt->jnt);
    for (i2 = 0; i2 < pnt->n2; i2++)
        sf_eno_close (pnt->ent[i2]);
    free (pnt->f);
    free (pnt->f1);
    free (pnt->ent);
    free (pnt);
}

void
sf_eno2_apply (sf_eno2 pnt,
               int i, int j,       /* grid location */
               double x, double y, /* offset from grid */
               double *f,          /* output data value */
               double *f1,         /* output derivative [2] */
               der what            /* what to compute [FUNC,DER,BOTH] */)
/*< Apply interpolation. >*/
{
    int k, b2;
    double g;

    if (j - pnt->order + 2 < 0)
        b2 = 0;
    else if (j + pnt->order - 1 > pnt->n2 - 1)
        b2 = pnt->n2 - pnt->ng;
    else
        b2 = j - pnt->order + 2;

    j -= b2;

    for (k = 0; k < pnt->ng; k++)
        if (what != FUNC)
            sf_eno_apply (pnt->ent[b2 + k], i, x, pnt->f + k, pnt->f1 + k, BOTH);
        else
            sf_eno_apply (pnt->ent[b2 + k], i, x, pnt->f + k, pnt->f1 + k, FUNC);

    sf_eno_set (pnt->jnt, pnt->f);
    sf_eno_apply (pnt->jnt, j, y, f, f1 + 1, what);

    if (what != FUNC) {
        sf_eno_set (pnt->jnt, pnt->f1);
        sf_eno_apply (pnt->jnt, j, y, f1, &g, FUNC);
    }
}

/*      $Id: eno2.c 9044 2012-08-13 19:35:59Z vovizmus $         */
