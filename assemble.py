#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Add classes whose to_material method generates a Material instance
'''

import random
import string
LEFT = -1
RIGHT = 1

# i <3 you, _randString!!!
def _randString(length=16, chars=string.letters):
  first = random.choice(string.letters[26:])
  return first+''.join([random.choice(chars) for i in range(length-1)])

class Idea(object) :
  def to_material(self, l) :
    return Material('','','',None,0.0)
    
class Flutter(Idea) :
  def to_material(self, l) :
    vl = _randString()
    vr = _randString()
    ngroups = random.randint(1,4)
    hands = [' \\transpose c c\'\'\' { << { \\tempo "vif" \\clef treble \\autoBeamOff \\cadenzaOn ','\\transpose c e\'\'\' { << { \\clef treble \\autoBeamOff ']
    p = 'c des d ees e f fis g aes a bes b'.split(' ')
    notes = [[p[random.randint(0,3)]+'16', p[random.randint(4,7)]+'16'],[p[random.randint(4,7)]+'16', p[random.randint(0,3)]+'16']]
    for x in range(ngroups) :
      wait = [0,random.randint(0,4)]
      if random.random() > 0.5 :
        wait.reverse()
      nnotes = random.randint(8,29)
      for y in range(2) :
        first = True
        last = False
        hands[y] += ('r8'*(wait[y]/2))+('r16'*(wait[y] - ((wait[y]/2)*2)))
        for z in range(nnotes) :
          if z == nnotes - 1 : last = True
          if z < wait[y] : pass #hands[y] += 'r16 '
          else :
            hands[y] += notes[y][z % 2]+' '+('[' if (z % 2 == 0) and (not last) else '')+(']' if (z % 2 == 1) and (not first) else '')
            first = False
        hands[y] += '\\bar "" r4\\fermata \\bar ""'
    for x in range(2) : hands[x] += '\\autoBeamOn \\cadenzaOff \\bar "||" } { FOO } >> }'
    hands[0] = hands[0].replace('FOO','s1*0')
    hands[1] = hands[1].replace('FOO','s16\\mp')
    return Material(vl+' = '+hands[0]+'\n\n'+vr+'='+hands[1]+'\n', vl, vr, Flutter, 15) # dummy len...

class Press(Idea) :
  def to_material(self, l) :
    vl = _randString()
    vr = _randString()
    left = [0,2,4,5,7,9,11]
    leftn = 'c d e f g a b'.split(' ')
    right = [1,3,6,8,10]
    rightn = 'cis dis fis gis ais'.split(' ')
    start = random.randint(0,11)
    end = start + random.randint(4,7)
    notes = range(start,end)
    lh = '< '
    rh = '< '
    for x in notes :
      if x % 12 in left :
        lh += leftn[left.index(x % 12)]+"'''"+("'"*(x/12))+' '
      else :
        rh += rightn[right.index(x % 12)]+"'''"+("'"*(x/12))+' '
    lh += '>4'
    rh += '>4'
    nt = range(random.randint(1,3))
    lh = ' '.join([lh for x in nt])
    rh = ' '.join([rh+('\\p ' if x == 0 else '') for x in nt])
    lh += 'r4 '
    rh += 'r4\\fermata '
    return Material(vl+' = { \\cadenzaOn \\tempo "modéré" \\clef treble '+lh+' \\cadenzaOff \\bar "||" }\n\n'+vr+'={'+rh+'}\n', vl, vr, Press, 15) # dummy len...

class FlutterAndPress(Idea) :
  def to_material(self, l) :
    vl = _randString()
    vr = _randString()
    fp = [Flutter,Press]*random.randint(1,3)
    fp = [x().to_material([]) for x in fp] #ugh...
    return Material('\n'.join(x.music for x in fp)+'\n'+vl+'={'+''.join(['\\'+x.vl for x in fp])+'}\n'+vr+'={'+''.join(['\\'+x.vr for x in fp])+'}\n',vl,vr,FlutterAndPress,15) #dummy len...

class MiddleOndulation(Idea) :
  def to_material(self, l) :
    vl = _randString()
    vr = _randString()
    notes = 'c d e f g a b'.split(' ')*2
    acc = ['es','','is']
    hands = ['< ','< ']
    for x in range(2) :
      beg = random.randint(0,9)
      gamut = range(beg,beg+4)
      alts = [random.randint(-1,1) for y in range(4)]
      must = [False, False]
      for y in range(3) :
        if must[0] :
          alts[y] = min(alts[y],0)
          alts[y+1] = min(alts[y+1],0)
        if must[1] :
          alts[y] = max(alts[y],0)
          alts[y+1] = max(alts[y+1],0)
        if (alts[y] == 1) and ((gamut[y] % 7 == 2) or (gamut[y] % 7 == 6)) :
          alts[y + 1] = 1
        elif alts[y] == 1 :
          alts[y + 1] = random.choice([0,1])
        elif (alts[y] == 0) and ((gamut[y] % 7 == 2) or (gamut[y] % 7 == 6)) :
          alts[y + 1] = random.choice([0,1])
        if alts[y] == -1 :
          must[0] = True
        if alts[y] == 1 :
          must[1] = True
      for y in range(4) :
        hands[x] += notes[gamut[y] % 7]+acc[alts[y] + 1]+("'" if gamut[y] > 6 else "")+' '
      hands[x] += '>4'
    if random.random() < 0.5 :
      hands.reverse()
    seq = ['','']
    for x in range(random.randint(5,15)) :
      for y in range(2) :
        seq[y] += (hands[y]+('\\mp' if (x == 0) and (y == 1) else '') if (x + y) % 2 else 'r4')+' \\bar ""\n'
    for x in range(2) : seq[x] += 'r4 \\bar ""\n'
    return Material(vl+' = \\transpose c c { \\tempo "presque lent" \\cadenzaOn \\clef bass '+seq[0]+' \\cadenzaOff \\bar "||" }\n\n'+vr+'= \\transpose c c\' {\\clef treble '+seq[1]+'}\n', vl, vr, MiddleOndulation, 15) # dummy len...

class CMajor(Idea) :
  def to_material(self, l) :
    vl = _randString()
    vr = _randString()
    possl = "c4X<c g>4X<c e g>4".split('X')
    possr = "c'4X<c' e'>4X<c' e' g'>4X<c' e' g' c''>4X<c' g' c''>4X<c' e' fis' g' c''>4".split('X')
    ntimes = random.randint(2,6)
    hands = ['','']
    for x in range(ntimes) :
      hands[0] += random.choice(possl)+' \\bar "" r4 \\bar "" '
      hands[1] += random.choice(possr)+('\\f ' if x == 0 else '')+' \\bar "" r4 \\bar "" '
    return Material(vl+' = { \\tempo "rubato" \\cadenzaOn \\clef bass '+hands[0]+' \\cadenzaOff \\bar "||" }\n\n'+vr+'= {\\clef treble '+hands[1]+'}\n', vl, vr, CMajor, 15) # dummy len...
      

class HighArpeggio(Idea) :
  def to_material(self, l) :
    pass

class SlowChromaticScale(Idea) :
  def to_material(self, l) :
    vl = _randString()
    vr = _randString()
    pitches = 'c cis d dis e f fis g gis a ais b'.split(' ')
    pitches = sum([[y+x for y in pitches] for x in [",,",",","","'","''","'''"]],[])
    pitches = [x+'4 \\bar ""' for x in pitches]
    start = random.choice(range(len(pitches) - 10))
    end = min(len(pitches), start + random.randint(7,40))
    out = ''
    if start >= 36 :
      out = '\\change Staff = "up"'
    for x in range(start,end) :
      if x == 36 :
        out += '\\change Staff = "up"'
      out += pitches[x]+' '
    return Material(vl+' = { \\tempo "molto rubato" \\cadenzaOn \\clef bass { '+out+'\\change Staff = "down" } \\cadenzaOff \\bar "||" }\n\n'+vr+'= {\\clef treble s4*'+str(end-start)+'}\n', vl, vr, SlowChromaticScale, 15) # dummy len...

class Ostinato(Idea) :
  ticker = 0
  total = 2
  def to_material(self, l) :
    nums = ['Zero','One','Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Eleven','Twelve']
    idx = Ostinato.ticker % Ostinato.total
    Ostinato.ticker += 1
    foo = file('ostinato/'+str(idx)+'.ly','r')
    music = foo.read()
    foo.close()
    return Material(music,'ostinato'+nums[idx]+'Left','ostinato'+nums[idx]+'Right',Ostinato,15) # dummy length...ugh...

class HighMinorSecond(Idea) :
  def to_material(self, l) :
    Q = 70.0
    first = True
    ntimes = random.randint(3,8)
    poss = 'FOOBAR16 HELLO8 FOOBAR8. HELLO4 FOOBAR4~FOOBAR16 FOOBAR4. FOOBAR4.. FOOBAR2 FOOBAR2~FOOBAR16 FOOBAR2~FOOBAR8 FOOBAR2~FOOBAR8. FOOBAR2. FOOBAR2.~FOOBAR16 FOOBAR2.. FOOBAR2... FOOBAR1'.split(' ')
    poss = poss + ['FOOBAR1~'+x for x in poss]
    poss = poss + ['FOOBAR1~'+x for x in poss[-16:]]
    rest = ['','r16','r8','r8.','r4','r4 r16','r4.','r4..','r2','r2 r16','r2 r8','r2 r8.','r2.','r2. r16','r2..','r2...']
    n16 = 0
    out = '  '
    for x in range(ntimes) :
      nn = random.randint(3,8)
      r = random.choice([True,False])
      for y in range(nn) :
        idx = int(len(poss) * (random.random() ** 11))
        out += poss[idx] + ("^\\mf" if first else "") + '\\bar "" '
        first = False
        n16 += (idx + 1)
      if r :
        idx = random.choice(range(len(rest)))
        out += rest[idx]
        n16 += idx
      out += '\n  '
    vl = _randString ()
    vr = _randString ()
    music = vr + '= {\n  \\clef treble \\cadenzaOn '+out+' \\cadenzaOff \\bar "||" \n}\n'+vl+'={\\clef bass \ns16*'+str(n16)+' \n}\n'
    music = music.replace('FOOBAR',random.choice(["<c''' des'''>","<cis''' d'''>","<d''' ees'''>","<dis''' e'''>"]))
    music = music.replace('HELLO',random.choice(["<c''' des''' ees'''>","<cis''' d''' ees'''>","<d''' ees''' fes'''>","<dis''' e''' fis'''>"]))
    return Material(music, vl, vr, HighMinorSecond, n16 * 1.0 / (4 * Q))

class RockLick(Idea) :
  ticker = 0
  total = 2
  def to_material(self, l) :
    nums = ['Zero','One','Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Eleven','Twelve']
    idx = RockLick.ticker % RockLick.total
    RockLick.ticker += 1
    foo = file('coldplay/'+str(idx)+'.ly','r')
    music = foo.read()
    foo.close()
    return Material(music,'coldplay'+nums[idx]+'Left','coldplay'+nums[idx]+'Right',RockLick,15) # dummy length...ugh...

class LowHammeredNote(Idea) :
  def to_material(self, l) :
    Q = 70.0
    first = True
    ntimes = random.randint(3,8)
    poss = 'b,,,16 b,,,8 b,,,8. b,,,4 b,,,4~b,,,16 b,,,4. b,,,4.. b,,,2 b,,,2~b,,,16 b,,,2~b,,,8 b,,,2~b,,,8. b,,,2. b,,,2.~b,,,16 b,,,2.. b,,,2... b,,,1'.split(' ')
    poss = poss + ['b,,,1~'+x for x in poss]
    poss = poss + ['b,,,1~'+x for x in poss[-16:]]
    rest = ['','r16','r8','r8.','r4','r4 r16','r4.','r4..','r2','r2 r16','r2 r8','r2 r8.','r2.','r2. r16','r2..','r2...']
    n16 = 0
    out = '  '
    for x in range(ntimes) :
      nn = random.randint(3,8)
      r = random.choice([True,False])
      for y in range(nn) :
        idx = int(len(poss) * (random.random() ** 6))
        out += poss[idx] + ("^\\mf" if first else "") + '\\bar "" '
        first = False
        n16 += (idx + 1)
      if r :
        idx = random.choice(range(len(rest)))
        out += rest[idx]
        n16 += idx
      out += '\n  '
    vl = _randString ()
    vr = _randString ()
    music = vl + '= {\n  \\clef bass \\cadenzaOn \\ottava #-1  '+out+' \\cadenzaOff \\bar "||" \\ottava #0 \n}\n'+vr+'={\\clef treble \ns16*'+str(n16)+'\n}\n'
    return Material(music, vl, vr, LowHammeredNote, n16 * 1.0 / (4 * Q))

class FailedScale(Idea) :
  def make_scale(self, point, first = False) :
    # MAX IS 23
    div = [['X32','X16','X16.','X8','X8~X32','X8.','X8..','X4'],
           ['X32','X16','X16.','X16.~X32','X16.~X16','X16.~X16.','X8..'],
           ['X32','X16','X16~X32','X16~X16','X16~X16.','X8.'],
           ['X32','X32~X32','X32~X16','X32~X16.','X32~X8'],
           ['X32','X16','X16.','X8'],
           ['X32','X16','X16.'],
           ['X32','X16'],
           ['X32']]
    front_prolation = ['','X32~','X16~','X16.~','X8~','X32~X8~','X8.~','X8..~']
    back_prolation = ['','X32','X16','X16.','X8','X8~X32','X8.','X8..']
    seq = 'r c d e f g a b'.split(' ')
    nnotes = [random.randint(2,7), random.randint(2,7)]
    durs = [[random.randint(2,23) for x in range(nnotes[0])], [random.randint(2,23) for x in range(nnotes[1])]]
    sums = [sum(durs[0]), sum(durs[1])]
    seqs = [seq[:len(durs[0])], seq[:len(durs[1])]]
    if sums[0] < sums[1] :
      seqs[0] += ['r']
      durs[0] += [sums[1] - sums[0]]
    elif sums[0] > sums[1] :
      seqs[1] += ['r']
      durs[1] += [sums[0] - sums[1]]
    hands = []
    for fff in range(2) :
      rpoint = point
      hand = ''
      for x in range(len(durs[fff])) :
        dur = durs[fff][x]
        p1 = (8 - (rpoint % 8)) % 8
        atbat = seqs[fff][x]
        if (rpoint % 8) + dur <= 8 :
          goods = div[(rpoint % 8)][dur - 1] # minus 1 because a quarter will be 8, but index 7
          goods = goods.replace('X',atbat)
        else :
          fp = front_prolation[p1]
          fp = fp.replace('X',atbat)
          mid = '~'.join([atbat+'4' for qq in range((dur - p1) / 8)])
          bp = back_prolation[(dur - p1) - (((dur - p1) / 8) * 8)]
          bp = bp.replace('X',atbat)
          if (bp == '') & (mid == '') :
            fp = fp[:-1]
          if bp != '' :
            mid += '~ '#\\bar "" '
          goods = fp + mid + bp
        if (atbat == 'r') :
          goods = goods.replace('~', ' ')
        hand += goods
        rpoint += dur
      hands.append(hand)
      assert (sum(durs[0]) == sum(durs[1]))
    return hands[0], hands[1], sum(durs[0])
  def to_material(self, l) :
    Q = 70.0
    vl = _randString ()
    vr = _randString ()
    ntimes = random.randint(3,15)
    key = random.randint(0,12)
    right = ''
    left = ''
    n32 = 0
    for x in range(ntimes) :
      le, ri, l = self.make_scale(n32, x == 0)
      right += ri+'\n'
      left += le+'\n'
      n32 += l
    leftover = n32 - ((n32/16) * 16)
    foobar = "bes, b, c des d ees e f fis g aes a bes b".split(' ')[key]
    counter = "\\once \\override Score.TimeSignature #'stencil = ##f\n  \\time 2/4 \\tempo \"rapide\" s2\\mf s2*"+str((n32/16) - 1)+'\\cadenzaOn s32*'+str(leftover)+'\\cadenzaOff \\bar "||" '
    #counter = "s1*0"
    music = vl + '= \\transpose c '+foobar+' {\n << { \\clef bass '+left+' } { s1*0 } >> \\bar "||" \n}\n'+vr+'= \\transpose c '+foobar+' \\transpose c c\' { << { \\clef treble '+right+' } { '+counter+' } >> \n}\n'
    return Material(music, vl, vr, LowHammeredNote, n32 * 1.0 / (8 * Q))

class Material(object) :
  def __init__(self, music, vl, vr, kls, dur) :
    self.music = music
    self.vl = vl
    self.vr = vr
    self.kls = kls
    self.dur = dur
  def simple(self) :
    return (self.kls, self.dur)

class Piece(object) :
  possibles = [LowHammeredNote, FailedScale, RockLick, Flutter, Press, FlutterAndPress, MiddleOndulation, CMajor, SlowChromaticScale, Ostinato]
  def __init__(self) :
    self.segments = []
    self.material = []
    self.rocklick = 0
    self.ostinato = 0
  def genmat(self) :
    last = None
    for x in range(40) :
      atbat = random.choice(self.possibles)
      while (atbat == last) or (atbat == FlutterAndPress and last in [Flutter, Press]) or (last == FlutterAndPress and atbat in [Flutter, Press]) or ((self.rocklick >= RockLick.total) and atbat == RockLick) or ((self.ostinato >= Ostinato.total) and atbat == Ostinato) :
        atbat = random.choice(self.possibles)
      last = atbat
      if atbat == RockLick :
        self.rocklick += 1
      if atbat == Ostinato :
        self.ostinato += 1
      m = atbat().to_material([x.simple() for x in self.material])
      self.material.append(m)
  def make(self) :
    self.genmat()
    music = ''
    l = ''
    r = ''
    for m in self.material :
      music += m.music+'\n'
      l += '\\'+m.vl+' '
      r +='\\'+m.vr+' '
    out = '\\version "2.14.0"\n\n\\header {\n  title = "the tragedy of intent iv"\n  subtitle = \\markup { "Conchita vs. The Philistines — AND HOW!" } \n  composer = "mike solomon"\n}\n\n'
    out += music
    out += '\\new PianoStaff <<\n  \\new Staff = "up" { \\clef treble'
    out += r
    out += '}\n  \\new Staff = "down" { \\clef bass'
    out += l
    out += '\\bar "|."}\n>>\n\\layout {\\context {\\Score \\override NonMusicalPaperColumn #\'allow-loose-spacing = ##f\n \\override DynamicText #\'extra-spacing-width = #\'(-0.15 . 0) }}\n'
    return out

p = Piece()
print p.make()