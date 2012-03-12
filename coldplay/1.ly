coldplayOneRight = \relative c' {
  \time 4/4
  \clef treble
  \tempo "rock" 4=200
  e8\f g b e, g b e, g | 
  e g c e, g b e, g |
  d fis a d, fis a d, fis |
  d fis a d, fis a d, fis |
  e8 g b e, g b e, g | 
  \mark \markup \italic "rit."
  \time 6/4
  b e, g b e, g r4 r2 |  
  \time 4/4
  e8 g b e, g b e, g | 
  e g c e, g b e, g |
  d fis a d, fis a d, fis ~ |
  fis2. r4 |
  \tempo 4=120
  e8 g b e, g b e, g | 
  e g c e, g b e, g ~ |
  g2 r2 |\bar "||"
}

coldplayOneLeft = \relative c {
  \time 4/4
  \clef bass
  e8 g b e, g b e, g | 
  e g c e, g b e, g |
  d fis a d, fis a d, fis |
  d fis a d, fis a d, fis |
  e8 g b e, g b e, g | 
  \time 6/4
  b e, g b e, g r4 r2 |
  \mark \markup \italic "loco"
  \time 4/4
  e8 g b e, g b e, g | 
  e g c e, g b e, g |
  d fis a d, fis a d, fis ~ |
  fis2. r4 |
  e8 g b e, g b e, g | 
  e g c e, g b e, g ~ |
  g2 r2 |
}