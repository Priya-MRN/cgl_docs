# -*- coding: utf-8 -*-
"""Insert downloaded figures into the chapter/GA markdown files.

Each rule: (relative md path, heading-substring to anchor after, image file,
caption). The image + italic caption are inserted immediately after the first
heading line containing the substring (case-insensitive). Idempotent: skips if
the image filename is already referenced in the file.
"""
import sys, io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
HERE = Path(__file__).resolve().parent

# md file (relative), heading substring, asset filename, caption
RULES = [
    # Ch1
    ("chapters/Ch01_Electronic_Components_Materials.md", "resistor", "resistor_colour_code.png", "Resistor colour-code chart"),
    ("chapters/Ch01_Electronic_Components_Materials.md", "capacitor", "capacitor_types.png", "Common capacitor types"),
    ("chapters/Ch01_Electronic_Components_Materials.md", "magnetic material", "bh_hysteresis_loop.png", "B–H hysteresis loops: soft vs hard magnetic material"),
    # Ch2
    ("chapters/Ch02_Electronic_Devices_Circuits.md", "Junction formation", "pn_junction_diode.png", "PN-junction diode: depletion region and circuit symbol"),
    ("chapters/Ch02_Electronic_Devices_Circuits.md", "Diode equation and V-I", "diode_iv_curve.png", "Diode forward/reverse V–I characteristic"),
    ("chapters/Ch02_Electronic_Devices_Circuits.md", "Bridge rectifier", "bridge_rectifier.png", "Full-wave bridge rectifier (Graetz bridge)"),
    ("chapters/Ch02_Electronic_Devices_Circuits.md", "Operation (active region", "npn_bjt_operation.png", "NPN BJT carrier flow in the active region"),
    ("chapters/Ch02_Electronic_Devices_Circuits.md", "LC oscillators", "colpitts_oscillator.png", "Colpitts oscillator (capacitive tap — an LC oscillator)"),
    ("chapters/Ch02_Electronic_Devices_Circuits.md", "SCR", "scr_symbol.png", "SCR / thyristor symbol"),
    # Ch3
    ("chapters/Ch03_Digital_Electronics.md", "Full adder", "full_adder.png", "Full-adder logic diagram"),
    ("chapters/Ch03_Digital_Electronics.md", "JK flip", "jk_flip_flop_timing.png", "JK flip-flop timing diagram"),
    ("chapters/Ch03_Digital_Electronics.md", "Asynchronous (ripple) counter", "ripple_counter.png", "Asynchronous (ripple) counter using JK flip-flops"),
    # Ch4
    ("chapters/Ch04_Linear_Integrated_Circuits.md", "Inverting", "opamp_inverting.png", "Inverting amplifier (gain −Rf/Rin)"),
    ("chapters/Ch04_Linear_Integrated_Circuits.md", "Non-inverting", "opamp_noninverting.png", "Non-inverting amplifier (gain 1+Rf/Rin)"),
    ("chapters/Ch04_Linear_Integrated_Circuits.md", "astable", "ne555_astable.png", "555 timer in astable mode"),
    ("chapters/Ch04_Linear_Integrated_Circuits.md", "phase-locked", "pll_block.png", "Phase-locked loop (PLL) block diagram"),
    # Ch5
    ("chapters/Ch05_Microprocessor_Microcontroller.md", "Intel 8085", "intel_8085_arch.png", "Intel 8085 internal architecture"),
    # Ch6
    ("chapters/Ch06_Electronic_Measurements.md", "CRT", "crt_diagram.png", "Cathode-ray tube of a CRO"),
    ("chapters/Ch06_Electronic_Measurements.md", "Wheatstone", "wheatstone_bridge.png", "Wheatstone bridge for resistance measurement"),
    ("chapters/Ch06_Electronic_Measurements.md", "LVDT", "lvdt.png", "LVDT displacement transducer"),
    # Ch7
    ("chapters/Ch07_Communication_Engineering.md", "Expression & Modulation Index", "amplitude_modulation.png", "Amplitude modulation: message, carrier, AM wave"),
    ("chapters/Ch07_Communication_Engineering.md", "Expressions", "frequency_modulation.png", "Frequency modulation waveform"),
    ("chapters/Ch07_Communication_Engineering.md", "Superheterodyne", "superheterodyne_rx.png", "Superheterodyne receiver block diagram"),
    ("chapters/Ch07_Communication_Engineering.md", "Optical", "optical_fibre_modes.png", "Step-index vs graded-index optical fibre"),
    ("chapters/Ch07_Communication_Engineering.md", "Frequency Bands", "em_spectrum.png", "Electromagnetic spectrum"),
    # Ch8
    ("chapters/Ch08_Data_Communication_Networks.md", "OSI", "osi_model.png", "OSI seven-layer reference model"),
    ("chapters/Ch08_Data_Communication_Networks.md", "topolog", "network_topologies.png", "Bus, star, ring, mesh and tree topologies"),
    # Ch10
    ("chapters/Ch10_Basic_Electrical_Engineering.md", "Ohm", "ohms_law.png", "Ohm's-law circuit"),
    ("chapters/Ch10_Basic_Electrical_Engineering.md", "Star", "star_delta.png", "Star (Y) and delta (Δ) connections"),
    # GA Physics
    ("general-abilities/GA01_Physics_NCERT.md", "light", "convex_lens_ray.png", "Ray diagram through a convex lens"),
    ("general-abilities/GA01_Physics_NCERT.md", "spectrum", "em_spectrum_physics.png", "Electromagnetic spectrum"),
    # GA Chemistry
    ("general-abilities/GA02_Chemistry_NCERT.md", "periodic", "periodic_table.png", "Modern periodic table"),
]


def insert(md_rel, anchor, img, caption):
    p = HERE / md_rel
    if not p.exists():
        print(f"SKIP  {md_rel} (missing)")
        return 0
    text = p.read_text(encoding="utf-8")
    if img in text:
        return 0  # already inserted
    lines = text.split("\n")
    a = anchor.lower()
    for idx, ln in enumerate(lines):
        if ln.lstrip().startswith("#") and a in ln.lower():
            fig = ["", f"![{caption}](../assets/{img})",
                   f"*{caption}.*", ""]
            lines[idx+1:idx+1] = fig
            p.write_text("\n".join(lines), encoding="utf-8")
            print(f"OK    {md_rel}: {img} after '{ln.strip()[:40]}'")
            return 1
    print(f"MISS  {md_rel}: no heading matched '{anchor}' for {img}")
    return 0


def main():
    n = sum(insert(*r) for r in RULES)
    print(f"\nInserted {n} figures")


if __name__ == "__main__":
    main()
