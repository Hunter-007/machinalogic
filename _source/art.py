"""Vector artwork for the Machina Logic site.

Every drawing is plain inline SVG, styled by site.css:
  .k  ink stroke      .b  flow-blue stroke   .r  live-red stroke   .y  hazard stroke
  .dr draw-in path (pathLength=1); drawn when its parent .art gets the class "on".
      Delay per element with style="--d:.4" (seconds).
Looping motion only runs while the art is on screen (site.js toggles .on / .off).
"""
import json, pathlib

ROOT = pathlib.Path(__file__).parent
AFRICA = json.loads((ROOT / "src" / "art" / "africa.json").read_text())


def dr(tag, delay=0, cls="k", **attrs):
    """A drawable element."""
    a = " ".join(f'{k.replace("_", "-")}="{v}"' for k, v in attrs.items())
    st = f' style="--d:{delay}"' if delay else ""
    if "dash" in cls.split():  # dashed lines can't use the dash-offset draw trick, so they fade in
        return f'<{tag} class="fade {cls}"{st} {a}/>'
    return f'<{tag} class="dr {cls}" pathLength="1"{st} {a}/>'


def P(d, delay=0, cls="k", **kw):
    return dr("path", delay, cls, d=d, **kw)


def pylon(x, top, base, delay=0):
    """Lattice transmission tower."""
    w = 26
    legs = f"M{x-w} {base} L{x-6} {top+18} L{x} {top} L{x+6} {top+18} L{x+w} {base}"
    arms = f"M{x-34} {top+22} H{x+34} M{x-26} {top+46} H{x+26}"
    brace = "".join(
        f"M{x-w+(w-6)*t1:.1f} {base-(base-top-18)*t1:.1f} L{x+w-(w-6)*t2:.1f} {base-(base-top-18)*t2:.1f} "
        f"M{x+w-(w-6)*t1:.1f} {base-(base-top-18)*t1:.1f} L{x-w+(w-6)*t2:.1f} {base-(base-top-18)*t2:.1f} "
        for t1, t2 in [(0, .32), (.32, .6), (.6, .85)])
    return P(legs, delay) + P(arms, delay + .15) + P(brace, delay + .25, "k thin")


def breaker(x, y, delay=0, cls="k", extra=""):
    return f'<rect class="dr {cls} brk {extra}" pathLength="1" style="--d:{delay}" x="{x-8}" y="{y-8}" width="16" height="16"/>'


def pulse(path_id, dur, begin=0, cls="pz", r=3.4):
    return (f'<circle class="{cls}" r="{r}"><animateMotion dur="{dur}s" begin="-{begin % dur:.2f}s" repeatCount="indefinite">'
            f'<mpath href="#{path_id}"/></animateMotion></circle>')


# ---------- small load pictograms (48 x 48 box, origin top-left) ----------
def ico_power(x, y, d=0):
    return P(f"M{x+27} {y+4} L{x+12} {y+27} H{x+24} L{x+20} {y+44} L{x+37} {y+19} H{x+25} Z", d)


def ico_mine(x, y, d=0):
    return (P(f"M{x+6} {y+46} L{x+24} {y+10} L{x+42} {y+46} M{x+12} {y+34} H{x+36} M{x+24} {y+10} V{y+46}", d)
            + f'<circle class="dr k spin" pathLength="1" style="--d:{d+.2}" cx="{x+24}" cy="{y+9}" r="7"/>')


def ico_factory(x, y, d=0):
    return P(f"M{x+2} {y+46} V{y+22} L{x+14} {y+30} V{y+22} L{x+26} {y+30} V{y+22} L{x+38} {y+30} V{y+4} H{x+46} V{y+46} Z", d)


def ico_water(x, y, d=0):
    return (P(f"M{x+24} {y+3} C{x+33} {y+16} {x+38} {y+23} {x+38} {y+30} A14 14 0 0 1 {x+10} {y+30} C{x+10} {y+23} {x+15} {y+16} {x+24} {y+3} Z", d)
            + P(f"M{x+17} {y+31} q4 6 10 5", d + .2, "b"))


def ico_port(x, y, d=0):
    return (P(f"M{x+10} {y+46} V{y+4} H{x+46} M{x+10} {y+12} L{x+22} {y+4} M{x+2} {y+46} H{x+30}", d)
            + f'<g class="hoist">{P(f"M{x+38} {y+4} V{y+22}", d+.2)}{P(f"M{x+31} {y+22} h14 v10 h-14 Z", d+.3, "b")}</g>')


def ico_gov(x, y, d=0):
    return P(f"M{x+2} {y+16} L{x+24} {y+3} L{x+46} {y+16} Z M{x+8} {y+18} V{y+40} M{x+19} {y+18} V{y+40} M{x+29} {y+18} V{y+40} M{x+40} {y+18} V{y+40} M{x+2} {y+45} H{x+46}", d)


LOADS = [("Power", ico_power), ("Oil, gas & mining", ico_mine), ("Factory", ico_factory),
         ("Water", ico_water), ("Port", ico_port), ("Public", ico_gov)]


# ---------- HERO: the grid feeding six industries, with a contained intrusion ----------
def hero():
    s = []
    # horizon
    s.append(P("M0 176 H640", 0, "k thin dash"))
    for i, x in enumerate([86, 236, 386]):
        s.append(pylon(x, 46, 176, .1 + i * .18))
    # conductors (catenaries) from the left edge across pylon arm tips to the substation
    wire = "M0 74 Q26 84 52 68 Q127 92 202 68 Q277 92 352 68 Q427 92 520 112"
    wire2 = "M0 98 Q30 106 60 92 Q136 112 210 92 Q286 112 360 92 Q430 112 520 112"
    s.append(f'<path id="hw1" class="dr k" pathLength="1" style="--d:.6" d="{wire}"/>')
    s.append(f'<path id="hw2" class="dr k thin" pathLength="1" style="--d:.7" d="{wire2}"/>')
    # substation gantry + transformer
    s.append(P("M500 176 V112 H540 V176", .9))
    s.append(P("M520 112 V196", 1.0))
    s.append(f'<circle class="dr k" pathLength="1" style="--d:1.05" cx="520" cy="214" r="18"/>')
    s.append(f'<circle class="dr k" pathLength="1" style="--d:1.1" cx="520" cy="240" r="18"/>')
    s.append(P("M520 258 V300", 1.2))
    s.append(breaker(520, 282, 1.25))
    # main busbar
    s.append(P("M52 316 H588", 1.35, "k bus"))
    s.append(P("M520 300 V316", 1.3))
    xs = [76, 166, 256, 346, 436, 526]
    for i, (label, fn) in enumerate(LOADS):
        x = xs[i]
        d = 1.55 + i * .08
        s.append(f'<path id="fd{i}" class="dr k" pathLength="1" style="--d:{d}" d="M{x} 316 V{(420)}"/>')
        s.append(breaker(x, 352, d + .1, "k", "f3" if i == 2 else ""))
        s.append(f'<g class="load{" hit" if i == 2 else ""}">{fn(x-24, 430, d + .25)}</g>')
        s.append(f'<text class="lbl" x="{x}" y="506" text-anchor="middle">{label.replace("&", "&amp;")}</text>')
    # current pulses (normal operation)
    s.append(pulse("hw1", 3.2, 1.8))
    s.append(pulse("hw1", 3.2, 3.4))
    for i in range(6):
        s.append(pulse(f"fd{i}", 1.6 + (i % 3) * .3, 2 + i * .21, "pz sm", 2.6))
    # the intrusion: remote vendor laptop -> feeder 3, then breaker opens and the zone is isolated
    s.append('<g class="intr">'
             '<path class="r lap" d="M8 236 h40 v26 h-40 z M2 268 h52"/>'
             '<path class="r atk" pathLength="1" d="M54 250 H150 Q200 250 200 300 V390 Q200 404 214 404 H256"/>'
             '<circle class="r ring" cx="256" cy="404" r="10"/>'
             '<rect class="y iso" x="214" y="334" width="84" height="196" rx="6"/>'
             '</g>')
    s.append('<g class="tag"><rect x="300" y="380" width="200" height="30" rx="4"/>'
             '<text x="312" y="400">Unscheduled write contained</text></g>')
    return ('<svg class="art-svg" viewBox="0 0 640 520" role="img" aria-label="Illustration: power flows from '
            'transmission lines through a substation to six industries. A remote connection attempts an '
            'unscheduled write to the factory feeder; it is detected and that feeder is isolated.">'
            + "".join(s) + "</svg>")


# ---------- THE GAP: convergence / scarcity / consequence ----------
def gap():
    s = []
    # plant floor (always present)
    s.append(P("M40 430 H520", 0, "k bus"))
    plcs = [80, 170, 260, 350, 440]
    for i, x in enumerate(plcs):
        s.append(P(f"M{x} 430 V400", .1 + i * .05))
        s.append(f'<rect class="dr k" pathLength="1" style="--d:{.15+i*.05}" x="{x-22}" y="370" width="44" height="30" rx="2"/>')
        s.append(P(f"M{x-12} 385 h8 M{x+4} 385 h8", .3, "k thin"))
    s.append(P("M260 370 V318", .3))
    s.append('<rect class="dr k" pathLength="1" style="--d:.35" x="214" y="270" width="92" height="48" rx="3"/>')
    s.append('<text class="lbl" x="260" y="299" text-anchor="middle">Control room</text>')
    # 1 convergence: everything connects in
    c = ['<g class="st st1">']
    srcs = [(70, 70, "Cloud"), (200, 46, "Head office"), (330, 62, "Vendor"), (460, 84, "Remote laptop")]
    for i, (x, y, lab) in enumerate(srcs):
        c.append(f'<rect class="dr b" pathLength="1" style="--d:{.1*i}" x="{x-42}" y="{y-16}" width="84" height="32" rx="16"/>')
        c.append(f'<text class="lbl" x="{x}" y="{y+5}" text-anchor="middle">{lab}</text>')
        c.append(f'<path id="cv{i}" class="dr b" pathLength="1" style="--d:{.3+.1*i}" d="M{x} {y+16} C{x} {y+120} 260 {170} 260 270"/>')
        c.append(pulse(f"cv{i}", 2.2 + i * .3, i * .4, "pz b", 3))
    c.append('</g>')
    # 2 scarcity: a crowd of IT generalists, one OT specialist
    sc = ['<g class="st st2">']
    k = 0
    for row in range(3):
        for col in range(9):
            x, y = 60 + col * 52, 70 + row * 62
            special = (row, col) == (1, 6)
            cls = "y fillhz" if special else "k"
            sc.append(f'<g class="who{" one" if special else ""}">'
                      f'<circle class="dr {cls}" pathLength="1" style="--d:{k*.02:.2f}" cx="{x}" cy="{y}" r="9"/>'
                      f'<path class="dr {cls}" pathLength="1" style="--d:{k*.02+.1:.2f}" d="M{x-15} {y+32} q0 -18 15 -18 q15 0 15 18"/></g>')
            k += 1
    sc.append('</g>')
    # 3 consequence: the plant trips, the town goes dark
    cq = ['<g class="st st3">']
    cq.append(P("M306 300 H396 M432 300 H520", 0, "r"))
    cq.append('<circle class="r" cx="396" cy="300" r="5"/><g class="trip"><path class="r w3" d="M396 300 L430 276"/></g>')
    cq.append(P("M40 214 V130 H90 V160 H130 V100 H170 V214 M190 214 V150 H240 V120 H300 V214 M320 214 V80 H360 V140 H420 V214 M440 214 V160 H500 V214", 0, "k"))
    for i, (x, y) in enumerate([(52, 150), (70, 150), (52, 176), (142, 120), (142, 146), (142, 172), (204, 166), (222, 190),
                                (256, 140), (276, 140), (256, 166), (332, 100), (332, 126), (346, 150), (380, 160), (400, 180),
                                (454, 176), (476, 176), (454, 196)]):
        cq.append(f'<rect class="win" style="--i:{i}" x="{x}" y="{y}" width="10" height="12"/>')
    cq.append('<path class="r warn" d="M480 236 l26 46 h-52 z M480 252 v14 M480 274 v3"/>')
    cq.append('</g>')
    s += c + sc + cq
    return ('<svg class="art-svg" viewBox="0 0 560 470" role="img" aria-label="Illustration of the security gap: '
            'outside networks connecting into a plant, very few OT specialists, and a tripped plant leaving a town dark.">'
            + "".join(s) + "</svg>")


# ---------- six service drawings (viewBox 480 x 340) ----------
def svc_visibility():
    s = []
    nodes = [(60, 260), (130, 180), (200, 260), (250, 120), (320, 200), (390, 110), (420, 260), (150, 80), (340, 300)]
    edges = [(0, 1), (1, 2), (1, 3), (3, 4), (4, 5), (4, 6), (3, 7), (4, 8), (2, 8)]
    for i, (a, b) in enumerate(edges):
        (x1, y1), (x2, y2) = nodes[a], nodes[b]
        hidden = b in (7, 8)
        s.append(f'<path class="{"fade b dash" if hidden else "dr k"}" pathLength="1" style="--d:{.1+i*.07:.2f}" d="M{x1} {y1} L{x2} {y2}"/>'.replace(' pathLength="1"' if hidden else '@@', ''))
    for i, (x, y) in enumerate(nodes):
        hidden = i in (7, 8)
        s.append(f'<rect class="dr {"b" if hidden else "k"} {"fillb" if hidden else "fillp"}" pathLength="1" style="--d:{.3+i*.06:.2f}" x="{x-11}" y="{y-11}" width="22" height="22" rx="{11 if i % 3 == 0 else 2}"/>')
        if hidden:
            s.append(f'<circle class="b ping" cx="{x}" cy="{y}" r="14"/>')
    s.append('<g class="sweep"><path class="b" d="M0 30 V320"/><rect class="sweepfill" x="-60" y="30" width="60" height="290"/></g>')
    s.append('<text class="lbl" x="150" y="54" text-anchor="middle">Undocumented</text>')
    return s


def svc_detection():
    s = [P("M30 280 H450 M30 60 V280", 0, "k thin")]
    for y in (100, 140, 180, 220, 260):
        s.append(P(f"M30 {y} H450", .05, "k hair"))
    s.append('<rect class="band" x="30" y="150" width="420" height="70"/>')
    wave = "M30 190 C60 170 80 170 100 186 S140 206 160 190 S200 168 220 186 S250 206 270 190"
    s.append(P(wave, .2, "b w3"))
    s.append(P("M270 190 L290 182 L302 80 L316 236 L330 186", .9, "r w3"))
    s.append(P("M330 186 C350 172 370 172 390 188 S430 204 450 190", 1.2, "b w3"))
    s.append('<circle class="r ring" cx="302" cy="80" r="12"/>')
    s.append('<g class="tag2"><rect x="322" y="62" width="118" height="28" rx="4"/><text x="333" y="81">Not in baseline</text></g>')
    return s


def svc_response():
    s = [P("M40 170 H180", 0, "k w3"), P("M240 170 H440", .3, "k w3")]
    s.append('<g class="blade"><path class="k w3" d="M180 170 L240 170"/></g>')
    s.append('<circle class="k fillp" cx="180" cy="170" r="6"/><circle class="k fillp" cx="240" cy="170" r="6"/>')
    s.append('<rect class="dr k" pathLength="1" style="--d:.5" x="360" y="120" width="80" height="100" rx="4"/>')
    s.append(P("M378 150 h44 M378 170 h44 M378 190 h28", .7, "k thin"))
    s.append('<path id="rs1" d="M40 170 H180"/>')
    s.append(pulse("rs1", 1.4, 0, "pz r", 5))
    s.append(P("M40 170 V60 H120", .2, "k thin dash"))
    s.append('<text class="lbl" x="128" y="64">Infected engineering laptop</text>')
    s.append('<rect class="iso2" x="340" y="100" width="120" height="140" rx="8"/>')
    s.append('<text class="lbl" x="400" y="266" text-anchor="middle">Process keeps running</text>')
    return s


def svc_risk():
    s = []
    cx, cy, R = 240, 250, 170
    s.append(P(f"M{cx-R} {cy} A{R} {R} 0 0 1 {cx+R} {cy}", 0, "k w3"))
    s.append(P(f"M{cx+R*0.5:.0f} {cy-R*0.866:.0f} A{R} {R} 0 0 1 {cx+R} {cy}", .3, "r w8"))
    import math
    for i in range(11):
        a = math.pi * (1 - i / 10)
        x1, y1 = cx + (R - 4) * math.cos(a), cy - (R - 4) * math.sin(a)
        x2, y2 = cx + (R - (22 if i % 5 == 0 else 14)) * math.cos(a), cy - (R - (22 if i % 5 == 0 else 14)) * math.sin(a)
        s.append(P(f"M{x1:.1f} {y1:.1f} L{x2:.1f} {y2:.1f}", .2 + i * .03, "k"))
    s.append('<text class="lbl" x="92" y="276">Low</text><text class="lbl" x="350" y="276">Severe</text>')
    s.append(f'<g class="needle" style="transform-origin:{cx}px {cy}px"><path class="k w3" d="M{cx} {cy} L{cx} {cy-R+34}"/></g>')
    s.append(f'<circle class="k fillk" cx="{cx}" cy="{cy}" r="9"/>')
    s.append(f'<text class="lbl" x="{cx}" y="{cy+40}" text-anchor="middle">Ranked by what could physically happen</text>')
    return s


def svc_compliance():
    s = []
    for i, (x, y) in enumerate([(120, 70), (140, 86), (160, 102)]):
        s.append(f'<rect class="dr k fillp" pathLength="1" style="--d:{i*.15}" x="{x}" y="{y}" width="190" height="230" rx="3"/>')
    for j, y in enumerate([140, 164, 188, 212, 236]):
        s.append(P(f"M184 {y} H{320 if j % 2 else 300}", .5 + j * .06, "k thin"))
    s.append(P("M184 266 l10 10 l20 -22", 1.0, "b w3"))
    s.append('<g class="stamp"><rect class="y fillhz" x="300" y="210" width="110" height="56" rx="6"/>'
             '<text class="stamptxt" x="355" y="246" text-anchor="middle">Audit ready</text></g>')
    s.append('<text class="lbl" x="120" y="50">Nigeria, Kenya, South Africa, Ghana</text>')
    return s


def svc_workforce():
    s = [P("M40 290 H440", 0, "k bus")]
    for i, x in enumerate([90, 210, 330]):
        s.append(f'<rect class="dr k fillp" pathLength="1" style="--d:{.1+i*.1}" x="{x}" y="80" width="100" height="70" rx="3"/>')
        s.append(P(f"M{x+50} 150 V170", .2 + i * .1))
        s.append(f'<circle class="dr k" pathLength="1" style="--d:{.4+i*.1}" cx="{x+50}" cy="206" r="14"/>')
        s.append(P(f"M{x+22} 262 q0 -34 28 -34 q28 0 28 34", .5 + i * .1))
    s.append(P("M108 128 H158 M134 128 V100 H174 M228 100 L250 130 L270 108 L292 124 M348 120 h18 v-14 h22 v24 h20", .8, "b"))
    s.append('<circle class="r ring" cx="388" cy="118" r="9"/>')
    s.append('<text class="lbl" x="240" y="320" text-anchor="middle">Tabletop exercise, scenario 4: ransomware on the historian</text>')
    return s


SERVICE_ART = {"visibility": svc_visibility, "detection": svc_detection, "response": svc_response,
               "risk": svc_risk, "compliance": svc_compliance, "workforce": svc_workforce}


def service_art(name, label):
    return (f'<svg class="art-svg" viewBox="0 0 480 340" role="img" aria-label="{label}">'
            + "".join(SERVICE_ART[name]()) + "</svg>")


# ---------- six sector drawings (viewBox 480 x 300) ----------
def sec_energy():
    s = [P("M0 260 H480", 0, "k thin dash")]
    for i, x in enumerate([90, 250, 410]):
        s.append(pylon(x, 60, 260, i * .15))
    w = "M0 88 Q36 100 56 82 Q140 112 216 82 Q300 112 376 82 Q440 104 480 92"
    s.append(f'<path id="se1" class="dr k" pathLength="1" style="--d:.5" d="{w}"/>')
    s.append(pulse("se1", 2.6, 0)); s.append(pulse("se1", 2.6, 1.3))
    return s


def sec_mining():
    s = [P("M0 262 H480", 0, "k")]
    s.append(P("M60 262 L130 70 L200 262 M84 196 H176 M100 150 H160 M130 70 V262", .1))
    s.append('<g class="wheel" style="transform-origin:130px 64px">'
             '<circle class="k" cx="130" cy="64" r="26"/><path class="k thin" d="M104 64 H156 M130 38 V90 M112 46 L148 82 M148 46 L112 82"/></g>')
    s.append(P("M156 64 L250 230", .5, "k thin"))
    # pumpjack
    s.append(P("M300 262 L340 170 L380 262 M310 262 H460", .4))
    s.append('<g class="jack" style="transform-origin:340px 168px"><path class="k w3" d="M270 160 L440 176"/>'
             '<path class="k" d="M440 176 q14 -30 0 -50 q-12 22 0 50"/></g>')
    s.append(P("M440 182 V262", .7, "k thin"))
    return s


def sec_manufacturing():
    s = [P("M20 232 H460", 0, "k w3"), P("M20 250 H460", .1, "k thin")]
    for x in range(40, 460, 40):
        s.append(f'<circle class="k roller" cx="{x}" cy="241" r="7"/>')
    s.append('<g class="belt">' + "".join(f'<rect class="k fillp" x="{x}" y="196" width="34" height="34" rx="2"/>' for x in (-120, 20, 160, 300, 440)) + "</g>")
    s.append('<g class="arm" style="transform-origin:250px 60px"><path class="k w3" d="M250 20 V60 L310 110 L290 160"/>'
             '<circle class="k fillp" cx="250" cy="60" r="8"/><circle class="k fillp" cx="310" cy="110" r="7"/>'
             '<path class="b w3" d="M278 160 h24 M282 160 v14 M298 160 v14"/></g>')
    s.append(P("M220 20 H280", .2, "k bus"))
    return s


def sec_water():
    s = [P("M40 120 h120 v130 h-120 z", 0), P("M40 160 h120", .2, "b")]
    s.append(P("M160 220 H300 V140 H440", .3, "k w3"))
    s.append('<path id="wp" d="M160 220 H300 V140 H440"/>')
    for i in range(4):
        s.append(pulse("wp", 3, i * .75, "pz b", 4))
    s.append(P("M300 220 V262 H440", .5, "k thin"))
    s.append('<circle class="dr k" pathLength="1" style="--d:.6" cx="300" cy="140" r="14"/>')
    s.append(P("M292 140 h16 M300 132 v16", .7, "k thin"))
    s.append('<text class="lbl" x="100" y="276" text-anchor="middle">Dosing</text>')
    s.append('<text class="lbl" x="300" y="112" text-anchor="middle">Pump station</text>')
    s.append('<g class="drip"><path class="b" d="M100 60 c6 9 9 14 9 19 a9 9 0 0 1 -18 0 c0 -5 3 -10 9 -19 z"/></g>')
    return s


def sec_ports():
    s = [P("M0 250 H480", 0, "k"), P("M0 268 q20 8 40 0 t40 0 t40 0 t40 0 t40 0 t40 0 t40 0 t40 0 t40 0 t40 0 t40 0 t40 0", .1, "b thin")]
    s.append(P("M110 250 V40 M190 250 V40 M80 40 H420 M110 120 H190 M110 40 L190 120 M190 40 L110 120", .2))
    s.append(P("M330 250 L320 200 H460 L450 250", .4))
    s.append('<g class="trolley"><path class="k" d="M262 40 v6 h28 v-6"/><path class="k thin" d="M268 46 V120 M284 46 V120"/>'
             '<rect class="b fillb" x="252" y="120" width="48" height="26" rx="2"/></g>')
    for i, x in enumerate((330, 372, 414)):
        s.append(f'<rect class="dr k fillp" pathLength="1" style="--d:{.6+i*.1}" x="{x}" y="174" width="40" height="26" rx="2"/>')
    return s


def sec_gov():
    s = [P("M140 110 L240 50 L340 110 Z", 0), P("M150 114 H330 M150 250 H330 M130 264 H350", .2)]
    for i, x in enumerate((165, 205, 245, 285, 315)):
        s.append(P(f"M{x} 120 V244", .3 + i * .05))
    for i, (x, y) in enumerate([(40, 70), (440, 70), (40, 200), (440, 200)]):
        s.append(f'<circle class="dr b" pathLength="1" style="--d:{.6+i*.1}" cx="{x}" cy="{y}" r="12"/>')
        tx = 140 if x < 240 else 340
        s.append(f'<path id="gv{i}" class="fade b dash" style="--d:{.7+i*.1}" d="M{x+(12 if x < 240 else -12)} {y} L{tx} {150 + (i // 2) * 40}"/>')
        s.append(pulse(f"gv{i}", 2.4, i * .5, "pz b", 3))
    return s


SECTOR_ART = {"energy": sec_energy, "mining": sec_mining, "manufacturing": sec_manufacturing,
              "water": sec_water, "ports": sec_ports, "government": sec_gov}


def sector_art(name, label):
    return (f'<svg class="art-svg" viewBox="0 0 480 300" role="img" aria-label="{label}">'
            + "".join(SECTOR_ART[name]()) + "</svg>")


# ---------- Africa network map ----------
MAP_LINKS = [("dakar", "abidjan"), ("abidjan", "accra"), ("accra", "lagos"), ("lagos", "abuja"), ("abuja", "kano"),
             ("lagos", "ph"), ("ph", "douala"), ("douala", "kinshasa"), ("kinshasa", "luanda"), ("kinshasa", "kolwezi"),
             ("kolwezi", "lusaka"), ("lusaka", "joburg"), ("joburg", "durban"), ("joburg", "capetown"), ("joburg", "maputo"),
             ("lusaka", "dar"), ("dar", "mombasa"), ("mombasa", "nairobi"), ("nairobi", "addis"), ("addis", "khartoum"),
             ("khartoum", "cairo"), ("cairo", "algiers"), ("algiers", "casablanca"), ("casablanca", "dakar"), ("kano", "khartoum"),
             ("abuja", "addis")]

# sector -> representative locations (illustrative, not client sites)
MAP_SECTORS = {"energy": ["kinshasa", "joburg", "abuja", "cairo"], "mining": ["kolwezi", "joburg", "ph", "accra"],
               "manufacturing": ["lagos", "cairo", "nairobi", "casablanca"], "water": ["lagos", "dar", "addis", "luanda"],
               "ports": ["lagos", "mombasa", "durban", "dakar", "abidjan"], "government": ["abuja", "nairobi", "accra", "khartoum"]}


def africa_map(label="Illustrative map of Africa showing a network linking major cities, with Lagos as the hub."):
    a, pts = AFRICA, AFRICA["pts"]
    s = [f'<path class="land" d="{a["outline"]}"/>', f'<path class="borders" d="{a["borders"]}"/>']
    for i, (u, v) in enumerate(MAP_LINKS):
        (x1, y1), (x2, y2) = pts[u], pts[v]
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        # gentle curve, bowed perpendicular to the link
        dx, dy = x2 - x1, y2 - y1
        cx, cy = mx - dy * .12, my + dx * .12
        s.append(f'<path id="ml{i}" class="dr b link" pathLength="1" style="--d:{.2+i*.05:.2f}" d="M{x1} {y1} Q{cx:.1f} {cy:.1f} {x2} {y2}"/>')
    for i in range(0, len(MAP_LINKS), 3):
        s.append(pulse(f"ml{i}", 2.2 + (i % 4) * .4, i * .15, "pz b", 2.6))
    for name, (x, y) in pts.items():
        tags = " ".join(k for k, v in MAP_SECTORS.items() if name in v)
        hub = name == "lagos"
        s.append(f'<g class="city{" hub" if hub else ""}" data-sectors="{tags}">'
                 f'<circle class="halo" cx="{x}" cy="{y}" r="14"/>'
                 f'<rect class="pt" x="{x-4.5}" y="{y-4.5}" width="9" height="9"/></g>')
    x, y = pts["lagos"]
    s.append(f'<text class="lbl hublbl" x="{x+4}" y="{y+40}" text-anchor="middle">Lagos</text>')
    return (f'<svg class="art-svg map" viewBox="0 0 600 560" role="img" aria-label="{label}">' + "".join(s) + "</svg>")


# ---------- Purdue model as an exploded stack ----------
PURDUE = [("L5 / L4", "Enterprise & business", "Email, ERP, internet access, corporate data centre and cloud", "it"),
          ("L3.5", "IT/OT DMZ", "Brokered exchange only: jump hosts, historian replicas, patch staging", "dmz"),
          ("L3", "Site operations", "Historians, engineering workstations, production management", ""),
          ("L2", "Supervisory control", "HMIs, SCADA servers and operator workstations", ""),
          ("L1", "Basic control", "PLCs, RTUs, DCS controllers and safety systems", ""),
          ("L0", "Physical process", "Sensors, actuators, motors, valves and drives", "l0")]


def purdue_stack():
    """Isometric slabs; site.js spreads them apart with --p. Text lives in HTML beside it."""
    s = []
    n = len(PURDUE)
    defs = ('<defs><pattern id="hzp" width="16" height="16" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
            '<rect width="8" height="16" class="hzfill"/></pattern></defs>')
    for i, (lvl, name, ex, kind) in enumerate(PURDUE):
        z = n - 1 - i  # 0 at bottom
        top = f"M240 {40} L440 {110} L240 {180} L40 {110} Z"
        side = "M40 110 V128 L240 198 V180 Z M240 198 L440 128 V110 L240 180 Z"
        deco = ""
        if kind == "dmz":
            deco = '<path class="stripes" d="M40 110 L240 40 L440 110 L240 180 Z" fill="url(#hzp)"/>'
        if kind == "l0":
            deco = ('<g class="minis"><circle class="k" cx="200" cy="110" r="12"/><rect class="k" x="250" y="96" width="26" height="22"/>'
                    '<path class="k" d="M300 120 l14 -24 l14 24 z"/></g>')
        if kind == "it":
            deco = '<path class="b thin" d="M150 100 h40 v20 h-40 z M210 86 h40 v20 h-40 z M270 104 h40 v20 h-40 z"/>'
        s.append(f'<g class="slab {kind}" style="--i:{i}"><path class="side" d="{side}"/><path class="top" d="{top}"/>{deco}'
                 f'<text class="slablbl" x="{372 if kind else 240}" y="118" text-anchor="middle">{lvl}</text></g>')
    s.reverse()  # lower layers first, so upper slabs sit in front
    s.insert(0, defs)
    return ('<svg class="art-svg purdue-svg" viewBox="0 -40 480 760" role="img" aria-label="The Purdue model drawn as six '
            'stacked layers, from enterprise IT at the top to the physical process at the bottom, with the IT/OT DMZ between them.">'
            + "".join(s) + "</svg>")


# ---------- services page: a switchboard with one breaker per service ----------
def board():
    s = ['<rect class="dr k fillp" pathLength="1" x="20" y="20" width="560" height="420" rx="8"/>',
         P("M60 92 H540", .2, "k bus"), P("M300 20 V92", .1, "k w3")]
    names = ["Asset visibility", "Detection", "Response", "Risk", "Compliance", "Workforce"]
    for i, n in enumerate(names):
        x = 90 + i * 84
        s.append(P(f"M{x} 92 V170", .3 + i * .06))
        s.append(f'<g class="sw" style="--i:{i}"><rect class="k swbox" x="{x-16}" y="170" width="32" height="32" rx="2"/>'
                 f'<path class="k w3 swblade" d="M{x} 178 V194"/></g>')
        s.append(P(f"M{x} 202 V300", .5 + i * .06))
        s.append(f'<circle class="dr k" pathLength="1" style="--d:{.6+i*.06:.2f}" cx="{x}" cy="314" r="14"/>')
        s.append(f'<path class="lampfill" style="--i:{i}" d="M{x-14} 314 a14 14 0 0 0 28 0 a14 14 0 0 0 -28 0"/>')
        s.append(f'<text class="lbl" x="{x}" y="{356 + (i % 2) * 22}" text-anchor="middle">{n}</text>')
    s.append('<text class="lbl" x="300" y="420" text-anchor="middle">One practice, six services, one switchboard</text>')
    return ('<svg class="art-svg" viewBox="0 0 600 460" role="img" aria-label="Illustration: a switchboard with six '
            'switches, one for each service, closing in turn and lighting their lamps.">' + "".join(s) + "</svg>")


def art(name, *args):
    return {"hero": hero, "gap": gap, "map": africa_map, "purdue": purdue_stack, "board": board}[name](*args)
