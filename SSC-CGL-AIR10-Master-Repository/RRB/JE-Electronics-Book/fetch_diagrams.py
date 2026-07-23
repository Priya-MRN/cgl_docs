# -*- coding: utf-8 -*-
"""Download standard, freely-licensed diagrams from Wikimedia Commons for the
RRB JE Electronics book, saving rendered PNGs into assets/.

We ask the Commons API for a rendered raster thumbnail (iiurlwidth) so SVGs
come back as PNG at a fixed width — reliable in the headless-Chrome PDF path and
consistent in size. Each entry: (Commons File: title, local filename, caption).

Only Commons files that are public domain or CC-licensed are used; an
attribution/credits file is written alongside so the book can cite sources.
"""
import urllib.request, urllib.parse, json, time, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ASSETS = HERE / "assets"
ASSETS.mkdir(exist_ok=True)
UA = {"User-Agent": "RRB-JE-Electronics-Book/1.0 (educational; contact info@interconnected.au)"}
API = "https://commons.wikimedia.org/w/api.php"
THUMB_W = 900  # px width for rendered raster

# (Commons File: title WITHOUT the 'File:' prefix, local name, human caption)
DIAGRAMS = [
    # --- Ch1 Components & Materials ---
    ("Resistor_colour_code.svg", "resistor_colour_code.png",
     "Fig 1.1  Resistor colour-code chart"),
    ("Types of capacitor.svg", "capacitor_types.png",
     "Fig 1.2  Common capacitor types"),
    ("Hysteresis_loop_(magnetic).svg", "bh_hysteresis_loop.png",
     "Fig 1.3  B–H hysteresis loop of a ferromagnetic material"),
    # --- Ch2 Devices & Circuits ---
    ("PN_diode_with_electrical_symbol.svg", "pn_junction_diode.png",
     "Fig 2.1  PN-junction diode: depletion region and symbol"),
    ("Diode-IV-Curve.svg", "diode_iv_curve.png",
     "Fig 2.2  Diode V–I characteristic"),
    ("Full-wave_rectifier.svg", "bridge_rectifier.png",
     "Fig 2.3  Full-wave bridge rectifier"),
    ("NPN_BJT_Basic_Operation_(Active).svg", "npn_bjt_operation.png",
     "Fig 2.4  NPN BJT operation in the active region"),
    ("Colpitts_oscillator.svg", "colpitts_oscillator.png",
     "Fig 2.5  Colpitts oscillator"),
    ("Thyristor_circuit_symbol.svg", "scr_symbol.png",
     "Fig 2.6  SCR (thyristor) symbol"),
    # --- Ch3 Digital Electronics ---
    ("Full-adder_logic_diagram.svg", "full_adder.png",
     "Fig 3.1  Full-adder logic diagram"),
    ("JK_timing_diagram.svg", "jk_flip_flop_timing.png",
     "Fig 3.2  JK flip-flop timing"),
    ("4-bit_ripple_counter.svg", "ripple_counter.png",
     "Fig 3.3  4-bit asynchronous (ripple) counter"),
    # --- Ch4 Linear ICs ---
    ("Op-Amp_Inverting_Amplifier.svg", "opamp_inverting.png",
     "Fig 4.1  Inverting op-amp amplifier"),
    ("Op-Amp_Non-Inverting_Amplifier.svg", "opamp_noninverting.png",
     "Fig 4.2  Non-inverting op-amp amplifier"),
    ("NE555_Astable.svg", "ne555_astable.png",
     "Fig 4.3  555 timer in astable mode"),
    ("Phase-locked_loop.svg", "pll_block.png",
     "Fig 4.4  Phase-locked loop block diagram"),
    # --- Ch5 Microprocessor ---
    ("Intel_8085_arch.svg", "intel_8085_arch.png",
     "Fig 5.1  Intel 8085 architecture"),
    # --- Ch6 Measurements ---
    ("Cathode_ray_tube_diagram-en.svg", "crt_diagram.png",
     "Fig 6.1  Cathode-ray tube of a CRO"),
    ("Wheatstone_Bridge.svg", "wheatstone_bridge.png",
     "Fig 6.2  Wheatstone bridge"),
    ("LVDT.png", "lvdt.png",
     "Fig 6.3  LVDT transducer construction"),
    # --- Ch7 Communication ---
    ("Amplitude_modulation.svg", "amplitude_modulation.png",
     "Fig 7.1  Amplitude modulation waveforms"),
    ("Frequency_modulation.svg", "frequency_modulation.png",
     "Fig 7.2  Frequency modulation waveforms"),
    ("Superheterodyne_receiver_block_diagram.svg", "superheterodyne_rx.png",
     "Fig 7.3  Superheterodyne receiver"),
    ("Optical_fiber_types.svg", "optical_fibre_modes.png",
     "Fig 7.4  Step-index vs graded-index optical fibre"),
    ("Electromagnetic_spectrum_-en.svg", "em_spectrum.png",
     "Fig 7.5  Electromagnetic spectrum"),
    # --- Ch8 Networks ---
    ("OSI_Model_v1.svg", "osi_model.png",
     "Fig 8.1  OSI seven-layer model"),
    ("NetworkTopologies.svg", "network_topologies.png",
     "Fig 8.2  Common network topologies"),
    # --- Ch10 Basic Electrical ---
    ("Ohm's_Law_with_Voltage_source_TeX.svg", "ohms_law.png",
     "Fig 10.1  Ohm's law circuit"),
    ("Wye-delta-2.svg", "star_delta.png",
     "Fig 10.2  Star (Y) and delta (Δ) connections"),
    # --- GA Physics ---
    ("Lens3.svg", "convex_lens_ray.png",
     "Fig P.1  Ray diagram of a convex lens"),
    ("Electromagnetic-Spectrum.svg", "em_spectrum_physics.png",
     "Fig P.2  Electromagnetic spectrum"),
    # --- GA Chemistry ---
    ("Periodic_table_large.svg", "periodic_table.png",
     "Fig C.1  Periodic table of the elements"),
]


def fetch_one(title, outname):
    params = {
        "action": "query", "titles": f"File:{title}",
        "prop": "imageinfo",
        "iiprop": "url|extmetadata", "iiurlwidth": str(THUMB_W),
        "format": "json",
    }
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=UA)
    data = json.load(urllib.request.urlopen(req, timeout=30))
    pages = data.get("query", {}).get("pages", {})
    page = next(iter(pages.values()))
    if "imageinfo" not in page:
        return None, None
    info = page["imageinfo"][0]
    thumb = info.get("thumburl") or info.get("url")
    meta = info.get("extmetadata", {})
    lic = meta.get("LicenseShortName", {}).get("value", "?")
    artist = meta.get("Artist", {}).get("value", "Wikimedia Commons")
    # strip html tags crudely from artist
    import re as _re
    artist = _re.sub("<[^>]+>", "", artist).strip()
    req2 = urllib.request.Request(thumb, headers=UA)
    blob = urllib.request.urlopen(req2, timeout=45).read()
    (ASSETS / outname).write_bytes(blob)
    return lic, artist


def main():
    credits = ["# Diagram credits\n",
               "All diagrams sourced from Wikimedia Commons under the licence noted. "
               "File title links to the Commons source.\n",
               "| Local file | Commons source | Licence | Author |",
               "|---|---|---|---|"]
    ok = 0
    for title, outname, _cap in DIAGRAMS:
        try:
            lic, artist = fetch_one(title, outname)
            if lic is None:
                print(f"MISS  {title}  (no imageinfo)")
                credits.append(f"| {outname} | File:{title} | NOT FOUND | — |")
                continue
            src = f"https://commons.wikimedia.org/wiki/File:{urllib.parse.quote(title)}"
            credits.append(f"| {outname} | [{title}]({src}) | {lic} | {artist[:60]} |")
            print(f"OK    {outname}  <- {title}  [{lic}]")
            ok += 1
        except Exception as e:
            print(f"ERR   {title}: {e}")
            credits.append(f"| {outname} | File:{title} | ERROR | — |")
        time.sleep(0.4)
    (ASSETS / "CREDITS.md").write_text("\n".join(credits) + "\n", encoding="utf-8")
    print(f"\n{ok}/{len(DIAGRAMS)} downloaded -> {ASSETS}")


if __name__ == "__main__":
    main()
