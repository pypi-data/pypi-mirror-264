#!/usr/bin/env python3
import argparse
import glob
import os
from pathlib import Path


def main():

    parser = argparse.ArgumentParser(description="Clean up powheg directory")

    # Adding optional argument with default value
    parser.add_argument(
        "-p", "--path", default=".", type=str, help="path to powheg directory"
    )

    args = parser.parse_args()

    for r in ["btl", "rm", "reg"]:
        # remove single file
        for f in [
            "bornequiv",
            f"pwg-{r}grid.top",
            "pwggrid.dat",
            "pwgubound.dat",
            f"realequivregions-{r}",
            "FlavRegList",
            "pwgborngrid.top",
            "pwgcounters.dat",
            "pwghistnorms.top",
            "pwgxgrid.dat",
            "realequivregions-rad",
            "pwgboundviolations.dat",
            "pwgevents.lhe",
            "pwg-stat.dat",
            "pwhg_checklimits",
            "virtequiv",
            "parameters.ol",
            f"mint_upb_{r}upb.top",
            f"mint_upb_{r}upb_rat.top",
            "pwg-btilde-fullgrid.lock",
            "sigborn_equiv",
            "pwg-remn-fullgrid.lock",
            f"mint_upb_{r}upb.top",
            f"pwggrid-{r}.dat",
        ]:
            p = os.path.join(args.path, f)
            if os.path.exists(p):
                os.remove(p)
        # remove parallel run files
        for n, s in [
            ("pwg-", "-stat.dat"),
            (f"pwgxgrid-{r}", ".dat"),
            (f"pwggrid-{r}-", ".dat"),
            (f"pwg{r}upb-", ".dat"),
            ("pwgboundviolations-", ".dat"),
            ("pwghistnorms-", ".top"),
            ("pwgevents-", ".lhe"),
            ("pwgcounters-st4-", ".dat"),
            ("pwgcounters-st3-", ".dat"),
            ("pwgcounters-st1-", ".dat"),
            ("pwgcounters-st2-", ".dat"),
            (f"pwg-xg1-{r}-", ".top"),
            (f"pwg-xg1-xgrid-{r}-", ".dat"),
            (f"pwg-xg2-xgrid-{r}-", ".dat"),
            (f"pwg-xg2-xgrid-{r}-", ".top"),
            (f"pwg-st2-xgrid-{r}-", ".top"),
            ("pwgubound-", ".dat"),
            ("sigborn_equiv-", ""),
            ("sigvirtual_equiv-", ""),
            (f"sigreal_{r}0_equiv-", ""),
            ("sigreal_rad_equiv-", ""),
            ("pwgalone-output", ".top"),
            (f"pwgfullgrid-{r}-", ".dat"),
            ("pwhg_checklimits-", ""),
            ("pwg-", "-NLO.top"),
            ("pwg-", "-borngrid-stat.dat"),
            ("pwg-", "-xg1-stat.dat"),
            ("pwg-", "-xg2-stat.dat"),
            ("pwg-", "-st3-stat.dat"),
            ("pwg-", "-st2-stat.dat"),
        ]:
            for f in Path(args.path).glob(f"{n}*{s}"):
                os.remove(f)


if __name__ == "__main__":
    main()
